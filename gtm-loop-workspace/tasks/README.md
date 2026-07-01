# GTM Loop Tasks

Markdown task files in this folder are the canonical task source of truth for the GTM Loop workstation.

`board.md` is only a manager-facing mirror. Update the task file first, then update the matching short summary in `../board.md`.

## File Rules

- One task per file: `GTM-###.md`.
- Every task file must include YAML frontmatter matching `../schemas/task-card.md`.
- Keep detailed loop state in the task body, not in board columns.
- Link evidence and artifacts instead of copying long logs or sensitive data.
- Do not store secrets, endpoint hosts, tenant IDs, auth headers, raw customer records, copied logs, or raw transcripts.
- Run the local validator after changing task files or `../board.md`.

## Validation

From the repo root:

```powershell
node scripts\validate-gtm-tasks.js
```

The validator checks task frontmatter, enum values, booleans, numeric fields, task filename/id alignment, attempt limits, board links, board sections, and obvious credential-style values in frontmatter.

Agents should run it after updating any `tasks/GTM-*.md` file or `../board.md`, and before relying on task files for frontend board work. Task validation must pass before connecting any executor, MCP write path, or external automation surface.

The Open WebUI routes are:

- `/gtm-loop`: cockpit dashboard.
- `/gtm-loop/board`: read-only Kanban board.

The board reads these task files through `GET /api/gtm-loop/tasks`. Status moves use `PATCH /api/gtm-loop/tasks/{task_id}/status` and may update only `board_status` and `last_updated` in YAML frontmatter. Successful status moves append a JSONL audit entry to `_audit/status-changes.jsonl`. Search and filters on `/gtm-loop/board` are client-side only and do not change task files, `board.md`, or the API response.

In local Docker development, `docker-compose.override.yaml` bind-mounts this workspace into the container at `/app/gtm-loop-workspace` as read-only, then overlays `tasks/` as writable for status-only updates and `_audit/status-changes.jsonl`. Production mode may still use the image-baked copy of the workspace.

## Status Audit

`_audit/status-changes.jsonl` is a local JSON Lines audit for status transitions from `/gtm-loop/board`.

Each line records:

- `timestamp`
- `task_id`
- `old_board_status`
- `new_board_status`
- `actor`
- `source`
- `endpoint`
- `success`

It does not log task bodies, secrets, credentials, cookies, auth headers, or external payloads. It is not the main run ledger; use `../runs/index.md` for meaningful workbench runs.

## Browser Smoke Test

1. Log in to Open WebUI.
2. Open `http://localhost:3000/gtm-loop/board`.
3. Confirm the status panel says `API: loaded` and task count is `11`.
4. Search for `GTM-001` and confirm only matching cards remain.
5. Use the `Blocked` quick filter, confirm non-matching cards are hidden, and then clear filters.
6. Move one test task from `planned` to `in-progress`, then back to `planned`.
7. Confirm only `board_status` and `last_updated` changed in frontmatter.
8. Confirm two audit entries were appended to `_audit/status-changes.jsonl`.
9. Run `node scripts\validate-gtm-tasks.js`.

The board has only status-only writes and task-local audit appends. Task title, body, manager request, evidence, artifacts, credentials, and external system fields still happen in Markdown files, not in the UI.

## Board Mapping

| Task state | Board column |
| --- | --- |
| Not started | Planned |
| Ricky, Brody, Archy, or Cody/Codex work | In Progress |
| Verifier work | Smoke Test |
| Reporter or manager gate | In Review |
| Completed and accepted | Done |

`blocked`, `approval_required`, and `rework_needed` are frontmatter flags. They are badges on a task, not board columns.

## Swimlanes

| Lane | Owns |
| --- | --- |
| Ricky | Research and source-grounded investigation. |
| Brody | Requirements, integration investigation, and evidence. |
| Archy | Architecture, design, ADRs, and risk. |
| Cody/Codex | Implementation, build, and workflow construction. |
| Verifier | Smoke tests, validation, drift checks, and definition-of-done checks. |
| Reporter | Board summaries, run ledger updates, and manager reports. |

## Agent Update Order

1. Read `../workbench.md`, `../orchestrator/state.md`, and the relevant `tasks/GTM-###.md`.
2. Update the task frontmatter and body.
3. Update `../board.md` with the short manager-facing summary.
4. Update `../runs/index.md` only for meaningful runs.
5. Promote durable context to `../llm-wiki/` only when future agents need it before work.
