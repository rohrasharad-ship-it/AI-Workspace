# Handover: Linear MCP requires re-authorization — idea-sweep cannot run at all in this scheduled session

**For:** Sharad (only he can complete the Linear connector OAuth flow) or any
future agent session confirmed to have working Linear MCP tool access
**From:** idea-sweep routine run for Application Agent, 2026-08-23 (scheduled/automated trigger, no live user)
**Blocked by:** The Linear MCP server is connected but reports "requires
authentication before its tools can be used." This session is non-interactive
(fired by a schedule), so it cannot complete an OAuth flow — there is no way
to reach any Linear MCP tool (`list_issues`, `search_issues`, `create_issue`,
`add_comment`, etc.) at all this run.
**Action:** Re-authorize the Linear connector for this account — claude.ai →
Settings → Connectors → Linear (reconnect/re-authorize). Once done, either
re-run this routine manually or let the next scheduled firing pick it up
normally; no other fix is needed.
**Issue:** N/A — this is a routine-level tooling blocker, not tied to one
Linear issue (same pattern as `handovers/preview-branch-cleanup-linear-api-key.md`,
which documents a *different*, already-tracked blocker — see "Not to be
confused with" below).

## Payload

This is a **new** blocker, distinct from anything previously logged. Every
prior `idea-sweep` run recorded in `data/sweep-runs.jsonl` (13 entries, most
recently 2026-08-19 for both Application Agent and AI Workspace) completed
with real Linear reads — e.g. the 2026-08-12 update in
`handovers/preview-branch-cleanup-linear-api-key.md` describes a session that
successfully called `list_issues` across the whole workspace. So Linear MCP
access has worked in prior scheduled sessions; it simply isn't authorized in
*this* one. Because the connector's auth state isn't visible to me across
sessions, **this may also be silently blocking other scheduled idea-sweep
firings (daily bug-error, weekly spec-drift/market-feature) on other
projects** until someone re-authorizes it — worth checking whether recent
runs for other projects also hit this.

**What I could and couldn't do this run (Application Agent, single-project
idea-sweep):**

- ❌ Issue Cap pre-flight (`agents/shared/issue-cap.md`) — needs `list_issues`
  filtered by Linear Project ID. Not run. Cap status for Application Agent
  (`7dc5202c-a586-4bed-b2d3-fba10f2dd913`) is unknown this cycle.
- ❌ spec-drift steps 1–9 (gap-filing) — blocked (needs Linear search + create).
- ❌ spec-drift step 10 (stale-issue sweep) — blocked (needs `list_issues` +
  comment).
- ❌ spec-drift step 11 (preview-branch housekeeping) — blocked for an
  **unrelated, already-tracked reason**: the cleanup script needs
  `LINEAR_API_KEY` as a repo secret, which still isn't set (see "Not to be
  confused with" below). Did not re-verify the branch list — the 2026-08-12
  update in that handover already says re-verifying wastes tokens with no new
  info, and I have no shell git/Linear access this session to check it anyway.
- ❌ spec-drift step 12 (OpenSpec archive sweep) — checked directly via GitHub
  MCP (doesn't need Linear): `openspec/changes/` in this repo contains only
  the `archive/` folder, no active change folders. Correctly a **clean 0**,
  not a new blocker.
- ❌ bug-error (all steps) — blocked on the cap check alone; also, separately,
  `projects.md` lists Application Agent's Vercel Prod as `TBD`, so even with
  Linear restored this role has no prod URL to read logs from yet. That's an
  independent, permanent blocker for this project until a prod URL is
  registered — worth fixing regardless of the Linear issue.
- ❌ market-feature (all steps) — blocked on the cap check alone. I did read
  `openspec/project.md` and the repo tree (see below) but did **not** draft
  or file any candidate features — without Linear I cannot search for
  existing/duplicate proposals first, and `agents/market-feature.md` step 4
  requires that dedupe search before drafting.

**Repo context gathered (harmless to share, no Linear needed):**
Application Agent (`rohrasharad-ship-it/Application-Agent`) has an
`openspec/` directory with `project.md` and a `specs/` folder, a Python
package under `src/`, `tests/`, and `agents/`/`profile/` directories — a
real, structured repo, not empty. Worth a full spec-drift/market-feature pass
once Linear access is restored; I did not go deeper than the top-level tree
this run since drafting candidates without the ability to dedupe against
Linear risks wasted/duplicate work for whoever picks this up.

## Not to be confused with

`handovers/preview-branch-cleanup-linear-api-key.md` tracks a **different**
Linear blocker: the `LINEAR_API_KEY` *repository secret* needed by
`scripts/cleanup-preview-branches.sh` and `scripts/generate-routine-log.mjs`
(shell scripts, not MCP). That one is still open (7+ consecutive hits) and
needs a repo secret added in GitHub Settings. This handover is about the
**Linear MCP connector's own OAuth authorization** for agent sessions — a
session-level auth issue, unrelated to that repo secret. Both need fixing;
neither fixes the other.

## Instructions for receiving agent

1. Confirm Linear MCP tools are reachable (e.g. `list_issues` with a small
   `limit` returns data, not an auth error).
2. Re-run `idea-sweep` for Application Agent from the top: Issue Cap
   pre-flight, then spec-drift steps 1–9, bug-error (note the Vercel Prod URL
   gap above — flag it back to Sharad rather than skipping silently if it's
   still `TBD`), and market-feature.
3. If other projects' scheduled idea-sweep runs also went quiet/empty around
   2026-08-23, they likely hit the same auth gap — worth a quick check of
   `data/sweep-runs.jsonl` for the same date across projects before assuming
   those were genuinely clean sweeps.
4. Delete this handover file once a run has confirmed Linear MCP is working
   again and Application Agent's idea-sweep completed normally.
