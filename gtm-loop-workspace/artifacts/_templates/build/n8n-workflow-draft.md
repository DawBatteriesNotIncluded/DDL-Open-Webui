# {{task_id}} n8n Workflow Draft

{{task_context}}

## Scope

| Field | Value |
| --- | --- |
| Task title | {{task_title}} |
| Client | `{{client}}` |
| Manager request | {{manager_request}} |
| Interpreted objective | {{interpreted_objective}} |
| Current lane | `{{current_lane}}` |
| Current gate | `{{current_gate}}` |
| Proposed workflow name | `{{proposed_workflow_name}}` |

## Trigger

{{trigger}}

## Node Outline

{{node_outline}}

## Fake Input Payload Links

{{fake_input_payload_links}}

## Fake Output Payload Links

{{fake_output_payload_links}}

## Data Mapping

{{data_mapping}}

## Error Handling

{{error_handling}}

## Validation Plan

{{validation_plan}}

## Rollback / Disable Plan

{{rollback_disable_plan}}

## Approval Boundary

{{approval_boundary}}

## Explicit Blocked Actions

{{explicit_blocked_actions}}

## Open Questions

- Which fake payload best represents the first happy-path test?
- Which fields are required before a future n8n draft can be reviewed?
- What approval record would be needed before any n8n MCP call?

## Next Action

{{next_action}}
