# Open WebUI Setup

Minimal setup for using this repo as an automation AI workbench.

## Knowledge To Attach

Use `openwebui-knowledge-packs.md` for exact bundles. Attach the Core Pack first:

- `gtm-loop-workspace/README.md`
- `gtm-loop-workspace/AGENTS.md`
- `gtm-loop-workspace/HOME.md`
- `gtm-loop-workspace/UPDATE-OWNERSHIP.md`
- `gtm-loop-workspace/workbench.md`
- `gtm-loop-workspace/orchestrator/`
- `gtm-loop-workspace/schemas/board-card.md`
- `gtm-loop-workspace/board.md`
- `gtm-loop-workspace/llm-wiki/`
- `gtm-loop-workspace/workflows/`
- `gtm-loop-workspace/clients/_template/`
- `gtm-loop-workspace/tools/tool-registry.md`
- `gtm-loop-workspace/governance/approval-gates.md`
- `gtm-loop-workspace/runs/_template.md`
- `gtm-loop-workspace/evals/gtm-loop-evals.md`
- `gtm-loop-workspace/openwebui-knowledge-packs.md`

## Primary Agent

Import the ready Workstation Agent file first:

- `gtm-loop-workspace/imports/openwebui-workstation-agent.gpt-5.4.json`

If your base model is not `gpt-5.4`, use:

- `gtm-loop-workspace/imports/openwebui-workstation-agent.import.json`

and replace `__BASE_MODEL_ID__` with an existing Open WebUI model id.

Use this as the default cockpit agent for daily loop engineering.

Attach the Core Pack from `openwebui-knowledge-packs.md`.

## Local Docker Runtime

Verified local test URL:

```text
http://localhost:3000
```

The GTM Loop route is available at:

```text
http://localhost:3000/gtm-loop
```

The read-only GTM Loop Kanban board is available at:

```text
http://localhost:3000/gtm-loop/board
```

`/gtm-loop` is the cockpit dashboard. `/gtm-loop/board` is a visual board over `gtm-loop-workspace/tasks/*.md`; task files remain the source of truth. Board search and filters are client-side only over the task list returned by `GET /api/gtm-loop/tasks`. Status moves use a narrow authenticated PATCH endpoint that may update only `board_status` and `last_updated`, then append a local audit entry under `tasks/_audit/status-changes.jsonl`. Card details use `GET /api/gtm-loop/tasks/{task_id}/audit` to show the latest matching status changes.

Use the existing compose stack:

```powershell
docker compose ps
docker compose up -d
docker compose restart open-webui
docker compose stop open-webui
```

Local development uses `docker-compose.override.yaml` to mount `./gtm-loop-workspace` into the container at `/app/gtm-loop-workspace` as read-only, with only `./gtm-loop-workspace/tasks` overlaid as writable for status-only updates and the task-local audit log. Production/image-only runs can still use the workspace copied by the `Dockerfile` when the override is not applied.

Do not run the setup import scripts with real credentials. For v1, keep HubSpot, Gong, AirOps, n8n writes, workflow activation, and external API writes disabled.

## Specialist Agents

Add these only when needed:

| Agent | Use |
| --- | --- |
| `agents/loop-architect-agent.md` | Turn vague work into loop specs. |
| `agents/build-controller-agent.md` | Coordinate design, build, QA, and approval. |
| `agents/workflow-debugger-agent.md` | Diagnose failed workflows and payloads. |
| `agents/n8n-builder-agent.md` | Draft n8n workflow plans. |
| `agents/hubspot-architect-agent.md` | HubSpot object/field/workflow design. |
| `agents/gong-intelligence-agent.md` | Gong signal extraction and deal intelligence. |

## Tool Rule

Start with Knowledge-only. Add n8n, HubSpot, Gong, AirOps, API, or repo tools only after `tools/tool-registry.md` and `governance/approval-gates.md` define the allowed actions.

## First Run

1. Open `HOME.md`.
2. Read `orchestrator/state.md` and `orchestrator/loop-constraints.md`.
3. Run `node scripts\validate-gtm-tasks.js`; the board should be trusted only when validation passes.
4. Open `http://localhost:3000/gtm-loop` for the cockpit or `/gtm-loop/board` for the read-only board.
5. Set active client in `workbench.md` and `llm-wiki/current-client.md`.
6. Pick one structured task file under `tasks/`.
7. Create or resume a run from `runs/_template.md`.
8. Run the Loop Engineering Workstation Agent.
9. Log the result in `runs/index.md`.

Full card editing, drag/drop, and broad task writes are intentionally deferred. The only UI write path is changing task `board_status`, which also updates `last_updated` and appends a local status audit entry.

## Manual UI Smoke Test

1. Open `http://localhost:3000/gtm-loop` while logged in.
2. Open `http://localhost:3000/gtm-loop/board`.
3. Confirm the board status panel says `API: loaded`.
4. Confirm task count is `11`.
5. Confirm Planned, In Progress, Smoke Test, In Review, and Done columns render.
6. Search for a task id or client and confirm only matching cards remain.
7. Try quick filters: `Blocked`, `Approval Required`, `Rework Needed`, `In Review`, and `Smoke Test`; confirm non-matching cards are hidden.
8. Clear filters and confirm all cards return.
9. Move one test task from `planned` to `in-progress`, then back to `planned`.
10. Confirm only `board_status` and `last_updated` changed in task frontmatter.
11. Confirm two entries were appended to `gtm-loop-workspace/tasks/_audit/status-changes.jsonl`.
12. Open task card details and confirm latest status changes display.
13. Run `node scripts\validate-gtm-tasks.js`.

If the status panel says `unauthorized`, log in to Open WebUI and refresh. The GTM task API is intentionally authenticated.

## API Setup Option

If local Open WebUI is running and you have an API token:

```powershell
$env:OPENWEBUI_URL="http://localhost:3000"
$env:OPENWEBUI_API_KEY="PASTE_TOKEN_HERE"
powershell -NoProfile -ExecutionPolicy Bypass -File .\gtm-loop-workspace\imports\setup-openwebui-workspace.ps1
```

This imports the Workstation Agent, creates/reuses Knowledge collections from `imports/openwebui-workspace-manifest.json`, uploads the Core Pack files, and attaches the Core Pack to the agent.
