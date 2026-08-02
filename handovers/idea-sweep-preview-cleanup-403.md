# Handover: Preview-branch cleanup blocked — no branch-delete permission this session

**For:** Any agent/session with full push access to `rohrasharad-ship-it/AI-Workspace` (able to run `git push origin --delete <branch>` successfully, or an equivalent GitHub API/MCP branch-delete call)
**From:** idea-sweep routine (spec-drift step 11, Usercon run), 2026-08-02
**Blocked by:** Two independent paths both failed:
1. `scripts/cleanup-preview-branches.sh` requires `LINEAR_API_KEY` in the environment — not set in this session.
2. Manual `git push origin --delete preview/<id>-v1` (replicating the script's own logic against Linear issue state fetched via the Linear MCP tool) returned `HTTP 403` on every single branch tested (101/101), including a bare confirmation retry. This session's git push scope appears restricted to its own designated feature branch (`claude/magical-fermat-39wnqo`), not arbitrary branch deletion. (Two other branches already in the repo, `test-push-permission-check` and `test-push-scope-check`, suggest this exact limitation was hit and probed before.)

**Action:** Delete the 101 orphaned `preview/*` branches listed below (all confirmed via the same logic `scripts/cleanup-preview-branches.sh` uses: issue state is Done/Canceled/Duplicate, or no longer labeled `spec-needed`). Then re-run `bash scripts/cleanup-preview-branches.sh --dry-run` (with `LINEAR_API_KEY` set) to confirm zero remaining orphans, or just spot check.

**Issue:** No single Linear issue — this was the housekeeping step of a routine `idea-sweep` run for Usercon (all 5 Usercon Backlog issues are at cap; see `data/sweep-runs.jsonl` entry for this run).

## Payload — branches to delete

All confirmed via Linear MCP `list_issues` (full workspace pull, 2026-08-02) cross-referenced against `git branch -r --list 'origin/preview/*'`. Each maps to an issue that is `Done`/`Canceled`/`Duplicate`, or no longer carries `spec-needed`:

```
preview/SHA-100-v1 preview/SHA-101-v1 preview/SHA-102-v1 preview/SHA-103-v1 preview/SHA-104-v1
preview/SHA-115-v1 preview/SHA-116-v1 preview/SHA-117-v1 preview/SHA-123-v1 preview/SHA-124-v1
preview/SHA-125-v1 preview/SHA-126-v1 preview/SHA-128-v1 preview/SHA-129-v1 preview/SHA-130-v1
preview/SHA-131-v1 preview/SHA-132-v1 preview/SHA-133-v1 preview/SHA-134-v1 preview/SHA-135-v1
preview/SHA-138-v1 preview/SHA-139-v1 preview/SHA-140-v1 preview/SHA-141-v1 preview/SHA-142-v1
preview/SHA-143-v1 preview/SHA-144-v1 preview/SHA-145-v1 preview/SHA-147-v1 preview/SHA-148-v1
preview/SHA-149-v1 preview/SHA-152-v1 preview/SHA-158-v1 preview/SHA-159-v1 preview/SHA-160-v1
preview/SHA-161-v1 preview/SHA-163-v1 preview/SHA-164-v1 preview/SHA-173-v1 preview/SHA-176-v1
preview/SHA-18-v1  preview/SHA-19-v1  preview/SHA-20-v1  preview/SHA-201-v1 preview/SHA-202-v1
preview/SHA-231-v1 preview/SHA-232-v1 preview/SHA-235-v1 preview/SHA-236-v1 preview/SHA-237-v1
preview/SHA-238-v1 preview/SHA-239-v1 preview/SHA-24-v1  preview/SHA-240-v1 preview/SHA-241-v1
preview/SHA-242-v1 preview/SHA-243-v1 preview/SHA-244-v1 preview/SHA-26-v1  preview/SHA-28-v1
preview/SHA-29-v1  preview/SHA-30-v1  preview/SHA-31-v1  preview/SHA-33-v1  preview/SHA-37-v1
preview/SHA-38-v1  preview/SHA-44-v1  preview/SHA-47-v1  preview/SHA-48-v1  preview/SHA-50-v1
preview/SHA-51-v1  preview/SHA-55-v1  preview/SHA-56-v1  preview/SHA-57-v1  preview/SHA-58-v2
preview/SHA-64-v1  preview/SHA-65-v1  preview/SHA-66-v1  preview/SHA-71-v1  preview/SHA-72-v1
preview/SHA-73-v1  preview/SHA-74-v1  preview/SHA-75-v1  preview/SHA-76-v1  preview/SHA-81-v1
preview/SHA-83-v1  preview/SHA-84-v1  preview/SHA-85-v1  preview/SHA-86-v1  preview/SHA-87-v1
preview/SHA-88-v1  preview/SHA-89-v1  preview/SHA-91-v1  preview/SHA-92-v1  preview/SHA-93-v1
preview/SHA-94-v1  preview/SHA-95-v1  preview/SHA-96-v1  preview/SHA-97-v1  preview/SHA-98-v1
preview/SHA-99-v1
```

**Do NOT delete these** — they map to still-open `Backlog` + `spec-needed` issues:
`preview/SHA-251-v1 SHA-252-v1 SHA-253-v1 SHA-254-v1 SHA-255-v1 SHA-256-v1 SHA-258-v1 SHA-259-v1 SHA-260-v1 SHA-261-v1 SHA-262-v1 SHA-263-v1 SHA-264-v1 SHA-265-v1 SHA-267-v1 SHA-268-v1 SHA-269-v1 SHA-270-v1 SHA-271-v1 SHA-272-v1`

**Also skipped (unrecognized by the script's naming regex, same as the script would do — not evaluated):** `preview/SHA-25-build`, `preview/sha-169-v1`, `preview/sha-170-v1`, `preview/sha-171-v1` (lowercase team key doesn't match `^preview/([A-Z]+-[0-9]+)-v([0-9]+)$`).

## Instructions for receiving agent

1. Get proper push/delete access to `rohrasharad-ship-it/AI-Workspace` (or `LINEAR_API_KEY` + normal git push access to run the real script).
2. Preferred: just run `bash scripts/cleanup-preview-branches.sh` with `LINEAR_API_KEY` exported — it will recompute from live Linear state and is more current than this snapshot. Compare its delete list against the payload above as a sanity check.
3. Fallback: `git push origin --delete <branch>` for each branch in the delete list above, one at a time (never a wildcard).
4. Do not touch `main` or any non-`preview/*` branch.
5. Delete this handover file once done.
