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
STATUS_AUDIT_LOG = TASKS_DIR / '_audit' / 'status-changes.jsonl'
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


class TaskStatusUpdate(BaseModel):
    board_status: str


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


def append_status_audit_entry(entry: dict) -> str | None:
    try:
        STATUS_AUDIT_LOG.parent.mkdir(parents=True, exist_ok=True)
        with STATUS_AUDIT_LOG.open('a', encoding='utf-8') as audit_file:
            audit_file.write(json.dumps(entry, separators=(',', ':')) + '\n')
    except OSError:
        return 'Status updated, but local audit append failed.'
    return None


def update_task_status_file(file_path: Path, board_status: str) -> tuple[dict, str, str]:
    if board_status not in ALLOWED_BOARD_STATUSES:
        raise HTTPException(status_code=400, detail='board_status is not allowed.')

    text = file_path.read_text(encoding='utf-8')
    match = re.match(r'^(---\r?\n)(?P<frontmatter>.*?)(\r?\n---\r?\n)(?P<body>.*)$', text, re.DOTALL)
    if not match:
        raise HTTPException(status_code=400, detail='Task file is missing YAML frontmatter.')

    old_board_status = parse_frontmatter(text).get('board_status')
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
    audit_warning = append_status_audit_entry(
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
