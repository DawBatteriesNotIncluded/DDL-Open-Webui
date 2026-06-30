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
- `/gtm-loop/board` is a read-only frontend board over task files; editing and card movement are deferred.
- Future frontend board work should rely on task files that pass `scripts/validate-gtm-tasks.js`.

## Source Safety

- Never write secrets, tokens, endpoint hosts, tenant IDs, auth headers, copied logs, or raw customer records.
- Local settings prove key names only, not production values.
- Gong transcripts, CRM data, customer strategy, and workflow payloads are sensitive. Summarize and redact.
- Human approval is required before external writes, CRM changes, workflow activation, email/send actions, or commercial decisions.

## Do Not Automate Yet

For v1, agents may plan, draft, validate, and prepare approval requests, but must not execute:

- API writes or production data mutation;
- workflow activation, deactivation, or production retry;
- email sends or external messages;
- credential, token, scope, or API key changes;
- destructive filesystem, container, database, or environment operations.

Task validation must pass before connecting any executor, MCP write path, or external automation surface.

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
