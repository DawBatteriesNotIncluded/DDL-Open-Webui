# n8n Notes

## Role

n8n is the runtime for triggers, scheduled workflows, integrations, retries, branching, and logging.

## V1 Workflow Pattern

Trigger -> Validate -> Normalize -> Enrich -> AI/decision -> Approval -> Write/action -> Log -> Error path.

## Rules

- Keep credentials in n8n credential store or environment variables.
- Use fake payloads for dry runs.
- Disable workflows until approved.
- Add idempotency keys before writes.
- Include error branches for API failures and mapping failures.
- Prefer manual approval before CRM writes in v1.

## Debugging

Capture execution ID, workflow ID, node name, input JSON, output JSON, error message, status code, and retry count.

