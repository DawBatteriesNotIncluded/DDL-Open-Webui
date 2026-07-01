# GTM-001 n8n Workflow Draft

| Field | Value |
| --- | --- |
| Task | `GTM-001` |
| Title | Onboard first real client |
| Client | `TBD` |
| Board status | `in-progress` |
| Lane | `cody` |
| Phase | `build` |
| Gate | `build-complete` |
| Generated | `2026-07-01T23:14:59Z` |

## Scope

| Field | Value |
| --- | --- |
| Task title | Onboard first real client |
| Client | `TBD` |
| Manager request | Select the first real client and initial automation objective. |
| Interpreted objective | Capture the first client slug, create the client folder, and record the active objective without sensitive values. |
| Current lane | `cody` |
| Current gate | `build-complete` |
| Proposed workflow name | `gtm-001-tbd-draft` |

## Trigger

Draft-only trigger. Use a fake/redacted webhook input payload; do not expose or call a live webhook.

## Node Outline

| Step | Draft node | Purpose | External write? |
| --- | --- | --- | --- |
| 1 | Webhook / Manual Test Trigger | Accept fake payload only. | No |
| 2 | Set / Code | Normalize fields and remove sensitive values. | No |
| 3 | IF | Route missing required fields to a local error branch. | No |
| 4 | Respond / No-op | Return fake validation output. | No |

## Fake Input Payload Links

- `gtm-loop-workspace/payloads/n8n/fake-airops-request.json`
- `gtm-loop-workspace/payloads/n8n/fake-gong-webhook.json`
- `gtm-loop-workspace/payloads/n8n/fake-hubspot-update-prep.json`
- `gtm-loop-workspace/payloads/n8n/webhook-input.fake.json`

## Fake Output Payload Links

- `gtm-loop-workspace/payloads/n8n/fake-airops-response.json`
- `gtm-loop-workspace/payloads/n8n/fake-n8n-workflow-test-result.json`

## Data Mapping

- Source fields: list only fake/redacted input fields.
- Normalized fields: map names, types, and required/optional status.
- Output fields: describe fake result shape only.
- Field owners: reference requirements or architecture artifacts when known.

## Error Handling

- Validate required fields before any draft output.
- Route invalid fake payloads to a local error response.
- Do not retry production webhooks or external writes.
- Record unresolved mapping questions in the task artifacts.

## Validation Plan

1. Test only with fake/redacted payloads from `gtm-loop-workspace/payloads/n8n/`.
2. Confirm the draft has no credentials, production URLs, or customer records.
3. Confirm every external-write node is absent or disabled in the draft.
4. Capture fake output in validation notes before requesting approval.

## Rollback / Disable Plan

- Markdown draft only: no runtime rollback is required.
- Before any future n8n activation, document how to disable the workflow, remove triggers, and stop schedules.

## Approval Boundary

No external API writes, workflow activation, credential changes, email sends, or production data mutation are allowed from this artifact. Use fake/redacted examples only until a human approves the exact external action.

## Explicit Blocked Actions

- Calling n8n MCP.
- Creating, updating, or activating a real n8n workflow.
- Calling production webhooks.
- Using real credentials, tokens, headers, tenant IDs, or customer data.
- Writing to HubSpot, Gong, AirOps, custom APIs, email, or external systems.

## Open Questions

- Which fake payload best represents the first happy-path test?
- Which fields are required before a future n8n draft can be reviewed?
- What approval record would be needed before any n8n MCP call?

## Next Action

Run Brody investigation / requirements lane.
