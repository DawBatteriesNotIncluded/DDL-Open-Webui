# Loop Spec Template

Use this template to turn a messy GTM/FDE task into a buildable loop.

## Loop Name

`<name>`

## Business Goal

`<specific business outcome>`

## Trigger

`<manual prompt, webhook, schedule, CRM event, transcript event, external signal>`

## Inputs

`<payloads, records, transcripts, docs, user prompt>`

## Context Sources

`<Open WebUI Knowledge, HubSpot, Gong, Evergrowth, AirOps, API docs>`

## Tools Required

`<Open WebUI, n8n, Codex, MCP/OpenAPI tools, vendor APIs>`

## Step-By-Step Loop Design

1. Receive trigger.
2. Validate payload.
3. Retrieve context.
4. Run planner/extractor/scorer.
5. Execute controlled tool step or prepare human review.
6. Evaluate output.
7. Log state and outcome.
8. Decide next action.
9. Stop, retry, or escalate.

## n8n Implementation Outline

`<trigger node, fetch/enrich nodes, AI node, IF node, write/draft node, log node, error branch>`

## Prompt Blocks

`<planner/extractor/scorer/evaluator prompts>`

## Data Mappings

| Source | Target | Notes |
|---|---|---|
| `<source>` | `<target>` | `<transform>` |

## State/Logging Requirements

`<idempotency key, execution ID, input hash, decision, output, approver, retry count>`

## Evaluation Checks

`<grounding, schema, privacy, business value, readiness>`

## Human Approval Gates

`<CRM writes, email sends, workflow activation, external content, sensitive data>`

## Stop Condition

`<success, duplicate, low confidence, missing data, approval denied, max retries>`

## Error Handling

`<validation errors, auth errors, rate limits, mapping failures, retry policy>`

## Test Payload

`<fake/anonymised payload or link to test-payloads>`

## Success Metrics

`<time saved, task completion, seller action, error rate, quality score>`

## Build Now Vs Later Recommendation

`<build now, prototype, defer, or manual-only>`

