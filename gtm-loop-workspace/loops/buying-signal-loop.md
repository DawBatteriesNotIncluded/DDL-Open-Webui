# Buying Signal Loop

Convert external buying signals into seller-ready actions while avoiding noisy CRM writes.

## Loop Name

Buying Signal Loop

## Business Goal

Convert credible external buying signals into timely seller-ready actions that improve account prioritisation and reduce manual research.

## Trigger

New external signal from Evergrowth, webhook, manual paste, job posting monitor, funding/news monitor, or other approved signal source.

## Inputs

- Signal payload with company, source, type, timestamp, summary, confidence, URL if available.
- Optional HubSpot account/deal/contact records.
- GTM ICP and scoring rules.

## Context Sources

- Open WebUI Knowledge: GTM playbook, signal scoring prompt, HubSpot notes.
- HubSpot account/deal/contact context where approved.
- Evergrowth or external signal source metadata.

## Tools Required

- Open WebUI for review and seller brief generation.
- n8n for webhook/schedule, enrichment, branching, logging.
- HubSpot API or node for approved reads and optional approved task creation.
- Signal Intelligence Agent and Eval and QA Agent.

## Step-By-Step Loop Design

1. Receive signal.
2. Validate source, timestamp, company identity, and signal type.
3. Match company to HubSpot account using domain first, then name fallback.
4. Retrieve account owner, lifecycle stage, open deals, and recent activity if approved.
5. Score ICP fit, signal relevance, urgency, and confidence.
6. Decide action: ignore, monitor, create seller brief, request human review, or draft HubSpot task.
7. Generate seller brief with evidence and recommended next action.
8. Require approval before creating HubSpot task or note.
9. Log signal, score, decision, and outcome.
10. Wait for seller action or close the loop as low priority.

## n8n Implementation Outline

Webhook or schedule trigger -> Validate payload -> Normalize company -> HubSpot search/read -> AI score signal -> IF confidence threshold -> Create approval item/draft brief -> Approved path creates HubSpot task -> Log outcome -> Error workflow.

## Prompt Blocks

Signal scorer: "Score this signal for ICP fit, urgency, confidence, evidence strength, and recommended action. Use only provided signal and retrieved account context. Flag uncertainty."

Seller brief: "Create a concise seller brief with signal, evidence, why it matters, suggested action, and approval status."

## Data Mappings

| Source | Target | Notes |
|---|---|---|
| `signal.company.domain` | HubSpot company domain | Primary match key |
| `signal.summary` | Task/body draft | Evidence only |
| `score.recommended_action` | Approval queue item | Do not auto-write in v1 |
| `signal.signalId` | Log idempotency key | Prevent duplicates |

## State/Logging Requirements

Log signal ID, source, account match, score, decision, generated brief, approval status, HubSpot object IDs, and seller action status.

## Evaluation Checks

- Is company match reliable?
- Is signal fresh and sourced?
- Is score grounded in evidence?
- Is HubSpot write gated by approval?
- Does output include uncertainty?

## Human Approval Gates

Approval required before CRM task/note creation, outreach, seller assignment changes, or escalation to leadership.

## Stop Condition

Stop when the signal is logged as actioned, rejected, duplicate, stale, low confidence, or awaiting seller action beyond the configured SLA.

## Error Handling

Route missing domain to manual match. Retry rate limits with backoff. Stop on auth failure. Send mapping errors to Workflow Debugger Agent.

## Test Payload

Use `test-payloads/evergrowth-signal.json`.

## Success Metrics

Signal-to-brief time, seller action rate, duplicate rate, accepted task rate, and false-positive rate.

## Build Now Vs Later Recommendation

Build now as a manual-approval v1. Defer automatic CRM writes until signal quality and seller acceptance are proven.

