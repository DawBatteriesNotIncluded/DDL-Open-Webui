# AirOps Workflow Design Prompt

```text
Design or review an AirOps workflow using the active client context.

Read:
- clients/<client-slug>/context.md
- clients/<client-slug>/airops.md
- clients/<client-slug>/field-mapping.md
- clients/<client-slug>/workflow-inventory.md

Return:
1. Workflow purpose.
2. Inputs and required fields.
3. Prompt-chain steps.
4. Output shape.
5. Quality checks.
6. Approval gates.
7. Failure modes.
8. Test cases with fake/redacted inputs.

Keep customer data and commercial strategy out of examples.
```
