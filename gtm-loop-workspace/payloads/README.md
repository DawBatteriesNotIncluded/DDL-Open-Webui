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

## Starter Payloads

| Payload | Use |
| --- | --- |
| `hubspot/contact-company-update.fake.json` | Fake HubSpot contact/company update mapping. |
| `gong/call-transcript-event.fake.json` | Fake/redacted Gong call event and signal extraction. |
| `n8n/webhook-input.fake.json` | Fake n8n webhook trigger input. |
| `airops/enrichment-request.fake.json` | Fake AirOps enrichment request. |
| `airops/enrichment-response.fake.json` | Fake AirOps enrichment response. |
| `api/custom-webhook.fake.json` | Fake custom API webhook input. |

## Payload Card Template

Use this shape in a short Markdown note if a payload needs explanation beyond the JSON file:

- Payload: `<name>`
- System: `TBD`
- Purpose: `TBD`
- Workflow: `TBD`
- Sensitivity: Fake / Redacted
- Expected result: `TBD`
- JSON file: `payloads/<system>/<name>.fake.json`

Keep the actual payload in a `.fake.json` file.

## Existing Samples

The existing `test-payloads/` folder contains earlier sample payloads. New workbench payloads should go here unless a legacy sample already fits.
