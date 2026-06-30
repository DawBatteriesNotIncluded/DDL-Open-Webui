# Approval Gates

Actions requiring explicit human approval before execution.

## Hard Approval Gates

| Action | Approval Required | Minimum Approval Text |
| --- | --- | --- |
| Activate or enable production n8n workflow | Always | Workflow name, environment, trigger, expected effect. |
| Retry production workflow execution | Always | Execution ID/name, idempotency check, expected writes. |
| Create/update/delete HubSpot record | Always | Object, fields, record scope, rollback/repair plan. |
| Send email or external message | Always | Audience, content, sender, timing. |
| Publish AirOps/customer-facing content | Always | Destination, audience, content summary. |
| Change credentials, scopes, or API keys | Always | Credential name, scope change, owner. |
| Mutate custom API production data | Always | Endpoint/action, payload class, records affected. |
| Run destructive local command | Always | Target path/resource and why required. |

## Allowed Without Extra Approval

| Action | Conditions |
| --- | --- |
| Edit Markdown in this workspace | No secrets or raw customer data. |
| Draft workflow specs or prompts | No external writes. |
| Create fake/redacted payloads | No real customer data. |
| Inspect local docs/source | Read-only and within allowed workspace. |
| Update board/run ledger | No sensitive values. |

## Approval Request Template

```markdown
# Approval Request: <action>

## Exact Action

## System / Environment

## Data Affected

## Why Needed

## Validation Already Done

## Risks

## Rollback / Disable Plan

## Approval Needed
Reply with explicit approval for this exact action.
```

## Rule

If the approval scope is ambiguous, do not act. Prepare the approval request instead.

## Do Not Automate Yet

These stay manual and approval-gated for v1:

- API writes or production data mutation.
- Workflow activation, deactivation, or production retry.
- Email sends or external messages.
- Credential, token, scope, or API key changes.
- Bulk imports, deletes, merges, or destructive operations.
- Uploading raw customer exports, Gong transcripts, logs, secrets, endpoint hosts, tenant IDs, or auth headers to Knowledge.

Agents may draft plans, payloads, approval requests, and validation notes for these actions, but must not execute them without explicit approval for the exact action.
