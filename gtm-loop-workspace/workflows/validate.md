# Validate Workflow

Use before calling a workflow, prompt chain, or code handoff ready.

## Checks

| Check | Required | Notes |
| --- | --- | --- |
| Fake/redacted test payload | Yes | No raw customer data. |
| Expected output recorded | Yes | Include field-level expectations. |
| Error path tested | Usually | Required for external writes or APIs. |
| Approval gate confirmed | Yes | CRM writes, sends, activation, and commercial decisions. |
| Secrets omitted | Yes | Setting names only. |
| Rollback/disable path known | Yes | Especially n8n active workflows. |

## Record Results

Update `clients/<client-slug>/validation-notes.md`:

- test scenario;
- input used;
- result;
- evidence reference;
- follow-up.

## Ready Means

Ready means validated enough for the stated environment, not perfect. Mark production readiness separately from local/test readiness.
