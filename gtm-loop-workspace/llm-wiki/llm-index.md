# LLM Wiki Index

Agent-readable entry point for the GTM Loop workspace.

## Read First

| Need | Start Here |
| --- | --- |
| Current client and priority | `current-client.md` |
| Shared operating context | `shared-context.md` |
| System and integration map | `systems-map.md` |
| Open questions across clients | `open-questions.md` |
| Field mappings across systems | `field-mappings.md` |
| Reusable automation patterns | `automation-patterns.md` |
| Local and client repo/source map | `repo-index.md` |

## Working Rule

Client-specific detail belongs in `clients/<client-slug>/`. Only promote durable context into `llm-wiki/` when future agents should read it before work.

## Evidence Labels

- `Confirmed`: directly supported by inspected evidence.
- `Confirmed mismatch`: inspected evidence contradicts the claim.
- `Unknown`: not enough evidence.
- `Inferred`: likely, but not production truth.
- `Recommendation`: proposed action based on evidence and assumptions.
