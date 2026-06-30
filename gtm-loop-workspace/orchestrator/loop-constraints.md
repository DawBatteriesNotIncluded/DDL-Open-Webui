# Loop Constraints

Safety and control constraints for the report-only orchestrator.

## Current Mode

`L1-report-only`

Agents may plan, investigate, design, draft, validate fake payloads, prepare approval requests, and update local workspace files.

Agents must not call external write APIs, activate workflows, retry production executions, send messages, change credentials, or mutate customer systems.

## Kill Switch

If any of these occur, stop and move the card to `Blocked`:

- Requested action would write to CRM, email, external messaging, workflow runtime, production API, or credentials.
- Tool permission is unknown.
- Real customer records, secrets, endpoint hosts, tenant IDs, auth headers, raw logs, or raw transcripts are required.
- Approval scope is ambiguous.
- Verifier fails the same card `Max attempts` times.
- Idempotency or rollback is unknown for a proposed external write.

## Attempt Caps

| Work Type | Max Attempts | Stop Condition |
| --- | --- | --- |
| Investigation | `3` | Evidence still missing or owner input needed. |
| Design | `3` | Architecture risk or unknown prevents safe build handoff. |
| Build draft | `3` | Acceptance checks still fail. |
| Validation | `3` | Expected and actual results cannot be reconciled. |

## Human Gates

Human approval is required before:

- n8n activation, deactivation, workflow edit, or production retry;
- HubSpot create/update/delete, association, note, task, or bulk import;
- Gong raw transcript storage or sensitive call-data export;
- AirOps publishing or customer-facing run;
- external email, Slack, Teams, Hermes, or customer message;
- credential, scope, token, API key, or environment change;
- destructive local, container, database, or filesystem action.

