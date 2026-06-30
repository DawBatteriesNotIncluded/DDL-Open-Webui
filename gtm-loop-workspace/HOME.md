# GTM Loop Home

Daily start page for the automation AI workbench. Update this page for quick status only; durable facts belong in the owner files listed in `UPDATE-OWNERSHIP.md`.

## Today

| Field | Value |
| --- | --- |
| Active client | `TBD` |
| Active task | `GTM-001` |
| Active run | `TBD` |
| Orchestration level | `L1-report-only` |
| Current lane | Brody |
| Board status | Planned |
| Readiness | Blocked on manager input |
| Kill switch | On |
| Primary agent | `agents/loop-engineering-workstation-agent.md` |
| Last updated | `2026-06-30` |

## Blocked Items

| Blocker | Owner | Needed To Unblock | Link |
| --- | --- | --- | --- |
| Active client not confirmed | User | Client name and first objective | `llm-wiki/current-client.md` |

## Next 3 Actions

1. Open `tasks/GTM-001.md`.
2. Provide the first real client name and initial automation objective.
3. Update `tasks/GTM-001.md`, then mirror the summary in `board.md`.

## Readiness Snapshot

| Area | Status | Source |
| --- | --- | --- |
| Workbench manifest | Ready for first client | `workbench.md` |
| Orchestrator spine | Ready for report-only mode | `orchestrator/state.md` |
| Task source of truth | Ready | `tasks/GTM-001.md` |
| Board mirror | Five-column manager view | `board.md` |
| Open WebUI cockpit | Ready | `src/routes/(app)/gtm-loop/+page.svelte` |
| Open WebUI read-only board | Ready | `src/routes/(app)/gtm-loop/board/+page.svelte` |
| Client context | Missing | `clients/onboarding.md` |
| Tool permissions | Unknown | `tools/tool-registry.md` |
| Approval gates | Draft | `governance/approval-gates.md` |
| Knowledge packs | Core Pack attached | `openwebui-knowledge-packs.md` |
| Fake payloads | Started | `payloads/` |

## Quick Links

| Need | Open |
| --- | --- |
| What to update where | `UPDATE-OWNERSHIP.md` |
| Workbench manifest | `workbench.md` |
| Orchestrator state | `orchestrator/state.md` |
| Transition rules | `orchestrator/transition-rules.md` |
| Task schema | `schemas/task-card.md` |
| Task files | `tasks/` |
| Kanban mirror | `board.md` |
| Open WebUI cockpit | `/gtm-loop` |
| Read-only Kanban board | `/gtm-loop/board` |
| Agent memory | `llm-wiki/llm-index.md` |
| First client onboarding | `clients/onboarding.md` |
| Tool access | `tools/tool-registry.md` |
| Approval rules | `governance/approval-gates.md` |
| Workflow registry | `workflows/registry.md` |
| Run ledger | `runs/index.md` |
| Readiness checks | `evals/gtm-loop-evals.md` |
| Open WebUI packs | `openwebui-knowledge-packs.md` |

## Safety Reminders

- No secrets, endpoint hosts, tenant IDs, auth headers, copied logs, or real customer records.
- No API writes, workflow activation, email sending, credential changes, or destructive operations without explicit approval.
- Use fake/redacted payloads only.
- If evidence is missing, mark it `Unknown`.
- Update `tasks/*.md` before updating `board.md`.
- Run `node scripts\validate-gtm-tasks.js` before trusting the board.
- UI editing and card movement are deferred.
