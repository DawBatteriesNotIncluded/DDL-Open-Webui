# Orchestrator State

Agent-readable state pointer for the GTM Loop workstation. Keep this short; `tasks/*.md` owns task state and `runs/` owns evidence.

## Current Level

| Field | Value |
| --- | --- |
| Orchestration level | `L1-report-only` |
| External writes | Disabled |
| Kill switch | On |
| Default max attempts | `3` |
| Implementer/verifier split | Required before Done |
| Last updated | `2026-06-30` |

## Active Pointer

| Field | Value |
| --- | --- |
| Active client | `TBD` |
| Client folder | `clients/TBD/` |
| Active task | `GTM-001` |
| Active task file | `tasks/GTM-001.md` |
| Active run | `TBD` |
| Current board status | Planned |
| Current lane | Brody |
| Current gate | Manager input required |
| Blocked | Yes |
| Next action | Manager provides first real client name and initial objective. |

## Level Ladder

| Level | Meaning | Current? |
| --- | --- | --- |
| `L0-docs` | Static workspace guidance only. | No |
| `L1-report-only` | Board-driven planning, drafts, handoffs, fake payload validation, and reports only. | Yes |
| `L2-read-only-tools` | Scoped inspection of external tools after registry confirmation. | No |
| `L3-draft-artifacts` | Draft workflow/config artifacts without activation or writes. | No |
| `L4-approval-gated-writes` | Exact human-approved writes only. | No |

## State Ownership

- `tasks/*.md` owns task status, lane, owner, attempts, gate, flags, evidence links, and next action.
- `board.md` mirrors the manager-facing five-column summary.
- `runs/` owns run evidence and verifier result.
- `workbench.md` mirrors the active pointer only.
- `llm-wiki/` owns durable memory after work is complete.
