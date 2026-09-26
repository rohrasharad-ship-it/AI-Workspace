# Handover: idea-sweep routine (Resume Website) blocked — no Linear access in this session

**For:** Any agent/session with Linear MCP access (or a session with `LINEAR_API_KEY` available)
**From:** Claude Code cloud session, idea-sweep routine run for Resume Website, 2026-09-26
**Blocked by:** This session has zero Linear access — the Linear MCP connector is not
authorized for this account/session (`ReadNotifications`/tool listings flagged it as
"requires authentication before its tools can be used"), and there is no `LINEAR_API_KEY`
env var available either. Every idea-sweep step depends on Linear, starting with the very
first one:

- **Pre-flight Issue Cap check** (`routines/idea-sweep.md` → `agents/shared/issue-cap.md`)
  requires `list_issues` filtered by the Resume Website Linear Project ID
  (`b01a99ac-46a3-4b00-9139-31e00fae781d`) — not callable.
- **spec-drift** steps 1–9 (dedupe search, file issues) and steps 10–11 (stale-issue sweep
  needs `list_issues`; branch-cleanup housekeeping script needs `LINEAR_API_KEY`) — not
  callable.
- **bug-error** step 3 (dedupe search) and step 4 (file issues) — not callable.
- **market-feature** step 4 (dedupe search) and step 5 (file issues) — not callable.

Note: this is a **broader** blocker than the one already tracked in
`handovers/preview-branch-cleanup-linear-api-key.md` (7 prior update entries there). Those
sessions had working Linear MCP tool access and only lacked the raw `LINEAR_API_KEY` env
var needed by the shell housekeeping script. This session has neither — no MCP OAuth, no
key — so nothing downstream of the pre-flight check could run at all, not even the cap
count itself.

**Action:** Authorize the Linear MCP connector for this account (claude.ai connector
settings), or ensure `LINEAR_API_KEY` is available as an env var to Claude Code cloud
sessions, so a future idea-sweep run (this project and others) can pass the pre-flight step
and actually execute. Once either exists, this handover can be deleted — no payload to
carry forward, since no research was performed downstream of the blocker (see below).

## What was and wasn't done this run

Per `agents/shared/conventions.md` rule 17 / Blocked-agent handover: stopped as soon as the
hard tool-access wall was confirmed, rather than improvising a Linear-less version of the
routine. Specifically avoided running spec-drift/market-feature's read-only research
(openspec vs. codebase comparison, feature ideation) standalone, because those roles are
designed to run together with the Linear dedupe/cap check that follows immediately after —
producing that research now without being able to check "is this already tracked?" risked
handing off stale or duplicate findings to whoever picks this up next. Better for the next
Linear-enabled run to do the research and the filing together, as designed.

One non-Linear check was completed, for reference only (time-sensitive, should be re-run
rather than trusted going forward): Vercel `get_runtime_errors` for `resume-website`
(project `prj_P1V3fzfZ1QwZcVvUNHzdq1DQRtGt`, team `team_P5vgMhFNfh2d4fCe2YkRLjey`), last 24h
as of 2026-09-26 — **no runtime errors found**. If a future run happens shortly after this
one, bug-error step 1 can likely be re-run quickly and may still come back clean.

Also observed (not verified against Linear, just noted for context): Resume Website's
`openspec/changes/` currently has 7 active, non-archived change folders (`fix-mobile-voice-
audio`, `journey-chapter-scrubber`, `mobile-qa-pass`, `save-contact-vcard`, `social-share-
preview`, `suggested-prompt-chips`, `warmer-chatbot-avatar`), and `openspec/project.md`
itself flags 3 more known-pending items (SHA-11 site-meta, SHA-13 emoji scroll-morph,
SHA-14 Cal.com button). A Linear-enabled spec-drift run should check whether the project is
already at or near the 5-issue cap before spending effort on new gap-finding — this may
turn out to be a cap-skip cycle (stale-sweep + housekeeping only) rather than a normal run.

## Instructions for receiving agent

1. Confirm Linear MCP access (or `LINEAR_API_KEY`) actually works in your session.
2. Run `routines/idea-sweep.md`'s pre-flight Issue Cap check for Resume Website
   (`b01a99ac-46a3-4b00-9139-31e00fae781d`) fresh — don't trust anything above as a
   substitute for that count.
3. Proceed with the routine normally from there (full spec-drift/bug-error/market-feature
   research, since none was done this run beyond the one Vercel check noted above).
4. Delete this handover file once a run completes successfully end-to-end for Resume
   Website (cap check ran, and either issues were filed/found-clean or the cap-skip path
   ran).
