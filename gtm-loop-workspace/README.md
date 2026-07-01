# GTM Loop Workspace

Lean Markdown workspace for GTM and Forward Deployed AI Solutions Engineering inside Open WebUI.

Use it to keep task state, client context, system maps, field mappings, workflow inventories, research notes, architecture decisions, and Codex/n8n/AirOps handoffs in one agent-readable source of truth.

## Start Here

1. Open `HOME.md`.
2. Read `AGENTS.md` before asking an agent to work in this workspace.
3. Read `workbench.md` for active workbench state.
4. Read `orchestrator/state.md`, `orchestrator/loop-constraints.md`, `orchestrator/transition-rules.md`, and `orchestrator/agent-routing.md`.
5. Read `UPDATE-OWNERSHIP.md` to understand where updates belong.
6. Read `llm-wiki/llm-index.md` for current context and routing.
7. Check `tasks/` for canonical task files.
8. Check `board.md` for the manager-facing board mirror.
9. Pick or create a client folder from `clients/_template/`.
10. Run the daily loop in `workflows/daily-operating-loop.md`.
11. Keep confirmed facts, mismatches, unknowns, and evidence separate.
12. Promote stable findings back into `llm-wiki/` so future agents start with the right context.

## Folder Map

| Path | Use |
| --- | --- |
| `HOME.md` | Daily dashboard for active client, active task, tools, readiness, quick links, and end-of-session checks. |
| `UPDATE-OWNERSHIP.md` | Rules for which file owns which update. |
| `workbench.md` | Current workbench manifest: active client, tools, control files, and safety rule. |
| `orchestrator/` | Report-only control spine: state pointer, constraints, transition rules, and agent routing. |
| `tasks/` | Canonical Markdown task files with YAML frontmatter. |
| `schemas/task-card.md` | Required task file/frontmatter contract. |
| `schemas/board-card.md` | Short manager-facing board mirror format. |
| `board.md` | Five-column manager-facing mirror over `tasks/*.md`; not the source of truth. |
| `agents/` | Open WebUI system prompts, including the Loop Engineering Workstation Agent. |
| `llm-wiki/` | Agent-readable source of truth: current client, system map, shared context, open questions, repo index, and reusable patterns. |
| `clients/_template/` | Client dossier template for HubSpot, Gong, AirOps, n8n, custom APIs, field mappings, endpoints, config, validation, and build handoff. |
| `tools/tool-registry.md` | Tool registry for access level, allowed actions, blocked actions, owner, and evidence. |
| `governance/approval-gates.md` | Hard approval rules for writes, sends, activation, retries, credentials, and destructive actions. |
| `runs/index.md` | Run ledger for investigations, builds, validations, debugging, and approval requests. |
| `runs/_template.md` | Per-run evidence template. |
| `payloads/` | Fake/redacted payload library for testing without real client data. |
| `research/_template/` | Ricky-style research session template with brief, sources, notes, and evidence cards. |
| `architecture/_template/` | Archy-style system map, integration flow, ADR, risk/threat model, and architecture review templates. |
| `prompts/` | Ready-to-paste prompts for Codex, client discovery, troubleshooting, and platform-specific design work. |
| `workflows/` | Repeatable operating loops for investigation, research, design, build, validation, and daily use. |
| `workflows/registry.md` | Cross-client registry of automations and runtime status. |
| `evals/gtm-loop-evals.md` | Grounding, safety, build-readiness, and validation checks. |
| `openwebui-setup.md` | Minimal setup guide for turning the workspace into Open WebUI Knowledge and agents. |
| `openwebui-knowledge-packs.md` | Recommended Knowledge bundles for global, client, tool, workflow, research, architecture, and build agents. |

Existing folders such as `agents/`, `build-system/`, `evals/`, `knowledge/`, `loops/`, and `workflow-templates/` are supporting material from the broader cockpit setup. Use them when helpful; do not let them replace the task files, board mirror, and orchestrator control files above.

## Task Model

`tasks/*.md` is the canonical source of truth. Each task has YAML frontmatter for structured state and a body for manager request, interpreted objective, status, lane history, gates, evidence, artifacts, decisions, open questions, next action, and manager report.

`board.md` is a manager-facing mirror with five columns only:

- Planned
- In Progress
- Smoke Test
- In Review
- Done

Detailed loop state stays inside task files. `Blocked`, `Approval Required`, and `Rework Needed` are task flags, not board columns.

`/gtm-loop` is the Open WebUI cockpit dashboard. `/gtm-loop/board` is the visual Kanban board over the local task files. It has one narrow write path: logged-in users may update `board_status`, which also refreshes `last_updated`. Full card editing and external actions remain blocked.

## Task Validation

Run the local validator from the repo root after changing `tasks/GTM-*.md` or `board.md`:

```powershell
node scripts\validate-gtm-tasks.js
```

It checks required frontmatter, allowed enum values, booleans, numeric fields, filename/id alignment, attempt limits, board links, board sections, board/task status alignment warnings, and suspicious credential-style frontmatter values.

Future frontend board work should read only from valid task files. Task validation must pass before connecting any executor, MCP write path, or external automation surface.

## Open WebUI Routes

| Route | Use |
| --- | --- |
| `/gtm-loop` | Cockpit dashboard with task counts, safety posture, starter prompt, and links. |
| `/gtm-loop/board` | Kanban board grouped by `board_status` from `tasks/*.md`, with client-side search, filters, status-only task updates, and latest status audit in card details. |

The board loads task metadata through `GET /api/gtm-loop/tasks`. Status moves use `PATCH /api/gtm-loop/tasks/{task_id}/status` and may change only `board_status` and `last_updated` in YAML frontmatter. Successful status moves append a local JSONL audit entry to `tasks/_audit/status-changes.jsonl`. Card details read the latest status changes through `GET /api/gtm-loop/tasks/{task_id}/audit`. It does not edit title, body, artifacts, manager request, evidence, credentials, or external system fields. It does not call external APIs or connect to n8n. Search and filters run client-side in the browser over the loaded task list.

In local Docker development, `docker-compose.override.yaml` mounts `./gtm-loop-workspace` into `/app/gtm-loop-workspace` read-only and overlays `./gtm-loop-workspace/tasks` as writable for status-only task updates and the task-local audit log. The `Dockerfile` still packages the workspace for image-baked runs where the override is not used.

Manual board smoke test:

1. Open `http://localhost:3000/gtm-loop` while logged in.
2. Open `http://localhost:3000/gtm-loop/board`.
3. Confirm the board status panel says loaded and task count is `11`.
4. Confirm the five columns render.
5. Search for `GTM-001` and confirm only matching cards remain.
6. Use quick filters such as `Blocked`, `In Review`, or `Smoke Test` and confirm non-matching cards are hidden.
7. Clear filters and confirm all task cards return.
8. Move one test task from `planned` to `in-progress`, then back to `planned`.
9. Confirm only `board_status` and `last_updated` changed in task frontmatter.
10. Confirm two entries were appended to `tasks/_audit/status-changes.jsonl`.
11. Open the task card details and confirm latest status changes display.
12. Run `node scripts\validate-gtm-tasks.js`.

## Evidence Labels

Use these labels everywhere:

| Label | Meaning |
| --- | --- |
| `Confirmed` | Direct source evidence supports the claim. |
| `Confirmed mismatch` | Source evidence contradicts a claim, assumption, doc, or stakeholder statement. |
| `Unknown` | Evidence is missing or insufficient. |
| `Inferred` | Evidence suggests the claim, but it is not production truth. |
| `Recommendation` | Proposed next action based on confirmed facts and stated assumptions. |

## Agentic Loop Mode

Use `agents/loop-engineering-workstation-agent.md` as the primary Open WebUI control agent. It should keep one `tasks/GTM-###.md` task active, follow `orchestrator/`, route work through `workflows/`, update the task file before `board.md`, update owning client files, and promote durable context to `llm-wiki/`.

## Update Ownership

Use `UPDATE-OWNERSHIP.md` when deciding where to write. Short version:

- `HOME.md`: daily dashboard only.
- `README.md`: static workspace overview.
- `workbench.md`: active control manifest.
- `orchestrator/`: state pointer, constraints, transition rules, and agent routing.
- `tasks/`: canonical task state and detailed task history.
- `board.md`: manager-facing five-column mirror over task files.
- `llm-wiki/`: durable agent memory.
- `clients/<client-slug>/`: client-specific source of truth.
- `runs/index.md`: meaningful run audit trail.
- `tools/tool-registry.md`: tools, permissions, and blocked actions.
- `workflows/registry.md`: cross-client automation inventory.

## Daily Use

1. Start in `workbench.md`, `orchestrator/state.md`, and `llm-wiki/current-client.md`.
2. Open the relevant task file under `tasks/`.
3. Update task frontmatter/body first, then update the `board.md` mirror.
4. Run `node scripts\validate-gtm-tasks.js`.
5. Create or resume a run from `runs/_template.md`.
6. Open the client folder and update `context.md`, `systems.md`, and `open-questions.md`.
7. Check `orchestrator/loop-constraints.md`, `tools/tool-registry.md`, and `governance/approval-gates.md` before using tools or planning writes.
8. Investigate systems using `workflows/investigate.md`.
9. Capture flows in `workflow-inventory.md`, `endpoint-matrix.md`, `field-mapping.md`, and `workflows/registry.md`.
10. Use `architecture/_template/` when the flow needs boundaries, risks, or an ADR.
11. Use `research/_template/` when external tool or repo research needs an audit trail.
12. Generate build handoffs in `build-handoff.md`.
13. Validate with fake/redacted payloads and `evals/gtm-loop-evals.md`.
14. Log meaningful work in `runs/index.md`.
15. Update the relevant `llm-wiki/` pages before ending the session.

## Safety Rules

- Do not store secrets, tokens, endpoint hosts, tenant IDs, auth headers, or copied logs.
- Record setting names and ownership only.
- Treat Gong transcripts, CRM records, sponsor data, sales strategy, and workflow payloads as sensitive.
- Use fake or redacted payloads for examples.
- Require human approval before CRM writes, external messages, email sends, production workflow activation, or commercial decisions.
- Keep Open WebUI as the cockpit, this folder as source of truth, and n8n/AirOps/custom code as execution surfaces.

## Do Not Automate Yet

No external API writes, workflow activation, email sending, credential changes, production retries, or destructive operations from this workbench without explicit approval for the exact action. The only local write path is status-only task frontmatter updates plus task-local status audit entries.

## Status Audit

`tasks/_audit/status-changes.jsonl` records local status transitions only. Each line includes timestamp, task id, old status, new status, actor when available, source, endpoint, and success. `GET /api/gtm-loop/tasks/{task_id}/audit` returns the latest matching entries for one task only. It does not store or return task bodies, secrets, credentials, cookies, auth headers, or external system payloads. Use `runs/index.md` for meaningful workbench runs; the JSONL file is only a lightweight transition audit.
