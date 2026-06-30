# Workflow Test Runbook

## Test Types

- Happy path: valid payload and expected decision.
- Missing required field: workflow stops with clear error.
- Malformed field: validation catches issue.
- Duplicate payload: idempotency prevents duplicate write.
- Low confidence: no CRM write; logs decision.
- Auth failure: stops and alerts; no secret exposure.
- Rate limit: backoff or queue behavior works.
- Approval denied: workflow stops without side effects.

## Minimum Pass Criteria

- Fake payload executes without production writes.
- Required fields are validated.
- Approval gate blocks side effects.
- Errors are classified and logged.
- Outputs are grounded in inputs.
- Retry is safe or disabled.

## Test Record

Document execution ID, payload used, expected result, actual result, pass/fail, fix required, and reviewer.

