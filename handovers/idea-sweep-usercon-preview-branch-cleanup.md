# Handover: Preview-branch cleanup blocked — no branch-delete access from this session

**For:** Any agent/session with `git push --delete` or branch-admin access to `rohrasharad-ship-it/AI-Workspace`
**From:** idea-sweep routine (spec-drift step 11), Usercon run, 2026-08-18
**Blocked by:** `git push origin --delete <branch>` returns `HTTP 403` / `RPC failed` for every `preview/*` branch from this session's git credential. No GitHub MCP tool exposes ref/branch deletion either (checked `mcp__github__*` — only `create_branch`, no delete equivalent). `LINEAR_API_KEY` env var is also unset, so `scripts/cleanup-preview-branches.sh` cannot run as documented (it requires the key to look up issue state).
**Action:** Delete the 102 orphaned `preview/*` branches listed below (issue is Done/Canceled/Duplicate, or a superseded older version), then optionally re-run `bash scripts/cleanup-preview-branches.sh` with `LINEAR_API_KEY` set to confirm the remainder is clean.
**Issue:** N/A — this is spec-drift's routine housekeeping step (`agents/spec-drift.md` step 11), not a single Linear issue.

## Payload

Computed by replicating `scripts/cleanup-preview-branches.sh`'s logic locally (Linear MCP `list_issues` across the whole workspace in place of the script's per-issue GraphQL call, since `LINEAR_API_KEY` isn't set in this session). Full workspace issue list paginated (269 issues) and cross-referenced against every `origin/preview/*` branch. Logic replicated exactly: an issue counts as deletable when its `statusType` is `completed`, `canceled`, or `duplicate`, or when it no longer carries the `spec-needed` label; branches with a newer `-v<n>` sibling for the same issue are also deletable regardless of state.

- 125 total `preview/*` branches found.
- 4 skipped as unrecognized names (don't match `preview/<TEAM>-<N>-v<N>`): `preview/SHA-25-build`, `preview/sha-169-v1`, `preview/sha-170-v1`, `preview/sha-171-v1` (lowercase `sha` doesn't match the script's `[A-Z]+` team-key regex — worth a human decision on whether these are also safe to delete, they were not evaluated).
- **19 branches correctly kept** — issue still `Backlog` + `spec-needed`: SHA-251, SHA-252, SHA-253, SHA-254, SHA-255, SHA-258, SHA-259, SHA-260, SHA-261, SHA-262, SHA-263, SHA-264, SHA-265, SHA-267, SHA-268, SHA-269, SHA-270, SHA-271, SHA-272.
- **102 branches to delete** (issue Done/Canceled/Duplicate — verified via Linear, not just guessed):

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
preview/SHA-242-v1 preview/SHA-243-v1 preview/SHA-244-v1 preview/SHA-256-v1 preview/SHA-26-v1
preview/SHA-28-v1  preview/SHA-29-v1  preview/SHA-30-v1  preview/SHA-31-v1  preview/SHA-33-v1
preview/SHA-37-v1  preview/SHA-38-v1  preview/SHA-44-v1  preview/SHA-47-v1  preview/SHA-48-v1
preview/SHA-50-v1  preview/SHA-51-v1  preview/SHA-55-v1  preview/SHA-56-v1  preview/SHA-57-v1
preview/SHA-58-v2  preview/SHA-64-v1  preview/SHA-65-v1  preview/SHA-66-v1  preview/SHA-71-v1
preview/SHA-72-v1  preview/SHA-73-v1  preview/SHA-74-v1  preview/SHA-75-v1  preview/SHA-76-v1
preview/SHA-81-v1  preview/SHA-83-v1  preview/SHA-84-v1  preview/SHA-85-v1  preview/SHA-86-v1
preview/SHA-87-v1  preview/SHA-88-v1  preview/SHA-89-v1  preview/SHA-91-v1  preview/SHA-92-v1
preview/SHA-93-v1  preview/SHA-94-v1  preview/SHA-95-v1  preview/SHA-96-v1  preview/SHA-97-v1
preview/SHA-98-v1  preview/SHA-99-v1
```

## Instructions for receiving agent

1. Confirm you have working `git push origin --delete` access to `rohrasharad-ship-it/AI-Workspace` (test on one branch from the list above first).
2. Either re-run `LINEAR_API_KEY=<key> bash scripts/cleanup-preview-branches.sh` fresh (preferred — it re-verifies live Linear state rather than trusting this snapshot), or delete the 102 branches listed above directly if you trust this snapshot is still current.
3. Do **not** delete the 19 kept branches or the 4 unrecognized-name branches without checking their issue state first.
4. Delete this handover file once the branches are cleaned up.

**Do not** attempt to force through the 403 with alternate git protocols, tokens, or admin overrides you don't already have — that's exactly the kind of privilege-escalation workaround this handover exists to avoid. Wait for a session with legitimate delete access.

## Related, smaller blocker: routine-log dashboard refresh also skipped

Same root cause (`LINEAR_API_KEY` unset in this session), separate script:
`node scripts/generate-routine-log.mjs` (refreshes `data/routine-log.json`
for the `/routine-log.html` sandbox dashboard) also failed with
`error: LINEAR_API_KEY is required`. The `data/sweep-runs.jsonl` ledger line
for this run was appended correctly by hand, so no data is lost — only the
derived dashboard JSON is stale until a session with the key re-runs the
generator. Lower priority than the branch cleanup above; a future run with
`LINEAR_API_KEY` set will pick this back up automatically.
