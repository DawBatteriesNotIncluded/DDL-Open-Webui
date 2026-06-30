# How To Debug n8n With Open WebUI

## Steps

1. Open Workflow Debugger Agent.
2. Paste redacted failed execution log.
3. Include workflow name, failing node, input JSON, output/error JSON, and expected behavior.
4. Ask the agent to classify the failure.
5. Review proposed fix and corrected test payload.
6. Test with fake payload.
7. Request approval before retrying production execution.

## Debug Prompt

```text
Here is a failed n8n execution log. Diagnose it and propose a fix. Classify whether the problem is prompt, data, API, auth, schema, mapping, environment, rate limit, or workflow logic.
```

## Do Not Paste

- API keys.
- Raw credentials.
- Patient-identifiable data.
- Private sponsor data.
- Sensitive customer data unless approved.

