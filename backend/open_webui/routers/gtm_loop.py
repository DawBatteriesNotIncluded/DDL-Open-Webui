from __future__ import annotations

import ast
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from open_webui.utils.auth import get_verified_user
from pydantic import BaseModel

router = APIRouter()

REPO_ROOT = Path(__file__).resolve().parents[3]
TASKS_DIR = REPO_ROOT / 'gtm-loop-workspace' / 'tasks'
ARTIFACTS_DIR = REPO_ROOT / 'gtm-loop-workspace' / 'artifacts'
STATUS_AUDIT_LOG = TASKS_DIR / '_audit' / 'status-changes.jsonl'
ARTIFACT_AUDIT_LOG = TASKS_DIR / '_audit' / 'artifact-events.jsonl'
SECRET_RE = re.compile(
    r'api_key|token|secret|password|bearer|private_key|client_secret|refresh_token|access_token',
    re.IGNORECASE,
)

TASK_FIELDS = [
    'gtm_task',
    'id',
    'title',
    'client',
    'board_status',
    'current_lane',
    'current_gate',
    'current_phase',
    'priority',
    'progress',
    'manager_request',
    'interpreted_objective',
    'executor',
    'verifier',
    'approval_required',
    'approval_status',
    'blocked',
    'blocker',
    'rework_needed',
    'proposal_required',
    'architecture_required',
    'current_attempt',
    'max_attempts',
    'dependencies',
    'tags',
    'artifact_links',
    'evidence_links',
    'next_action',
    'definition_of_done',
    'manager_summary',
    'last_updated',
]

BODY_SECTIONS = {
    'manager_request': 'Manager request',
    'interpreted_objective': 'Interpreted objective',
    'definition_of_done': 'Definition of done',
    'evidence': 'Evidence',
    'artifacts': 'Artifacts',
    'decisions': 'Decisions',
    'open_questions': 'Open questions',
    'next_action': 'Next action',
    'manager_report': 'Manager report',
}

BOARD_COLUMNS = {
    'planned': 'Planned',
    'in-progress': 'In Progress',
    'smoke-test': 'Smoke Test',
    'in-review': 'In Review',
    'done': 'Done',
}
ALLOWED_BOARD_STATUSES = set(BOARD_COLUMNS) | {'cancelled'}
TASK_ID_RE = re.compile(r'^GTM-\d+$')
TRANSITION_UPDATES = {
    'pick-up': {
        'board_status': 'in-progress',
        'current_lane': 'brody',
        'current_phase': 'requirements',
        'current_gate': 'requirements-accepted',
        'next_action': 'Run Brody investigation / requirements lane.',
        'manager_summary': 'Task picked up by GTM Engineer Orchestrator.',
    },
    'move-to-ricky': {
        'board_status': 'in-progress',
        'current_lane': 'ricky',
        'current_phase': 'research',
        'current_gate': 'research-accepted',
    },
    'move-to-brody': {
        'board_status': 'in-progress',
        'current_lane': 'brody',
        'current_phase': 'requirements',
        'current_gate': 'requirements-accepted',
    },
    'move-to-archy': {
        'board_status': 'in-progress',
        'current_lane': 'archy',
        'current_phase': 'architecture',
        'current_gate': 'architecture-accepted',
    },
    'move-to-cody': {
        'board_status': 'in-progress',
        'current_lane': 'cody',
        'current_phase': 'build',
        'current_gate': 'build-complete',
    },
    'move-to-verifier': {
        'board_status': 'smoke-test',
        'current_lane': 'verifier',
        'current_phase': 'smoke-test',
        'current_gate': 'smoke-test-passed',
    },
    'move-to-reporter': {
        'board_status': 'in-review',
        'current_lane': 'reporter',
        'current_phase': 'report',
        'current_gate': 'manager-review',
    },
    'mark-done': {
        'board_status': 'done',
        'current_lane': 'manager',
        'current_phase': 'done',
        'current_gate': 'done',
    },
}
ALLOWED_TRANSITIONS = set(TRANSITION_UPDATES) | {'send-back-for-rework'}
LANE_ARTIFACTS = {
    'research': ['brief.md', 'sources.md', 'notes.md', 'evidence-cards.md'],
    'requirements': [
        'requirements.md',
        'endpoint-matrix.md',
        'field-mapping.md',
        'open-questions.md',
        'build-handoff.md',
    ],
    'architecture': ['architecture.md', 'integration-flow.md', 'adr.md', 'risks.md'],
    'build': ['build-plan.md', 'tool-plan.md', 'test-plan.md', 'rollback-plan.md'],
    'verification': ['verification-report.md', 'failed-checks.md', 'rework-instructions.md'],
    'report': ['completion-report.md', 'manager-summary.md', 'approval-request.md'],
}


class TaskStatusUpdate(BaseModel):
    board_status: str


class TaskTransitionUpdate(BaseModel):
    transition: str


class TaskArtifactCreate(BaseModel):
    overwrite: bool = False


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')


def get_source_mode() -> str:
    workspace_path = (REPO_ROOT / 'gtm-loop-workspace').as_posix()
    try:
        for line in Path('/proc/self/mountinfo').read_text(encoding='utf-8').splitlines():
            fields = line.split()
            if len(fields) > 4 and fields[4] == workspace_path:
                return 'bind-mounted/dev'
    except OSError:
        pass

    try:
        return (
            'bind-mounted/dev'
            if Path(workspace_path).stat().st_dev != REPO_ROOT.stat().st_dev
            else 'packaged/image'
        )
    except OSError:
        return 'unknown'


def parse_scalar(raw: str):
    value = raw.strip()
    if value == 'true':
        return True
    if value == 'false':
        return False
    if re.fullmatch(r'-?\d+', value):
        return int(value)
    if value == '[]':
        return []
    if value.startswith('[') and value.endswith(']'):
        try:
            parsed = ast.literal_eval(value)
            return parsed if isinstance(parsed, list) else value
        except (SyntaxError, ValueError):
            return []
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    return value


def sanitize(value):
    if isinstance(value, str):
        return '[redacted: credential-style value]' if SECRET_RE.search(value) else value
    if isinstance(value, list):
        return [sanitize(item) for item in value]
    return value


def parse_frontmatter(text: str) -> dict:
    match = re.match(r'^---\r?\n(?P<body>.*?)\r?\n---\r?\n', text, re.DOTALL)
    if not match:
        return {}

    data = {}
    for line in match.group('body').splitlines():
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        field = re.match(r'^([A-Za-z0-9_-]+):(?:\s*(.*))?$', line)
        if field:
            key = field.group(1)
            if SECRET_RE.search(key):
                continue
            data[key] = sanitize(parse_scalar(field.group(2) or ''))
    return data


def parse_sections(text: str) -> dict:
    sections = {}
    matches = list(re.finditer(r'^##\s+(.+?)\s*$', text, re.MULTILINE))
    for index, match in enumerate(matches):
        title = match.group(1).strip().lower()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections[title] = sanitize(text[start:end].strip())

    return {
        key: sections.get(section_name.lower(), '')
        for key, section_name in BODY_SECTIONS.items()
    }


def read_task(file_path: Path) -> dict:
    text = file_path.read_text(encoding='utf-8')
    frontmatter = parse_frontmatter(text)

    task = {field: frontmatter.get(field) for field in TASK_FIELDS}
    task['source_path'] = file_path.relative_to(REPO_ROOT).as_posix()
    task['body_sections'] = parse_sections(text)
    return task


def actor_from_user(user) -> str:
    for field in ('email', 'name', 'id'):
        value = getattr(user, field, None)
        if value:
            return str(value)
    return 'authenticated-user'


def task_file_for_id(task_id: str) -> Path:
    if not TASK_ID_RE.fullmatch(task_id):
        raise HTTPException(status_code=400, detail='task_id must match GTM-###.')

    file_path = TASKS_DIR / f'{task_id}.md'
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail='GTM task file not found.')
    return file_path


def replace_frontmatter_field(frontmatter: str, field: str, value: str) -> str:
    line_re = re.compile(rf'^(?P<prefix>{re.escape(field)}:\s*)(?P<value>.*)$', re.MULTILINE)
    if line_re.search(frontmatter):
        def replace(match: re.Match) -> str:
            raw_value = match.group('value').strip()
            quote = raw_value[:1] if raw_value[:1] in {'"', "'"} and raw_value.endswith(raw_value[:1]) else ''
            return f"{match.group('prefix')}{quote}{value}{quote}"

        return line_re.sub(replace, frontmatter, count=1)
    return f'{frontmatter.rstrip()}\n{field}: {value}\n'


def append_audit_entry(log_path: Path, entry: dict) -> str | None:
    try:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with log_path.open('a', encoding='utf-8') as audit_file:
            audit_file.write(json.dumps(entry, separators=(',', ':')) + '\n')
    except OSError:
        return 'Task updated, but local audit append failed.'
    return None


def append_task_audit_entry(entry: dict) -> str | None:
    return append_audit_entry(STATUS_AUDIT_LOG, entry)


def append_artifact_audit_entry(entry: dict) -> str | None:
    return append_audit_entry(ARTIFACT_AUDIT_LOG, entry)


def read_status_audit_entries(task_id: str, limit: int) -> list[dict]:
    if not STATUS_AUDIT_LOG.exists():
        return []

    entries = []
    for line in STATUS_AUDIT_LOG.read_text(encoding='utf-8').splitlines():
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue

        if entry.get('task_id') != task_id:
            continue

        entries.append(
            {
                'timestamp': str(entry.get('timestamp', '')),
                'task_id': str(entry.get('task_id', '')),
                'old_board_status': str(entry.get('old_board_status', '')),
                'new_board_status': str(entry.get('new_board_status', '')),
                'transition': str(entry.get('transition', '')),
                'old_lane': str(entry.get('old_lane', '')),
                'new_lane': str(entry.get('new_lane', '')),
                'old_phase': str(entry.get('old_phase', '')),
                'new_phase': str(entry.get('new_phase', '')),
                'old_gate': str(entry.get('old_gate', '')),
                'new_gate': str(entry.get('new_gate', '')),
                'actor': str(entry.get('actor', '')),
                'source': str(entry.get('source', '')),
                'endpoint': str(entry.get('endpoint', '')),
                'success': entry.get('success') is True,
            }
        )

    return entries[-limit:][::-1]


def update_task_status_file(file_path: Path, board_status: str) -> tuple[dict, str, str]:
    if board_status not in ALLOWED_BOARD_STATUSES:
        raise HTTPException(status_code=400, detail='board_status is not allowed.')

    text = file_path.read_text(encoding='utf-8')
    match = re.match(r'^(---\r?\n)(?P<frontmatter>.*?)(\r?\n---\r?\n)(?P<body>.*)$', text, re.DOTALL)
    if not match:
        raise HTTPException(status_code=400, detail='Task file is missing YAML frontmatter.')

    frontmatter_data = parse_frontmatter(text)
    old_board_status = frontmatter_data.get('board_status')
    if board_status == 'done':
        blockers = []
        if frontmatter_data.get('blocked') is True:
            blockers.append('task is blocked')
        if frontmatter_data.get('rework_needed') is True:
            blockers.append('task needs rework')
        if frontmatter_data.get('approval_required') is True and frontmatter_data.get('approval_status') != 'approved':
            blockers.append('approval is required but approval_status is not approved')
        done_ready = (
            old_board_status == 'in-review'
            or frontmatter_data.get('current_lane') in {'reporter', 'manager'}
            or frontmatter_data.get('current_phase') == 'report'
            or frontmatter_data.get('current_gate') == 'manager-review'
        )
        if not done_ready:
            blockers.append('task is not in a reporter/manager review state')
        if blockers:
            raise HTTPException(
                status_code=400,
                detail='Cannot move task to done via status update: ' + '; '.join(blockers) + '.',
            )

    timestamp = now_iso()
    frontmatter = replace_frontmatter_field(match.group('frontmatter'), 'board_status', board_status)
    frontmatter = replace_frontmatter_field(frontmatter, 'last_updated', timestamp)
    updated_text = f"{match.group(1)}{frontmatter}{match.group(3)}{match.group('body')}"

    try:
        file_path.write_text(updated_text, encoding='utf-8')
    except OSError as exc:
        raise HTTPException(
            status_code=409,
            detail='Task file is not writable. In local dev, mount gtm-loop-workspace/tasks as writable.',
        ) from exc

    task = read_task(file_path)
    if task.get('id') != file_path.stem or task.get('board_status') != board_status:
        raise HTTPException(status_code=500, detail='Task status update failed validation.')
    return task, str(old_board_status or ''), timestamp


def update_task_transition_file(
    file_path: Path, transition: str
) -> tuple[dict, dict, dict, str]:
    if transition not in ALLOWED_TRANSITIONS:
        raise HTTPException(status_code=400, detail='transition is not allowed.')

    text = file_path.read_text(encoding='utf-8')
    match = re.match(r'^(---\r?\n)(?P<frontmatter>.*?)(\r?\n---\r?\n)(?P<body>.*)$', text, re.DOTALL)
    if not match:
        raise HTTPException(status_code=400, detail='Task file is missing YAML frontmatter.')

    old = parse_frontmatter(text)
    current_attempt = int(old.get('current_attempt') or 0)
    max_attempts = int(old.get('max_attempts') or 0)
    if current_attempt > max_attempts:
        raise HTTPException(status_code=400, detail='current_attempt exceeds max_attempts.')

    if transition == 'pick-up' and old.get('board_status') != 'planned':
        raise HTTPException(status_code=400, detail='pick-up is only allowed from planned.')

    if transition == 'mark-done':
        if old.get('blocked') is True:
            raise HTTPException(status_code=400, detail='mark-done is not allowed while blocked.')
        if old.get('current_lane') not in {'reporter', 'manager'} and old.get('board_status') != 'in-review':
            raise HTTPException(
                status_code=400,
                detail='mark-done requires reporter/manager lane or in-review status.',
            )
        updates = dict(TRANSITION_UPDATES[transition])
    elif transition == 'send-back-for-rework':
        new_attempt = current_attempt + 1
        blocked = old.get('blocked') is True
        if new_attempt > max_attempts:
            new_attempt = max_attempts
            blocked = True
        updates = {
            'board_status': 'in-progress',
            'current_lane': 'cody',
            'current_phase': 'rework',
            'current_gate': 'build-complete',
            'rework_needed': True,
            'current_attempt': new_attempt,
            'blocked': blocked,
        }
    else:
        updates = dict(TRANSITION_UPDATES[transition])

    timestamp = now_iso()
    updates['last_updated'] = timestamp
    frontmatter = match.group('frontmatter')
    for field, value in updates.items():
        if isinstance(value, bool):
            raw_value = 'true' if value else 'false'
        else:
            raw_value = str(value)
        frontmatter = replace_frontmatter_field(frontmatter, field, raw_value)

    updated_text = f"{match.group(1)}{frontmatter}{match.group(3)}{match.group('body')}"

    try:
        file_path.write_text(updated_text, encoding='utf-8')
    except OSError as exc:
        raise HTTPException(
            status_code=409,
            detail='Task file is not writable. In local dev, mount gtm-loop-workspace/tasks as writable.',
        ) from exc

    task = read_task(file_path)
    for field, value in updates.items():
        if task.get(field) != value:
            raise HTTPException(status_code=500, detail='Task transition failed validation.')
    if int(task.get('current_attempt') or 0) > int(task.get('max_attempts') or 0):
        raise HTTPException(status_code=500, detail='Task attempt validation failed.')
    return task, old, updates, timestamp


def yaml_list(values: list[str]) -> str:
    return '[' + ', '.join(json.dumps(value) for value in values) + ']'


def artifact_path_for(task_id: str, lane: str, filename: str) -> Path:
    root = ARTIFACTS_DIR.resolve()
    task_root = (ARTIFACTS_DIR / task_id).resolve()
    target = (task_root / lane / filename).resolve()
    if root != task_root and root not in task_root.parents:
        raise HTTPException(status_code=400, detail='Artifact task path is invalid.')
    if task_root != target and task_root not in target.parents:
        raise HTTPException(status_code=400, detail='Artifact path is invalid.')
    return target


def artifact_link_for(task_id: str, lane: str, filename: str) -> str:
    return f'gtm-loop-workspace/artifacts/{task_id}/{lane}/{filename}'


def render_artifact(task: dict, lane: str, filename: str, timestamp: str) -> str:
    title = filename.removesuffix('.md').replace('-', ' ').title()
    template_path = ARTIFACTS_DIR / '_templates' / lane / filename
    template = (
        template_path.read_text(encoding='utf-8')
        if template_path.exists()
        else '# {{task_id}} {{file_title}}\n\n{{task_context}}\n\n{{approval_boundary}}\n'
    )
    body_sections = task.get('body_sections') or {}
    values = {
        'task_id': str(task.get('id') or ''),
        'task_title': str(task.get('title') or ''),
        'client': str(task.get('client') or ''),
        'lane': lane,
        'file_title': title,
        'board_status': str(task.get('board_status') or ''),
        'current_lane': str(task.get('current_lane') or ''),
        'current_phase': str(task.get('current_phase') or ''),
        'current_gate': str(task.get('current_gate') or ''),
        'manager_request': str(
            task.get('manager_request') or body_sections.get('manager_request') or ''
        ),
        'interpreted_objective': str(
            task.get('interpreted_objective')
            or body_sections.get('interpreted_objective')
            or ''
        ),
        'next_action': str(task.get('next_action') or body_sections.get('next_action') or ''),
        'definition_of_done': str(
            task.get('definition_of_done') or body_sections.get('definition_of_done') or ''
        ),
        'generated_at': timestamp,
    }
    values['task_context'] = (
        f"| Field | Value |\n"
        f"| --- | --- |\n"
        f"| Task | `{values['task_id']}` |\n"
        f"| Title | {values['task_title']} |\n"
        f"| Client | `{values['client']}` |\n"
        f"| Board status | `{values['board_status']}` |\n"
        f"| Lane | `{values['current_lane']}` |\n"
        f"| Phase | `{values['current_phase']}` |\n"
        f"| Gate | `{values['current_gate']}` |\n"
        f"| Generated | `{timestamp}` |"
    )
    values['approval_boundary'] = (
        "No external API writes, workflow activation, credential changes, email sends, "
        "or production data mutation are allowed from this artifact. Use fake/redacted "
        "examples only until a human approves the exact external action."
    )
    for key, value in values.items():
        template = template.replace('{{' + key + '}}', value)
    return template.rstrip() + '\n'


def update_task_artifact_links(file_path: Path, artifact_links: list[str]) -> tuple[dict, str]:
    text = file_path.read_text(encoding='utf-8')
    match = re.match(r'^(---\r?\n)(?P<frontmatter>.*?)(\r?\n---\r?\n)(?P<body>.*)$', text, re.DOTALL)
    if not match:
        raise HTTPException(status_code=400, detail='Task file is missing YAML frontmatter.')

    frontmatter_data = parse_frontmatter(text)
    links = list(frontmatter_data.get('artifact_links') or [])
    for link in artifact_links:
        if link not in links:
            links.append(link)

    timestamp = now_iso()
    frontmatter = replace_frontmatter_field(match.group('frontmatter'), 'artifact_links', yaml_list(links))
    frontmatter = replace_frontmatter_field(frontmatter, 'last_updated', timestamp)
    updated_text = f"{match.group(1)}{frontmatter}{match.group(3)}{match.group('body')}"

    try:
        file_path.write_text(updated_text, encoding='utf-8')
    except OSError as exc:
        raise HTTPException(
            status_code=409,
            detail='Task file is not writable. In local dev, mount gtm-loop-workspace/tasks as writable.',
        ) from exc

    task = read_task(file_path)
    if task.get('id') != file_path.stem:
        raise HTTPException(status_code=500, detail='Task artifact update failed validation.')
    if any(link not in (task.get('artifact_links') or []) for link in artifact_links):
        raise HTTPException(status_code=500, detail='Task artifact links failed validation.')
    return task, timestamp


def create_task_lane_artifacts(
    file_path: Path,
    lane: str,
    overwrite: bool,
) -> tuple[dict, list[str], list[str], str]:
    if lane not in LANE_ARTIFACTS:
        raise HTTPException(status_code=400, detail='artifact lane is not allowed.')

    task = read_task(file_path)
    task_id = str(task.get('id') or file_path.stem)
    timestamp = now_iso()
    created = []
    skipped = []
    links = []

    for filename in LANE_ARTIFACTS[lane]:
        target = artifact_path_for(task_id, lane, filename)
        link = artifact_link_for(task_id, lane, filename)
        links.append(link)

        if target.exists() and not overwrite:
            skipped.append(link)
            continue

        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(render_artifact(task, lane, filename, timestamp), encoding='utf-8')
        except OSError as exc:
            raise HTTPException(
                status_code=409,
                detail='Artifact path is not writable. In local dev, mount gtm-loop-workspace/artifacts as writable.',
            ) from exc
        created.append(link)

    updated_task, update_timestamp = update_task_artifact_links(file_path, links)
    return updated_task, created, skipped, update_timestamp


@router.get('/tasks')
async def get_gtm_loop_tasks(user=Depends(get_verified_user)):
    task_files = sorted(TASKS_DIR.glob('GTM-*.md')) if TASKS_DIR.exists() else []
    tasks = [read_task(file_path) for file_path in task_files]

    counts = {
        'total': len(tasks),
        'blocked': sum(1 for task in tasks if task.get('blocked') is True),
        'approval_required': sum(
            1 for task in tasks if task.get('approval_required') is True
        ),
        'in_review': sum(1 for task in tasks if task.get('board_status') == 'in-review'),
    }

    columns = {
        status: [task['id'] for task in tasks if task.get('board_status') == status]
        for status in BOARD_COLUMNS
    }

    return {
        'tasks': tasks,
        'counts': counts,
        'columns': columns,
        'workspace_path': (REPO_ROOT / 'gtm-loop-workspace').as_posix(),
        'task_count': len(tasks),
        'source_mode': get_source_mode(),
    }


@router.patch('/tasks/{task_id}/status')
async def update_gtm_loop_task_status(
    task_id: str,
    payload: TaskStatusUpdate,
    user=Depends(get_verified_user),
):
    file_path = task_file_for_id(task_id)
    task, old_board_status, timestamp = update_task_status_file(file_path, payload.board_status)
    audit_warning = append_task_audit_entry(
        {
            'timestamp': timestamp,
            'task_id': task_id,
            'old_board_status': old_board_status,
            'new_board_status': payload.board_status,
            'actor': actor_from_user(user),
            'source': '/gtm-loop/board',
            'endpoint': 'PATCH /api/gtm-loop/tasks/{task_id}/status',
            'success': True,
        }
    )
    task['audit_logged'] = audit_warning is None
    if audit_warning:
        task['audit_warning'] = audit_warning
    return task


@router.patch('/tasks/{task_id}/transition')
async def transition_gtm_loop_task(
    task_id: str,
    payload: TaskTransitionUpdate,
    user=Depends(get_verified_user),
):
    file_path = task_file_for_id(task_id)
    task, old, updates, timestamp = update_task_transition_file(file_path, payload.transition)
    audit_warning = append_task_audit_entry(
        {
            'timestamp': timestamp,
            'task_id': task_id,
            'transition': payload.transition,
            'old_board_status': str(old.get('board_status') or ''),
            'new_board_status': str(updates.get('board_status') or old.get('board_status') or ''),
            'old_lane': str(old.get('current_lane') or ''),
            'new_lane': str(updates.get('current_lane') or old.get('current_lane') or ''),
            'old_phase': str(old.get('current_phase') or ''),
            'new_phase': str(updates.get('current_phase') or old.get('current_phase') or ''),
            'old_gate': str(old.get('current_gate') or ''),
            'new_gate': str(updates.get('current_gate') or old.get('current_gate') or ''),
            'actor': actor_from_user(user),
            'source': '/gtm-loop/board',
            'endpoint': 'PATCH /api/gtm-loop/tasks/{task_id}/transition',
            'success': True,
        }
    )
    task['audit_logged'] = audit_warning is None
    if audit_warning:
        task['audit_warning'] = audit_warning
    return task


@router.post('/tasks/{task_id}/artifacts/{lane}')
async def create_gtm_loop_task_artifacts(
    task_id: str,
    lane: str,
    payload: TaskArtifactCreate | None = None,
    user=Depends(get_verified_user),
):
    file_path = task_file_for_id(task_id)
    overwrite = payload.overwrite if payload else False
    task, created, skipped, timestamp = create_task_lane_artifacts(file_path, lane, overwrite)
    audit_warning = append_artifact_audit_entry(
        {
            'timestamp': timestamp,
            'task_id': task_id,
            'lane': lane,
            'files_created': created,
            'files_skipped': skipped,
            'actor': actor_from_user(user),
            'source': '/gtm-loop/board',
            'endpoint': 'POST /api/gtm-loop/tasks/{task_id}/artifacts/{lane}',
            'success': True,
        }
    )
    task['files_created'] = created
    task['files_skipped'] = skipped
    task['audit_logged'] = audit_warning is None
    if audit_warning:
        task['audit_warning'] = audit_warning
    return task


@router.get('/tasks/{task_id}/audit')
async def get_gtm_loop_task_audit(
    task_id: str,
    limit: int = 3,
    user=Depends(get_verified_user),
):
    task_file_for_id(task_id)
    return {
        'task_id': task_id,
        'entries': read_status_audit_entries(task_id, max(1, min(limit, 50))),
    }
