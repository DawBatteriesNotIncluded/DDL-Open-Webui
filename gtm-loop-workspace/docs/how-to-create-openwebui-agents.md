# How To Create Open WebUI Agents

## Steps

1. Open Open WebUI.
2. Go to Workspace -> Models.
3. Create a new custom model.
4. Name it after the agent, for example `Loop Architect Agent`.
5. Open the matching file in `gtm-loop-workspace/agents`.
6. Copy only the `System Prompt` section.
7. Paste it into the model system prompt.
8. Attach relevant Knowledge collections.
9. Enable tools only if the agent needs them.
10. Save and test with a fake prompt.

## Recommended First Agents

- Loop Architect Agent.
- Build Controller Agent.
- GTM Flow Builder Agent.
- Workflow Debugger Agent.
- Eval and QA Agent.

## Test Prompt

```text
Design a loop that turns a Gong call transcript into a HubSpot deal brief.
```

