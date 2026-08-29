# Handover: idea-sweep blocked end-to-end — Linear MCP connector not authorized in this session

**For:** Sharad, or any agent/human who can authorize the Linear connector for this session type
**From:** Claude Code (scheduled/automated `idea-sweep` trigger), Resume Website run, 2026-08-29
**Blocked by:** No Linear MCP tool access at all in this session — every `mcp__linear__*`
tool is listed as requiring authentication, and this is a non-interactive scheduled session
so the OAuth flow cannot be run here. There is also no `LINEAR_API_KEY` environment variable
available as a fallback for shell-script paths.
**Action:** Authorize the Linear connector for this account's scheduled/automated Claude Code
sessions (claude.ai → Settings → Connectors → Linear → re-authorize, or whatever surface
grants this specific session type access — the interactive/chat sessions that produced the
other handovers below clearly did have Linear MCP access, so this looks like a gap specific
to non-interactive scheduled runs, not a account-wide disconnection).
**Issue:** none created — this is a pre-filing infra blocker, no Linear issue exists yet.

## Payload

This is a **more severe** blocker than the one already tracked in
`handovers/preview-branch-cleanup-linear-api-key.md`. That file documents prior sessions that
*did* have working Linear MCP (used for issue-cap counts, dedup search, and the stale-issue
sweep) but lacked the raw `LINEAR_API_KEY` needed by the GitHub Action / shell-script path
(preview-branch cleanup, routine-log generation). This session has neither — no Linear MCP
tool, no `LINEAR_API_KEY` env var — which blocks the *entire* `idea-sweep` routine at its very
first gate, not just the housekeeping scripts.

Per `agents/shared/issue-cap.md` and `routines/idea-sweep.md`, the mandatory pre-flight for
every idea-generation role is a Linear issue-cap count. Every subsequent step (dedup search
before filing, issue creation, first-comment execution detail, stale-issue-sweep comments) is
also a direct Linear MCP call. With zero Linear access, none of the following could run for
the **Resume Website** project this cycle:

- Issue Cap pre-flight (`agents/shared/issue-cap.md`)
- `spec-drift.md` steps 1–9 (gap-filing) **and** step 10 (stale-issue sweep — needs
  `list_issues` + comment reads)
- `spec-drift.md` step 11 (preview-branch housekeeping) — separately blocked anyway by the
  missing `LINEAR_API_KEY`, tracked in `handovers/preview-branch-cleanup-linear-api-key.md`
- `bug-error.md` (Vercel logs were readable via MCP, but filing/dedup against Linear was not
  possible, so no candidate bugs were pursued past that point)
- `market-feature.md` (same — Linear dedup search is a hard requirement before proposing
  anything, so no candidates were drafted)

I deliberately did **not** fabricate speculative issue drafts (gaps, bugs, feature ideas) to
hand off in this file. Every role's process requires searching Linear first to skip anything
already tracked — without that, a blind draft risks duplicating existing Backlog issues once
someone with Linear access picks this up. The safer handoff is: fix the access gap, then let
the next scheduled `idea-sweep` firing (or a manual re-run) do the real research with working
dedup, rather than working from a stale, unverified list.

`agents/shared/openspec.md` structure is in place for Resume Website (`openspec/project.md`,
`openspec/specs/`, `openspec/changes/`) — confirmed reachable via GitHub MCP, so once Linear
access exists, the next run has what it needs to actually do steps 1–2 immediately.

## Instructions for receiving agent / human

1. Confirm whether this is a one-off gap for this particular scheduled session or a
   structural gap for all non-interactive/scheduled Claude Code sessions on this account. If
   the latter, every future scheduled `idea-sweep` firing (daily bug-error, weekly
   spec-drift/market-feature, across all 5+ projects in `projects.md`) will hit the same wall
   until it's fixed — this is not specific to Resume Website.
2. Authorize/reconnect the Linear MCP connector so it's available to scheduled sessions, not
   just interactive ones.
3. Once fixed, re-run `idea-sweep` for Resume Website (and any other projects whose scheduled
   runs were skipped in the meantime) rather than assuming this file's absence of findings
   means the project is clean — no real gap/bug/feature research happened this cycle.
4. Delete this handover file once Linear MCP access is confirmed working from a scheduled
   session and a subsequent `idea-sweep` run completes normally.
5. This is unrelated to the still-open `LINEAR_API_KEY` repo-secret gap in
   `handovers/preview-branch-cleanup-linear-api-key.md` — fixing one does not fix the other;
   both are needed for the routine to fully complete (Linear MCP for filing/search, the repo
   secret for the GitHub Action / shell-script housekeeping paths).
