# AirOps Notes

## Role

AirOps is useful for repeatable content and prompt-chain workflows, especially where multiple generation and QA steps are needed.

## Good Fits

- Content repurposing.
- Proposal content assembly.
- Multi-step content QA.
- Reusable prompt chains.

## Poor Fits

- Stateful integration runtime.
- Credential-heavy CRM writes.
- Workflow activation or operational retries.

## Handoff Pattern

Open WebUI designs the chain, AirOps runs repeatable content production, n8n routes inputs/outputs, and humans approve external use.

