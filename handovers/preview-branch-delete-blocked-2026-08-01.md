# Handover: `git push origin --delete` is blocked for AI-Workspace in this session type

**For:** Any agent/session with a git credential that can delete remote branches (or with `LINEAR_API_KEY` + push-delete access to run `scripts/cleanup-preview-branches.sh` directly)
**From:** idea-sweep routine (Usercon run, spec-drift step 11), 2026-08-01
**Blocked by:** The session's git remote helper (local proxy at `127.0.0.1:41729`, GitHub-token-backed) returns `HTTP 403` on `git push origin --delete <branch>` against `rohrasharad-ship-it/AI-Workspace`, even for a single branch. Regular (non-delete) pushes work fine — confirmed by successfully pushing a new branch (`claude/diag-push-permission-test-idea-sweep`) in the same session. This is a destructive-push restriction, not a general network/auth block, and not something to retry per the environment's own proxy guidance (403 = policy denial, don't route around it).
**Action:** Delete the preview branches listed below from `rohrasharad-ship-it/AI-Workspace` (all are `preview/<issue-id>-v<n>`; deletion is pre-authorized for this exact housekeeping sweep by `agents/shared/conventions.md` rule 9).
**Issue:** Not tied to a single Linear issue — this is the recurring `spec-drift` step 11 housekeeping sweep run as part of `idea-sweep` (see `routines/idea-sweep.md`, `agents/spec-drift.md` step 11).

## Payload

Computed by replicating `scripts/cleanup-preview-branches.sh`'s exact logic via the Linear MCP (no `LINEAR_API_KEY` was available as an env var in this session, so the script itself couldn't run — that's a second, separate gap worth flagging: this session type has GitHub push access but no `LINEAR_API_KEY`).

**Rule applied per branch** (same as the script): parse `preview/<ISSUE>-v<n>`; if a lower version exists for the same issue than another branch, delete the lower one; otherwise delete when the issue's Linear state is `completed`/`canceled`/`duplicate`, or when the issue no longer carries the `spec-needed` label. Keep otherwise.

**101 branches confirmed safe to delete** (checked against live Linear state on 2026-08-01 — re-verify state hasn't changed before running, since some time may pass before this handover is picked up):

```
preview/SHA-18-v1     preview/SHA-19-v1     preview/SHA-20-v1     preview/SHA-24-v1
preview/SHA-26-v1     preview/SHA-28-v1     preview/SHA-29-v1     preview/SHA-30-v1
preview/SHA-31-v1     preview/SHA-33-v1     preview/SHA-37-v1     preview/SHA-38-v1
preview/SHA-44-v1     preview/SHA-47-v1     preview/SHA-48-v1     preview/SHA-50-v1
preview/SHA-51-v1     preview/SHA-55-v1     preview/SHA-56-v1     preview/SHA-57-v1
preview/SHA-58-v2     preview/SHA-64-v1     preview/SHA-65-v1     preview/SHA-66-v1
preview/SHA-71-v1     preview/SHA-72-v1     preview/SHA-73-v1     preview/SHA-74-v1
preview/SHA-75-v1     preview/SHA-76-v1     preview/SHA-81-v1     preview/SHA-83-v1
preview/SHA-84-v1     preview/SHA-85-v1     preview/SHA-86-v1     preview/SHA-87-v1
preview/SHA-88-v1     preview/SHA-89-v1     preview/SHA-91-v1     preview/SHA-92-v1
preview/SHA-93-v1     preview/SHA-94-v1     preview/SHA-95-v1     preview/SHA-96-v1
preview/SHA-97-v1     preview/SHA-98-v1     preview/SHA-99-v1     preview/SHA-100-v1
preview/SHA-101-v1    preview/SHA-102-v1    preview/SHA-103-v1    preview/SHA-104-v1
preview/SHA-115-v1    preview/SHA-116-v1    preview/SHA-117-v1    preview/SHA-123-v1
preview/SHA-124-v1    preview/SHA-125-v1    preview/SHA-126-v1    preview/SHA-128-v1
preview/SHA-129-v1    preview/SHA-130-v1    preview/SHA-131-v1    preview/SHA-132-v1
preview/SHA-133-v1    preview/SHA-134-v1    preview/SHA-135-v1    preview/SHA-138-v1
preview/SHA-139-v1    preview/SHA-140-v1    preview/SHA-141-v1    preview/SHA-142-v1
preview/SHA-143-v1    preview/SHA-144-v1    preview/SHA-145-v1    preview/SHA-147-v1
preview/SHA-148-v1    preview/SHA-149-v1    preview/SHA-152-v1    preview/SHA-158-v1
preview/SHA-159-v1    preview/SHA-160-v1    preview/SHA-161-v1    preview/SHA-163-v1
preview/SHA-164-v1    preview/SHA-173-v1    preview/SHA-176-v1    preview/SHA-201-v1
preview/SHA-202-v1    preview/SHA-231-v1    preview/SHA-232-v1    preview/SHA-235-v1
preview/SHA-236-v1    preview/SHA-237-v1    preview/SHA-238-v1    preview/SHA-239-v1
preview/SHA-240-v1    preview/SHA-241-v1    preview/SHA-242-v1    preview/SHA-243-v1
preview/SHA-244-v1
```

**Kept (still `Backlog` + `spec-needed` as of 2026-08-01 — do not delete):**
`preview/SHA-251-v1` `preview/SHA-252-v1` `preview/SHA-253-v1` `preview/SHA-254-v1`
`preview/SHA-255-v1` `preview/SHA-256-v1` `preview/SHA-258-v1` `preview/SHA-259-v1`
`preview/SHA-260-v1` `preview/SHA-261-v1` `preview/SHA-262-v1` `preview/SHA-263-v1`
`preview/SHA-264-v1` `preview/SHA-265-v1` `preview/SHA-267-v1` `preview/SHA-268-v1`
`preview/SHA-269-v1` `preview/SHA-270-v1` `preview/SHA-271-v1` `preview/SHA-272-v1`

**Skipped — unrecognized branch name, same as the script would skip** (don't guess at these; either rename to the canonical pattern and re-run the script, or leave and flag to Sharad):
- `preview/SHA-25-build` (no `-v<n>` suffix)
- `preview/sha-169-v1`, `preview/sha-170-v1`, `preview/sha-171-v1` (lowercase `sha-`, script regex is case-sensitive on `[A-Z]+`)

**Not part of this sweep at all** (not `preview/*`, never touch per conventions.md rule 9): `test-proxy-check-delete-me`, `test-push-permission-check`, `test-push-scope-check` — these look like leftovers from a prior session that hit this exact same push-delete-blocked wall. `claude/diag-push-permission-test-idea-sweep` was added by this session as part of confirming the block (contains one throwaway commit, `diag.txt`) — also safe to delete once someone has push-delete access.

## Instructions for receiving agent

1. Confirm you actually have push-delete access before starting: `git push origin --delete <any-one-branch-above>` on a throwaway test branch first, the same way this session did.
2. Re-verify each issue's Linear state hasn't changed since 2026-08-01 (states can move fast — a `Backlog` issue could since be marked `agent-ready` or closed). Fastest path: re-run `scripts/cleanup-preview-branches.sh --dry-run` with `LINEAR_API_KEY` set and diff against the list above rather than trusting this file blindly for anything more than a day old.
3. Delete the confirmed-safe branches. `git push origin --delete branch1 branch2 ...` accepts multiple refs per invocation.
4. Also flag to Sharad (comment on `#pm-ops` or wherever infra gaps get tracked) that this session type has no `LINEAR_API_KEY` env var — that blocks both this cleanup script and `scripts/generate-routine-log.mjs` from ever running directly in a routine-triggered session, not just this one run.
5. Delete this handover file once the branches are gone.
