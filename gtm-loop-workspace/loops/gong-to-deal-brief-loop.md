# Gong To Deal Brief Loop

Turn Gong calls into structured deal intelligence and seller follow-up.

## Loop Name

Gong to Deal Brief Loop

## Business Goal

Turn Gong transcripts into structured deal intelligence that helps sellers act faster and keeps HubSpot deal context current.

## Trigger

New Gong transcript, manual transcript paste, or scheduled review of recent calls.

## Inputs

- Gong call metadata and transcript.
- HubSpot deal stage, owner, account, notes, and tasks where approved.
- Deal brief schema.

## Context Sources

- Open WebUI Knowledge: Gong notes, seller brief prompt, GTM playbook.
- Gong transcript and metadata.
- HubSpot deal context where approved.

## Tools Required

- Open WebUI for analysis and review.
- n8n for transcript event handling and routing.
- Gong API/read access where approved.
- HubSpot read/write tools only after approval.

## Step-By-Step Loop Design

1. Receive transcript.
2. Validate transcript completeness and speaker labels.
3. Extract stakeholders, pain, objections, competitor mentions, risks, next steps, timeline, and decision criteria.
4. Compare extraction with HubSpot deal stage and known next step.
5. Generate deal brief with evidence and uncertainty.
6. Decide whether to draft HubSpot note/task.
7. Require human approval before CRM write.
8. Log extraction, linked call, deal ID, approval, and seller action.
9. Track whether seller acted or follow-up is overdue.

## n8n Implementation Outline

Gong trigger/schedule -> Fetch transcript -> HubSpot deal lookup -> AI extraction -> AI deal brief -> IF missing required evidence -> Manual review -> Approval -> HubSpot note/task -> Log outcome.

## Prompt Blocks

Transcript extractor: "Extract only evidence-backed stakeholders, pains, objections, risks, competitor mentions, next steps, and dates. Separate direct evidence from inference."

Deal brief generator: "Create a seller-ready deal brief grounded in transcript evidence and HubSpot stage context."

## Data Mappings

| Source | Target | Notes |
|---|---|---|
| `callId` | HubSpot note external reference | Preserve traceability |
| `participants[]` | Stakeholder list | Mark role confidence |
| `extracted.next_steps` | Task draft | Approval required |
| `competitor_mentions[]` | Brief section | Evidence required |

## State/Logging Requirements

Log call ID, deal ID, transcript hash, extraction version, brief version, approval status, CRM write IDs, and seller action status.

## Evaluation Checks

- Are claims grounded in transcript?
- Are inferences labeled?
- Is sensitive content minimized?
- Is CRM write approval present?
- Does HubSpot stage comparison identify discrepancies?

## Human Approval Gates

Approval required before adding notes/tasks to HubSpot, sharing briefs externally, or using sensitive transcript content in proposals.

## Stop Condition

Stop when brief is approved/logged, rejected, duplicate, insufficient transcript quality, or seller action is tracked.

## Error Handling

Route missing transcript or deal match to manual review. Retry transient Gong/HubSpot failures. Stop on auth/scope errors.

## Test Payload

Use `test-payloads/gong-call-transcript.json`.

## Success Metrics

Brief completion time, seller task acceptance, stage discrepancy detection, grounded extraction score, and CRM note usefulness.

## Build Now Vs Later Recommendation

Build now with manual approval before CRM writes. Add automatic task creation later only for high-confidence low-risk cases.

