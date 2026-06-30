# Competitor Intelligence Loop

Surface competitor and market intelligence from calls and signals.

## Loop Name

Competitor Intelligence Loop

## Business Goal

Aggregate competitor mentions and market signals into evidence-backed leadership briefs and account-level insights.

## Trigger

Gong transcript, external signal, manual note, or scheduled intelligence review.

## Inputs

- Transcript excerpts or signal payloads.
- Competitor taxonomy.
- Account/deal metadata where approved.

## Context Sources

- Open WebUI Knowledge: GTM playbook, Gong notes, signal notes.
- Gong transcripts where approved.
- HubSpot account/deal context where approved.

## Tools Required

- Open WebUI for classification and brief generation.
- n8n for ingestion and aggregation.
- Optional Gong/HubSpot/Evergrowth reads.

## Step-By-Step Loop Design

1. Receive transcript or signal.
2. Detect competitor mention.
3. Classify theme: pricing, product gap, implementation, trust, incumbent, displacement, or market trend.
4. Extract evidence and account context.
5. Aggregate by competitor/theme/time period.
6. Produce leadership brief with evidence and caveats.
7. Gate any external or CRM action for approval.
8. Log evidence source and sensitivity.

## n8n Implementation Outline

Input trigger -> Competitor detection -> Theme classifier -> Store evidence/log -> Scheduled aggregation -> Brief generation -> Human review -> Optional approved distribution.

## Prompt Blocks

Classifier: "Detect competitor mentions and classify theme. Separate direct quote evidence from interpretation. Do not overstate a trend from one example."

## Data Mappings

| Source | Target | Notes |
|---|---|---|
| `transcript.text` | Evidence item | Minimize sensitive content |
| `competitor_name` | Intelligence theme | Normalize names |
| `account_id` | Aggregation key | Only if approved |
| `theme` | Brief section | Evidence required |

## State/Logging Requirements

Log source ID, competitor, theme, evidence pointer, sensitivity level, aggregation window, and reviewer approval.

## Evaluation Checks

- Is mention explicit?
- Is evidence sufficient?
- Are claims aggregated responsibly?
- Is sensitive transcript content minimized?
- Is distribution approved?

## Human Approval Gates

Approval required before leadership distribution, CRM writes, customer-facing claims, or use of sensitive call content.

## Stop Condition

Stop when logged as evidence, classified low confidence, aggregated into brief, or rejected by reviewer.

## Error Handling

Route ambiguous competitor names to manual review. Avoid storing full transcript when excerpt is sufficient.

## Test Payload

Use `test-payloads/gong-call-transcript.json` or `test-payloads/webhook-example.json`.

## Success Metrics

Useful intelligence items, leadership brief acceptance, evidence quality score, and false trend rate.

## Build Now Vs Later Recommendation

Build a manual-review intelligence log now. Add automated aggregation after taxonomy and evidence quality stabilize.

