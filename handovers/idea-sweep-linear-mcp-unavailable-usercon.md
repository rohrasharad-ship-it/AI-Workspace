# Handover: idea-sweep (Usercon) blocked end-to-end — Linear MCP not authenticated this session

**For:** Any agent/session with Linear connected (or Sharad, to authorize the Linear connector)
**From:** idea-sweep routine run for Usercon, triggered by scheduled task, 2026-09-16
**Blocked by:** The Linear MCP connector for this account is not authenticated in this session (`ListConnectors` reports `installState: "connect_incomplete"`, `connected: false` for Linear). No Linear tools are loaded at all — not a scoped/permission issue, the connector itself needs OAuth completed via claude.ai connector settings.
**Action:** Authorize the Linear connector (claude.ai → connector settings → Linear → connect), then re-run `idea-sweep` for Usercon from a session where Linear is connected.

## What this blocked

Followed `routines/idea-sweep.md` → `routines/README.md` → `agents/spec-drift.md` /
`agents/bug-error.md` / `agents/market-feature.md` / `agents/shared/issue-cap.md`
exactly. Every step in all three roles needs Linear:

- **Issue Cap pre-flight** (`agents/shared/issue-cap.md`) — needs `list_issues` filtered by
  Usercon's Linear Project ID (`47ebefac-a4f4-4bdd-a382-4506f7e79b6b`). Could not run.
- **spec-drift steps 1–9** (gap-filing) — needs Linear search + issue creation. Blocked.
- **spec-drift step 10** (stale-issue sweep) — needs to list/read/comment on open Backlog
  issues. Blocked.
- **spec-drift step 11** (preview-branch cleanup) — `scripts/cleanup-preview-branches.sh`
  needs `LINEAR_API_KEY` to look up each issue's label/state; also not set as an env var in
  this session (checked: empty). Blocked on a second, independent path.
- **bug-error, market-feature** — both need Linear search + issue creation from step 1
  onward. Blocked entirely.

**Step 12** (`scripts/archive-merged-openspec-changes.sh --sweep`, OpenSpec archive
housekeeping) does not itself need Linear, but this session also has no `gh` CLI (GitHub
access here is MCP-only per this session's operating instructions), and the script's
`has_open_pr_for_change` check requires `gh` to confirm a change has no open PR before
archiving. Running it with that check silently degraded (a `gh`-not-available warning,
not a hard stop) risked archiving one of Usercon's ~30 active `openspec/changes/*` folders
that actually has an open PR. Declined to run it this session rather than risk an
unsafe archive — did not touch `openspec/changes/`.

No Linear issues were created, searched, commented on, or modified this run. No preview
branches were deleted. No OpenSpec changes were archived. Nothing in `data/sweep-runs.jsonl`
was appended for this run — logging a `"clean": true` line would misrepresent a blocked
run as a checked-and-empty one; the record of what happened is this file.

## Instructions for receiving agent/session

1. Confirm Linear is connected: `ListConnectors` (or equivalent) should show
   `connected: true` for Linear before starting.
2. Re-run the full `idea-sweep` routine for Usercon from scratch — nothing from this
   session can be resumed or skipped, since none of it executed:
   - Issue Cap pre-flight (Usercon Linear Project ID: `47ebefac-a4f4-4bdd-a382-4506f7e79b6b`)
   - `agents/spec-drift.md` (steps 1–12)
   - `agents/bug-error.md`
   - `agents/market-feature.md`
3. If `LINEAR_API_KEY` is still unset as an env var when you get to spec-drift step 11,
   that's a separate, already-tracked blocker — see
   `handovers/preview-branch-cleanup-linear-api-key.md` before re-deriving it.
4. If `gh` CLI is available in your session, step 12's open-PR check will work normally —
   no special handling needed, this note doesn't apply to you.
5. Delete this file once a full Usercon idea-sweep run has actually executed (whether or
   not it finds anything to file).
