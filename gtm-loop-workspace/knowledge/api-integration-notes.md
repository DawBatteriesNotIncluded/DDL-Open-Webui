# API Integration Notes

## Checklist

- Endpoint and method.
- Auth type and scopes.
- Request schema.
- Response schema.
- Pagination.
- Rate limits.
- Idempotency.
- Retry behavior.
- Error format.
- Field mapping.
- Logging.

## Rules

- Do not hardcode credentials.
- Use placeholders in examples.
- Validate payloads before API calls.
- Stop on auth errors.
- Back off on rate limits.
- Redact sensitive fields from logs.

