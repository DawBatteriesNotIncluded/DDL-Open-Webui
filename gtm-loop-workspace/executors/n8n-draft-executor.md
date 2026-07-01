# n8n Draft Executor

Purpose: define how the Cody/build lane may use n8n MCP later without turning the workbench into a production automation runner.

## Scope

The n8n draft executor produces local draft artifacts only. It may describe a workflow, prepare draft JSON, and validate with fake payloads. It must not create, update, activate, disable, schedule, or run live n8n workflows without explicit approval for the exact action.

## Required Inputs

Before drafting n8n work, link these artifacts from the active task:

- `artifacts/<task_id>/requirements/build-handoff.md`
- `artifacts/<task_id>/architecture/integration-flow.md`
- `artifacts/<task_id>/build/build-plan.md`
- `artifacts/<task_id>/build/tool-plan.md`
- fake/redacted payloads from `payloads/` or `artifacts/<task_id>/`

## Outputs

- n8n workflow draft spec.
- n8n workflow JSON draft if the shape is known and can stay local.
- fake payload validation notes.
- local approval request before activation, live webhook use, credential use, or production writes.

## Draft Workflow File

Use:

```text
gtm-loop-workspace/artifacts/_templates/build/n8n-workflow-draft.md
```

Task-specific drafts should live under:

```text
gtm-loop-workspace/artifacts/<task_id>/build/n8n-workflow-draft.md
```

The board action `Create n8n workflow draft` creates this Markdown file locally for Cody/build tasks. It does not call n8n MCP, does not create or update a workflow, and does not create an approval record.

## Blocked Actions

- Production workflow activation.
- Live workflow creation or update.
- Real credential use.
- Real CRM, Gong, AirOps, or custom API writes.
- Live webhook calls.
- Scheduled production triggers.
- External sends or customer-facing actions.

## Cody Lane Procedure

1. Confirm the task is in `current_lane: cody`.
2. Read the requirements, integration flow, build plan, and tool plan.
3. Select only fake/redacted payloads.
4. Draft the n8n workflow spec locally, or create the starter from `/gtm-loop/board`.
5. Mark every node as `draft`, `mock`, or `approval-gated`.
6. Record fake payload validation notes.
7. Prepare an approval request for any live n8n action.

The approval request should be stored as a local approval record under `tasks/_approvals/APP-####.json`. Approval does not execute the action. Future executor code must check for a matching approved approval before any n8n MCP create/update, activation, credential use, live webhook, retry, or scheduled loop call.

## Completion Criteria

- Draft has trigger, nodes, transformations, fake input, fake output, validation plan, and rollback/disable plan.
- Draft explicitly says external writes are blocked until approval.
- No secrets or real client payloads are stored.
- Task `artifact_links` points to the draft artifact when created.
