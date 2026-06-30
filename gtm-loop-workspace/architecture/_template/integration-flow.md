# Integration Flow

## Flow Summary

`TBD`

## Sequence

```mermaid
sequenceDiagram
  participant Trigger
  participant Runtime as n8n/AirOps/custom
  participant CRM as HubSpot
  participant API as Custom API
  Trigger->>Runtime: event or schedule
  Runtime->>CRM: read context
  Runtime->>API: enrich or act
  Runtime-->>CRM: proposed or approved write
```

## Steps

| Step | System | Action | Data | Status | Evidence |
| --- | --- | --- | --- | --- | --- |
| 1 | `TBD` | `TBD` | `TBD` | Unknown | `TBD` |

## Failure Modes

| Failure | Expected Behavior | Owner | Evidence |
| --- | --- | --- | --- |
| `TBD` | Retry / skip / alert / manual review | `TBD` | `TBD` |

## Approval Gates

- `TBD`
