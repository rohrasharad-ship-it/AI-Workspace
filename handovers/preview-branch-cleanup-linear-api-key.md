# Handover: preview-branch-cleanup.yml has never succeeded — missing LINEAR_API_KEY repo secret

**For:** Any agent/human with repo Settings → Secrets access on `rohrasharad-ship-it/AI-Workspace`
**From:** spec-drift housekeeping (step 11), idea-sweep routine run for Resume Website, 2026-08-06 (previously: AI Landscape 2026, 2026-08-02; Resume Website, 2026-08-05)
**Blocked by:** `.github/workflows/preview-branch-cleanup.yml` requires `secrets.LINEAR_API_KEY`, which is not set on this repo. All runs to date (2026-07-21, 2026-07-27, 2026-08-02, 2026-08-05, and this 2026-08-06 run, run IDs 29878193147 / 30266096565 / 30772723638) failed or were blocked identically. This session again had no Linear API key as a Bash env var (only Linear MCP tool access, which the shell script can't use), no working `git push` for arbitrary branch deletion (proxy returns HTTP 403 on `push --delete preview/*`, even though push to this session's own designated branch succeeds — the deploy credential is scoped, not a transient network issue), and no MCP tool that deletes a git ref — so neither the automated path nor a manual fallback could complete this session either. **Three consecutive routine runs now confirm the same root cause; this is not a fluke.**
**Action:** Add `LINEAR_API_KEY` as a repository secret (Settings → Secrets and variables → Actions → New repository secret), then either re-run the workflow via `workflow_dispatch` or wait for the next Monday 09:00 UTC schedule. That single fix clears the entire backlog below — no per-branch manual work needed once the secret exists.

## Payload

Using Linear MCP (`list_issues` across the whole workspace, all 270 issues, both pages) cross-referenced against every `preview/*` branch in this repo (full `git branch -r --list 'origin/preview/*'` after `git fetch --prune`), this 2026-08-06 run confirmed an **exhaustive** list of 101 branches safe to delete under the rule in `agents/spec-drift.md` step 11 (issue no longer `spec-needed`, or terminal status — Done/Canceled/Duplicate). This supersedes the earlier non-exhaustive list — every branch below was checked, none skipped for lack of pagination:

```
preview/SHA-18-v1, preview/SHA-19-v1, preview/SHA-20-v1, preview/SHA-24-v1, preview/SHA-26-v1,
preview/SHA-28-v1, preview/SHA-29-v1, preview/SHA-30-v1, preview/SHA-31-v1, preview/SHA-33-v1,
preview/SHA-37-v1, preview/SHA-38-v1, preview/SHA-44-v1, preview/SHA-47-v1, preview/SHA-48-v1,
preview/SHA-50-v1, preview/SHA-51-v1, preview/SHA-55-v1, preview/SHA-56-v1, preview/SHA-57-v1,
preview/SHA-58-v2, preview/SHA-64-v1, preview/SHA-65-v1, preview/SHA-66-v1, preview/SHA-71-v1,
preview/SHA-72-v1, preview/SHA-73-v1, preview/SHA-74-v1, preview/SHA-75-v1, preview/SHA-76-v1,
preview/SHA-81-v1, preview/SHA-83-v1, preview/SHA-84-v1, preview/SHA-85-v1, preview/SHA-86-v1,
preview/SHA-87-v1, preview/SHA-88-v1, preview/SHA-89-v1, preview/SHA-91-v1, preview/SHA-92-v1,
preview/SHA-93-v1, preview/SHA-94-v1, preview/SHA-95-v1, preview/SHA-96-v1, preview/SHA-97-v1,
preview/SHA-98-v1, preview/SHA-99-v1, preview/SHA-100-v1, preview/SHA-101-v1, preview/SHA-102-v1,
preview/SHA-103-v1, preview/SHA-104-v1, preview/SHA-115-v1, preview/SHA-116-v1, preview/SHA-117-v1,
preview/SHA-123-v1, preview/SHA-124-v1, preview/SHA-125-v1, preview/SHA-126-v1, preview/SHA-128-v1,
preview/SHA-129-v1, preview/SHA-130-v1, preview/SHA-131-v1, preview/SHA-132-v1, preview/SHA-133-v1,
preview/SHA-134-v1, preview/SHA-135-v1, preview/SHA-138-v1, preview/SHA-139-v1, preview/SHA-140-v1,
preview/SHA-141-v1, preview/SHA-142-v1, preview/SHA-143-v1, preview/SHA-144-v1, preview/SHA-145-v1,
preview/SHA-147-v1, preview/SHA-148-v1, preview/SHA-149-v1, preview/SHA-152-v1, preview/SHA-158-v1,
preview/SHA-159-v1, preview/SHA-160-v1, preview/SHA-161-v1, preview/SHA-163-v1, preview/SHA-164-v1,
preview/SHA-173-v1, preview/SHA-176-v1, preview/SHA-201-v1, preview/SHA-202-v1, preview/SHA-231-v1,
preview/SHA-232-v1, preview/SHA-235-v1, preview/SHA-236-v1, preview/SHA-237-v1, preview/SHA-238-v1,
preview/SHA-239-v1, preview/SHA-240-v1, preview/SHA-241-v1, preview/SHA-242-v1, preview/SHA-243-v1,
preview/SHA-244-v1
```

Not touched (unrecognized branch name, same as the script's own regex would skip): `preview/sha-169-v1`, `preview/sha-170-v1`, `preview/sha-171-v1` (lowercase issue prefix), `preview/SHA-25-build` (no `-v<n>` suffix). These need manual review/rename, not blind deletion, if they're actually orphaned.

**Do NOT delete** (still Backlog + `spec-needed`, actively awaiting spec/triage): SHA-251, SHA-252, SHA-253, SHA-254, SHA-255, SHA-256, SHA-258, SHA-259, SHA-260, SHA-261, SHA-262, SHA-263, SHA-264, SHA-265, SHA-267, SHA-268, SHA-269, SHA-270, SHA-271, SHA-272.

Also present but **not** `preview/*` — do not touch: `test-proxy-check-delete-me`, `test-push-permission-check`, `test-push-scope-check` (out of scope for this cleanup; only `preview/*` branches are ever authorized for deletion per `agents/shared/visual-specs.md`).

## Instructions for receiving agent

1. Add the `LINEAR_API_KEY` repo secret.
2. Trigger `preview-branch-cleanup.yml` via `workflow_dispatch` (or let the Monday cron do it).
3. Confirm the run's conclusion is `success` and check the job log for the actual delete count.
4. If it succeeds, this handover file can be deleted — the backlog above will be cleared programmatically, no need to hand-verify my list against it.
