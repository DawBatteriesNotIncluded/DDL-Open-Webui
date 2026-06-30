# Security And Secrets

## Rules

- Do not hardcode credentials.
- Do not put real secrets in `.env.example`, prompts, docs, workflow JSON, or Knowledge.
- Use placeholders only.
- Keep real secrets in approved secret stores or n8n credentials.
- Treat Gong transcripts, HubSpot data, sponsor information, and commercial strategy as sensitive.
- Do not include patient-identifiable data.
- Use fake/anonymised examples.

## Approval Required

Approval is required before:

- CRM writes.
- Email sends.
- External messages.
- Workflow activation.
- Production data changes.
- Sensitive data processing.
- Customer-facing or commercial decisions.

## Redaction

Before pasting logs into Open WebUI, remove tokens, cookies, private URLs, internal IDs where unnecessary, personal data, and confidential sponsor/customer details.

