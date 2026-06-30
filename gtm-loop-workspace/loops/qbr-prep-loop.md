# QBR Prep Loop

Reduce manual account prep for QBRs and account reviews.

## Loop Name

QBR Prep Loop

## Business Goal

Reduce manual account prep time by generating grounded account review briefs from approved account context.

## Trigger

Upcoming QBR/account review, calendar event, manual request, or scheduled account-review queue.

## Inputs

- Account name/domain.
- HubSpot account, deal, task, and note context where approved.
- Gong call summaries where approved.
- Usage or support context if available and approved.

## Context Sources

- Open WebUI Knowledge: GTM playbook and QBR template.
- HubSpot and Gong reads where approved.
- Internal docs only if permitted.

## Tools Required

- Open WebUI for summarization and review.
- n8n for scheduled prep queue.
- HubSpot/Gong reads where approved.

## Step-By-Step Loop Design

1. Trigger from upcoming review or manual account request.
2. Retrieve approved account context.
3. Summarize activity, open opportunities, risks, stakeholders, next steps, and unresolved questions.
4. Identify missing context.
5. Generate prep brief.
6. Run QA for grounding and sensitivity.
7. Require review before sharing broadly.
8. Log brief version and reviewer.

## n8n Implementation Outline

Schedule/calendar/manual trigger -> Account lookup -> Fetch context -> AI prep brief -> QA check -> Reviewer queue -> Optional approved share/log.

## Prompt Blocks

QBR brief: "Create a concise QBR prep brief grounded only in provided account context. Flag missing context and assumptions."

## Data Mappings

| Source | Target | Notes |
|---|---|---|
| Account ID | Brief header | Traceability |
| Open deals | Opportunity section | Include stage/date |
| Recent calls | Activity summary | Sensitive by default |
| Tasks/notes | Next steps | Do not invent |

## State/Logging Requirements

Log account ID, source timestamps, brief version, missing data, reviewer, approval, and share destination if any.

## Evaluation Checks

- Are summaries grounded?
- Are stale sources flagged?
- Is sensitive content minimized?
- Are assumptions explicit?
- Is sharing approved?

## Human Approval Gates

Approval required before broad internal distribution, customer-facing use, or CRM writes.

## Stop Condition

Stop when brief is reviewed, rejected, stale, missing required access, or review date passes.

## Error Handling

If account match is ambiguous, ask for confirmation. If context is stale, label it and avoid strong recommendations.

## Test Payload

Use `test-payloads/hubspot-deal-updated.json` plus manual account notes.

## Success Metrics

Prep time saved, reviewer acceptance, missing-context rate, and actionability score.

## Build Now Vs Later Recommendation

Build now as manual request plus approved reads. Defer calendar automation until access and templates are stable.

