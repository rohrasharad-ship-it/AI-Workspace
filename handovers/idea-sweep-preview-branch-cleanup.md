# Handover: Preview-branch cleanup blocked — no branch-delete access in this session

**For:** Any agent/session with `git push --delete` or branch-delete API access to `rohrasharad-ship-it/AI-Workspace`
**From:** idea-sweep routine (spec-drift step 11, housekeeping), Application Agent project, 2026-07-23
**Blocked by:** This session has read-only git access to AI-Workspace (git push over the proxy returns HTTP 403) and no `LINEAR_API_KEY` secret, so `scripts/cleanup-preview-branches.sh` cannot run directly. The GitHub MCP server also exposes no branch-delete tool, and raw GitHub REST DELETE calls are blocked by the sandbox proxy ("Write access to this GitHub API path is not permitted through this proxy").
**Action:** Delete the 87 orphaned `preview/*` branches listed below from `rohrasharad-ship-it/AI-Workspace`. Do not touch the 4 branches listed as "keep" or the 4 listed as "unrecognized naming" (leave those for a future run of the real script).
**Issue:** N/A — this is the repo-wide preview-branch housekeeping step (`agents/spec-drift.md` step 11), not tied to a single Linear issue.

## Payload

I could not run `scripts/cleanup-preview-branches.sh` itself (no `LINEAR_API_KEY`), so I reproduced its exact logic by hand using the Linear MCP `list_issues` tool (paginated the full workspace, 228 issues, single page) cross-referenced against `git branch -r --list 'origin/preview/*'` (95 branches) in a local clone of AI-Workspace. Same decision rules as the script: delete if a newer version branch exists for the same issue, or if the issue's `statusType` is `completed`/`canceled`/`duplicate`, or if the issue no longer carries the `spec-needed` label.

### Branches to DELETE (87) — reason in parentheses

```
preview/SHA-100-v1 (issue state is completed (Done))
preview/SHA-101-v1 (issue state is canceled (Canceled))
preview/SHA-102-v1 (issue state is canceled (Canceled))
preview/SHA-103-v1 (issue state is completed (Done))
preview/SHA-104-v1 (issue state is canceled (Canceled))
preview/SHA-115-v1 (issue state is completed (Done))
preview/SHA-116-v1 (issue state is completed (Done))
preview/SHA-117-v1 (issue state is completed (Done))
preview/SHA-123-v1 (issue state is canceled (Canceled))
preview/SHA-124-v1 (issue state is canceled (Canceled))
preview/SHA-125-v1 (issue state is canceled (Canceled))
preview/SHA-126-v1 (issue state is duplicate (Duplicate))
preview/SHA-128-v1 (issue state is duplicate (Duplicate))
preview/SHA-129-v1 (issue state is duplicate (Duplicate))
preview/SHA-130-v1 (issue state is duplicate (Duplicate))
preview/SHA-131-v1 (issue state is duplicate (Duplicate))
preview/SHA-132-v1 (issue state is duplicate (Duplicate))
preview/SHA-133-v1 (issue state is duplicate (Duplicate))
preview/SHA-134-v1 (issue state is duplicate (Duplicate))
preview/SHA-135-v1 (issue state is canceled (Canceled))
preview/SHA-138-v1 (issue state is completed (Done))
preview/SHA-139-v1 (issue state is completed (Done))
preview/SHA-140-v1 (issue state is completed (Done))
preview/SHA-141-v1 (issue state is canceled (Canceled))
preview/SHA-142-v1 (issue state is canceled (Canceled))
preview/SHA-143-v1 (issue state is completed (Done))
preview/SHA-144-v1 (issue state is canceled (Canceled))
preview/SHA-145-v1 (issue state is canceled (Canceled))
preview/SHA-147-v1 (issue state is canceled (Canceled))
preview/SHA-148-v1 (issue state is canceled (Canceled))
preview/SHA-149-v1 (issue state is canceled (Canceled))
preview/SHA-152-v1 (issue state is canceled (Canceled))
preview/SHA-158-v1 (issue state is canceled (Canceled))
preview/SHA-159-v1 (issue state is canceled (Canceled))
preview/SHA-160-v1 (issue state is canceled (Canceled))
preview/SHA-161-v1 (issue state is canceled (Canceled))
preview/SHA-163-v1 (issue state is canceled (Canceled))
preview/SHA-164-v1 (issue state is canceled (Canceled))
preview/SHA-173-v1 (issue state is completed (Done))
preview/SHA-176-v1 (issue state is canceled (Canceled))
preview/SHA-18-v1 (issue state is canceled (Canceled))
preview/SHA-19-v1 (issue state is canceled (Canceled))
preview/SHA-20-v1 (issue state is canceled (Canceled))
preview/SHA-201-v1 (issue state is canceled (Canceled))
preview/SHA-202-v1 (issue state is canceled (Canceled))
preview/SHA-24-v1 (issue state is canceled (Canceled))
preview/SHA-26-v1 (issue state is canceled (Canceled))
preview/SHA-28-v1 (issue state is canceled (Canceled))
preview/SHA-29-v1 (issue state is completed (Done))
preview/SHA-31-v1 (issue state is canceled (Canceled))
preview/SHA-33-v1 (issue state is completed (Done))
preview/SHA-37-v1 (issue state is canceled (Canceled))
preview/SHA-38-v1 (issue state is canceled (Canceled))
preview/SHA-44-v1 (issue state is completed (Done))
preview/SHA-47-v1 (issue state is canceled (Canceled))
preview/SHA-48-v1 (issue state is canceled (Canceled))
preview/SHA-50-v1 (issue state is canceled (Canceled))
preview/SHA-51-v1 (issue state is canceled (Canceled))
preview/SHA-55-v1 (issue state is canceled (Canceled))
preview/SHA-56-v1 (issue state is canceled (Canceled))
preview/SHA-57-v1 (issue state is canceled (Canceled))
preview/SHA-58-v2 (issue state is canceled (Canceled))
preview/SHA-64-v1 (issue state is completed (Done))
preview/SHA-66-v1 (issue state is canceled (Canceled))
preview/SHA-71-v1 (issue state is canceled (Canceled))
preview/SHA-72-v1 (issue state is completed (Done))
preview/SHA-73-v1 (issue state is canceled (Canceled))
preview/SHA-74-v1 (issue state is completed (Done))
preview/SHA-75-v1 (issue state is completed (Done))
preview/SHA-76-v1 (issue state is completed (Done))
preview/SHA-81-v1 (issue state is completed (Done))
preview/SHA-83-v1 (issue state is canceled (Canceled))
preview/SHA-84-v1 (issue state is canceled (Canceled))
preview/SHA-85-v1 (issue state is canceled (Canceled))
preview/SHA-86-v1 (issue state is canceled (Canceled))
preview/SHA-87-v1 (issue state is canceled (Canceled))
preview/SHA-88-v1 (issue state is canceled (Canceled))
preview/SHA-89-v1 (issue state is canceled (Canceled))
preview/SHA-91-v1 (issue state is canceled (Canceled))
preview/SHA-92-v1 (issue state is canceled (Canceled))
preview/SHA-93-v1 (issue state is canceled (Canceled))
preview/SHA-94-v1 (issue state is canceled (Canceled))
preview/SHA-95-v1 (issue state is canceled (Canceled))
preview/SHA-96-v1 (issue state is completed (Done))
preview/SHA-97-v1 (issue state is canceled (Canceled))
preview/SHA-98-v1 (issue state is canceled (Canceled))
preview/SHA-99-v1 (issue state is canceled (Canceled))
```

### Branches to KEEP (4) — still `spec-needed`, do not delete

```
preview/SHA-30-v1  (Todo)
preview/SHA-42-v2  (Todo)
preview/SHA-43-v1  (Todo)
preview/SHA-65-v1  (Todo)
```

### Branches SKIPPED — unrecognized naming (script would also skip these; needs a human/manual look, not an automatic delete)

```
preview/SHA-25-build   (doesn't match preview/<ISSUE-ID>-v<n>)
preview/sha-169-v1     (lowercase issue id, regex requires uppercase)
preview/sha-170-v1
preview/sha-171-v1
```

## Instructions for receiving agent

1. `cd` into a working clone of `rohrasharad-ship-it/AI-Workspace` with push access (or use `git push origin --delete <branch>` directly if your session's git credentials have write scope — mine didn't).
2. For each branch under "Branches to DELETE" above, run exactly:
   ```
   git push origin --delete <branch-name>
   ```
   Fully-qualified `preview/*` names only — never a bare or wildcard delete, per `agents/shared/visual-specs.md` branch-safety rule.
3. Do **not** delete anything under "Branches to KEEP" or "SKIPPED — unrecognized naming".
4. Optionally re-run `bash scripts/cleanup-preview-branches.sh --dry-run` afterward (with `LINEAR_API_KEY` set) to confirm the tree now matches — it should report 0 more deletions and only the skip/keep set remaining.
5. Delete this handover file once the deletes are done — this data goes stale immediately after.
