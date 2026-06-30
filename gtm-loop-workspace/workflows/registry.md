# Workflow Registry

Inventory of automations known to the workbench.

This file owns cross-client automation lifecycle status. Per-client workflow details belong in `clients/<client-slug>/workflow-inventory.md`.

| Workflow | Client | Runtime | Trigger | Systems | Status | Owner | Last Validated | Approval Gate | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `TBD` | `TBD` | n8n / AirOps / custom / manual | `TBD` | `TBD` | Proposed / Test / Active / Paused / Retired / Unknown | `TBD` | `TBD` | Yes / No / Unknown | `TBD` |

## Status Values

- `Proposed`: design exists, not built.
- `Test`: built or simulated outside production.
- `Active`: running in production.
- `Paused`: exists but disabled.
- `Retired`: no longer used.
- `Unknown`: not enough evidence.

## Registry Rule

Add a row here only when an automation is useful outside a single client note or needs lifecycle tracking.
