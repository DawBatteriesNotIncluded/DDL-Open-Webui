# n8n Workflow JSON Rules

Use these rules before importing generated workflow JSON.

## Rules

- Do not include credentials or secrets in JSON.
- Use placeholder credential names only.
- Include manual trigger or disabled activation for first import.
- Use explicit node names that match the loop step.
- Validate each expression against the test payload.
- Include an error path or documented error workflow.
- Include idempotency key for write operations.
- Keep CRM writes behind approval for v1.
- Avoid hardcoded production IDs unless approved.
- Do not activate imported workflows until tests and approval pass.

## Review Checklist

- Trigger node exists.
- Required fields are validated.
- Transform nodes produce expected schema.
- API nodes have scoped auth placeholders.
- IF nodes have clear thresholds.
- Error handling is present.
- Logging captures execution ID and decision.
- Approval gate exists before side effects.

