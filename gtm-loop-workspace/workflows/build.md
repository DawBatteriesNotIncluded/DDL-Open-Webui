# Build Workflow

Use after `clients/<client-slug>/build-handoff.md` is ready.

## Preconditions

- Objective is clear.
- Required fields and endpoints are mapped.
- Unknowns that block build are resolved or explicitly accepted.
- Human approval gates are recorded.
- Fake/redacted test payload exists or can be created safely.

## Steps

1. Read the build handoff.
2. Make the smallest working change in the target surface.
3. Avoid new dependencies unless they remove real work or match the existing stack.
4. Keep credentials and customer data out of files.
5. Run the smallest useful validation.
6. Update `validation-notes.md`.

## Build Handoff Result

| Field | Notes |
| --- | --- |
| Files/workflows changed | `TBD` |
| Validation run | `TBD` |
| Remaining unknowns | `TBD` |
| Production activation needed | Yes / No / Unknown |
