# ClinicalTrials Signal Loop

Convert ClinicalTrials.gov or programme updates into account intelligence.

## Loop Name

ClinicalTrials Signal Loop

## Business Goal

Identify relevant clinical trial updates and convert them into useful account intelligence for sellers without exposing sensitive sponsor or patient data.

## Trigger

New ClinicalTrials.gov update, scheduled search, RSS/API change, or manual payload.

## Inputs

- Trial update metadata.
- Sponsor/company name.
- Study phase, status, condition, location/enrollment changes.
- HubSpot account context where approved.

## Context Sources

- Public ClinicalTrials.gov data.
- Open WebUI Knowledge: GTM playbook and clinical signal notes.
- HubSpot account/deal context where approved.

## Tools Required

- n8n schedule/API polling.
- Open WebUI analysis.
- HubSpot read/write tools only with approval.
- Signal Intelligence Agent.

## Step-By-Step Loop Design

1. Detect trial update.
2. Validate source is public and payload contains no patient-identifiable data.
3. Normalize sponsor/company.
4. Match to HubSpot account.
5. Score relevance based on phase, status change, geography, timeline, and ICP fit.
6. Generate seller alert if useful.
7. Require approval before CRM enrichment or seller task.
8. Log decision and account match.

## n8n Implementation Outline

Schedule/API trigger -> Fetch updates -> Normalize sponsor -> HubSpot account match -> AI relevance score -> IF useful -> Approval queue -> HubSpot task/note after approval -> Log.

## Prompt Blocks

Clinical signal scorer: "Assess whether this public trial update is commercially relevant. Do not infer private sponsor strategy. Use only public update and approved account context."

## Data Mappings

| Source | Target | Notes |
|---|---|---|
| `nctId` | Alert reference | Public identifier |
| `sponsor` | HubSpot company match | Verify match confidence |
| `status` | Relevance score | Recruiting/status change signal |
| `phase` | Brief context | Avoid medical claims |

## State/Logging Requirements

Log NCT ID, update timestamp, sponsor match, score, decision, approval, and HubSpot write IDs.

## Evaluation Checks

- Is data public?
- Is there no patient-identifiable data?
- Is sponsor match reliable?
- Is relevance grounded?
- Is CRM write gated?

## Human Approval Gates

Approval required before HubSpot enrichment, seller alert, task creation, or commercial interpretation.

## Stop Condition

Stop on duplicate update, low relevance, no reliable account match, approval denied, or alert logged.

## Error Handling

Route ambiguous sponsor matches to manual review. Stop on sensitive data concerns. Retry public API rate limits with backoff.

## Test Payload

Use `test-payloads/clinicaltrials-update.json`.

## Success Metrics

Useful alert rate, account match accuracy, false-positive rate, and seller follow-up rate.

## Build Now Vs Later Recommendation

Prototype now with manual review. Defer automated CRM writes until matching and relevance scoring are proven.

