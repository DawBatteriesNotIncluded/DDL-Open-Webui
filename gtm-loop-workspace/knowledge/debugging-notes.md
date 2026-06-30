# Debugging Notes

## Error Classes

- Prompt: model output wrong, ungrounded, malformed, or ambiguous.
- Data: missing, stale, duplicate, or malformed input.
- API: endpoint, status, schema, pagination, or rate limit issue.
- Auth: missing credentials, expired token, wrong scope.
- Mapping: source field does not match target field.
- Environment: missing env var or credential reference.
- Workflow logic: wrong branch, ordering, retry, or stop condition.

## Debugging Order

1. Identify failing node.
2. Capture exact input and output.
3. Classify error.
4. Compare actual schema with expected schema.
5. Propose smallest fix.
6. Create a test payload.
7. Decide whether retry is safe.
8. Document prevention.

