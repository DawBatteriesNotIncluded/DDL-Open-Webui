# n8n Workflow Design Prompt

```text
Design a lean n8n workflow from the active GTM Loop client context.

Read:
- clients/<client-slug>/context.md
- clients/<client-slug>/systems.md
- clients/<client-slug>/n8n.md
- clients/<client-slug>/workflow-inventory.md
- clients/<client-slug>/field-mapping.md
- clients/<client-slug>/endpoint-matrix.md

Return:
1. Workflow objective.
2. Trigger.
3. Node-by-node outline.
4. Inputs and outputs.
5. Credential names needed, values omitted.
6. Error handling and retry behavior.
7. Human approval gates.
8. Fake/redacted test payload.
9. Validation checks.

Do not activate production workflows or write to CRM without explicit human approval.
```
