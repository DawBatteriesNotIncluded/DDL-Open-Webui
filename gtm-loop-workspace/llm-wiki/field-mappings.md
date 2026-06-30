# Field Mappings

Cross-client index of reusable field mapping patterns. Put detailed mappings in `clients/<client-slug>/field-mapping.md`.

## Common Mapping Table

| Source System | Source Field | Target System | Target Field | Transform | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| HubSpot | `TBD` | n8n | `TBD` | None / normalize / lookup / enrich | Unknown | Add source path or admin screenshot reference. |

## Mapping Rules

- Record API/internal names, not only display labels.
- Include object type, required/optional, enum values, and owner.
- Mark mismatches when a field exists in one system but no target field is confirmed.
- Do not store real customer data in examples.
