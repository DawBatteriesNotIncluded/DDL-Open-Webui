# Open WebUI Loop Engineering Setup

## Usage Model

- Open WebUI: cockpit for reasoning, design, debugging, supervision, and review.
- n8n: runtime for scheduled/background workflows and integrations.
- AirOps: content and prompt-chain production workflows.
- Codex: code/file/workspace builder.
- MCP/OpenAPI tools: controlled action layer.
- GitHub/repo: versioned source of truth.
- Knowledge/RAG: reusable context and documentation.
- Evals: quality and safety checks.

## Setup Steps

1. Create Knowledge collections for operating docs, loops, build-system, integrations, prompts, and evals.
2. Upload selected Markdown files from this workspace.
3. Create custom Models for the main agents.
4. Paste each agent's `System Prompt` section into its model.
5. Attach relevant Knowledge collections to each model.
6. Enable n8n MCP only for agents that need workflow design, inspection, or debugging.
7. Test each agent with fake payloads before using real data.

## Model Prompt Vs Knowledge Vs Tool Vs n8n Workflow

- Model prompt: stable role, rules, output format, safety boundaries.
- Knowledge: reusable docs, templates, schemas, examples, playbooks.
- Tool: controlled action or data retrieval layer.
- n8n workflow: repeatable runtime automation with triggers, retries, logs, and state.

