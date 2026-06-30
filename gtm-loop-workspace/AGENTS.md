# GTM Loop Agent Instructions

This workspace is a lean GTM/FDE engineering source of truth. Future Codex and Open WebUI agents should keep it practical, evidence-backed, and easy to maintain.

## Operating Rules

- Read `README.md` and `llm-wiki/llm-index.md` first.
- Read `workbench.md` for active client, enabled surfaces, and control files.
- Read `board.md` and keep one card current for the session.
- Start from `llm-wiki/current-client.md` before client work.
- Prefer updating existing Markdown over creating new structures.
- Keep reference repos and client/source repos read-only unless the user explicitly asks for implementation work there.
- Do not copy external repos wholesale. Extract patterns, summarize evidence, and link or cite source paths.
- Separate `Confirmed`, `Confirmed mismatch`, `Unknown`, `Inferred`, and `Recommendation`.
- Store detailed client facts in `clients/<client-slug>/`; promote durable shared facts into `llm-wiki/`.
- Use ADRs only for durable decisions with real alternatives.
- Keep prompts and handoffs short enough to paste into Open WebUI, Codex, n8n, or AirOps.

## Loop Engineering Mode

For issue solving, architecture, or build work:

1. Create or update one `board.md` card.
2. Classify the work as issue, investigation, research, architecture/design, build, validation, or memory update.
3. Check `tools/tool-registry.md` and `governance/approval-gates.md` before tool use or writes.
4. Use the matching workflow in `workflows/`.
5. Produce a build handoff before implementation.
6. Record validation before marking work done.
7. Log meaningful runs in `runs/index.md`.
8. Move the board card at closeout.

## Source Safety

- Never write secrets, tokens, endpoint hosts, tenant IDs, auth headers, copied logs, or raw customer records.
- Local settings prove key names only, not production values.
- Gong transcripts, CRM data, customer strategy, and workflow payloads are sensitive. Summarize and redact.
- Human approval is required before external writes, CRM changes, workflow activation, email/send actions, or commercial decisions.

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

- a row in `workflows/registry.md`;
- allowed and blocked tool actions in `tools/tool-registry.md`;
- approval gates checked in `governance/approval-gates.md`;
- fake/redacted payloads in `payloads/` or a linked existing sample;
- readiness checks from `evals/gtm-loop-evals.md`;
- a meaningful run entry in `runs/index.md`.

## Closeout

Before finishing a session:

- Update `llm-wiki/current-client.md` if client state changed.
- Update `llm-wiki/open-questions.md` with unresolved questions.
- Add or update client validation notes.
- Add or update a run ledger entry when the session changed workbench state.
- Confirm no sensitive values were written.
- State what remains unknown and what evidence would resolve it.
