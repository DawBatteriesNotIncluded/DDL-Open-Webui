# GTM Loop Agent Instructions

This workspace is a lean GTM/FDE engineering source of truth. Future Codex and Open WebUI agents should keep it practical, evidence-backed, and easy to maintain.

## Operating Rules

- Start from `HOME.md`.
- Read `workbench.md` for active client, active task, lane, enabled surfaces, and safety posture.
- Read `orchestrator/state.md`, `orchestrator/loop-constraints.md`, `orchestrator/transition-rules.md`, and `orchestrator/agent-routing.md` before moving work.
- Read the active task file under `tasks/` before acting.
- Read `llm-wiki/llm-index.md` for durable agent memory.
- Read `UPDATE-OWNERSHIP.md` before changing status, tasks, run history, tools, or client facts.
- Use `tasks/*.md` as the canonical task source of truth, following `schemas/task-card.md`.
- Use `board.md` as a manager-facing five-column mirror only.
- Run `node scripts\validate-gtm-tasks.js` after changing task files or `board.md`.
- Start from `llm-wiki/current-client.md` before client work.
- Prefer updating existing Markdown over creating new structures.
- Keep reference repos and client/source repos read-only unless the user explicitly asks for implementation work there.
- Do not copy external repos wholesale. Extract patterns, summarize evidence, and link or cite source paths.
- Separate `Confirmed`, `Confirmed mismatch`, `Unknown`, `Inferred`, and `Recommendation`.
- Store detailed client facts in `clients/<client-slug>/`; promote durable shared facts into `llm-wiki/`.
- Use ADRs only for durable decisions with real alternatives.
- Keep prompts and handoffs short enough to paste into Open WebUI, Codex, n8n, or AirOps.
- For repo/code understanding during coding tasks, prefer codebase-memory-mcp tools before grep or ad hoc file search.
- Apply Ponytail-style minimal-change discipline: reuse existing patterns, avoid dependencies, and make the smallest change that works.

## Loop Engineering Mode

For issue solving, architecture, or build work:

1. Create or update one structured `tasks/GTM-###.md` task.
2. Create or resume one run using `runs/_template.md`.
3. Classify the work as issue, investigation, research, architecture/design, build, validation, or memory update.
4. Route roles through `orchestrator/agent-routing.md`.
5. Check `orchestrator/loop-constraints.md`, `tools/tool-registry.md`, and `governance/approval-gates.md` before tool use or writes.
6. Use the matching workflow in `workflows/`.
7. Produce a build handoff before implementation.
8. Record verifier evidence before marking work done.
9. Log meaningful runs in `runs/index.md`.
10. Update the task file first, then update the `board.md` mirror according to `orchestrator/transition-rules.md`.
11. Run `node scripts\validate-gtm-tasks.js` before closeout.

## Board Model

- `tasks/*.md` is canonical.
- `board.md` is a manager-facing mirror.
- Board columns are only Planned, In Progress, Smoke Test, In Review, and Done.
- `Blocked`, `Approval Required`, and `Rework Needed` are task frontmatter flags, not board columns.
- Detailed loop state and swimlane history belong inside task files.
- `/gtm-loop/board` has two narrow write paths: manager status moves and orchestrator swimlane/gate transitions.
- Status moves may update only `board_status` and `last_updated`.
- Drag/drop is a status move only. It must use the status endpoint, must not mutate lane/phase/gate, and must keep the existing audit behavior.
- Moving a task to Done through status movement is blocked unless the task is unblocked, does not need rework, has required approval approved, and is already in reporter/manager review state.
- Requested or deferred approval records under `tasks/_approvals/` also block Done, even if task frontmatter is stale.
- Orchestrator transitions may update only the required safe task frontmatter fields: `board_status`, `current_lane`, `current_phase`, `current_gate`, `next_action`, `manager_summary`, `rework_needed`, `current_attempt`, `blocked`, and `last_updated`.
- Lane artifact creation may write only deterministic local Markdown starters under `artifacts/<task-id>/` and may update only `artifact_links` plus `last_updated` in task frontmatter.
- The n8n workflow draft action is a Cody/build-lane artifact action only. It may create `artifacts/<task-id>/build/n8n-workflow-draft.md`, update task artifact/summary frontmatter, and append artifact audit; it must not call n8n MCP or create/update/activate workflows.
- Approval requests and decisions may write only `tasks/_approvals/APP-####.json`, task approval summary frontmatter, and `tasks/_audit/approval-events.jsonl`.
- Approval records are intent records only. An approved record does not execute the action; future executor code must check for a matching approved approval before any tool call.
- Status and transition changes append local JSONL audit entries under `tasks/_audit/status-changes.jsonl`; this is task-local transition audit, not the main run ledger.
- n8n MCP is a Cody/build-lane draft executor surface only. Agents may draft local specs, draft JSON, and fake payload validation notes, but must not create, update, activate, or run live n8n workflows without explicit approval for the exact action.
- Full card editing, body editing, evidence editing, credentials, external systems, drag/drop lane transitions, and workflow activation remain blocked.
- Future frontend board work should rely on task files that pass `scripts/validate-gtm-tasks.js`.

## Source Safety

- Never write secrets, tokens, endpoint hosts, tenant IDs, auth headers, copied logs, or raw customer records.
- Local settings prove key names only, not production values.
- Gong transcripts, CRM data, customer strategy, and workflow payloads are sensitive. Summarize and redact.
- Human approval is required before external writes, CRM changes, workflow activation, email/send actions, or commercial decisions.
- Use local approval records for exact risky actions. Do not treat chat approval, a task flag, or a board move as enough for future live tool execution.

## Do Not Automate Yet

For v1, agents may plan, draft, validate, and prepare approval requests, but must not execute:

- API writes or production data mutation;
- workflow activation, deactivation, or production retry;
- n8n workflow creation/update, live webhook calls, scheduled production triggers, or credential use;
- email sends or external messages;
- credential, token, scope, or API key changes;
- destructive filesystem, container, database, or environment operations.

Task validation must pass before connecting any executor, MCP write path, or external automation surface. Local n8n draft Markdown creation is allowed without approval because it uses fake/redacted payload links only and executes nothing.

Local approval records are allowed in v1 because they do not execute actions. Store one approval per exact future action under `tasks/_approvals/APP-####.json`, and audit requests/decisions in `tasks/_audit/approval-events.jsonl`. New approvals must start as `requested`; `approved`, `rejected`, and `cancelled` are terminal decision states. Reject, defer, and cancelled approvals keep execution blocked unless a later exact approval is requested and approved.

## Investigation Standard

Every client or integration investigation should leave:

- current objective and scope;
- evidence consulted;
- confirmed facts;
- mismatches;
- unknowns and owner questions;
- endpoint or workflow matrix when APIs or automations are involved;
- field mapping when data crosses systems;
- configuration inventory with names only;
- validation notes;
- build handoff if implementation is needed.

## Automation Workbench Standard

Every automation intended for repeated use should have:

- a task file that follows `schemas/task-card.md`;
- a board summary in `board.md`;
- a row in `workflows/registry.md`;
- allowed and blocked tool actions in `tools/tool-registry.md`;
- approval gates checked in `governance/approval-gates.md`;
- fake/redacted payloads in `payloads/` or a linked existing sample;
- readiness checks from `evals/gtm-loop-evals.md`;
- a meaningful run entry in `runs/index.md`.

## Closeout

Before finishing a session:

- Confirm the active task and run pointer still match `orchestrator/state.md` and `workbench.md`.
- Update the task file before the board mirror.
- Update `llm-wiki/current-client.md` if client state changed.
- Update `llm-wiki/open-questions.md` with unresolved questions.
- Add or update client validation notes.
- Add or update a run ledger entry when the session changed workbench state.
- Confirm no sensitive values were written.
- State what remains unknown and what evidence would resolve it.
