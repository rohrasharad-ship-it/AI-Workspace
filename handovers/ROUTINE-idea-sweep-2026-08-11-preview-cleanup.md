# Handover: Preview-branch cleanup blocked — no branch-delete access this session

**For:** Any agent/session with `git push origin --delete` access to `rohrasharad-ship-it/AI-Workspace` (or repo-admin GitHub API access for ref deletion)
**From:** idea-sweep routine (spec-drift step 11, housekeeping), triggered for AI Landscape, 2026-08-11
**Blocked by:** This session's GitHub write access goes through the GitHub MCP server only. There is no `delete_branch`/ref-deletion MCP tool, and raw `git push origin --delete <branch>` over HTTPS fails with `403` (RPC failed) even though other git/MCP writes (e.g. `create_branch`, `create_or_update_file`) succeed — branch/ref deletion specifically appears to be blocked at the proxy/token level for this session.
**Action:** Run `bash scripts/cleanup-preview-branches.sh` for real (with `LINEAR_API_KEY` set), or manually run `git push origin --delete <branch>` for each branch in the **Delete list** below, from an environment with real delete access.
**Issue:** Not tied to a single Linear issue — this is the shared preview-branch housekeeping step (`agents/spec-drift.md` step 11) that runs as part of every `idea-sweep` routine call, currently triggered from the AI Landscape project run.

## Payload

This session recomputed `scripts/cleanup-preview-branches.sh`'s logic by hand (Linear MCP `list_issues` across the whole workspace, paginated, cross-referenced against every `preview/*` branch in `AI-Workspace`), since the script itself needs `LINEAR_API_KEY` which isn't set in this session's environment. The computed plan should be equivalent to what the script would produce — but re-running the actual script (or at minimum re-verifying against current Linear state, since issue states may have moved since this was computed) is the safer path given how large this batch is.

- Total `preview/*` branches found: 125
- Recognized `preview/<ISSUE-ID>-v<n>` pattern: 121
- Unrecognized names (left alone, need manual look if ever cleaned up): `preview/SHA-25-build`, `preview/sha-169-v1`, `preview/sha-170-v1`, `preview/sha-171-v1` (lowercase `sha-` prefix, don't match the script's branch-name regex)
- **To delete: 101** (issue is Done/Canceled/Duplicate, no longer `spec-needed`, or an older version than the latest branch for that issue)
- **To keep: 20** (issue still Backlog/Todo/In Progress/In Review + still labeled `spec-needed`)

### Keep list (do NOT delete these — active spec-needed issues, across all projects)

```
preview/SHA-251-v1  preview/SHA-252-v1  preview/SHA-253-v1  preview/SHA-254-v1
preview/SHA-255-v1  preview/SHA-256-v1  preview/SHA-258-v1  preview/SHA-259-v1
preview/SHA-260-v1  preview/SHA-261-v1  preview/SHA-262-v1  preview/SHA-263-v1
preview/SHA-264-v1  preview/SHA-265-v1  preview/SHA-267-v1  preview/SHA-268-v1
preview/SHA-269-v1  preview/SHA-270-v1  preview/SHA-271-v1  preview/SHA-272-v1
```

### Delete list (101 branches — issue is Done/Canceled/Duplicate, or no longer spec-needed)

```
preview/SHA-100-v1  preview/SHA-101-v1  preview/SHA-102-v1  preview/SHA-103-v1
preview/SHA-104-v1  preview/SHA-115-v1  preview/SHA-116-v1  preview/SHA-117-v1
preview/SHA-123-v1  preview/SHA-124-v1  preview/SHA-125-v1  preview/SHA-126-v1
preview/SHA-128-v1  preview/SHA-129-v1  preview/SHA-130-v1  preview/SHA-131-v1
preview/SHA-132-v1  preview/SHA-133-v1  preview/SHA-134-v1  preview/SHA-135-v1
preview/SHA-138-v1  preview/SHA-139-v1  preview/SHA-140-v1  preview/SHA-141-v1
preview/SHA-142-v1  preview/SHA-143-v1  preview/SHA-144-v1  preview/SHA-145-v1
preview/SHA-147-v1  preview/SHA-148-v1  preview/SHA-149-v1  preview/SHA-152-v1
preview/SHA-158-v1  preview/SHA-159-v1  preview/SHA-160-v1  preview/SHA-161-v1
preview/SHA-163-v1  preview/SHA-164-v1  preview/SHA-173-v1  preview/SHA-176-v1
preview/SHA-18-v1   preview/SHA-19-v1   preview/SHA-20-v1   preview/SHA-201-v1
preview/SHA-202-v1  preview/SHA-231-v1  preview/SHA-232-v1  preview/SHA-235-v1
preview/SHA-236-v1  preview/SHA-237-v1  preview/SHA-238-v1  preview/SHA-239-v1
preview/SHA-24-v1   preview/SHA-240-v1  preview/SHA-241-v1  preview/SHA-242-v1
preview/SHA-243-v1  preview/SHA-244-v1  preview/SHA-26-v1   preview/SHA-28-v1
preview/SHA-29-v1   preview/SHA-30-v1   preview/SHA-31-v1   preview/SHA-33-v1
preview/SHA-37-v1   preview/SHA-38-v1   preview/SHA-44-v1   preview/SHA-47-v1
preview/SHA-48-v1   preview/SHA-50-v1   preview/SHA-51-v1   preview/SHA-55-v1
preview/SHA-56-v1   preview/SHA-57-v1   preview/SHA-58-v2   preview/SHA-64-v1
preview/SHA-65-v1   preview/SHA-66-v1   preview/SHA-71-v1   preview/SHA-72-v1
preview/SHA-73-v1   preview/SHA-74-v1   preview/SHA-75-v1   preview/SHA-76-v1
preview/SHA-81-v1   preview/SHA-83-v1   preview/SHA-84-v1   preview/SHA-85-v1
preview/SHA-86-v1   preview/SHA-87-v1   preview/SHA-88-v1   preview/SHA-89-v1
preview/SHA-91-v1   preview/SHA-92-v1   preview/SHA-93-v1   preview/SHA-94-v1
preview/SHA-95-v1   preview/SHA-96-v1   preview/SHA-97-v1   preview/SHA-98-v1
preview/SHA-99-v1
```

Every branch in the delete list matches `preview/<ISSUE-ID>-v<n>` and was checked against that issue's current Linear state (`completed`/`canceled`/`duplicate` state, or missing the `spec-needed` label, or an older version number than the latest branch for that same issue). None of them are `main` or any non-`preview/*` ref.

## Instructions for receiving agent

1. Re-fetch current Linear state for the issues above before deleting, in case anything changed since 2026-08-11 (states can move between when this was computed and when you run it).
2. Prefer running the real script: `cd AI-Workspace && export LINEAR_API_KEY=... && bash scripts/cleanup-preview-branches.sh --dry-run` first to confirm it reproduces this same plan, then re-run without `--dry-run`.
3. If running by hand instead, only ever run `git push origin --delete <branch>` with the exact `preview/<ISSUE-ID>-v<n>` branch name from the delete list above — never a wildcard or bare delete, per `agents/shared/conventions.md`.
4. Do not touch the four unrecognized-name branches (`preview/SHA-25-build`, `preview/sha-169-v1`, `preview/sha-170-v1`, `preview/sha-171-v1`) — the script itself skips them too; they need a human decision, not automated cleanup.
5. Delete this handover file and this handover branch once the cleanup is complete.
