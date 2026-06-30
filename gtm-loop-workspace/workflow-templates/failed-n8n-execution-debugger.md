# Failed n8n Execution Debugger

## Purpose

Classify failed executions and produce a fix plan.

## n8n Outline

1. Error trigger or manual log input.
2. Capture execution details.
3. Redact sensitive values.
4. Classify error.
5. Propose fix and corrected test payload.
6. Create debug record.
7. Human approval before retry.

## Required Approval

Approval before retrying production execution or editing active workflow.

## Test Payload

`test-payloads/failed-n8n-execution.json`

