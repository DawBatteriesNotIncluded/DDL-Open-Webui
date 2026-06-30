# Agent Routing

Swimlane routing for board-driven GTM Loop work.

Task files under `../tasks/` own lane, gate, attempt, evidence, and manager-report state. `../board.md` mirrors the current manager-facing status.

## Roles

| Role | Job | May Change `board_status`? |
| --- | --- | --- |
| Manager | Sets priorities, approves gates, provides missing business context. | Yes |
| GTM Engineer Orchestrator | Reads active task, starts/resumes run, routes lanes, enforces gates. | Yes |
| Ricky Research Agent | Performs source-grounded research and separates confirmed facts from inference. | No |
| Brody Investigation Agent | Captures requirements, integration evidence, mismatches, unknowns, and owner questions. | No |
| Archy Architecture Agent | Records architecture, boundaries, risks, ADRs, and design tradeoffs when needed. | No |
| Cody Build Agent | Creates the smallest useful draft, spec, prompt, payload, workflow artifact, or code change from the handoff. | No |
| GTM Verifier Agent | Checks evidence, evals, fake payloads, acceptance criteria, drift, and definition of done. | No |
| GTM Reporter Agent | Updates task files, board mirror, run ledger, and manager report after verifier result. | Yes, after verifier result |

## Lane Responsibilities

| Lane | Use When | Typical Evidence |
| --- | --- | --- |
| `ricky` | External or source-grounded research is needed. | Source list, evidence cards, date/context notes. |
| `brody` | Requirements, client workflow, system facts, or integration evidence are unclear. | Confirmed facts, mismatches, unknowns, endpoint/field notes. |
| `archy` | Architecture, risk, boundaries, data flow, or ADR is needed. | System map, integration flow, risk notes, ADR when justified. |
| `cody` | A build, workflow draft, prompt, payload, or implementation handoff must be produced. | Build handoff, artifact links, acceptance checks. |
| `verifier` | Smoke test, validation, drift check, or definition-of-done check is required. | Expected/actual result, fake payload, verifier decision. |
| `reporter` | Board, run log, durable memory, or manager summary must be updated. | Board mirror, run ledger row, manager report. |

## Tool Placement

| Tool | Role Now | Later Upgrade |
| --- | --- | --- |
| Codex | Local repo edits, Markdown task state, scripts, safe validation. | Build controlled artifacts from handoffs. |
| Open WebUI | Cockpit, Knowledge, review, manager interaction. | Live board after task files are stable. |
| board MCP | Not connected. Board remains local Markdown. | Read/update task files only after schema is stable. |
| codebase-memory-mcp | Code discovery and impact analysis for repo work. | Same. |
| n8n MCP | Disabled for writes. Planning/inspection only after tool registry confirms scope. | Draft/import workflows only after approval gates. |
| AirOps | Guidance only. | Draft content workflows when content production is in scope. |
| HubSpot | Guidance only. | Read metadata first; writes require exact approval. |
| Gong | Guidance only. | Redacted summaries/metadata first; raw transcript handling needs approval. |
| Docker | Local service/status validation only. | Local test harnesses. |
| GitHub MCP | Deferred. | Issues/PR sync after local task control works. |
| Hermes | Deferred until send/write surface is defined. | Approval-gated messaging only. |
| OpenHands | Deferred executor. | Use only from a verified build handoff. |

## Routing Rule

If a task can be completed by updating Markdown state, do that before adding tools or automation.

Agents must read `../tasks/GTM-###.md` before acting, update that file first, and then update the summary in `../board.md`.
