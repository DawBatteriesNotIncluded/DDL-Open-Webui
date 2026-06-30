# Proposal Generation Loop

Compress proposal prep from hours to minutes while keeping human control.

## Loop Name

Proposal Generation Loop

## Business Goal

Generate grounded proposal skeletons from approved deal context so proposal prep is faster and assumptions are visible.

## Trigger

Manual request, deal stage change, proposal-request note, or approved seller prompt.

## Inputs

- Deal context.
- Gong calls and HubSpot notes where approved.
- Product/service capability notes.
- Proposal template.

## Context Sources

- Open WebUI Knowledge: GTM playbook, proposal prompt, grounding checklist.
- HubSpot/Gong reads where approved.
- AirOps content workflows if production chain is needed.

## Tools Required

- Open WebUI for reasoning and review.
- AirOps for content chain where approved.
- n8n for routing and handoff.
- HubSpot/Gong reads only with approval.

## Step-By-Step Loop Design

1. Receive proposal request.
2. Retrieve approved deal context.
3. Extract requirements, buyer goals, constraints, stakeholders, timeline, and risks.
4. Generate proposal skeleton.
5. Flag assumptions, missing inputs, and unsupported claims.
6. Run QA and privacy check.
7. Require human approval before external sharing.
8. Log final approved version.

## n8n Implementation Outline

Manual/deal trigger -> Fetch context -> AI requirements extraction -> Proposal skeleton generation -> QA -> Human approval -> Optional AirOps production handoff -> Log.

## Prompt Blocks

Proposal skeleton: "Generate a proposal skeleton grounded in provided context. Do not invent capabilities, pricing, timelines, or commitments. Flag assumptions."

## Data Mappings

| Source | Target | Notes |
|---|---|---|
| Deal notes | Requirements | Evidence required |
| Gong transcript | Buyer language | Sensitive by default |
| Product notes | Proposed approach | No unsupported claims |
| Assumptions | Review checklist | Must be explicit |

## State/Logging Requirements

Log deal ID, source timestamps, proposal version, assumptions, reviewer, approval status, and external-share status.

## Evaluation Checks

- Are claims grounded?
- Are assumptions explicit?
- Are sensitive details removed?
- Are legal/pricing claims avoided unless provided?
- Is approval captured?

## Human Approval Gates

Approval required before customer sharing, pricing/legal claims, CRM writes, or external content generation.

## Stop Condition

Stop when approved draft is produced, missing context blocks generation, or reviewer rejects assumptions.

## Error Handling

Route insufficient context to question list. Stop if source data contains restricted content.

## Test Payload

Use `test-payloads/gong-call-transcript.json` and fake deal notes.

## Success Metrics

Draft time saved, assumption reduction, reviewer edit distance, and proposal acceptance quality.

## Build Now Vs Later Recommendation

Build now as an Open WebUI-assisted workflow. Automate retrieval later after approval/data boundaries are clear.

