# Handover: idea-sweep for Resume Website couldn't file anything — no Linear MCP access this session

**For:** Any agent session with Linear MCP tool access (or a human who can authorize the Linear connector for this account)
**From:** idea-sweep routine run (spec-drift + bug-error + market-feature), Resume Website, 2026-09-08, automated/scheduled session
**Blocked by:** The Linear MCP server is not authorized for this account/session. The session's own tooling notice states it explicitly: Linear requires an OAuth flow, and this was a non-interactive scheduled run with no human present to complete it. No `LINEAR_API_KEY` env var was present either, so not even a direct-API fallback was possible.
**Action:** Once Linear MCP access (or a `LINEAR_API_KEY`) is available in a session, run the blocked steps below for Resume Website: the Issue Cap pre-flight, then spec-drift steps 1–9 (skip — see Payload, nothing to file), bug-error (skip — see Payload, nothing to file), market-feature (see candidate below), and spec-drift step 10 (stale-issue sweep) and step 11 (preview-branch cleanup — see the separate `preview-branch-cleanup-linear-api-key.md` handover, which has its own long-standing blocker independent of this one).
**Issue:** N/A — this is a routine-level blocker, not tied to one existing Linear issue.

## What this session could and couldn't do

Per `agents/shared/conventions.md`'s Blocked-agent handover convention, this session did
everything it could without Linear before stopping:

### Done — no Linear needed

- **spec-drift steps 1–9 (gap analysis):** Read `openspec/project.md` and all 7 files under
  `openspec/specs/` in `rohrasharad-ship-it/resume-website`, cross-checked against the
  current codebase (`lib/content/eras.ts`, `public/photo/`, `public/videos/`,
  `components/sections/Currently.tsx`, etc.). **Result: no meaningful unbuilt gaps found.**
  The two "pending" items visible in the specs (Cal.com booking button, emoji scroll-morph
  animation) are already tracked as SHA-14 and SHA-13 respectively per `openspec/project.md`
  and `openspec/specs/design-system/spec.md` — correctly not re-proposed. All four Journey
  era videos (`amadeus.mp4`, `isb.mp4`, `impact-analytics.mp4`, `dtu.mp4`) now exist in
  `public/videos/`, even though the repo's own `CLAUDE.md` "Pending Items" table still lists
  Impact Analytics/DTU videos as pending — that table is stale and worth a docs fix, but
  is not itself a spec-drift gap (nothing to build, code already handles it correctly).
  Also noted, not filed (doc-hygiene, not a product gap): `openspec/project.md`'s capability
  table says Site Meta is "In progress, see SHA-11" while `openspec/specs/site-meta/spec.md`
  itself says "Live — SHA-173" — these disagree and one is stale. Also,
  `openspec/specs/voice-agent/spec.md`'s "Avatar Photo" section (describes a photo-based
  avatar with `avatar.jpeg`/`avatar.png`) appears to predate the current SVG illustrated-face
  avatar design documented earlier in the same file — likely dead spec content, not a gap to
  build. None of these three are "meaningful gaps" per the role's bar (planned-but-unbuilt
  product functionality) — they're spec/doc accuracy issues. Flagging for whoever next
  touches those spec files, not filing as Backlog issues.

- **bug-error:** Checked Vercel production runtime errors (`get_runtime_errors`, last 24h)
  and runtime logs grouped by status code for `resume-website` (project
  `prj_P1V3fzfZ1QwZcVvUNHzdq1DQRtGt`, team `team_P5vgMhFNfh2d4fCe2YkRLjey`). **Result: zero
  runtime errors, zero log volume in the window.** Nothing to file.

- **market-feature:** Read `openspec/project.md` vision/non-negotiables/out-of-scope and all
  specs. Given the volume of recently shipped/in-flight differentiation work (5 openspec
  changes shipped since July: warmer chatbot avatar, suggested prompt chips, save-contact
  vCard, journey chapter scrubber, mobile QA pass; 1 more in progress —
  `fix-mobile-voice-audio`; PR #21 "Colleague Signal Wall" testimonials in review), most
  obvious differentiation ideas are already covered. One loose, **unvetted** idea worth a
  human look rather than filed as-is (no visual mockup made, no Linear dedupe done): a small
  "recently shipped" or "what's new" marker somewhere on the page tying back to the
  living-product-demo positioning (e.g. a subtle badge noting the site itself shipped a
  feature this week) — reinforces the "living product demo" pitch in `project.md` without
  touching any Out of Scope item. Did not force this or two more ideas to hit the cap of 3
  — `agents/market-feature.md` step 9 says not to invent filler, and this is genuinely the
  only candidate that came to mind after reading the current spec set.

- **spec-drift step 12 (OpenSpec archive housekeeping):** Ran directly against
  `rohrasharad-ship-it/resume-website` (not via `AI-Workspace/scripts/archive-merged-openspec-changes.sh`,
  since that script's age check relies on directory mtime, which this session's fresh
  checkout resets to "now" for every folder regardless of true age — running it as-is would
  have incorrectly skipped everything as "younger than 24h"). Instead verified the two
  things the script checks via more reliable methods: `npx @fission-ai/openspec list --json`
  for completion status, and `list_pull_requests` (GitHub MCP) for open PRs — only one open
  PR exists on the repo (#21, unrelated path). Cross-checked real merge dates via `git log`
  (all well over 24h old, most from July). Archived 3 of 7 active change folders that were
  `status: complete`, had no open PR, and were weeks old: `warmer-chatbot-avatar`,
  `suggested-prompt-chips`, `save-contact-vcard` — via `npx @fission-ai/openspec archive
  <name> -y --skip-specs`, committed, pushed to `claude/trusting-ramanujan-sjyhxf`.
  **Left in place, not archived:**
  - `journey-chapter-scrubber` and `mobile-qa-pass` — both `status: complete` but fail
    openspec's own delta validation (`Delta sections ## ADDED Requirements were found, but
    no requirement entries parsed` — malformed `### Requirement:` blocks in their
    `specs/*/spec.md` deltas). Did not force past this with `--no-validate` since the CLI
    itself says that's not recommended. These two change folders' delta specs need a
    formatting fix before they can be archived — not a Linear-blocked task, just not done
    this run for scope reasons.
  - `social-share-preview` — `status: no-tasks` (no `tasks.md` ever existed), even though
    its own `openspec/specs/site-meta/spec.md` says the feature is "Live — SHA-173" and its
    proposal is clearly shipped (matches the archive script's own conservative rule: only
    `status: complete` qualifies).
  - `fix-mobile-voice-audio` — genuinely still in progress (7/8 tasks), correctly left alone.

- **Ledger:** Appended a line to `data/sweep-runs.jsonl` for this run (`filed: {bugs: 0,
  features: 0}, clean: true`, with a `note` field explaining the blocker — the counts are
  accurate since nothing was filed, but the *reason* is "blocked," not "nothing to find" for
  the sweep/cleanup steps specifically). Did **not** run
  `node scripts/generate-routine-log.mjs` — it hard-requires `LINEAR_API_KEY`, which isn't
  set in this session either (same root cause as the linked handover below).

### Blocked — needs Linear MCP (or a `LINEAR_API_KEY`)

- **Issue Cap pre-flight** (`agents/shared/issue-cap.md`) — could not count Resume Website's
  active pipeline issues at all, so no idea-generation role could confirm it was safe to file
  even if it had found something.
- **Dedupe search** — none of the analysis above was cross-checked against existing Linear
  issues. Before filing the one market-feature idea above (or anything else), search the
  Resume Website Linear project (`b01a99ac-46a3-4b00-9139-31e00fae781d`) first.
- **spec-drift step 10 (stale-issue sweep)** — could not list or comment on open Backlog
  issues in the Resume Website Linear project.
- **spec-drift step 11 (preview-branch cleanup)** — separately and repeatedly blocked across
  8 runs now on a missing `LINEAR_API_KEY` repo secret; see
  `handovers/preview-branch-cleanup-linear-api-key.md` (this run's update is appended there,
  not duplicated here).

## Instructions for receiving agent

1. Confirm Linear MCP tools (or `LINEAR_API_KEY`) are available in your session.
2. Run the Issue Cap check for Resume Website (`agents/shared/issue-cap.md`, project ID
   `b01a99ac-46a3-4b00-9139-31e00fae781d`). If at/over cap, stop — nothing below needs filing
   this cycle anyway since spec-drift/bug-error found nothing.
3. If under cap: search Linear for the one market-feature idea above ("living product demo"
   / recently-shipped marker). If not already tracked, decide independently whether it's
   worth filing (it was *not* vetted with a visual mockup or thorough differentiation
   reasoning — treat this handover's description as a starting point, not a ready Issue
   Brief) — do not file on my say-so alone.
4. Run spec-drift step 10 (stale-issue sweep) for Resume Website fresh — this session
   couldn't check it at all, so there's no partial state to resume from.
5. Point to `preview-branch-cleanup-linear-api-key.md` for step 11 rather than re-deriving it.
6. Once Linear access exists, re-run `node scripts/generate-routine-log.mjs` (needs
   `LINEAR_API_KEY`) to refresh `data/routine-log.json`.
7. Delete this handover file once steps 2–4 above are actually done for this cycle (not
   just once Linear access exists) — until then it's the record of what's still open.
