# Open WebUI Code Change Recommendations

No Open WebUI source changes are required for this v1 workspace.

## If Future Changes Are Considered

Do not modify Open WebUI core casually. Prefer:

- Importing prompts through Workspace -> Models.
- Uploading Markdown through Workspace -> Knowledge.
- Attaching n8n MCP through supported tool configuration.
- Keeping workflow runtime in n8n.

Potential future enhancements to evaluate without implementing here:

- Agent bundle import/export.
- Knowledge collection automation.
- Read-only tool permission profiles.
- Safer MCP action confirmation UX.

