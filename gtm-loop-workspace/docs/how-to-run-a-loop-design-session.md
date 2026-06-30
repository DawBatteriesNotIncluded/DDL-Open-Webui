# How To Run A Loop Design Session

## Session Flow

1. Start with Loop Architect Agent.
2. Describe the messy manual task.
3. Ask for a buildable loop spec.
4. Send the loop spec to Eval and QA Agent.
5. If score is acceptable, send it to GTM Flow Builder Agent.
6. Ask for n8n implementation outline and test payloads.
7. Use Build Controller Agent to track status and next action.

## Starter Prompt

```text
Turn this repeated manual GTM task into an automation spec:

<describe task>
```

## Output To Save

- Loop spec.
- n8n design.
- Test payload.
- Build status.
- Approval request.

