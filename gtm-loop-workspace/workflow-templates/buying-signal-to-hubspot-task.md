# Buying Signal To HubSpot Task

## Purpose

Convert a validated buying signal into a seller-reviewed HubSpot task.

## n8n Outline

1. Webhook or schedule trigger.
2. Validate signal payload.
3. Normalize company domain.
4. Search HubSpot company.
5. Score signal using AI.
6. If score is below threshold, log and stop.
7. Generate seller task draft.
8. Human approval.
9. Create HubSpot task after approval.
10. Log outcome.

## Required Approval

Approval before HubSpot task creation.

## Test Payload

`test-payloads/evergrowth-signal.json`

