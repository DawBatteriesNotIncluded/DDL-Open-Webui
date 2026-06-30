# Automation Patterns

Reusable GTM automation patterns for discovery and build handoff.

## Pattern Index

| Pattern | Trigger | Runtime | Typical Systems | Approval Gate |
| --- | --- | --- | --- | --- |
| Call signal to CRM task | Gong transcript or score | n8n / AirOps | Gong, HubSpot | Before CRM write |
| Deal brief generation | HubSpot deal stage change | AirOps / n8n | HubSpot, Gong | Before seller-facing output |
| Failed workflow triage | n8n execution failure | n8n + Open WebUI | n8n, Slack/Teams, logs | Before retrying production action |
| Lead/account enrichment | Scheduled or record change | n8n / custom API | HubSpot, vendor API | Before record overwrite |

## Pattern Template

| Field | Notes |
| --- | --- |
| Trigger | What starts the workflow. |
| Inputs | Systems, records, payloads, and files. |
| Transform | Extraction, scoring, matching, enrichment, routing. |
| Outputs | Records, tasks, content, notifications, files. |
| Failure Mode | Retry, dead letter, manual review, skip. |
| Human Approval | Required writes, messages, activation, or commercial decisions. |
| Validation | Minimal fake payload and expected result. |
