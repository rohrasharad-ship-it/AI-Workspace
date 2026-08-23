# Handover: idea-sweep (Resume Website) blocked — Linear MCP not authorized

**For:** Any agent/session with Linear MCP access (or Sharad, to authorize the connector)
**From:** Scheduled idea-sweep run, Resume Website project, 2026-08-23
**Blocked by:** Linear MCP server requires OAuth authorization; this is a non-interactive scheduled session and cannot run the OAuth flow
**Action:** Authorize the Linear MCP connector (claude.ai connector settings), then re-run the idea-sweep for Resume Website
**Issue:** none created — the routine could not get far enough to file or even count issues

---

## What happened

This session was fired by the scheduled `idea-sweep` trigger:

```
Run the "idea-sweep" routine for Resume Website.
Follow rohrasharad-ship-it/AI-Workspace/routines/idea-sweep.md exactly.
```

Per `routines/idea-sweep.md` → `routines/README.md` → `agents/shared/issue-cap.md`,
the very first thing any of the three roles (spec-drift, bug-error,
market-feature) must do is the Issue Cap pre-flight: `list_issues` filtered by
the **Resume Website** Linear Project ID (`b01a99ac-46a3-4b00-9139-31e00fae781d`
from `projects.md`).

The session's tool list has no Linear MCP tools at all — the runtime's own
system reminder states:

> The following MCP servers require authentication before their tools can be
> used: Linear... This session is non-interactive, so Claude cannot run the
> OAuth flow here.

A `ToolSearch` for `"Linear"` returned zero matching deferred tools, confirming
there is no Linear MCP access to fall back to, not even a degraded/read-only
path.

## Why the whole routine stops here, not just filing

Every downstream step needs Linear:

- **Issue Cap pre-flight** (`agents/shared/issue-cap.md`) — needs `list_issues`.
- **spec-drift steps 1–9** — dedupe search + `save_issue`/create.
- **spec-drift step 10** (stale-issue sweep) — needs `list_issues` + read
  comments + post comments on existing issues.
- **spec-drift step 11** (preview-branch housekeeping) —
  `scripts/cleanup-preview-branches.sh` requires `LINEAR_API_KEY` to look up
  each `preview/<issue-id>-vN` branch's issue state.
- **bug-error, market-feature** — same dedupe-search + create-issue pattern.

So this isn't a partial-cap-style skip (run steps 10–11 only) — there is no
Linear access at all this run, so nothing in the routine could execute,
including the housekeeping steps that don't count against the issue cap.

No local resume-website codebase changes were made — there was nothing to
build; this run never got past the pre-flight.

## What was NOT done, so the next run doesn't assume otherwise

- No Linear query was made (cap unknown, not "under cap").
- No issues were created, no comments posted, no stale-issue sweep run, no
  preview-branch cleanup run, no OpenSpec archive sweep run.
- `data/sweep-runs.jsonl` was deliberately **not** appended — a `"clean":
  true"` line would misrepresent "checked, found nothing" when the real state
  is "could not check." Appending a false-clean ledger line would make a
  future dashboard/read of `data/sweep-runs.jsonl` look like this cycle ran
  normally.

## Instructions for receiving agent / Sharad

1. If you're Sharad: authorize the Linear connector for this account (claude.ai
   → Settings → Connectors → Linear), or confirm whichever scheduled-session
   Linear auth flow your setup uses. Non-interactive sessions cannot do this
   themselves — see `<system-reminder>` guidance any future agent hitting this
   will also see.
2. Once Linear access is confirmed working in a session, re-run:
   ```
   Run the "idea-sweep" routine for Resume Website.
   Follow rohrasharad-ship-it/AI-Workspace/routines/idea-sweep.md exactly.
   ```
3. Delete this handover file once a clean idea-sweep run for Resume Website
   completes (or fails for a different, more specific reason) — until then it
   documents why the 2026-08-23 cycle produced nothing.

## Note on prior art

`handovers/linear-issue-vercel-preview-blocker.md` documents a different,
already-resolved-by-precedent case (cloud agent session without Linear MCP,
July 2026 SHA-25). This handover is the same root cause (no Linear MCP in a
given session) but on a *scheduled* trigger rather than a build session, and
blocks 100% of the routine rather than just one issue's creation — worth
folding into that same discussion if Sharad is looking at both.
