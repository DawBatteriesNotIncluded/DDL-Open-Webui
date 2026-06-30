# ClinicalTrials Update To Account Alert

## Purpose

Convert public trial updates into reviewed account intelligence.

## n8n Outline

1. Scheduled public data check.
2. Detect changed trials.
3. Normalize sponsor.
4. Match HubSpot account.
5. Score relevance.
6. Generate alert draft.
7. Human approval before CRM note/task.
8. Log update.

## Required Approval

Approval before CRM writes or seller alert.

## Test Payload

`test-payloads/clinicaltrials-update.json`

