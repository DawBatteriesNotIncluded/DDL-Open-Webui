# Content Repurposing Loop

Turn approved source content into reusable GTM assets.

## Loop Name

Content Repurposing Loop

## Business Goal

Convert existing approved content into channel-specific GTM assets faster while preserving accuracy and review control.

## Trigger

New podcast, whitepaper, case study, webinar, sales note, or manual content request.

## Inputs

- Approved source content.
- Target channels and audience.
- Brand/tone guidance.
- Claims and restricted-content rules.

## Context Sources

- Open WebUI Knowledge: GTM playbook, prompt engineering notes, AirOps notes.
- Source content.
- Eval checklists.

## Tools Required

- Open WebUI for ideation and QA.
- AirOps for repeatable content chains where useful.
- n8n for routing and approvals.

## Step-By-Step Loop Design

1. Receive approved source material.
2. Extract themes, proof points, claims, audience angles, and constraints.
3. Generate channel-specific variants.
4. Run unsupported-claims and privacy QA.
5. Route to human approval.
6. Prepare final assets or AirOps handoff.
7. Log source, variants, reviewer, and approval.

## n8n Implementation Outline

Manual/content trigger -> Source validation -> Theme extraction -> Variant generation -> QA check -> Approval -> Optional AirOps/publishing handoff -> Log.

## Prompt Blocks

Repurposer: "Create channel-specific GTM assets from the approved source. Preserve claims, flag unsupported statements, and adapt angle for audience."

## Data Mappings

| Source | Target | Notes |
|---|---|---|
| Source title | Asset metadata | Trace source |
| Themes | Variant sections | Grounded only |
| Claims | QA checklist | Must be supported |
| Audience | Channel angle | Adapt tone |

## State/Logging Requirements

Log source ID, content hash, generated variants, unsupported claims, reviewer, approval, and publication status.

## Evaluation Checks

- Are claims supported?
- Is sensitive data removed?
- Does each variant fit the channel?
- Is approval required before publishing?
- Is source traceable?

## Human Approval Gates

Approval required before publishing, external distribution, customer-specific usage, or use of sensitive source material.

## Stop Condition

Stop when assets are approved, rejected, source is not approved, or unsupported claims cannot be resolved.

## Error Handling

If source is not approved, stop. If claims are unsupported, route to revision. If audience is unclear, create generic internal draft only.

## Test Payload

Use a fake whitepaper summary or anonymised podcast transcript excerpt.

## Success Metrics

Asset production time, approval rate, unsupported-claim count, and channel engagement after publishing.

## Build Now Vs Later Recommendation

Build now as a prompt-chain plus QA checklist. Use AirOps when content volume justifies a repeatable production chain.

