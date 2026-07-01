# Latest Codex Handoff

## Current Branch

`gtm-loop-workspace-v1`

## Latest Commit

`823c58ba1` - `Add drag and drop GTM board status movement`

## Working Tree Status

Dirty. Uncommitted work includes the local GTM approval queue implementation, docs updates, and this handoff.

Key dirty paths:

- `backend/open_webui/routers/gtm_loop.py`
- `src/lib/apis/gtm-loop/index.ts`
- `src/routes/(app)/gtm-loop/+page.svelte`
- `src/routes/(app)/gtm-loop/board/+page.svelte`
- `gtm-loop-workspace/`

## Built In This Session

Added the local GTM approval queue:

- Local approval records under `gtm-loop-workspace/tasks/_approvals/APP-####.json`.
- Approval audit events under `gtm-loop-workspace/tasks/_audit/approval-events.jsonl`.
- Authenticated approval endpoints for listing, task-specific listing, creation, and decisions.
- Cockpit approval summary counts on `/gtm-loop`.
- Board card approval section on `/gtm-loop/board`.
- Card-level approval request and approve/reject/defer/cancel actions.
- Done guards now check unresolved approval records as well as task summary fields.

## Current GTM Loop Capabilities

- Markdown task files are canonical.
- `node scripts/validate-gtm-tasks.js` validates task/board state.
- `/gtm-loop` cockpit loads task and approval summaries.
- `/gtm-loop/board` supports Kanban columns, filters, search, status dropdowns, and status-only drag/drop.
- Status moves, lane/gate transitions, artifact creation, and approval decisions are local and audited.
- Lane artifacts can be created under `gtm-loop-workspace/artifacts/<task_id>/`.
- n8n MCP is documented as available-local, draft-only, and approval-gated.

## Current Limitations

- Approval queue work is not committed yet.
- Docker has not been rebuilt with the new approval UI.
- Frontend `npm run check` was not run because local `node_modules` is absent.
- No n8n MCP calls exist.
- No external systems are connected.
- No broad card editing, drag/drop lane movement, or action execution exists.

## Current Safety Boundaries

- Approval records do not execute actions.
- No n8n workflow creation/update/activation.
- No HubSpot, Gong, AirOps, custom API, email, credential, webhook, or production data writes.
- Writes remain local: task frontmatter summaries, local approval JSON, and local audit JSONL.
- Requested/deferred approvals block Done.
- Future executor code must check for a matching approved approval before any live tool action.

## Current Local Runtime Status

Observed with `docker ps`:

| Container | Status | Surface |
| --- | --- | --- |
| `open-webui` | Up, healthy | `http://localhost:3000` |
| `ollama` | Up | internal `11434/tcp` |
| `n8n-mcp` | Up, healthy | `http://localhost:3001` |
| `n8n` | Up, healthy | `http://localhost:5678` |

## Inspect Next Time

- `backend/open_webui/routers/gtm_loop.py`
- `src/lib/apis/gtm-loop/index.ts`
- `src/routes/(app)/gtm-loop/+page.svelte`
- `src/routes/(app)/gtm-loop/board/+page.svelte`
- `gtm-loop-workspace/tasks/_approvals/`
- `gtm-loop-workspace/tasks/_audit/approval-events.jsonl`
- `gtm-loop-workspace/governance/approval-gates.md`
- `gtm-loop-workspace/orchestrator/transition-rules.md`
- `gtm-loop-workspace/runs/index.md`

## Recommended Next Task

Rebuild/restart Docker, manually test the approval queue UI in a logged-in browser, then commit the approval queue work if the smoke test passes.

Suggested checks:

```powershell
docker compose up -d --build open-webui
node scripts\validate-gtm-tasks.js
git diff --check -- gtm-loop-workspace scripts src backend Dockerfile docker-compose.yaml docker-compose.override.yaml
```

Browser smoke:

1. Open `http://localhost:3000/gtm-loop`.
2. Confirm approval counts load.
3. Open `http://localhost:3000/gtm-loop/board`.
4. Open `GTM-001` details.
5. Create a fake/redacted approval request.
6. Approve, defer, reject, or cancel it.
7. Confirm `tasks/_approvals/APP-####.json` and `tasks/_audit/approval-events.jsonl` update.
8. Confirm validator still passes.

## Exact Continuation Prompt

```text
You are working in the current Open WebUI repo on branch gtm-loop-workspace-v1.

Start by reading gtm-loop-workspace/runs/latest-codex-handoff.md.

The latest commit is 823c58ba1. The working tree contains uncommitted local GTM approval queue work. Do not add new functionality yet.

Task:
1. Inspect the current diff.
2. Rebuild/restart Docker if needed so the new approval UI is live.
3. Run:
   node scripts\validate-gtm-tasks.js
   git diff --check -- gtm-loop-workspace scripts src backend Dockerfile docker-compose.yaml docker-compose.override.yaml
4. Smoke test /gtm-loop and /gtm-loop/board in a logged-in browser.
5. Create a fake/redacted approval request for GTM-001, make one decision, confirm approval JSON and audit JSONL update, then restore/clean up any test approval if appropriate.
6. If all checks pass, report status and ask whether to commit.

Do not connect n8n MCP.
Do not call external APIs.
Do not activate workflows.
Do not add credentials.
Do not execute approved actions.
```
