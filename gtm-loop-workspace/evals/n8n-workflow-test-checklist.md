# n8n Workflow Test Checklist

- [ ] Fake happy-path payload passes.
- [ ] Missing required field fails safely.
- [ ] Malformed JSON fails safely.
- [ ] Duplicate payload does not duplicate writes.
- [ ] Low-confidence input stops before write.
- [ ] Auth failure stops safely.
- [ ] Rate limit behavior is defined.
- [ ] Approval denied path stops cleanly.
- [ ] Logs contain execution ID and decision.
- [ ] No production writes occurred during test.

