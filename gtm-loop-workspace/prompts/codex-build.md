# Codex Build Prompt

Use after `build-handoff.md` is ready.

```text
You are Codex working from a GTM Loop build handoff.

Read:
- gtm-loop-workspace/AGENTS.md
- gtm-loop-workspace/llm-wiki/shared-context.md
- clients/<client-slug>/build-handoff.md
- clients/<client-slug>/validation-notes.md

Task:
<specific build task>

Rules:
- Implement the smallest working change.
- Reuse existing repo patterns.
- Avoid new dependencies unless clearly necessary.
- Do not modify external/reference/client repos unless explicitly approved.
- Do not store secrets or real customer data.
- Leave one runnable validation check when logic changes.

Closeout:
- State files changed.
- State validation run or why skipped.
- Update client validation notes if requested.
```
