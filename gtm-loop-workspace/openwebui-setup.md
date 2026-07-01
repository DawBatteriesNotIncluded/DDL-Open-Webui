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

The GTM Loop Kanban board is available at:

```text
http://localhost:3000/gtm-loop/board
```

`/gtm-loop` is the cockpit dashboard. `/gtm-loop/board` is a visual board over `gtm-loop-workspace/tasks/*.md`; task files remain the source of truth. Board search and filters are client-side only over the task list returned by `GET /api/gtm-loop/tasks`. Manager status moves and drag/drop use a narrow authenticated PATCH endpoint that may update only `board_status` and `last_updated`. Drag/drop is status-only and does not change lane, phase, or gate state. Moving to Done is guarded by blocked, rework, unresolved approvals, approval summary, and reporter/manager review checks. Orchestrator transitions use a separate narrow authenticated PATCH endpoint for swimlane/gate progression. Lane artifact creation uses a narrow authenticated POST endpoint that creates deterministic Markdown starters under `artifacts/<task_id>/` and updates `artifact_links`. Cody/build tasks can also create a local `n8n-workflow-draft.md` artifact; this is file-only and does not call n8n MCP. Approval queue endpoints store local JSON records under `tasks/_approvals/`, update only task approval summary frontmatter, and never execute the requested action. New approvals always start as `requested`; approved, rejected, and cancelled decisions are terminal. Status and transition moves append local audit entries under `tasks/_audit/status-changes.jsonl`; artifact creation appends to `tasks/_audit/artifact-events.jsonl`; approval requests and decisions append to `tasks/_audit/approval-events.jsonl`. Card details use `GET /api/gtm-loop/tasks/{task_id}/audit` to show the latest matching task changes.

Use the existing compose stack:

```powershell
docker compose ps
docker compose up -d
docker compose restart open-webui
docker compose stop open-webui
```

Local development uses `docker-compose.override.yaml` to mount `./gtm-loop-workspace` into the container at `/app/gtm-loop-workspace` as read-only, with only `./gtm-loop-workspace/tasks` and `./gtm-loop-workspace/artifacts` overlaid as writable. Production/image-only runs can still use the workspace copied by the `Dockerfile` when the override is not applied.

Local n8n and n8n MCP containers may be available on the developer machine. Treat them as draft-only unless the user explicitly approves a specific live action. Use `integrations/n8n-mcp.md` and `executors/n8n-draft-executor.md` as Knowledge references for allowed draft behavior. The GTM Loop UI does not call n8n MCP in this pass.

Do not run the setup import scripts with real credentials. For v1, keep HubSpot, Gong, AirOps, n8n writes, workflow activation, live webhooks, and external API writes disabled.

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

For n8n MCP, the current allowed mode is `available-local / draft-only / approval-gated`: inspect local availability, draft local workflow artifacts, prepare draft JSON, and validate fake payloads. The board's n8n draft button creates local Markdown only. Do not enable live workflow creation, updates, activation, production webhooks, credential use, or external writes from Open WebUI without explicit approval.

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

Full card editing, drag/drop lane transitions, action execution, and broad task writes are intentionally deferred. The UI write paths are limited to manager status movement, status-only drag/drop, orchestrator swimlane/gate transitions, deterministic local Markdown artifact creation, and local approval records.

## Manual UI Smoke Test

1. Open `http://localhost:3000/gtm-loop` while logged in.
2. Open `http://localhost:3000/gtm-loop/board`.
3. Confirm the board status panel says `API: loaded`.
4. Confirm task count is `11`.
5. Confirm Planned, In Progress, Smoke Test, In Review, and Done columns render.
6. Search for a task id or client and confirm only matching cards remain.
7. Try quick filters: `Blocked`, `Approval Required`, `Rework Needed`, `In Review`, and `Smoke Test`; confirm non-matching cards are hidden.
8. Clear filters and confirm all cards return.
9. Move one test task from `planned` to `in-progress`, then back to `planned` using the dropdown or drag/drop.
10. Open task details and run `Pick up task`, `Send to Archy`, `Send to Verifier`, and `Send to Reporter`.
11. Confirm status moves changed only `board_status` and `last_updated`.
12. Confirm orchestrator transitions changed only lane/gate/status frontmatter and `last_updated`.
13. Create lane artifacts and confirm files appear under `gtm-loop-workspace/artifacts/<task_id>/`.
14. Confirm `artifact_links` and `gtm-loop-workspace/tasks/_audit/artifact-events.jsonl` were updated.
15. For a Cody/build task, create the local n8n workflow draft and confirm `gtm-loop-workspace/artifacts/<task_id>/build/n8n-workflow-draft.md` exists.
16. Confirm entries were appended to `gtm-loop-workspace/tasks/_audit/status-changes.jsonl`.
17. Restore the test task to its original state if needed.
18. Open task card details and confirm latest task changes display.
19. Create a local approval request, then approve/defer/reject/cancel it.
20. Confirm `gtm-loop-workspace/tasks/_approvals/APP-####.json` and `gtm-loop-workspace/tasks/_audit/approval-events.jsonl` update.
21. Run `node scripts\validate-gtm-tasks.js`.

If the status panel says `unauthorized`, log in to Open WebUI and refresh. The GTM task API is intentionally authenticated.

## API Setup Option

If local Open WebUI is running and you have an API token:

```powershell
$env:OPENWEBUI_URL="http://localhost:3000"
$env:OPENWEBUI_API_KEY="PASTE_TOKEN_HERE"
powershell -NoProfile -ExecutionPolicy Bypass -File .\gtm-loop-workspace\imports\setup-openwebui-workspace.ps1
```

This imports the Workstation Agent, creates/reuses Knowledge collections from `imports/openwebui-workspace-manifest.json`, uploads the Core Pack files, and attaches the Core Pack to the agent.
