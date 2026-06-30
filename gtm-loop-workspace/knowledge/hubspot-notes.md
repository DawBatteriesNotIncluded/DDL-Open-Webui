# HubSpot Notes

## Role

HubSpot is the CRM system of record. It should not be polluted by low-confidence signals or unreviewed AI outputs.

## Safe V1 Pattern

Read account/deal/contact context -> generate recommendation -> human approval -> create task or note.

## Common Writes

- Task for seller action.
- Note with evidence-backed summary.
- Deal property update only after explicit approval.

## Required Considerations

- Object associations.
- Owner assignment.
- Duplicate prevention.
- Field validation.
- Required scopes.
- Auditability.

## Approval

All CRM writes require explicit approval until the loop has proven quality and safety.

