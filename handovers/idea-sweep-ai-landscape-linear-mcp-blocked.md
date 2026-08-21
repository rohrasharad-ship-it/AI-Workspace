# Handover: idea-sweep routine (AI Landscape 2026) — blocked, no Linear MCP access

**For:** Any agent/session with Linear MCP access authorized
**From:** Claude, scheduled `idea-sweep` trigger session, 2026-08-21
**Blocked by:** Linear connector requires OAuth; this is a non-interactive
scheduled session and cannot complete the authorization flow. `ListConnectors`
reports the Linear connector as `enabledInChat: true` but `installState:
unknown`/`isAuthless: false`, and no Linear MCP tools are exposed to this
session (confirmed via `ToolSearch`).
**Action:** Once Linear MCP is reachable, run `idea-sweep` for **AI Landscape
2026** (`rohrasharad-ship-it/ai-landscape`, Linear Project ID
`4ef7d096-f5bb-44f4-bac5-417e4488cdb8`) for real — nothing from this run
should be treated as a completed sweep.
**Issue:** N/A — this handover blocks the routine itself, not a single
tracked issue. (Follows the same no-issue-ID precedent as
`handovers/preview-branch-cleanup-linear-api-key.md`.)

---

## What happened

The scheduled trigger asked for `routines/idea-sweep.md` to run for **AI
Landscape 2026**. Per `routines/README.md`, every idea-generation role
(spec-drift, bug-error, market-feature) depends on Linear MCP for the
mandatory Issue Cap pre-flight (`agents/shared/issue-cap.md`), Linear search
for dedupe, issue creation, and issue commenting. None of that is possible
without Linear access, so **no roles ran past reading reference docs**:

- Issue Cap pre-flight: not run (needs `list_issues` against project ID
  `4ef7d096-f5bb-44f4-bac5-417e4488cdb8`)
- spec-drift steps 1–9 (gap filing): not run
- spec-drift steps 10–11 (stale-issue sweep, preview-branch housekeeping):
  **not run either** — step 10 needs to list/comment on Linear issues, which
  also requires Linear MCP. (Step 12, OpenSpec archive sweep, is the one
  piece that doesn't need Linear — see below.)
- bug-error: not run
- market-feature: not run

**No `data/sweep-runs.jsonl` entry was appended for this run.** Appending
`{"clean": true, ...}` would misrepresent history — the sweep didn't execute,
it was blocked before it could determine cleanliness. Leave the ledger as-is
until a real run completes; don't backfill a synthetic entry for
2026-08-21.

## One thing worth noting independent of the Linear blocker

`agents/bug-error.md` reads "Vercel production runtime logs/errors" for the
target repo. AI Landscape 2026's prod URL in `projects.md` is
`https://rohrasharad-ship-it.github.io/ai-landscape/` — **GitHub Pages, not
Vercel.** There's no Vercel deployment to pull runtime logs from for this
project. When a working session eventually runs bug-error for AI Landscape,
it will need a different signal source (GitHub Pages doesn't expose runtime
error logs the way Vercel does) — browser console errors captured via
Playwright against the live URL is the most likely substitute, but that's a
process gap worth flagging to Sharad rather than silently improvising.

## What was and wasn't attempted

| Step | Result |
|---|---|
| Read `routines/idea-sweep.md`, `routines/README.md`, `projects.md` | ✅ done |
| Read `agents/shared/issue-cap.md`, `agents/spec-drift.md`, `agents/bug-error.md`, `agents/market-feature.md` | ✅ done |
| Read `agents/shared/conventions.md` | ✅ done |
| `ToolSearch` for any Linear MCP tool | ✅ done — none found |
| `ListConnectors(["Linear"])` | ✅ done — confirms connector present but not usable this session |
| Any `list_issues` / `create_issue` / comment call | ❌ not attempted — no tool available to call |
| GitHub-side reading of `openspec/` for AI Landscape (spec-drift step 1–2 groundwork) | ❌ not done — filing issues afterward wasn't possible anyway, so this would have been wasted analysis with no output; better to hand off cleanly than half-run |

## Instructions for receiving agent

1. Confirm Linear MCP tools are available in your session (`ToolSearch` a
   Linear keyword, or check they're already loaded).
2. Run `routines/idea-sweep.md` for **AI Landscape 2026** from scratch,
   following it exactly — this handover changes nothing about the routine
   itself, it's purely a "the last attempt didn't run" note.
3. After the real run completes, append the `data/sweep-runs.jsonl` entry
   yourself per the routine's Output section, and run
   `node scripts/generate-routine-log.mjs`.
4. Consider raising the GitHub-Pages-vs-Vercel gap above with Sharad (or file
   a `spec-needed` issue in **PM OS** about it) if bug-error keeps needing to
   run against AI Landscape — this handover intentionally does not file that
   issue itself since it hits the exact same Linear-access blocker.
5. Delete this handover file once a real idea-sweep run for AI Landscape 2026
   has completed.
