# Workbench Manifest

Current control surface for the GTM Loop automation workbench.

## Active State

| Field | Value |
| --- | --- |
| Active client | `TBD` |
| Client folder | `clients/TBD/` |
| Active board card | `TBD` |
| Current stage | Backlog / Investigating / Designing / Building / Validating / Blocked / Done |
| Primary agent | `agents/loop-engineering-workstation-agent.md` |
| Last updated | `TBD` |

## Enabled Surfaces

| Surface | Purpose | Status | Registry |
| --- | --- | --- | --- |
| Open WebUI | Cockpit, reasoning, review, knowledge | Planned | `openwebui-setup.md` |
| Codex | Files, repo work, scripts, validation | Available in this repo | `.agents/skills/gtm-loop-engineering/SKILL.md` |
| n8n | Workflow runtime | Unknown | `tools/tool-registry.md` |
| HubSpot | CRM | Unknown | `tools/tool-registry.md` |
| Gong | Calls and transcripts | Unknown | `tools/tool-registry.md` |
| AirOps | Content and prompt workflows | Unknown | `tools/tool-registry.md` |
| Custom APIs | Client/internal integrations | Unknown | `tools/tool-registry.md` |

## Control Files

| File | Role |
| --- | --- |
| `HOME.md` | Daily dashboard and quick links. |
| `board.md` | Work queue and stage control. |
| `tools/tool-registry.md` | Tool access, allowed actions, blocked actions, owners. |
| `governance/approval-gates.md` | Actions requiring explicit human approval. |
| `workflows/registry.md` | Automation inventory and runtime status. |
| `runs/index.md` | Workbench run ledger. |
| `payloads/README.md` | Fake/redacted payload library rules. |
| `evals/gtm-loop-evals.md` | Workbench readiness checks. |

## Rule

No external write, workflow activation, credential change, CRM mutation, or customer-facing send happens from this workbench without explicit human approval for that exact action.
