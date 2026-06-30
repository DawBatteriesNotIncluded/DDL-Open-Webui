# How To Attach n8n MCP Tools

## Agents That Should Usually Have n8n MCP Enabled

- Build Controller Agent.
- GTM Flow Builder Agent.
- Workflow Debugger Agent.
- n8n Builder Agent.

## Agents That Usually Do Not Need n8n MCP

- Eval and QA Agent, unless inspection-only review is needed.
- Content Repurposing Agent.
- Proposal Brief Agent.
- Signal Intelligence Agent, unless workflow inspection is needed.

## Safe Tool Policy

- Prefer read/inspect operations first.
- Do not activate workflows without explicit approval.
- Do not retry production executions without explicit approval.
- Do not write CRM records through n8n unless approved.
- Do not expose credentials in chat.

## Test

Start with a read-only question:

```text
List the available n8n workflow metadata you can inspect. Do not modify anything.
```

