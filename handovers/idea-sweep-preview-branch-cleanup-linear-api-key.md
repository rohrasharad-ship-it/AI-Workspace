# Handover: Preview-branch cleanup blocked — git branch deletion rejected by session proxy

**For:** Any agent/session with real `git push origin --delete` capability against `rohrasharad-ship-it/AI-Workspace` (or a `LINEAR_API_KEY` env var to run the script from a session that can push-delete)
**From:** spec-drift housekeeping (idea-sweep routine, step 10-11 path), triggered for project "Usercon" (Linear project `47ebefac-a4f4-4bdd-a382-4506f7e79b6b`), 2026-07-30
**Blocked by:** This session's local git relay (`http://127.0.0.1:41729/git/rohrasharad-ship-it/AI-Workspace`) returns `HTTP 403` on **any** `git push origin --delete <branch>`, including a single harmless orphaned `preview/*` branch (`preview/SHA-100-v1`, issue completed long ago) — confirmed it is not a batch-size issue by retrying with one branch alone. Normal (non-delete) pushes to this session's designated branch succeed fine (`git push origin HEAD:refs/heads/claude/magical-fermat-6jzlie --dry-run` → `new branch`). The GitHub MCP server also exposes no delete-branch/delete-ref tool (only `delete_file`, which deletes a file, not a ref). Per the proxy's own guidance (`/root/.ccr/README.md`), a 403 is a policy denial to report, not to route around — so no direct GitHub REST/GraphQL delete-ref workaround was attempted.
**Action:** From a session where `git push origin --delete <branch>` actually succeeds against this repo, delete the 101 branches listed below (or re-run `scripts/cleanup-preview-branches.sh`, which needs `LINEAR_API_KEY` — also unavailable in this session's env — and independently reaches the same set).
**Issue:** No single Linear issue drives this — routine housekeeping (`agents/spec-drift.md` step 11), not a product gap. Do not file a Linear issue against any project for this.

## Payload

This session could not run `scripts/cleanup-preview-branches.sh` directly (no `LINEAR_API_KEY`), so it **replicated the script's exact selection logic** using live Linear MCP data instead (fetched every issue in the `Sharad Rohra` team — `teamId 4d02f6ce-cd9a-4dd9-97d1-86b17bdf83b8` — covering all 5 projects, paginated in full, 271 issues) cross-referenced against the live `origin/preview/*` branch list (130 branches as of this run, up from ~95 noted in the prior version of this handover on 2026-07-27). The same rules as the script were applied:
- Delete if branch version < that issue's max branch version ("older version").
- Delete if the issue's Linear state is `completed`, `canceled`, or `duplicate`.
- Delete if the issue no longer carries the `spec-needed` label (moved to `agent-ready` etc. without it).
- Otherwise keep.
- Branch names not matching `preview/[A-Z]+-[0-9]+-v[0-9]+` are left untouched, matching the script's own regex (it would also skip these): `preview/SHA-25-build`, `preview/sha-169-v1`, `preview/sha-170-v1`, `preview/sha-171-v1` (the last three are lowercase `sha-`, so they never matched the script's uppercase-only pattern — worth fixing at the source, i.e. whichever agent created them, but out of scope for this handover).

**Result: 101 to delete, 17 to keep, 0 unresolvable (every issue referenced by a branch was found in Linear), 4 branches left alone as unrecognized names.**

No `git push origin --delete` was actually executed successfully in this session — every attempt returned the 403 above, so **nothing was deleted**. This plan is a dry-run equivalent only.

### Branches to delete (101) — `<branch>\t<reason>`

```
preview/SHA-100-v1	issue state is completed
preview/SHA-101-v1	issue state is canceled
preview/SHA-102-v1	issue state is canceled
preview/SHA-103-v1	issue state is completed
preview/SHA-104-v1	issue state is canceled
preview/SHA-115-v1	issue state is completed
preview/SHA-116-v1	issue state is completed
preview/SHA-117-v1	issue state is completed
preview/SHA-123-v1	issue state is canceled
preview/SHA-124-v1	issue state is canceled
preview/SHA-125-v1	issue state is canceled
preview/SHA-126-v1	issue state is duplicate
preview/SHA-128-v1	issue state is duplicate
preview/SHA-129-v1	issue state is duplicate
preview/SHA-130-v1	issue state is duplicate
preview/SHA-131-v1	issue state is duplicate
preview/SHA-132-v1	issue state is duplicate
preview/SHA-133-v1	issue state is duplicate
preview/SHA-134-v1	issue state is duplicate
preview/SHA-135-v1	issue state is canceled
preview/SHA-138-v1	issue state is completed
preview/SHA-139-v1	issue state is completed
preview/SHA-140-v1	issue state is completed
preview/SHA-141-v1	issue state is canceled
preview/SHA-142-v1	issue state is canceled
preview/SHA-143-v1	issue state is completed
preview/SHA-144-v1	issue state is canceled
preview/SHA-145-v1	issue state is canceled
preview/SHA-147-v1	issue state is canceled
preview/SHA-148-v1	issue state is canceled
preview/SHA-149-v1	issue state is canceled
preview/SHA-152-v1	issue state is canceled
preview/SHA-158-v1	issue state is canceled
preview/SHA-159-v1	issue state is canceled
preview/SHA-160-v1	issue state is canceled
preview/SHA-161-v1	issue state is canceled
preview/SHA-163-v1	issue state is canceled
preview/SHA-164-v1	issue state is canceled
preview/SHA-173-v1	issue state is completed
preview/SHA-176-v1	issue state is canceled
preview/SHA-18-v1	issue state is canceled
preview/SHA-19-v1	issue state is canceled
preview/SHA-20-v1	issue state is canceled
preview/SHA-201-v1	issue state is canceled
preview/SHA-202-v1	issue state is canceled
preview/SHA-231-v1	issue state is completed
preview/SHA-232-v1	issue state is canceled
preview/SHA-235-v1	issue state is canceled
preview/SHA-236-v1	issue state is canceled
preview/SHA-237-v1	issue state is canceled
preview/SHA-238-v1	issue state is canceled
preview/SHA-239-v1	issue state is completed
preview/SHA-24-v1	issue state is canceled
preview/SHA-240-v1	issue state is canceled
preview/SHA-241-v1	issue state is canceled
preview/SHA-242-v1	issue state is canceled
preview/SHA-243-v1	issue state is completed
preview/SHA-244-v1	issue state is canceled
preview/SHA-26-v1	issue state is canceled
preview/SHA-28-v1	issue state is canceled
preview/SHA-29-v1	issue state is completed
preview/SHA-30-v1	issue state is canceled
preview/SHA-31-v1	issue state is canceled
preview/SHA-33-v1	issue state is completed
preview/SHA-37-v1	issue state is canceled
preview/SHA-38-v1	issue state is canceled
preview/SHA-44-v1	issue state is completed
preview/SHA-47-v1	issue state is canceled
preview/SHA-48-v1	issue state is canceled
preview/SHA-50-v1	issue state is canceled
preview/SHA-51-v1	issue state is canceled
preview/SHA-55-v1	issue state is canceled
preview/SHA-56-v1	issue state is canceled
preview/SHA-57-v1	issue state is canceled
preview/SHA-58-v2	issue state is canceled
preview/SHA-64-v1	issue state is completed
preview/SHA-65-v1	issue state is completed
preview/SHA-66-v1	issue state is canceled
preview/SHA-71-v1	issue state is canceled
preview/SHA-72-v1	issue state is completed
preview/SHA-73-v1	issue state is canceled
preview/SHA-74-v1	issue state is completed
preview/SHA-75-v1	issue state is completed
preview/SHA-76-v1	issue state is completed
preview/SHA-81-v1	issue state is completed
preview/SHA-83-v1	issue state is canceled
preview/SHA-84-v1	issue state is canceled
preview/SHA-85-v1	issue state is canceled
preview/SHA-86-v1	issue state is canceled
preview/SHA-87-v1	issue state is canceled
preview/SHA-88-v1	issue state is canceled
preview/SHA-89-v1	issue state is canceled
preview/SHA-91-v1	issue state is canceled
preview/SHA-92-v1	issue state is canceled
preview/SHA-93-v1	issue state is canceled
preview/SHA-94-v1	issue state is canceled
preview/SHA-95-v1	issue state is canceled
preview/SHA-96-v1	issue state is completed
preview/SHA-97-v1	issue state is canceled
preview/SHA-98-v1	issue state is canceled
preview/SHA-99-v1	issue state is canceled
```

### Branches to keep (17) — still `spec-needed` at their latest version

```
preview/SHA-251-v1, preview/SHA-252-v1, preview/SHA-253-v1, preview/SHA-254-v1,
preview/SHA-255-v1, preview/SHA-256-v1, preview/SHA-258-v1, preview/SHA-259-v1,
preview/SHA-260-v1, preview/SHA-261-v1, preview/SHA-262-v1, preview/SHA-263-v1,
preview/SHA-264-v1, preview/SHA-265-v1, preview/SHA-267-v1, preview/SHA-268-v1,
preview/SHA-269-v1
```

## Instructions for receiving agent

1. Confirm your session's `git push origin --delete <branch>` actually works against `rohrasharad-ship-it/AI-Workspace` before trusting this plan blindly (try one branch from the delete list first, e.g. `preview/SHA-100-v1`).
2. Given time may have passed since 2026-07-30, either re-run `scripts/cleanup-preview-branches.sh --dry-run` (if you have `LINEAR_API_KEY`) to get a fresh authoritative list, or at minimum spot-check a handful of the "delete" entries above against current Linear state before bulk-deleting — issue states can change.
3. Delete the confirmed-stale branches: `git push origin --delete $(cat list-of-branches.txt)` in reasonably small batches.
4. Report the final deleted/kept/skipped counts wherever this routine's results are tracked (e.g. `data/sweep-runs.jsonl`).
5. Also worth a look, not required to unblock this handover: fix or delete the 4 unrecognized-name branches (`preview/SHA-25-build`, `preview/sha-169-v1`, `preview/sha-170-v1`, `preview/sha-171-v1`) — the lowercase `sha-` ones look like a naming-convention slip by whichever agent created them (`agents/shared/visual-specs.md` specifies `preview/<issue-id>-v<n>` with the issue ID as Linear returns it, i.e. uppercase `SHA-`).
6. Delete this handover file once the cleanup has actually run successfully.

**Do not** execute deletions from a session where `git push origin --delete` is itself untested — verify capability first (step 1) rather than assuming this session's blocker was one-off.
