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

The board reads these task files through `GET /api/gtm-loop/tasks`. Manager status moves and drag/drop use `PATCH /api/gtm-loop/tasks/{task_id}/status` and may update only `board_status` and `last_updated` in YAML frontmatter. Drag/drop does not change `current_lane`, `current_phase`, or `current_gate`; use explicit orchestrator transition buttons for those fields. Moving to `done` through the status endpoint is blocked unless the task is unblocked, does not need rework, has any required approval approved, and is already in reporter/manager review state. Orchestrator swimlane/gate transitions use `PATCH /api/gtm-loop/tasks/{task_id}/transition` and may update only the safe transition fields needed for the selected lane/gate. Lane artifacts use `POST /api/gtm-loop/tasks/{task_id}/artifacts/{lane}` and may create deterministic Markdown starters only under `../artifacts/<task_id>/`, then update `artifact_links` and `last_updated`. Successful moves append a JSONL audit entry to `_audit/status-changes.jsonl`; artifact creation appends to `_audit/artifact-events.jsonl`. Card details read latest task changes through `GET /api/gtm-loop/tasks/{task_id}/audit`. Search and filters on `/gtm-loop/board` are client-side only and do not change task files, `board.md`, or the API response.

In local Docker development, `docker-compose.override.yaml` bind-mounts this workspace into the container at `/app/gtm-loop-workspace` as read-only, then overlays only `tasks/` and `artifacts/` as writable. Production mode may still use the image-baked copy of the workspace.

## Status Audit

`_audit/status-changes.jsonl` is a local JSON Lines audit for status and orchestrator transitions from `/gtm-loop/board`.

Each line records:

- `timestamp`
- `task_id`
- `transition` when a swimlane/gate transition was used
- `old_board_status`
- `new_board_status`
- `old_lane`, `new_lane`, `old_phase`, `new_phase`, `old_gate`, `new_gate` when present
- `actor`
- `source`
- `endpoint`
- `success`

It does not log task bodies, secrets, credentials, cookies, auth headers, or external payloads. The read-only audit endpoint returns only matching entries for one task, latest first. It is not the main run ledger; use `../runs/index.md` for meaningful workbench runs.

`_audit/artifact-events.jsonl` records local artifact creation events with timestamp, task id, lane, files created, files skipped, actor, source, endpoint, and success. It does not log artifact bodies or external payloads.

## Browser Smoke Test

1. Log in to Open WebUI.
2. Open `http://localhost:3000/gtm-loop/board`.
3. Confirm the status panel says `API: loaded` and task count is `11`.
4. Search for `GTM-001` and confirm only matching cards remain.
5. Use the `Blocked` quick filter, confirm non-matching cards are hidden, and then clear filters.
6. Move one test task from `planned` to `in-progress`, then back to `planned` using the dropdown or drag/drop.
7. Open card details and run `Pick up task`, `Send to Archy`, `Send to Verifier`, and `Send to Reporter`.
8. Confirm manager status moves changed only `board_status` and `last_updated`.
9. Confirm orchestrator transitions changed only lane/gate/status frontmatter and `last_updated`.
10. Create lane artifacts and confirm files appear under `../artifacts/<task_id>/`.
11. Confirm `artifact_links` and `_audit/artifact-events.jsonl` were updated.
12. Confirm audit entries were appended to `_audit/status-changes.jsonl`.
13. Restore the test task to its original state if needed.
14. Open card details and confirm latest task changes display.
15. Run `node scripts\validate-gtm-tasks.js`.

The board has only narrow status/transition writes, status-only drag/drop, deterministic artifact starter creation, and task-local audit appends. Task title, body, manager request, evidence, credentials, and external system fields still happen in Markdown files, not in the UI.

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

For Cody/build work, n8n MCP is draft-only and approval-gated. Agents may create local workflow draft artifacts and validate fake payloads, but must not create/update live workflows, activate workflows, call production webhooks, use credentials, or write HubSpot/Gong/AirOps/custom API data without explicit approval.

## Agent Update Order

1. Read `../workbench.md`, `../orchestrator/state.md`, and the relevant `tasks/GTM-###.md`.
2. Update the task frontmatter and body.
3. Update `../board.md` with the short manager-facing summary.
4. Update `../runs/index.md` only for meaningful runs.
5. Promote durable context to `../llm-wiki/` only when future agents need it before work.
