# Handover: preview-branch cleanup computed but blocked on git delete permission

**For:** Any agent/session whose git remote for `AI-Workspace` allows `push --delete` (e.g. the scheduled `.github/workflows/preview-branch-cleanup.yml` Action, or a session with unrestricted push scope)
**From:** idea-sweep routine (spec-drift steps 10-11), triggered for Application Agent, 2026-07-30
**Blocked by:** This session's git remote is proxied (`http://local_proxy@127.0.0.1:.../git/...`) and returns `HTTP 403` on any `git push origin --delete <branch>` or `:refs/heads/<branch>` refspec, even though normal pushes (new commits/branches) succeed. Confirmed with both a batched multi-refspec delete and a single-branch delete — both 403. Not a Linear-data problem this time (unlike the earlier `handover/preview-cleanup-linear-api-key` handover): this run had full Linear MCP access and computed branch disposition directly from Linear issue state/labels, bypassing `scripts/cleanup-preview-branches.sh` entirely (no `LINEAR_API_KEY` needed).
**Action:** Run `git push origin --delete <branch>` for every branch listed below (all already verified as safe to delete — no live-computation needed, just execute the deletes).
**Issue:** N/A — routine housekeeping (idea-sweep for Application Agent, `routines/idea-sweep.md` step 10-11), not tied to a single Linear issue.

## Payload

Each branch was cross-checked against current Linear issue state via `list_issues`/`get_issue` (team `SHA`, all projects) on 2026-07-30. Every branch below belongs to an issue that is `Done`/`Completed`, `Canceled`, or `Duplicate` (or is a superseded older version) — i.e. no longer `spec-needed`+active, matching the delete condition in `scripts/cleanup-preview-branches.sh` / `agents/spec-drift.md` step 11.

105 branches to delete:

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
preview/SHA-25-build
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
preview/sha-169-v1
preview/sha-170-v1
preview/sha-171-v1
```

**Do NOT delete** these — still `Backlog` + `spec-needed` (active): `preview/SHA-251-v1`, `preview/SHA-252-v1`, `preview/SHA-253-v1`, `preview/SHA-254-v1`, `preview/SHA-255-v1`, `preview/SHA-256-v1`, `preview/SHA-258-v1`, `preview/SHA-259-v1`, `preview/SHA-260-v1`, `preview/SHA-261-v1`, `preview/SHA-262-v1`, `preview/SHA-263-v1`, `preview/SHA-264-v1`, `preview/SHA-265-v1`, `preview/SHA-267-v1`, `preview/SHA-268-v1`, `preview/SHA-269-v1`.

**Also worth deleting (not a preview branch, unrelated stray):** `test-push-permission-check` and `test-proxy-check-delete-me` were observed on `origin` during this run but are outside this handover's scope (not `preview/*`) — flagging only, not part of the payload above, since agents must never delete non-`preview/*` branches per `agents/shared/conventions.md`.

## Instructions for receiving agent

1. `git fetch origin --prune` to confirm the branch list above still matches reality (Linear state may have moved between this handover and pickup — if an issue in the delete list has since moved back to active `spec-needed`, skip that one branch and note it).
2. Delete each listed branch: `git push origin --delete <branch>` (or batch via `git push origin :refs/heads/<branch1> :refs/heads/<branch2> ...`).
3. Do not touch the "Do NOT delete" list or any non-`preview/*` branch.
4. Delete this handover file once all branches are gone.
