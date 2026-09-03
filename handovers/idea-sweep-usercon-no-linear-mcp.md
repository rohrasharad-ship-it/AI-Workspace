# Handover: idea-sweep routine for Usercon could not file/search Linear — no Linear MCP access this session

**For:** Any agent session with working Linear MCP tool access
**From:** idea-sweep routine run (Claude Code, scheduled trigger), Usercon, 2026-09-03
**Blocked by:** This session has no Linear MCP tools at all — not a missing `LINEAR_API_KEY`
(that's the separate, already-documented blocker in
`handovers/preview-branch-cleanup-linear-api-key.md`, unrelated to this one). Here the
Linear MCP *server* itself was never authorized for this session (harness reported it as
requiring OAuth, which this non-interactive session cannot run). Every idea-generation step
that touches Linear — the Issue Cap pre-flight, dedupe search, `save_issue`,
issue comments, and the stale-issue sweep — was unreachable this run.
**Action:** Re-run the `idea-sweep` routine for Usercon (`routines/idea-sweep.md`) from a
session that has Linear MCP connected, or ask Sharad to authorize the Linear connector for
this account (claude.ai → Settings → Connectors) so scheduled/cloud sessions stop hitting
this wall. The research below is reusable — no need to redo it, just pick up at the Issue
Cap check.

## What ran and what didn't

- **Issue Cap pre-flight** (`agents/shared/issue-cap.md`): not run — requires
  `list_issues` filtered by Usercon's Linear Project ID
  (`47ebefac-a4f4-4bdd-a382-4506f7e79b6b`). Unknown whether Usercon is at/over the 5-issue
  cap this cycle.
- **bug-error** (`agents/bug-error.md`) steps 1-2: **completed**. Pulled Vercel runtime
  errors for the Usercon project (`prj_MAkmwIEkHssO8BH1DfYLbPTNNKxU`, team
  `team_P5vgMhFNfh2d4fCe2YkRLjey`) for the last 7 days via `get_runtime_errors` — **zero
  runtime errors in that window.** Per step 8 ("if the site is clean, create nothing"),
  bug-error would have filed nothing this cycle regardless of Linear/cap status. No further
  action needed on bug-error unless a future run finds real errors.
  - Side finding: `projects.md`'s Vercel Prod column for Usercon was `TBD`; fixed in this
    same branch to `usercon.vercel.app` (confirmed via the Vercel project link and
    Usercon's own `NEXT.md`, which references `https://usercon.vercel.app` directly as the
    verified production URL). Future bug-error runs no longer need to rediscover this.
- **spec-drift** (`agents/spec-drift.md`) steps 1-9: not run. Steps 4-9 need Linear
  (dedupe search + filing) so were skipped regardless of research depth. Light context
  gathered for whoever picks this up:
  - Read `openspec/project.md` and the `openspec/specs/` capability list (agent-api,
    context-graph, context-receipt, context-review, context-usage-insights, drive-storage,
    mcp-oauth, settings-screen, plus `mobile-shell` under `openspec/changes/sha-204-.../`).
  - Read `NEXT.md` in full. **Important for whoever runs this next:** Usercon tracks its
    own near-term backlog very explicitly in `NEXT.md` and `DECISIONS.md` outside of Linear
    (Phase 0/Phase 1 self-test clock, a numbered "Build Order," and an explicit "Do Not
    Start Yet" list: chatbot, native app packaging, preset context bundles, full permission
    matrix, conflict/duplicate resolution, browser clipboard flow, manual questionnaires,
    hard delete — several of these overlap with `openspec/project.md`'s "Out of Scope"
    section). A spec-drift run here should cross-check candidate gaps against both
    `NEXT.md` and `DECISIONS.md` before proposing anything, to avoid re-discovering
    already-tracked or already-rejected work as if it were new.
  - Did not do a full line-by-line spec-vs-code diff (that step is dedupe-gated on Linear
    access anyway, per the routine's own ordering — no point finding gaps that can't be
    filed or checked against what's already open).
  - Stale-issue sweep (step 10) and preview-branch/openspec-archive housekeeping (steps
    11-12): not run — also Linear-gated (comment posting, `LINEAR_API_KEY` for the cleanup
    script). Note the pre-existing, extensively-documented blocker in
    `handovers/preview-branch-cleanup-linear-api-key.md` already covers step 11's structural
    fix (missing repo secret) — that file explicitly says no further re-verification is
    needed, just add the secret. Not duplicating that work here.
- **market-feature** (`agents/market-feature.md`): not run at all. Steps 1-3 (read vision,
  propose features) don't strictly need Linear, but step 4 (dedupe against Linear) gates
  filing, and speculative feature ideas without a dedupe check risk proposing something
  already rejected in `openspec/project.md`'s Out of Scope list or already tracked. Skipped
  entirely rather than half-do it.

## Instructions for receiving agent

1. Confirm Linear MCP access works (`list_issues` or similar).
2. Run the Issue Cap pre-flight for Usercon (`47ebefac-a4f4-4bdd-a382-4506f7e79b6b`) per
   `agents/shared/issue-cap.md`.
3. If under cap: `agents/bug-error.md` steps 3-8 are moot (0 errors found this run,
   nothing to file) — optionally re-check `get_runtime_errors` since time has passed, but
   this isn't urgent. Run `agents/spec-drift.md` steps 1-9 and `agents/market-feature.md` in
   full, using the `NEXT.md`/`DECISIONS.md` cross-check note above to avoid duplicate
   proposals.
4. If at/over cap: skip straight to spec-drift steps 10-12 (stale-issue sweep, housekeeping)
   — step 11's `LINEAR_API_KEY` requirement is a separate known blocker, see the other
   handover file referenced above.
5. Delete this file once a session with real Linear access has completed the above for
   Usercon — it's no longer needed as a placeholder at that point.
