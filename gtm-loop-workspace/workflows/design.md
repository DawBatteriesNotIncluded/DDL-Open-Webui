# Design Workflow

Use when the investigation is clear enough to sketch a workflow or integration.

## Steps

1. Confirm objective and non-goals.
2. Identify source of truth and write targets.
3. Map trigger, inputs, transforms, outputs, and approvals.
4. Update `workflow-inventory.md`, `field-mapping.md`, and `endpoint-matrix.md`.
5. Add `architecture/_template/integration-flow.md` when boundaries or sequence matter.
6. Add `risks-and-threat-model.md` when sensitive data, external writes, or auth boundaries matter.
7. Create an ADR only for durable decisions with real alternatives.

## Minimal Design Output

- Workflow objective.
- Trigger.
- Inputs and outputs.
- Field mapping.
- Error behavior.
- Human approval gates.
- Validation plan.
