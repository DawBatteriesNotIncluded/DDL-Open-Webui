# Open WebUI Import Guide

## Recommended Knowledge Uploads

Upload Markdown files from:

- `knowledge/`
- `loops/`
- `build-system/`
- `workflow-templates/`
- `prompts/`
- `evals/`
- `docs/security-and-secrets.md`

## Agent Setup

Create one custom model per agent in Workspace -> Models. Paste only the `System Prompt` section from the agent file into the model's system prompt field.

## Tool Setup

Enable n8n MCP only for agents that need workflow design, inspection, or debugging. Do not enable write-capable tools for agents that only evaluate or summarize.

## Secrets

Never upload `.env` files, real credentials, private customer data, patient data, or sensitive sponsor data to Knowledge.

