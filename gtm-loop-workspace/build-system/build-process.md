# Build Process

Use this process for every loop. Do not skip approval gates for v1.

## 1. Messy Manual Task

Capture the task in the user's words. Include frequency, owner, systems, current pain, and business impact.

## 2. Loop Spec

Use the Loop Architect Agent and `loops/loop-spec-template.md` to define trigger, inputs, context, steps, tools, state, evals, approval, and stop condition.

## 3. n8n Workflow Design

Use GTM Flow Builder or n8n Builder to create a node-by-node plan. Identify credentials, scopes, idempotency keys, retry policy, and error workflow.

## 4. Generated Workflow JSON Or Implementation Checklist

For v1, prefer an implementation checklist unless the workflow is simple and schema is clear. If JSON is generated, review it against `n8n-workflow-json-rules.md` before import.

## 5. Test Payload

Create fake/anonymised payloads for happy path, missing field, malformed field, duplicate, low-confidence, and rate-limit cases.

## 6. Validation

Validate JSON, required fields, field mappings, auth assumptions, privacy boundaries, and approval gates.

## 7. Debugging

Use Workflow Debugger Agent for any failed execution. Classify root cause before changing the workflow.

## 8. Approval

Prepare a human approval request that states exactly what the workflow will read, write, send, activate, or change.

## 9. Activation

Activate only after explicit approval, test pass, monitoring path, rollback plan, and credentials are confirmed.

## 10. Monitoring

Track executions, failures, skipped items, approval queue, seller action, output quality, and business outcome.

