# Workflow Debugging Loop

Debug failed automations faster with structured error classification and test payloads.

## Loop Name

Workflow Debugging Loop

## Business Goal

Reduce time spent diagnosing failed n8n workflows by classifying errors, identifying root cause, proposing fixes, and creating reproducible tests.

## Trigger

Failed execution log pasted into Open WebUI, received via n8n error workflow, or manually exported from n8n.

## Inputs

- Failed n8n execution log.
- Node name/type, error message, input/output JSON.
- Workflow spec and expected schema.

## Context Sources

- Open WebUI Knowledge: debugging notes, n8n notes, API integration notes.
- n8n execution details where approved.
- Vendor API docs and error responses.

## Tools Required

- Workflow Debugger Agent.
- Open WebUI for analysis.
- n8n MCP/API for approved inspection.
- Codex for updating test payloads/docs.

## Step-By-Step Loop Design

1. Receive failure log.
2. Validate whether JSON/log content is complete.
3. Classify error as prompt, data, API, auth, schema, mapping, rate limit, environment, or workflow logic.
4. Identify failing node and immediate cause.
5. Compare actual payload to expected schema.
6. Propose minimal fix.
7. Create corrected fake test payload or mapping.
8. Recommend retry only if idempotency is safe.
9. Document root cause and prevention.

## n8n Implementation Outline

Error trigger -> Capture workflow/execution/node/error/input -> Send to Open WebUI/debug review -> Create issue/log item -> Manual fix path -> Test with fake payload -> Approved retry.

## Prompt Blocks

Debugger: "Classify this failure, cite evidence from the log, identify root cause, propose the smallest safe fix, and state whether retry is safe."

## Data Mappings

| Source | Target | Notes |
|---|---|---|
| `executionId` | Debug log ID | Trace failure |
| `node.name` | Root-cause report | Identify failing node |
| `error.httpStatus` | Error class | API/auth/rate limit clues |
| `input` | Test payload | Anonymise before saving |

## State/Logging Requirements

Log execution ID, workflow ID, failing node, error class, root cause, fix, test payload, retry decision, and prevention action.

## Evaluation Checks

- Is root cause evidence-backed?
- Is retry safe and idempotent?
- Is sensitive data removed?
- Is corrected payload valid JSON?
- Is prevention actionable?

## Human Approval Gates

Approval required before retrying production executions, changing credentials, editing active workflows, or modifying external systems.

## Stop Condition

Stop when root cause is documented, fix is tested, issue is escalated, or retry is approved and completed.

## Error Handling

If log is incomplete, request specific missing fields. If auth failure, do not expose secrets. If rate limited, recommend backoff and queueing.

## Test Payload

Use `test-payloads/failed-n8n-execution.json`.

## Success Metrics

Mean time to root cause, repeat failure rate, corrected payload pass rate, and safe retry rate.

## Build Now Vs Later Recommendation

Build now as a manual debugging workflow. Add automated error ingestion later after redaction is reliable.

