# Approval Gates

Actions requiring explicit human approval before execution.

## Hard Approval Gates

| Action | Approval Required | Minimum Approval Text |
| --- | --- | --- |
| Activate or enable production n8n workflow | Always | Workflow name, environment, trigger, expected effect. |
| Create or update live n8n workflow | Always | Workflow name, environment, draft source, trigger, expected effect. |
| Expose or call live n8n webhook | Always | Webhook name/path, environment, caller, expected payload class. |
| Use real n8n credentials | Always | Credential name, scope, owner, workflow affected. |
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
| Draft local n8n workflow Markdown/JSON | Fake/redacted payloads only; no n8n MCP call, live workflow mutation, or activation. |
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

## Local Approval Queue

Approval records live under:

```text
gtm-loop-workspace/tasks/_approvals/APP-####.json
```

The queue is local and records manager intent only. Creating or approving a record does not execute the action. Future executor code must check for a matching approved approval record before any n8n MCP call, CRM write, external send, credential change, destructive command, production data use, or scheduled loop activation.

New approval records always start as `requested`. Approval decisions may move `requested` to `approved`, `rejected`, `deferred`, or `cancelled`, and may move `deferred` to `approved`, `rejected`, or `cancelled`. `approved`, `rejected`, and `cancelled` are terminal states; create a new approval record to revisit a terminal decision.

Task frontmatter keeps only a summary:

- `approval_required: true` when any approval is `requested` or `deferred`.
- `approval_status: requested` when any requested approval exists.
- `approval_status: deferred` when no requested approval exists but at least one deferred approval exists.
- `approval_status: rejected` when the latest relevant decision is rejected and no requested/deferred approval exists.
- `approval_status: approved` when all active approvals are approved.
- `approval_status: not_required` when no approval is active.

Approval events are audited in `gtm-loop-workspace/tasks/_audit/approval-events.jsonl`. Do not log secrets, auth headers, tokens, cookies, raw customer data, production payloads, or task bodies.

## Do Not Automate Yet

These stay manual and approval-gated for v1:

- API writes or production data mutation.
- Workflow activation, deactivation, or production retry.
- Email sends or external messages.
- Credential, token, scope, or API key changes.
- Bulk imports, deletes, merges, or destructive operations.
- Uploading raw customer exports, Gong transcripts, logs, secrets, endpoint hosts, tenant IDs, or auth headers to Knowledge.

Agents may draft plans, payloads, approval requests, and validation notes for these actions, but must not execute them without explicit approval for the exact action.

Creating `gtm-loop-workspace/artifacts/<task_id>/build/n8n-workflow-draft.md` from the board is allowed without approval because it is local Markdown only and uses fake/redacted payload links. Any future n8n MCP create/update/activation still requires a matching approved approval record before execution.
