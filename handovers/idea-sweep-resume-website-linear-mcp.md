# Handover: idea-sweep routine for Resume Website blocked on missing Linear MCP + Playwright

**For:** Any agent/session with Linear MCP access and a Playwright/browser tool
**From:** idea-sweep routine orchestrator, Resume Website, 2026-07-26 (scheduled run)
**Blocked by:** No Linear MCP connector available in this session (requires
interactive OAuth this non-interactive scheduled session cannot perform), and
no Playwright/browser tool available for the mandatory Visual Self-QA
screenshot step.
**Action:** Re-run the `idea-sweep` routine for Resume Website
(`routines/idea-sweep.md`) from a session that has both Linear MCP and
Playwright available. Nothing was filed to Linear this cycle — there is no
partial state to reconcile, just a clean re-run.
**Issue:** N/A — this blocker occurred before any issue existed (Issue Cap
pre-flight requires Linear, which was unavailable), so there is no single
Linear issue to comment on.

## Payload

Ran the three idea-generation roles for **Resume Website**
(`rohrasharad-ship-it/resume-website`, Linear Project ID
`b01a99ac-46a3-4b00-9139-31e00fae781d`, Slack `#resume-website`, prod
`meet-sharad.vercel.app`) per `routines/idea-sweep.md`.

### bug-error — completed normally, no blocker
- Checked Vercel production runtime errors via `mcp__Vercel__get_runtime_errors`
  for project `prj_P1V3fzfZ1QwZcVvUNHzdq1DQRtGt` (team
  `team_P5vgMhFNfh2d4fCe2YkRLjey`), both the default 24h window and a 7d
  window.
- **Result: no runtime errors found.** Site is clean — nothing to file. This
  role needs no re-run; it already reached a valid terminal state ("clean").

### spec-drift — blocked before step 1
- **Step 0 (Issue Cap pre-flight)** requires `list_issues` filtered by Linear
  Project ID (`agents/shared/issue-cap.md`). No Linear MCP tool was reachable
  in this session (search for Linear-prefixed tools returned nothing; the
  connector is listed as requiring interactive auth). Could not determine
  whether Resume Website is at/over the 5-issue active-pipeline cap, so
  steps 1–9 (gap-filing) were **not attempted** — proceeding without knowing
  the cap risks flooding an already-full backlog.
- **Steps 10–11** (stale-issue sweep, preview-branch housekeeping) also need
  Linear (list/read/comment on issues; `LINEAR_API_KEY` for the cleanup
  script) — `LINEAR_API_KEY` is not set in this session's environment either.
  Not attempted.
- **Step 12** (OpenSpec archive sweep) was **skipped deliberately**, not just
  blocked: `agents/spec-drift.md` says completed change folders "live in
  AI-Workspace," but Resume Website actually has its own populated
  `openspec/changes/` (6 active change folders: `fix-mobile-voice-audio`,
  `journey-chapter-scrubber`, `mobile-qa-pass`, `save-contact-vcard`,
  `social-share-preview`, `warmer-chatbot-avatar`). Running
  `archive-merged-openspec-changes.sh --sweep` from AI-Workspace would not
  reach these, and the script commits/pushes archive changes — running it
  against the wrong repo on a guess risked an unwanted push. **Worth a human
  look:** the step-12 instruction may be stale/inconsistent with how
  per-project `openspec/changes/` actually works now — flagging for Sharad
  rather than silently "fixing" the routine doc myself.
- No codebase-vs-spec gap analysis was done this cycle (deferred entirely,
  not partially — see rationale above for not risking cap overrun blind).

### market-feature — blocked before step 1
- Same Step 0 Issue Cap dependency as spec-drift — not attempted for the same
  reason (Linear MCP unavailable, cap unknown).
- Did do lightweight, non-authoritative context reading in case it saves time
  on re-run: `openspec/project.md` vision/non-negotiables/out-of-scope, and
  the `openspec/specs/` capability table, which already flags known
  in-flight gaps tracked as SHA-14 (Cal.com button), SHA-13 (emoji
  scroll-morph), SHA-11 (site-meta). Don't re-propose these — they're
  presumably already Linear issues (unverified this cycle, confirm on
  re-run).

### Second independent blocker: no Playwright/browser tool
Separately from Linear, this session had no Playwright or browser-automation
tool reachable (checked via tool search). Even if Linear had been available,
the mandatory Visual Self-QA screenshot (`agents/shared/visual-self-qa.md`,
required for every issue any of these three roles creates) could not have
been produced. Both blockers need to be resolved for a full run, not just
Linear.

## Instructions for receiving agent

1. Confirm Linear MCP and a Playwright/browser tool are both reachable
   (quick tool search for each) before starting.
2. Re-run `routines/idea-sweep.md` for **Resume Website** from the top,
   including the Issue Cap pre-flight — nothing from this cycle needs
   reconciling, since zero issues were filed.
3. bug-error can be treated as already covered for this cycle (clean, 7d
   window checked 2026-07-26) — re-run only if it's a new day/cycle by the
   time you pick this up.
4. For spec-drift step 12, before running the AI-Workspace archive sweep
   against Resume Website's own `openspec/changes/`, resolve the
   AI-Workspace-vs-per-project inconsistency noted above (ask Sharad or check
   git history for `agents/spec-drift.md` step 12 intent) rather than
   guessing.
5. Delete this handover file once a clean idea-sweep run for Resume Website
   completes (or supersedes this one).
