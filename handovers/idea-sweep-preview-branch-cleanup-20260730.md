# Handover: Delete 101 orphaned preview/* branches (idea-sweep housekeeping)

**For:** Any agent with unrestricted git push access to `rohrasharad-ship-it/AI-Workspace` (or a `delete_branch`/ref-delete capable GitHub token)
**From:** idea-sweep routine (spec-drift step 11, AI Landscape project run), 2026-07-30
**Blocked by:** This session's git remote is restricted to pushing only the designated `claude/*` feature branch — `git push origin --delete preview/<x>` returns `HTTP 403` from the proxy for every `preview/*` branch. The GitHub MCP server exposes no branch/ref-delete tool (only `delete_file`, which deletes file content, not refs).
**Action:** Run `bash scripts/cleanup-preview-branches.sh` for real (with `LINEAR_API_KEY` set), or delete exactly the branches listed below.
**Issue:** Not tied to a single Linear issue — this is the `idea-sweep` routine's `agents/spec-drift.md` step 11 (preview-branch housekeeping), run for the **AI Landscape** project per `routines/idea-sweep.md`.

## Payload

I could not run `scripts/cleanup-preview-branches.sh` directly (no `LINEAR_API_KEY` secret in this session either), so I replicated its exact logic by hand:

1. Listed all `origin/preview/*` branches (122 total, via `git ls-remote`/`list_branches`).
2. Listed every issue in the workspace's Linear team (`SHA-1` .. `SHA-269`, paginated `list_issues`, 250/page) with `status`, `statusType`, `labels`.
3. Applied the script's rule per branch: delete if (a) it's an older version than the max `-v<n>` for that issue, or (b) the issue's `statusType` is `completed`/`canceled`/`duplicate`, or (c) the issue no longer carries the `spec-needed` label. Otherwise keep.

Result — **101 branches to delete**, **17 to keep**, **4 unrecognized (skip, matches script behavior)**.

### Delete (101) — issue is Done/Canceled/Duplicate, safe per script logic
```
preview/SHA-18-v1  preview/SHA-19-v1  preview/SHA-20-v1  preview/SHA-24-v1  preview/SHA-26-v1
preview/SHA-28-v1  preview/SHA-29-v1  preview/SHA-30-v1  preview/SHA-31-v1  preview/SHA-33-v1
preview/SHA-37-v1  preview/SHA-38-v1  preview/SHA-44-v1  preview/SHA-47-v1  preview/SHA-48-v1
preview/SHA-50-v1  preview/SHA-51-v1  preview/SHA-55-v1  preview/SHA-56-v1  preview/SHA-57-v1
preview/SHA-58-v2  preview/SHA-64-v1  preview/SHA-65-v1  preview/SHA-66-v1  preview/SHA-71-v1
preview/SHA-72-v1  preview/SHA-73-v1  preview/SHA-74-v1  preview/SHA-75-v1  preview/SHA-76-v1
preview/SHA-81-v1  preview/SHA-83-v1  preview/SHA-84-v1  preview/SHA-85-v1  preview/SHA-86-v1
preview/SHA-87-v1  preview/SHA-88-v1  preview/SHA-89-v1  preview/SHA-91-v1  preview/SHA-92-v1
preview/SHA-93-v1  preview/SHA-94-v1  preview/SHA-95-v1  preview/SHA-96-v1  preview/SHA-97-v1
preview/SHA-98-v1  preview/SHA-99-v1  preview/SHA-100-v1 preview/SHA-101-v1 preview/SHA-102-v1
preview/SHA-103-v1 preview/SHA-104-v1 preview/SHA-115-v1 preview/SHA-116-v1 preview/SHA-117-v1
preview/SHA-123-v1 preview/SHA-124-v1 preview/SHA-125-v1 preview/SHA-126-v1 preview/SHA-128-v1
preview/SHA-129-v1 preview/SHA-130-v1 preview/SHA-131-v1 preview/SHA-132-v1 preview/SHA-133-v1
preview/SHA-134-v1 preview/SHA-135-v1 preview/SHA-138-v1 preview/SHA-139-v1 preview/SHA-140-v1
preview/SHA-141-v1 preview/SHA-142-v1 preview/SHA-143-v1 preview/SHA-144-v1 preview/SHA-145-v1
preview/SHA-147-v1 preview/SHA-148-v1 preview/SHA-149-v1 preview/SHA-152-v1 preview/SHA-158-v1
preview/SHA-159-v1 preview/SHA-160-v1 preview/SHA-161-v1 preview/SHA-163-v1 preview/SHA-164-v1
preview/SHA-173-v1 preview/SHA-176-v1 preview/SHA-201-v1 preview/SHA-202-v1 preview/SHA-231-v1
preview/SHA-232-v1 preview/SHA-235-v1 preview/SHA-236-v1 preview/SHA-237-v1 preview/SHA-238-v1
preview/SHA-239-v1 preview/SHA-240-v1 preview/SHA-241-v1 preview/SHA-242-v1 preview/SHA-243-v1
preview/SHA-244-v1
```

### Keep — issue still Backlog + spec-needed (do NOT delete)
```
preview/SHA-251-v1 preview/SHA-252-v1 preview/SHA-253-v1 preview/SHA-254-v1 preview/SHA-255-v1
preview/SHA-256-v1 preview/SHA-258-v1 preview/SHA-259-v1 preview/SHA-260-v1 preview/SHA-261-v1
preview/SHA-262-v1 preview/SHA-263-v1 preview/SHA-264-v1 preview/SHA-265-v1 preview/SHA-267-v1
preview/SHA-268-v1 preview/SHA-269-v1
```

### Skip — unrecognized branch name (script would also skip these; not this handover's concern)
```
preview/SHA-25-build  preview/sha-169-v1  preview/sha-170-v1  preview/sha-171-v1
```

## Instructions for receiving agent

1. Get a git remote/session with real push access to `rohrasharad-ship-it/AI-Workspace` (not restricted to a single designated branch), or a GitHub token capable of ref deletion.
2. Preferred: just run `bash scripts/cleanup-preview-branches.sh` with `LINEAR_API_KEY` set — it will re-derive the same result live and is more current than this snapshot if issue states changed since 2026-07-30.
3. If running the script isn't convenient, `git push origin --delete <branch>` for each branch in the **Delete** list above only. Do not touch **Keep** or **Skip** branches.
4. Do not touch `main` or any non-`preview/*` branch.
5. Delete this handover file once the cleanup is done.
