# Human Approval Gates

Human approval is required before:

- Activating workflows.
- Sending emails or external messages.
- Creating or modifying CRM records.
- Changing production data.
- Using sensitive Gong, HubSpot, sponsor, or customer data.
- Publishing content.
- Making customer-facing claims.
- Making commercial recommendations that affect customers or sellers.

## Approval Request Format

```markdown
## Approval Request

Action requested:
Systems affected:
Data read:
Data written:
External side effects:
Test evidence:
Risks:
Rollback:
Approve? yes/no
```

## Default V1 Policy

Prefer manual review queues and draft outputs. Move to automated writes only after repeated successful tests and explicit approval.

