# Architecture To Build Workflow

Use when a client workflow, integration, or system change needs architecture thinking before build.

## Steps

1. Start from the client objective and current system map.
2. Identify actors, systems, runtime units, data stores, APIs, queues, files, and owners.
3. Mark boundaries:
   - user/customer;
   - auth/identity;
   - internal/external service;
   - data store/secret;
   - vendor/client.
4. Draw the simplest Mermaid-friendly flow.
5. Capture confirmed facts, mismatches, and unknowns.
6. Review risks using `architecture/_template/risks-and-threat-model.md` when sensitive data or external writes are involved.
7. Create an ADR only if the decision is durable, hard to reverse, and has real alternatives.
8. Convert the design into `clients/<client-slug>/build-handoff.md`.
9. Add validation checks before build.

## Minimum Architecture Pack

| Artifact | Use |
| --- | --- |
| `systems.md` | System inventory and ownership. |
| `workflow-inventory.md` | Trigger, inputs, outputs, runtime, status. |
| `field-mapping.md` | Data crossing system boundaries. |
| `endpoint-matrix.md` | API and webhook surfaces. |
| `architecture/_template/integration-flow.md` | Flow when sequence matters. |
| `architecture/_template/risks-and-threat-model.md` | Sensitive data, auth, writes, or vendor boundaries. |
| `build-handoff.md` | Implementation-ready package. |

## Build Handoff Gate

Do not start build until these are known or explicitly accepted as unknown:

- source of truth;
- write target;
- trigger;
- required fields;
- auth model;
- approval gates;
- failure behavior;
- validation input and expected output.
