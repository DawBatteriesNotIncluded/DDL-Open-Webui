# HubSpot Field Mapping Prompt

```text
Create or review a HubSpot field mapping for the active client.

Read:
- clients/<client-slug>/hubspot.md
- clients/<client-slug>/field-mapping.md
- clients/<client-slug>/systems.md

For each mapped field, capture:
- source system and object;
- source API/internal field name;
- HubSpot object and field API name;
- display label if helpful;
- type and enum values;
- required/optional status;
- transform rule;
- write behavior;
- evidence;
- unknowns.

Flag mismatches where labels, enums, required fields, or ownership do not align.
```
