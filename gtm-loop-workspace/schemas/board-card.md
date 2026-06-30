# Board Card Contract

`board.md` is now a manager-facing mirror. Task files under `../tasks/` own the canonical state.

Use `task-card.md` for the source-of-truth schema.

## Board Entry Format

```markdown
- [GTM-###](tasks/GTM-###.md) - <short outcome>
  - Client: <client slug or Global>
  - Lane: Ricky / Brody / Archy / Cody / Verifier / Reporter
  - Status: Planned / In Progress / Smoke Test / In Review / Done
  - Blocked: yes / no
  - Next action: <one concrete next action>
```

## Rules

- Keep only five sections: Planned, In Progress, Smoke Test, In Review, Done.
- Do not add Blocked, Approval Required, Rework Needed, Backlog, Investigating, Designing, Building, or Validating as columns.
- Store those details as frontmatter flags and body notes in `../tasks/GTM-###.md`.
- Update the task first, then update the board mirror.
