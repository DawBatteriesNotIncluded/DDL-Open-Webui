# Codex Plan Prompt

Use when the work needs a plan before file edits or build activity.

```text
You are working in the GTM Loop workspace.

Read:
- gtm-loop-workspace/AGENTS.md
- gtm-loop-workspace/llm-wiki/llm-index.md
- the active client folder

Goal:
<state the desired outcome>

Constraints:
- Keep changes lean.
- Prefer Markdown/templates unless implementation is explicitly requested.
- Do not write secrets, endpoint hosts, tenant IDs, tokens, auth headers, copied logs, or raw customer data.
- Separate Confirmed, Confirmed mismatch, Unknown, Inferred, and Recommendation.

Return:
1. Current understanding.
2. Files you need to inspect.
3. Proposed file changes.
4. Validation/checks.
5. Open questions that materially affect the work.
```
