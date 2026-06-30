# Workbench Manifest

Agent-readable control manifest for the GTM Loop automation workbench. Update this only when the active pointer or safety posture changes.

## Active Control State

| Field | Value |
| --- | --- |
| Orchestration level | `L1-report-only` |
| Kill switch | On |
| Active client | `TBD` |
| Client folder | `clients/TBD/` |
| Active task id | `GTM-001` |
| Active task file | `tasks/GTM-001.md` |
| Active run id | `TBD` |
| Current lane | Brody |
| Current board status | Planned |
| Current gate | Manager input required |
| Blocked | Yes |
| Attempt | `0/3` |
| Approval mode | Manual approval required for all external writes |
| Knowledge pack version | `v1-core` |
| Safety posture | Workstation Agent and GTM Loop UI are Knowledge-only; task files are local Markdown; external tool writes remain disabled |
| Last updated | `2026-06-30` |

## Enabled Tools

| Tool | Access | Notes |
| --- | --- | --- |
| Codex | Repo Markdown edits and local validation | Use minimal-change discipline. |
| Open WebUI Knowledge | Ready | Workstation Agent imported and Core Pack attached. |
| Open WebUI GTM Loop UI | Ready | Sidebar link and `/gtm-loop` page added; frontend Kanban board is not implemented yet. |
| codebase-memory-mcp | Ready | Use for code discovery before grep during coding tasks. |

## Disabled Or Unconfirmed Tools

| Tool | Status | Reason |
| --- | --- | --- |
| n8n MCP/API | Disabled | Tool access and approval rules not confirmed. |
| Board MCP | Deferred | `tasks/*.md` and `board.md` remain local Markdown until the task contract is stable. |
| HubSpot API | Unconfirmed | No write scope approved. |
| Gong API/export | Unconfirmed | Transcript/data handling not confirmed. |
| AirOps | Unconfirmed | Publish/run authority not confirmed. |
| Custom APIs | Unconfirmed | Endpoint/auth/write scope not confirmed. |
| GitHub MCP | Deferred | PR/issue sync should wait until local board control works. |
| Hermes | Deferred | Send/write surface not defined. |
| OpenHands | Deferred | Executor should wait for build handoff and verifier gates. |

## Control Files

| File | Role |
| --- | --- |
| `orchestrator/state.md` | Active orchestration level, kill switch, active task/run pointer, and attempt limits. |
| `orchestrator/transition-rules.md` | Allowed task and board mirror movement and done criteria. |
| `orchestrator/agent-routing.md` | Ricky, Brody, Archy, Cody/Codex, verifier, and reporter responsibilities. |
| `orchestrator/loop-constraints.md` | Report-only boundaries, stop conditions, human gates, and attempt caps. |
| `HOME.md` | Daily dashboard and quick links. |
| `UPDATE-OWNERSHIP.md` | Defines which file owns which updates. |
| `tasks/` | Canonical Markdown task files with YAML frontmatter. |
| `board.md` | Five-column manager-facing mirror over task files. |
| `schemas/task-card.md` | Required fields for each task file. |
| `schemas/board-card.md` | Required summary shape for board mirror entries. |
| `tools/tool-registry.md` | Tool access, allowed actions, blocked actions, owners. |
| `governance/approval-gates.md` | Actions requiring explicit human approval. |
| `workflows/registry.md` | Cross-client automation inventory and runtime status. |
| `runs/index.md` | Workbench run ledger. |
| `runs/_template.md` | Per-run evidence template. |
| `payloads/README.md` | Fake/redacted payload library rules. |
| `evals/gtm-loop-evals.md` | Workbench readiness checks. |

## Do Not Automate Yet

- API writes.
- Workflow activation.
- Production workflow retries.
- Email or external message sending.
- Credential, scope, or API key changes.
- Destructive filesystem or environment operations.
