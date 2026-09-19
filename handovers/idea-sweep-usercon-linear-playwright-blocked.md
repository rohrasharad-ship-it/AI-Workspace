# Handover: idea-sweep routine blocked for Usercon — no Linear MCP / no Playwright in this session

**For:** Any agent with Linear MCP access and Playwright/browser automation
**From:** idea-sweep routine session (scheduled trigger), 2026-09-19
**Blocked by:** No Linear MCP tools available in this non-interactive session (the Linear MCP server needs an interactive OAuth authorization that can't be completed from a scheduled/non-interactive run) and no Playwright/browser automation tool available in this session
**Action:** Complete `agents/spec-drift.md` (steps 1–12) and `agents/market-feature.md` (steps 1–9) for Usercon once Linear + Playwright access is available, then append the sweep-runs ledger entry for this cycle
**Issue:** N/A — this is a routine run (`routines/idea-sweep.md`), not driven by a single Linear issue. Target: **Usercon**, repo `rohrasharad-ship-it/Usercon`, Linear project `UserCon`, Linear Project ID `47ebefac-a4f4-4bdd-a382-4506f7e79b6b`

## Payload — what ran, what didn't, and why

Trigger: "Run the idea-sweep routine for Usercon" (scheduled, 2026-09-19).

- **Issue Cap pre-flight — NOT run.** Requires `list_issues` filtered by Linear
  Project ID `47ebefac-a4f4-4bdd-a382-4506f7e79b6b` (`agents/shared/issue-cap.md`).
  No Linear MCP tool was reachable in this session. Cap status for Usercon is
  **unknown** as of this run — check it fresh, don't assume clear.

- **bug-error — completed, cleanly, no blocker.** Checked Vercel production
  runtime errors for the last 24h via `get_runtime_errors` on project
  `prj_MAkmwIEkHssO8BH1DfYLbPTNNKxU` (name `usercon`, team
  `team_P5vgMhFNfh2d4fCe2YkRLjey`): **zero runtime errors** in the window. Per
  role step 8 ("if the site is clean, create nothing"), there was nothing to
  file — this outcome needed no Linear or Playwright access. **No further
  action needed for bug-error this cycle** unless the receiving agent is
  treating this as a fresh cycle rather than resuming this one.
  - Side note, not acted on: `projects.md` lists Usercon's Vercel Prod as
    `TBD`, but a Vercel project named `usercon` does exist (id above). Worth
    filling in `projects.md` with its production URL sometime.

- **spec-drift — NOT run (steps 1–9, and 10–11).**
  - Steps 1–9 (gap-filing) need Linear (dedup search, cap check already noted
    above, issue creation, first comment) and a Playwright screenshot per
    created issue — none available here.
  - Steps 10–11 (stale-issue sweep, preview-branch housekeeping) need Linear
    (list/read/comment on issues) and `LINEAR_API_KEY` for
    `scripts/cleanup-preview-branches.sh` — also unavailable here.
  - Step 12 (openspec archive sweep, `scripts/archive-merged-openspec-changes.sh
    --sweep`) does *not* need Linear and could run standalone, but wasn't
    attempted here since it's generic AI-Workspace housekeeping decoupled from
    the Usercon-specific analysis, and the weekly GitHub Action
    (`.github/workflows/openspec-archive.yml`) already covers it structurally.
  - What I did check, read-only, for context only (not a substitute for the
    real gap-finding pass): `openspec/project.md` and `openspec/specs/` for
    Usercon list 9 capabilities — `context-graph`, `context-review`,
    `agent-api`, `context-usage-insights`, `context-receipt`, `drive-storage`,
    `mcp-oauth`, `settings-screen`, and `mobile-shell` (added via
    `openspec/changes/sha-204-mobile-tab-nav/`). I deliberately did **not** do
    the full spec-vs-codebase read-through (`openspec/specs/**` vs `src/`),
    because any gap found here can't be deduped against Linear or filed
    without Linear access — starting it risks either duplicated effort by the
    receiving agent or someone acting on stale findings from this file later.

- **market-feature — NOT run**, same blockers as spec-drift steps 1–9 (Linear
  dedup + filing + Playwright screenshot). Not attempted for the same reason.

- **Sweep ledger — intentionally NOT appended** to `data/sweep-runs.jsonl` for
  this cycle. The ledger records a *finished* run; this one only finished 1 of
  3 roles. Appending `{"filed":{"bugs":0,"features":0},"clean":true}` would
  misrepresent spec-drift and market-feature as having run and found nothing,
  when they never ran. The receiving agent should append the real entry once
  spec-drift + market-feature actually complete for this cycle.

## Instructions for receiving agent

1. Confirm Linear MCP tools are reachable (this typically needs OAuth
   authorization done once via `claude mcp` / `/mcp` in an interactive
   session) and that a Playwright/browser tool is available.
2. Run the Issue Cap pre-flight once for Usercon (`agents/shared/issue-cap.md`,
   Linear Project ID `47ebefac-a4f4-4bdd-a382-4506f7e79b6b`) — don't skip this
   just because bug-error already ran clean.
3. If under cap: run `agents/spec-drift.md` steps 1–12 and
   `agents/market-feature.md` steps 1–9 for Usercon. If at/over cap: run
   spec-drift steps 10–11 only, per `routines/idea-sweep.md`'s pre-flight.
4. bug-error does not need to be re-run for this cycle (see Payload above) —
   unless you're treating this as a new scheduled firing rather than resuming
   this one, in which case just re-check the last 24h as normal.
5. Once all three roles have actually run for this cycle, append the real
   sweep ledger line to `data/sweep-runs.jsonl`, then run
   `node scripts/generate-routine-log.mjs` (needs `LINEAR_API_KEY`) to refresh
   `data/routine-log.json`.
6. Delete this handover file once the cycle is genuinely complete.

Do not invent Linear issues or screenshots to make this cycle look complete —
leave the filing to whichever agent next has real Linear + Playwright access.
