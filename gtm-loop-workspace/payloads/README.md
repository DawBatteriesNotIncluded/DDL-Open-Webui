# Payload Library

Library for fake or redacted payloads used in workflow design, validation, and debugging.

## Rules

- Use fake or redacted data only.
- Do not store real customer records, transcript text, tokens, auth headers, endpoint hosts, tenant IDs, or copied logs.
- Keep payloads small enough to inspect.
- Each payload should state purpose, source system, target workflow, expected result, and sensitivity.

## Suggested Folders

| Folder | Use |
| --- | --- |
| `hubspot/` | Fake CRM object examples and field mapping tests. |
| `gong/` | Redacted call metadata or synthetic transcript snippets. |
| `n8n/` | Webhook and execution test inputs. |
| `airops/` | Prompt-chain input/output examples. |
| `api/` | Custom API request/response examples. |

## Payload Card Template

```markdown
# Payload: <name>

| Field | Value |
| --- | --- |
| System | `TBD` |
| Purpose | `TBD` |
| Workflow | `TBD` |
| Sensitivity | Fake / Redacted |
| Expected Result | `TBD` |

## Payload

```json
{}
```
```

## Existing Samples

The existing `test-payloads/` folder contains earlier sample payloads. New workbench payloads should go here unless a legacy sample already fits.
