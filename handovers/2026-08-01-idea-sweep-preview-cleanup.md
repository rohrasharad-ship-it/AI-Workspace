# Handover: Preview-branch housekeeping blocked (idea-sweep, spec-drift step 11)

**For:** Any agent/session with a `LINEAR_API_KEY` env var and unrestricted git push access to `rohrasharad-ship-it/AI-Workspace` (or run via the scheduled `.github/workflows/preview-branch-cleanup.yml` Action, which has both).
**From:** idea-sweep routine, spec-drift role (steps 10-11), Resume Website run, 2026-08-01
**Blocked by:** Two independent blockers in this session:
1. `scripts/cleanup-preview-branches.sh` requires `LINEAR_API_KEY` in the shell environment — not set in this session.
2. Even bypassing the script and deleting branches directly via `git push origin --delete preview/<id>-v<n>`, the session's git proxy returned `HTTP 403` on every delete attempt. This session can only push to its own designated branch (`claude/vibrant-faraday-5z45q6`), not delete arbitrary branches.
**Action:** Delete the 101 orphaned `preview/*` branches listed below from `rohrasharad-ship-it/AI-Workspace` (each `git push origin --delete preview/<branch>`), or re-run `scripts/cleanup-preview-branches.sh` with `LINEAR_API_KEY` set, which will reach the same conclusion.
**Issue:** Not issue-specific — this is routine housekeeping from `agents/spec-drift.md` step 11, triggered by the `idea-sweep` routine for Resume Website.

## Payload

Computed independently in this session by cross-referencing every `preview/<ISSUE-ID>-v<n>` branch against current Linear issue state (`list_issues`, no project filter, paginated, 271 issues fetched) — same logic as `scripts/cleanup-preview-branches.sh` (delete if a newer version exists for the same issue, or the issue's status is `completed`/`canceled`/`duplicate`, or the issue no longer carries the `spec-needed` label).

**101 branches to delete** (all confirmed orphaned — issue is Done/Canceled/Duplicate, or moved off `spec-needed` to `agent-ready`):

```
preview/SHA-100-v1  (SHA-100: Done)
preview/SHA-101-v1  (SHA-101: Canceled)
preview/SHA-102-v1  (SHA-102: Canceled)
preview/SHA-103-v1  (SHA-103: Done)
preview/SHA-104-v1  (SHA-104: Canceled)
preview/SHA-115-v1  (SHA-115: Done)
preview/SHA-116-v1  (SHA-116: Done)
preview/SHA-117-v1  (SHA-117: Done)
preview/SHA-123-v1  (SHA-123: Canceled)
preview/SHA-124-v1  (SHA-124: Canceled)
preview/SHA-125-v1  (SHA-125: Canceled)
preview/SHA-126-v1  (SHA-126: Duplicate)
preview/SHA-128-v1  (SHA-128: Duplicate)
preview/SHA-129-v1  (SHA-129: Duplicate)
preview/SHA-130-v1  (SHA-130: Duplicate)
preview/SHA-131-v1  (SHA-131: Duplicate)
preview/SHA-132-v1  (SHA-132: Duplicate)
preview/SHA-133-v1  (SHA-133: Duplicate)
preview/SHA-134-v1  (SHA-134: Duplicate)
preview/SHA-135-v1  (SHA-135: Canceled)
preview/SHA-138-v1  (SHA-138: Done)
preview/SHA-139-v1  (SHA-139: Done)
preview/SHA-140-v1  (SHA-140: Done)
preview/SHA-141-v1  (SHA-141: Canceled)
preview/SHA-142-v1  (SHA-142: Canceled)
preview/SHA-143-v1  (SHA-143: Done)
preview/SHA-144-v1  (SHA-144: Canceled)
preview/SHA-145-v1  (SHA-145: Canceled)
preview/SHA-147-v1  (SHA-147: Canceled)
preview/SHA-148-v1  (SHA-148: Canceled)
preview/SHA-149-v1  (SHA-149: Canceled)
preview/SHA-152-v1  (SHA-152: Canceled)
preview/SHA-158-v1  (SHA-158: Canceled)
preview/SHA-159-v1  (SHA-159: Canceled)
preview/SHA-160-v1  (SHA-160: Canceled)
preview/SHA-161-v1  (SHA-161: Canceled)
preview/SHA-163-v1  (SHA-163: Canceled)
preview/SHA-164-v1  (SHA-164: Canceled)
preview/SHA-173-v1  (SHA-173: Done)
preview/SHA-176-v1  (SHA-176: Canceled)
preview/SHA-18-v1   (SHA-18: Canceled)
preview/SHA-19-v1   (SHA-19: Canceled)
preview/SHA-20-v1   (SHA-20: Canceled)
preview/SHA-201-v1  (SHA-201: Canceled)
preview/SHA-202-v1  (SHA-202: Canceled)
preview/SHA-231-v1  (SHA-231: Done)
preview/SHA-232-v1  (SHA-232: Canceled)
preview/SHA-235-v1  (SHA-235: Canceled)
preview/SHA-236-v1  (SHA-236: Canceled)
preview/SHA-237-v1  (SHA-237: Canceled)
preview/SHA-238-v1  (SHA-238: Canceled)
preview/SHA-239-v1  (SHA-239: Done)
preview/SHA-24-v1   (SHA-24: Canceled)
preview/SHA-240-v1  (SHA-240: Canceled)
preview/SHA-241-v1  (SHA-241: Canceled)
preview/SHA-242-v1  (SHA-242: Canceled)
preview/SHA-243-v1  (SHA-243: Done)
preview/SHA-244-v1  (SHA-244: Canceled)
preview/SHA-26-v1   (SHA-26: Canceled)
preview/SHA-28-v1   (SHA-28: Canceled)
preview/SHA-29-v1   (SHA-29: Done)
preview/SHA-30-v1   (SHA-30: Canceled)
preview/SHA-31-v1   (SHA-31: Canceled)
preview/SHA-33-v1   (SHA-33: Done)
preview/SHA-37-v1   (SHA-37: Canceled)
preview/SHA-38-v1   (SHA-38: Canceled)
preview/SHA-44-v1   (SHA-44: Done)
preview/SHA-47-v1   (SHA-47: Canceled)
preview/SHA-48-v1   (SHA-48: Canceled)
preview/SHA-50-v1   (SHA-50: Canceled)
preview/SHA-51-v1   (SHA-51: Canceled)
preview/SHA-55-v1   (SHA-55: Canceled)
preview/SHA-56-v1   (SHA-56: Canceled)
preview/SHA-57-v1   (SHA-57: Canceled)
preview/SHA-58-v2   (SHA-58: Canceled)
preview/SHA-64-v1   (SHA-64: Done)
preview/SHA-65-v1   (SHA-65: Done)
preview/SHA-66-v1   (SHA-66: Canceled)
preview/SHA-71-v1   (SHA-71: Canceled)
preview/SHA-72-v1   (SHA-72: Done)
preview/SHA-73-v1   (SHA-73: Canceled)
preview/SHA-74-v1   (SHA-74: Done)
preview/SHA-75-v1   (SHA-75: Done)
preview/SHA-76-v1   (SHA-76: Done)
preview/SHA-81-v1   (SHA-81: Done)
preview/SHA-83-v1   (SHA-83: Canceled)
preview/SHA-84-v1   (SHA-84: Canceled)
preview/SHA-85-v1   (SHA-85: Canceled)
preview/SHA-86-v1   (SHA-86: Canceled)
preview/SHA-87-v1   (SHA-87: Canceled)
preview/SHA-88-v1   (SHA-88: Canceled)
preview/SHA-89-v1   (SHA-89: Canceled)
preview/SHA-91-v1   (SHA-91: Canceled)
preview/SHA-92-v1   (SHA-92: Canceled)
preview/SHA-93-v1   (SHA-93: Canceled)
preview/SHA-94-v1   (SHA-94: Canceled)
preview/SHA-95-v1   (SHA-95: Canceled)
preview/SHA-96-v1   (SHA-96: Done)
preview/SHA-97-v1   (SHA-97: Canceled)
preview/SHA-98-v1   (SHA-98: Canceled)
preview/SHA-99-v1   (SHA-99: Canceled)
```

**20 branches confirmed still valid — do NOT delete** (issue still `Backlog` + `spec-needed`):
`SHA-251,252,253,254,255,256,258,259,260,261,262,263,264,265,267,268,269,270,271,272` (all `-v1`).

**4 branches skipped as unrecognized by the naming convention** (matches the script's own `skip: unrecognized branch name` behavior — do not touch without manual review): `preview/SHA-25-build`, `preview/sha-169-v1`, `preview/sha-170-v1`, `preview/sha-171-v1`.

## Instructions for receiving agent

1. Confirm `LINEAR_API_KEY` is set (or push access allows unrestricted branch deletion).
2. Either re-run `scripts/cleanup-preview-branches.sh` fresh (it will independently re-derive the same list from current Linear state — issue states may have moved on since 2026-08-01) or delete exactly the branches listed above if state is unchanged.
3. Do not delete the 20 "still valid" or 4 "unrecognized" branches.
4. Delete this handover file once the cleanup is confirmed complete.

**What not to do:** don't force this through the current session's proxy again — the 403 is a session-level restriction, not a transient error; retrying won't help.

## Second, related blocker: routine-log regeneration

`node scripts/generate-routine-log.mjs` also requires `LINEAR_API_KEY` and could
not be run in this session after appending to `data/sweep-runs.jsonl` (commit
`776d949`, 2026-08-01 Resume Website entry). Once `LINEAR_API_KEY` is available,
re-run it to refresh `data/routine-log.json` for the `/routine-log.html`
dashboard — it will pick up today's ledger entry along with the preview-branch
cleanup once that's done.
