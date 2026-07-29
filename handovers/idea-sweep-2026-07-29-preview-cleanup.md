# Handover: Preview-branch cleanup computed but not pushed (git delete blocked)

**For:** Any agent/session with unrestricted push access to `rohrasharad-ship-it/AI-Workspace` (or the weekly `preview-branch-cleanup.yml` GitHub Action, which already has this covered as a structural backup)
**From:** idea-sweep routine (spec-drift step 11), Application Agent cycle, 2026-07-29
**Blocked by:** `git push origin --delete <branch>` returned `HTTP 403` from this session's git remote (both single-branch and batched attempts) — this session's write scope appears limited to its own designated branch (`claude/festive-goodall-x8yqq2`). No GitHub MCP tool exposes a raw delete-ref call as an alternative path.
**Action:** Delete the 104 orphaned `preview/*` branches listed below from `rohrasharad-ship-it/AI-Workspace`.
**Issue:** N/A — this is routine infrastructure housekeeping (`agents/spec-drift.md` step 11), not tied to a single Linear issue.

## Payload

Computed by replicating `scripts/cleanup-preview-branches.sh`'s `should_delete_branch` logic
against a fresh `list_issues` pull (all issues, all projects, team `SHA`) instead of the
script's own Linear GraphQL calls (no `LINEAR_API_KEY` was available in this session either —
that's a second, independent blocker for running the script as-is).

- **118** `preview/*` branches existed at run time.
- **104** are orphaned (issue is `Done`/`Canceled`/`Duplicate`, or no longer labeled `spec-needed`) → delete.
- **13** belong to issues still `Backlog` + `spec-needed` → keep (SHA-251 through SHA-264, see below).
- **1** (`preview/SHA-25-build`) doesn't match the `preview/<ISSUE-ID>-v<n>` naming convention → left alone, same as the script would.

### Delete (104)

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
preview/SHA-99-v1   preview/sha-169-v1  preview/sha-170-v1  preview/sha-171-v1
```

### Keep (13 — still `Backlog` + `spec-needed`)

`preview/SHA-251-v1`, `SHA-252-v1`, `SHA-253-v1`, `SHA-254-v1`, `SHA-255-v1`, `SHA-256-v1`,
`SHA-258-v1`, `SHA-259-v1`, `SHA-260-v1`, `SHA-261-v1`, `SHA-262-v1`, `SHA-263-v1`, `SHA-264-v1`

## Instructions for receiving agent

1. Confirm `LINEAR_API_KEY` is set, then run the real script for a fresh, authoritative pass:
   ```bash
   cd AI-Workspace
   export LINEAR_API_KEY=...
   bash scripts/cleanup-preview-branches.sh --dry-run   # sanity-check against this payload
   bash scripts/cleanup-preview-branches.sh             # deletes for real
   ```
   The payload above is a point-in-time snapshot (2026-07-29) — some of the "keep" issues may have
   moved on by the time this runs, so trust the script's live Linear lookup over this list if they
   disagree.
2. If the weekly `.github/workflows/preview-branch-cleanup.yml` Action already ran since
   2026-07-29 and cleared these, this handover is stale — delete this file.
3. Do not delete anything outside the `preview/<ISSUE-ID>-v<n>` pattern (skip
   `preview/SHA-25-build`, matching the script's own behavior).
