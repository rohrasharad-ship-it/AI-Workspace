# Handover: idea-sweep routine for Resume Website — blocked, no Linear MCP

**For:** Any agent/session with Linear MCP access
**From:** Claude Code (non-interactive scheduled session), idea-sweep run for Resume Website, 2026-09-20
**Blocked by:** This session has no Linear MCP connection at all — the "Linear" MCP
server is listed as requiring authentication that cannot be completed in a
non-interactive session. This is a harder blocker than the `LINEAR_API_KEY`
repo-secret gap already tracked in
`handovers/preview-branch-cleanup-linear-api-key.md` (that file's prior updates all
had live Linear MCP access and only lacked the raw API key for the shell script —
this session has neither). It also had no Playwright/browser tool available, which
independently blocks the mandatory Visual Self-QA screenshot every idea-generation
issue must carry, even once Linear access exists.
**Action:** Pick up the `idea-sweep` routine for **Resume Website** from the point
below — do the Issue Cap pre-flight, then whichever of spec-drift/market-feature
steps are still warranted, using the notes in Payload so you don't have to re-derive
them.
**Issue:** none — this is a routine run, not a single Linear issue.

---

## Payload — what this session could and couldn't do

Routine followed: `routines/idea-sweep.md` (spec-drift → bug-error → market-feature,
single project). Read `routines/README.md`, `agents/shared/issue-cap.md`,
`agents/spec-drift.md`, `agents/bug-error.md`, `agents/market-feature.md`,
`agents/shared/conventions.md` per the routine's own instructions.

### Issue Cap pre-flight — NOT DONE
Requires `list_issues` filtered by Resume Website's Linear Project ID
(`b01a99ac-46a3-4b00-9139-31e00fae781d` per `projects.md`). No Linear MCP tool was
present in this session's tool list (confirmed via ToolSearch — only GitHub/Vercel/
Slack tools resolved). Do this first before filing anything.

### bug-error — DONE, clean, nothing to file
Pulled `get_runtime_errors` from Vercel for the Resume Website project
(`prj_P1V3fzfZ1QwZcVvUNHzdq1DQRtGt`, team `team_P5vgMhFNfh2d4fCe2YkRLjey`) over the
last 7 days: **zero runtime errors**. Nothing to file for this role this cycle — this
part of the routine is genuinely complete, not just blocked.

### spec-drift — NOT DONE (dedupe + filing both need Linear)
Read `openspec/project.md`. Its capability table already flags the known gaps as
tracked, not undiscovered:
- Contact — Cal.com booking button pending, see **SHA-14**
- Design System — emoji scroll-morph pending, see **SHA-13**
- Site Meta (OG tags/SEO) — in progress, see **SHA-11**

`CLAUDE.md`'s own Pending Items table matches this (avatar headshot, Impact
Analytics/DTU demo videos, Cal.com link). Did not do a full spec-vs-codebase read of
every file under `openspec/specs/` (about, contact, design-system, hero, journey,
site-meta, voice-agent) since without Linear I can't check whether SHA-11/13/14 are
still open or whether anything else is already tracked — a full read would just
produce candidates I can't dedupe or file anyway. **Next session: start by pulling
SHA-11, SHA-13, SHA-14's current status; only do the full spec-vs-code read if you
still have budget after that and after the cap check clears.**

### market-feature — NOT ATTEMPTED
Blocked on the same Linear dedupe/filing requirement, plus every issue this role
creates mandatorily needs both a mockup visual and a real Playwright screenshot of
the current homepage (`agents/market-feature.md` steps 6–7) — no browser/Playwright
tool was available in this session either, so even a speculative proposal couldn't
be finished to spec. Not started, no candidates drafted, to avoid inventing filler
ideas without being able to verify they're not already proposed.

### Stale-issue sweep / preview-branch / openspec-archive housekeeping (spec-drift
steps 10–12) — NOT DONE
All three need either Linear MCP (steps 10–11) or, for step 11's script,
`LINEAR_API_KEY` as a shell env var — also unavailable (env var access itself was
denied by this session's own credential-materialization guard, separate from
whether the secret exists). See `handovers/preview-branch-cleanup-linear-api-key.md`
for the pre-existing, separately-tracked version of that specific gap across other
projects.

## Instructions for receiving agent

1. Do the Issue Cap check for Resume Website (`agents/shared/issue-cap.md`,
   project ID `b01a99ac-46a3-4b00-9139-31e00fae781d`). If at/over cap, only run
   spec-drift steps 10–11 and stop.
2. If under cap: check current status of SHA-11, SHA-13, SHA-14 first. If any look
   stale/resolved, that's spec-drift's stale-issue-sweep job (step 10), not new
   filing.
3. Only then do a full `openspec/specs/` vs. codebase read for spec-drift steps 1–9,
   and a market-feature pass (steps 1–9, with the mandatory mockup + live-site
   screenshot) if cap budget remains.
4. bug-error does not need to be re-run today — already clean for the last 7 days as
   of 2026-09-20 (re-run tomorrow per normal daily cadence, not as follow-up to this
   handover).
5. Delete this handover file once the cap check + any filing for this cycle is done.
