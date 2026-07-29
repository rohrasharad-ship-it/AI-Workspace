# Handover: preview-branch cleanup blocked — no branch-delete access this session

**For:** Any agent/session with `git push --delete` or repo-admin access to `rohrasharad-ship-it/AI-Workspace`
**From:** idea-sweep routine (spec-drift step 11), triggered for AI Landscape 2026, 2026-07-29
**Blocked by:** `git push origin --delete <branch>` returns `HTTP 403` through this session's git credential proxy (tested on a single branch and in batches — consistent 403 on every delete attempt, not a transient failure). No `LINEAR_API_KEY` env var was available to run `scripts/cleanup-preview-branches.sh` directly, and no GitHub MCP tool in this session exposes ref/branch deletion either.
**Action:** Delete the branches listed below from `rohrasharad-ship-it/AI-Workspace` (all are `preview/*`, matching the safety rule in `agents/shared/conventions.md` — never anything else).
**Issue:** Not tied to a single Linear issue — this is the routine housekeeping step from `agents/spec-drift.md` step 11 / `agents/shared/conventions.md` "Structural backup for preview-branch pileup".

## Payload

Applied the exact decision logic from `scripts/cleanup-preview-branches.sh` by hand: for each `preview/<ISSUE-ID>-v<n>` branch, queried the issue's current state/labels via the Linear MCP (`list_issues`, full workspace, paginated) instead of the script's own `curl` call to the Linear GraphQL API (no `LINEAR_API_KEY` in this session's env). Delete if state is `completed`/`canceled`/`duplicate`, or if it no longer carries the `spec-needed` label, or if it's an older version than another branch for the same issue. Keep only if still `Backlog`/active and `spec-needed`. Skip if the branch name doesn't match `preview/<TEAM>-<NUM>-v<N>` exactly (case-sensitive).

**Delete (101 branches — confirmed Done/Canceled/Duplicate in Linear, no longer `spec-needed`):**
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

**Keep (13 branches — issue still Backlog + `spec-needed`, all in the AI Landscape project):**
```
preview/SHA-251-v1 preview/SHA-252-v1 preview/SHA-253-v1 preview/SHA-254-v1 preview/SHA-255-v1
preview/SHA-256-v1 preview/SHA-258-v1 preview/SHA-259-v1 preview/SHA-260-v1 preview/SHA-261-v1
preview/SHA-262-v1 preview/SHA-263-v1 preview/SHA-264-v1
```

**Skip (4 branches — unrecognized name, script's regex is case-sensitive and requires `-v<N>`):**
```
preview/SHA-25-build   (no "-v<N>" suffix)
preview/sha-169-v1     (lowercase "sha", not "SHA")
preview/sha-170-v1     (lowercase "sha", not "SHA")
preview/sha-171-v1     (lowercase "sha", not "SHA")
```
These three lowercase ones and `SHA-25-build` need a human decision — the actual script would also skip them as "unrecognized branch name," so they've never been auto-cleaned. Worth a one-time manual look to confirm they're safe to delete or rename to match the convention.

## Instructions for receiving agent

1. `cd` into a clone of `rohrasharad-ship-it/AI-Workspace` with push access that isn't blocked on branch deletion.
2. Re-verify with `git fetch origin --prune` that these branches still exist (this list is accurate as of 2026-07-29; some may already be gone if the weekly GitHub Action `.github/workflows/preview-branch-cleanup.yml` ran in the meantime — that's the structural backup for exactly this failure mode, so it may self-resolve before anyone reads this).
3. Run `git push origin --delete <branch1> <branch2> ...` for the **Delete** list only. Never touch the **Keep** list or anything outside `preview/*`.
4. Decide on the 4 **Skip** branches by hand (rename to match convention, or confirm safe to delete some other way) — the script won't touch them automatically.
5. Delete this handover file once done.

## Why this matters now

This session (`idea-sweep` for AI Landscape 2026) hit the project's issue cap (6 active pipeline issues ≥ cap of 5), so per `routines/idea-sweep.md` pre-flight it ran spec-drift steps 10–11 only. Step 10 (stale-issue sweep) completed normally (0 flagged — none of the 6 Backlog issues showed high-confidence evidence of already being shipped). Step 11 (this cleanup) could not complete due to the tool-access wall above.
