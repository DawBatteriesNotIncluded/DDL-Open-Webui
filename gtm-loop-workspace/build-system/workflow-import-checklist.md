# Workflow Import Checklist

Before importing into n8n:

- [ ] Workflow purpose is documented.
- [ ] JSON contains no secrets.
- [ ] Credentials are placeholders or existing approved credentials.
- [ ] Workflow imports disabled.
- [ ] Test payload is available.
- [ ] Approval gate exists before writes/sends.
- [ ] Error branch is documented.
- [ ] Idempotency key is defined.
- [ ] Owner is assigned.
- [ ] Rollback plan is documented.

After importing:

- [ ] Run manual trigger with fake payload.
- [ ] Confirm all expressions resolve.
- [ ] Confirm no production writes occur during dry run.
- [ ] Confirm logs are readable.
- [ ] Confirm failure path works.
- [ ] Update build status.

