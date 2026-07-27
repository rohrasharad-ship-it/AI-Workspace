# Handover: 101 orphaned preview/* branches identified for deletion, cannot delete from this session

**For:** Any agent/session with branch-delete push access to `rohrasharad-ship-it/AI-Workspace`
**From:** idea-sweep routine (spec-drift step 11, standalone housekeeping run), 2026-07-27
**Blocked by:** `git push origin --delete <branch>` returns `error: RPC failed; HTTP 403` from this session's git proxy (`http://local_proxy@127.0.0.1:41729/...`). No `delete_branch`/ref-delete tool is exposed via the GitHub MCP server either (only `create_branch` is available). `LINEAR_API_KEY` is also not set in this session's environment, so `scripts/cleanup-preview-branches.sh` itself cannot run (it calls the Linear GraphQL API directly with curl) — the analysis below was produced by reimplementing the script's exact logic using the Linear MCP tools instead.
**Action:** Run `git push origin --delete` for each branch listed below (all already verified against the script's deletion rule — see Payload), then re-run `bash scripts/cleanup-preview-branches.sh --dry-run` to confirm nothing is left over.
**Issue:** N/A — this is routine housekeeping (`agents/spec-drift.md` step 11 / `routines/idea-sweep.md`), not tied to a single Linear issue.

## Payload

Reproduced the script's logic exactly (`scripts/cleanup-preview-branches.sh`):
1. Listed all `origin/preview/*` branches (105 total).
2. Parsed each against `^preview/([A-Z]+-[0-9]+)-v([0-9]+)$`. 4 did not match and were left alone (same as the script's "skip: unrecognized branch name" behavior): `preview/SHA-25-build`, `preview/sha-169-v1`, `preview/sha-170-v1`, `preview/sha-171-v1` (lowercase issue IDs — the script's regex requires uppercase).
3. Of the 101 recognized branches, grouped by issue ID: none were an older version than another branch for the same issue (each issue only has one preview branch).
4. Looked up all 101 issues via Linear MCP (`list_issues`, workspace-wide, single page, 249 total issues, no pagination needed). Every one of the 101 issues is in a terminal state (`Done`/`Canceled`/`Duplicate`) — matching the script's `completed|canceled|duplicate` deletion rule. None needed the `spec-needed` label check (that branch of the logic only applies to issues still in an active state).

**Result: all 101 recognized branches are safe to delete per the script's own rule.** Full list:

```
preview/SHA-100-v1  preview/SHA-101-v1  preview/SHA-102-v1  preview/SHA-103-v1  preview/SHA-104-v1
preview/SHA-115-v1  preview/SHA-116-v1  preview/SHA-117-v1  preview/SHA-123-v1  preview/SHA-124-v1
preview/SHA-125-v1  preview/SHA-126-v1  preview/SHA-128-v1  preview/SHA-129-v1  preview/SHA-130-v1
preview/SHA-131-v1  preview/SHA-132-v1  preview/SHA-133-v1  preview/SHA-134-v1  preview/SHA-135-v1
preview/SHA-138-v1  preview/SHA-139-v1  preview/SHA-140-v1  preview/SHA-141-v1  preview/SHA-142-v1
preview/SHA-143-v1  preview/SHA-144-v1  preview/SHA-145-v1  preview/SHA-147-v1  preview/SHA-148-v1
preview/SHA-149-v1  preview/SHA-152-v1  preview/SHA-158-v1  preview/SHA-159-v1  preview/SHA-160-v1
preview/SHA-161-v1  preview/SHA-163-v1  preview/SHA-164-v1  preview/SHA-173-v1  preview/SHA-176-v1
preview/SHA-18-v1   preview/SHA-19-v1   preview/SHA-20-v1   preview/SHA-201-v1  preview/SHA-202-v1
preview/SHA-231-v1  preview/SHA-232-v1  preview/SHA-235-v1  preview/SHA-236-v1  preview/SHA-237-v1
preview/SHA-238-v1  preview/SHA-239-v1  preview/SHA-24-v1   preview/SHA-240-v1  preview/SHA-241-v1
preview/SHA-242-v1  preview/SHA-243-v1  preview/SHA-244-v1  preview/SHA-26-v1   preview/SHA-28-v1
preview/SHA-29-v1   preview/SHA-30-v1   preview/SHA-31-v1   preview/SHA-33-v1   preview/SHA-37-v1
preview/SHA-38-v1   preview/SHA-44-v1   preview/SHA-47-v1   preview/SHA-48-v1   preview/SHA-50-v1
preview/SHA-51-v1   preview/SHA-55-v1   preview/SHA-56-v1   preview/SHA-57-v1   preview/SHA-58-v2
preview/SHA-64-v1   preview/SHA-65-v1   preview/SHA-66-v1   preview/SHA-71-v1   preview/SHA-72-v1
preview/SHA-73-v1   preview/SHA-74-v1   preview/SHA-75-v1   preview/SHA-76-v1   preview/SHA-81-v1
preview/SHA-83-v1   preview/SHA-84-v1   preview/SHA-85-v1   preview/SHA-86-v1   preview/SHA-87-v1
preview/SHA-88-v1   preview/SHA-89-v1   preview/SHA-91-v1   preview/SHA-92-v1   preview/SHA-93-v1
preview/SHA-94-v1   preview/SHA-95-v1   preview/SHA-96-v1   preview/SHA-97-v1   preview/SHA-98-v1
preview/SHA-99-v1
```

One-liner to delete them all once a session has delete access:

```bash
cd AI-Workspace
git fetch origin --prune
git push origin --delete \
  preview/SHA-100-v1 preview/SHA-101-v1 preview/SHA-102-v1 preview/SHA-103-v1 preview/SHA-104-v1 \
  preview/SHA-115-v1 preview/SHA-116-v1 preview/SHA-117-v1 preview/SHA-123-v1 preview/SHA-124-v1 \
  preview/SHA-125-v1 preview/SHA-126-v1 preview/SHA-128-v1 preview/SHA-129-v1 preview/SHA-130-v1 \
  preview/SHA-131-v1 preview/SHA-132-v1 preview/SHA-133-v1 preview/SHA-134-v1 preview/SHA-135-v1 \
  preview/SHA-138-v1 preview/SHA-139-v1 preview/SHA-140-v1 preview/SHA-141-v1 preview/SHA-142-v1 \
  preview/SHA-143-v1 preview/SHA-144-v1 preview/SHA-145-v1 preview/SHA-147-v1 preview/SHA-148-v1 \
  preview/SHA-149-v1 preview/SHA-152-v1 preview/SHA-158-v1 preview/SHA-159-v1 preview/SHA-160-v1 \
  preview/SHA-161-v1 preview/SHA-163-v1 preview/SHA-164-v1 preview/SHA-173-v1 preview/SHA-176-v1 \
  preview/SHA-18-v1 preview/SHA-19-v1 preview/SHA-20-v1 preview/SHA-201-v1 preview/SHA-202-v1 \
  preview/SHA-231-v1 preview/SHA-232-v1 preview/SHA-235-v1 preview/SHA-236-v1 preview/SHA-237-v1 \
  preview/SHA-238-v1 preview/SHA-239-v1 preview/SHA-24-v1 preview/SHA-240-v1 preview/SHA-241-v1 \
  preview/SHA-242-v1 preview/SHA-243-v1 preview/SHA-244-v1 preview/SHA-26-v1 preview/SHA-28-v1 \
  preview/SHA-29-v1 preview/SHA-30-v1 preview/SHA-31-v1 preview/SHA-33-v1 preview/SHA-37-v1 \
  preview/SHA-38-v1 preview/SHA-44-v1 preview/SHA-47-v1 preview/SHA-48-v1 preview/SHA-50-v1 \
  preview/SHA-51-v1 preview/SHA-55-v1 preview/SHA-56-v1 preview/SHA-57-v1 preview/SHA-58-v2 \
  preview/SHA-64-v1 preview/SHA-65-v1 preview/SHA-66-v1 preview/SHA-71-v1 preview/SHA-72-v1 \
  preview/SHA-73-v1 preview/SHA-74-v1 preview/SHA-75-v1 preview/SHA-76-v1 preview/SHA-81-v1 \
  preview/SHA-83-v1 preview/SHA-84-v1 preview/SHA-85-v1 preview/SHA-86-v1 preview/SHA-87-v1 \
  preview/SHA-88-v1 preview/SHA-89-v1 preview/SHA-91-v1 preview/SHA-92-v1 preview/SHA-93-v1 \
  preview/SHA-94-v1 preview/SHA-95-v1 preview/SHA-96-v1 preview/SHA-97-v1 preview/SHA-98-v1 \
  preview/SHA-99-v1
```

The 4 unrecognized (lowercase / non-versioned) branches were intentionally left untouched, matching the
script's own behavior — they need a human decision, not an automated one:
`preview/SHA-25-build`, `preview/sha-169-v1`, `preview/sha-170-v1`, `preview/sha-171-v1`.

## Instructions for receiving agent

1. Re-verify branch state hasn't changed (`git fetch origin --prune && git branch -r | grep preview`) —
   if new preview branches were pushed since 2026-07-27, re-run
   `bash scripts/cleanup-preview-branches.sh --dry-run` (needs `LINEAR_API_KEY`) instead of blindly
   reusing the list above.
2. Run the one-liner above (or the script itself, if `LINEAR_API_KEY` is available in your session) to
   delete the 101 branches.
3. Delete this handover file once done — the work is complete and tracked in git history from here.
4. Do not touch `main` or the 4 unrecognized branches listed above.

## Related, same root cause: `data/routine-log.json` not regenerated

The idea-sweep routine's Output section also calls for
`node scripts/generate-routine-log.mjs` after the ledger append, to refresh the sandbox
dashboard at `/routine-log.html`. That script also requires `LINEAR_API_KEY` (not just
for branch cleanup — it queries Linear directly) and is not set in this session, so it
was not run this cycle. `data/sweep-runs.jsonl` **was** updated (the ledger append does
not need Linear access), so a future run with `LINEAR_API_KEY` set just needs:

```bash
cd AI-Workspace
LINEAR_API_KEY=... node scripts/generate-routine-log.mjs
git add data/routine-log.json && git commit -m "Refresh routine-log.json" && git push
```
