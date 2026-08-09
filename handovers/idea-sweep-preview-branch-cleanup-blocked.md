# Handover: idea-sweep preview-branch cleanup could not delete branches (no ref-delete permission)

**For:** Any agent/session with `git push origin --delete` or a GitHub ref-delete
capability against `rohrasharad-ship-it/AI-Workspace`
**From:** idea-sweep routine (spec-drift step 11, orchestrating session), triggered
for AI Landscape, 2026-08-09
**Blocked by:** `git push origin --delete <branch>` returns `HTTP 403` for this
session's GitHub credential, even for a branch the same session just created
itself two minutes earlier (confirmed not a stale/protected-branch issue —
normal branch creation and content pushes succeed fine, only ref deletion is
rejected). No GitHub MCP tool in this session's toolset exposes branch/ref
deletion either (`create_branch` exists; there is no `delete_branch`).
**Action:** Delete the 101 orphaned `preview/*` branches listed below from
`rohrasharad-ship-it/AI-Workspace`, computed by replicating
`scripts/cleanup-preview-branches.sh`'s exact logic (older-version-than-latest,
or Linear issue state is `completed`/`canceled`/`duplicate`, or issue no
longer labeled `spec-needed`) against a full Linear workspace issue dump.
`scripts/cleanup-preview-branches.sh` itself could not be run this session
either — `LINEAR_API_KEY` is not present in this session's environment.
**Issue:** N/A — this is routine housekeeping (`idea-sweep` → spec-drift step 11
for AI Landscape), not tied to a single Linear issue.

## Payload

Run (from a session with real delete access):

```bash
cd AI-Workspace
git fetch origin --prune
while read -r b; do git push origin --delete "$b"; done < delete-list.txt
```

Where `delete-list.txt` contains exactly these 101 branches (verified against
Linear issue state as of 2026-08-09):

```
preview/SHA-100-v1
preview/SHA-101-v1
preview/SHA-102-v1
preview/SHA-103-v1
preview/SHA-104-v1
preview/SHA-115-v1
preview/SHA-116-v1
preview/SHA-117-v1
preview/SHA-123-v1
preview/SHA-124-v1
preview/SHA-125-v1
preview/SHA-126-v1
preview/SHA-128-v1
preview/SHA-129-v1
preview/SHA-130-v1
preview/SHA-131-v1
preview/SHA-132-v1
preview/SHA-133-v1
preview/SHA-134-v1
preview/SHA-135-v1
preview/SHA-138-v1
preview/SHA-139-v1
preview/SHA-140-v1
preview/SHA-141-v1
preview/SHA-142-v1
preview/SHA-143-v1
preview/SHA-144-v1
preview/SHA-145-v1
preview/SHA-147-v1
preview/SHA-148-v1
preview/SHA-149-v1
preview/SHA-152-v1
preview/SHA-158-v1
preview/SHA-159-v1
preview/SHA-160-v1
preview/SHA-161-v1
preview/SHA-163-v1
preview/SHA-164-v1
preview/SHA-173-v1
preview/SHA-176-v1
preview/SHA-18-v1
preview/SHA-19-v1
preview/SHA-20-v1
preview/SHA-201-v1
preview/SHA-202-v1
preview/SHA-231-v1
preview/SHA-232-v1
preview/SHA-235-v1
preview/SHA-236-v1
preview/SHA-237-v1
preview/SHA-238-v1
preview/SHA-239-v1
preview/SHA-24-v1
preview/SHA-240-v1
preview/SHA-241-v1
preview/SHA-242-v1
preview/SHA-243-v1
preview/SHA-244-v1
preview/SHA-26-v1
preview/SHA-28-v1
preview/SHA-29-v1
preview/SHA-30-v1
preview/SHA-31-v1
preview/SHA-33-v1
preview/SHA-37-v1
preview/SHA-38-v1
preview/SHA-44-v1
preview/SHA-47-v1
preview/SHA-48-v1
preview/SHA-50-v1
preview/SHA-51-v1
preview/SHA-55-v1
preview/SHA-56-v1
preview/SHA-57-v1
preview/SHA-58-v2
preview/SHA-64-v1
preview/SHA-65-v1
preview/SHA-66-v1
preview/SHA-71-v1
preview/SHA-72-v1
preview/SHA-73-v1
preview/SHA-74-v1
preview/SHA-75-v1
preview/SHA-76-v1
preview/SHA-81-v1
preview/SHA-83-v1
preview/SHA-84-v1
preview/SHA-85-v1
preview/SHA-86-v1
preview/SHA-87-v1
preview/SHA-88-v1
preview/SHA-89-v1
preview/SHA-91-v1
preview/SHA-92-v1
preview/SHA-93-v1
preview/SHA-94-v1
preview/SHA-95-v1
preview/SHA-96-v1
preview/SHA-97-v1
preview/SHA-98-v1
preview/SHA-99-v1
```

**Also clean up:** `test-push-probe-delete-me` — a throwaway empty-commit
branch this session pushed to confirm push-vs-delete behavior differs (push
succeeded, delete of this same branch also 403'd). Harmless but should be
deleted alongside the above.

**Branches kept (verified still `spec-needed`, do not delete):**
`preview/SHA-251-v1`, `SHA-252-v1`, `SHA-253-v1`, `SHA-254-v1`, `SHA-255-v1`,
`SHA-256-v1`, `SHA-258-v1`, `SHA-259-v1`, `SHA-260-v1`, `SHA-261-v1`,
`SHA-262-v1`, `SHA-263-v1`, `SHA-264-v1`, `SHA-265-v1`, `SHA-267-v1`,
`SHA-268-v1`, `SHA-269-v1`, `SHA-270-v1`, `SHA-271-v1`, `SHA-272-v1`.

**Skipped, not evaluated (branch name doesn't match the script's
`preview/[A-Z]+-[0-9]+-v[0-9]+` pattern):** `preview/SHA-25-build`,
`preview/sha-169-v1`, `preview/sha-170-v1`, `preview/sha-171-v1` (lowercase
`sha-` prefix). Same behavior as the shell script — left untouched
deliberately, not a bug in this analysis.

## Instructions for receiving agent

1. Confirm your session's git/GitHub credential can actually delete a ref
   (try one branch first, e.g. `test-push-probe-delete-me`, before the batch).
2. If `LINEAR_API_KEY` is available, prefer just running
   `bash scripts/cleanup-preview-branches.sh` fresh rather than trusting this
   list blindly — Linear state may have moved since 2026-08-09. If not
   available, the list above is a faithful snapshot; recheck any issue you're
   unsure about with the Linear MCP before deleting.
3. Delete the 101 branches (plus the probe branch) with
   `git push origin --delete <branch>`.
4. Delete this handover file once done — its job is finished as soon as the
   branches are gone.
5. Do not touch `main` or any branch not listed above.
