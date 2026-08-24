# Handover: idea-sweep for AI Landscape 2026 — no Linear MCP access this session

**For:** Any agent whose session has Linear MCP tools available (authorized/connected)
**From:** idea-sweep routine (spec-drift + bug-error + market-feature), triggered for "AI Landscape" (project.md: AI Landscape 2026), 2026-08-24
**Blocked by:** This session's Linear MCP connector reported "requires authentication before its tools can be used" — no `list_issues`, `search_issues`, `create_issue`, or `create_comment` equivalents were available at any point in the run. This is a connector-auth state, not a missing secret like the recurring `LINEAR_API_KEY` blocker tracked in `handovers/preview-branch-cleanup-linear-api-key.md` — it needs Sharad to reconnect Linear under claude.ai connector settings (or the equivalent for whatever client started this scheduled run), not a repo secret.
**Action:** Once Linear MCP is available in a session: (1) run the Issue Cap pre-flight for AI Landscape (`agents/shared/issue-cap.md`, Linear Project ID `4ef7d096-f5bb-44f4-bac5-417e4488cdb8`), (2) if under cap, search Linear for the candidate below and file it if it's not already tracked (Issue Brief format, Backlog + `spec-needed`, assignee Sharad Rohra, screenshot via Playwright), (3) optionally consider the two speculative feature ideas below, (4) run the stale-issue sweep (spec-drift step 10) against AI Landscape's open Backlog issues, which this session could not do at all.
**Issue:** N/A — no Linear issue drives this session; this is a routine (cron) trigger, not an assigned issue.

## What this session could and couldn't do

No Linear MCP, no Vercel MCP tools loaded, no Playwright/browser tool available, and
network egress to `ai-landscape-ten.vercel.app` was blocked by this session's proxy policy
(`EGRESS_BLOCKED`). That rules out: the Issue Cap check, Linear search/dedupe, filing,
commenting, the stale-issue sweep, mandatory screenshots, and bug-error's "read Vercel
runtime logs" and "check the live site" steps entirely. Bug-error found nothing to report
this run **only because it couldn't check** — treat this as "not run," not "clean."

What *was* possible without any of those tools: reading the target repo's `openspec/`
specs and `index.html` via GitHub MCP (read-only, no auth needed) and comparing them
line-by-line. That surfaced one real, verifiable gap below.

## Payload — 1 spec-drift/bug candidate (ready to file as-is)

**🐛 Catalog freshness stamp uses stale hardcoded line ranges, will silently drift further**

- **In short:** The "Updated Mon YYYY" freshness label (required by
  `openspec/specs/radial-map/spec.md` and `openspec/specs/mobile-experience/spec.md`) is
  computed from `git blame` on hardcoded line ranges in
  `scripts/inject-catalog-freshness.js` that no longer match where `NODES`/`LINKS_RAW`
  actually live in `index.html`.
- **Problem:** `scripts/inject-catalog-freshness.js` defines
  `CATALOG_RANGES = [[271,465],[469,844]]` as the line spans for `NODES` and `LINKS_RAW`.
  In the current `index.html` (commit `f580b488`), `NODES` actually spans lines 317–512
  and `LINKS_RAW` spans lines 515–891 — both arrays have drifted 46 lines from what the
  script blames. So the build-time freshness date is computed from the wrong lines: partly
  from unrelated CSS/markup above the real `NODES` start, and missing roughly the last 47
  lines of each array entirely. This isn't cosmetic — the spec explicitly requires the
  stamp to reflect "the latest catalog change date," and every future edit to the tail of
  either array (very plausible, since new tools/links are appended) won't move the
  displayed date at all.
- **Solution:** Don't hardcode line numbers. Locate `NODES`/`LINKS_RAW` by pattern (e.g.
  find the line matching `^const NODES = \[` through the matching `^\];`, same for
  `LINKS_RAW`) before running `git blame`, or blame the whole file and filter by content
  instead of by line range.
- **Why:** Freshness is a trust signal for a "keep the catalog current" product — a stamp
  that quietly stops updating undermines the one thing it's there to prove. Confidence is
  high on the line-range drift itself (directly diffed the script's constants against the
  live line numbers); confidence is lower on real-world *impact* since this session
  couldn't reach the production URL to see what date is actually displayed today — that's
  the one thing the receiving agent should check first (Playwright screenshot of the title
  area, or view source) before filing, since if `git blame` still resolves to correct-ish
  content by luck (both ranges still fall inside the right array, just clipped), the
  displayed date might currently be *close enough* to correct rather than visibly wrong.
- **What it looks like:** Not visual by itself (it's a build-script bug) — no mockup
  needed. Do still take the mandatory screenshot of the current title/freshness area per
  `agents/shared/visual-self-qa.md` once Linear access exists, both as the required
  attachment and to confirm current on-page behavior before filing.
- **Dedupe:** Could not search Linear (no MCP access) — search terms to use once available:
  "freshness", "Updated", "catalog freshness", "inject-catalog-freshness".
- **Suggested labels/fields:** Backlog, `spec-needed`, assignee Sharad Rohra, title
  `🐛 Catalog freshness stamp drifts from stale hardcoded line ranges`, priority Medium
  (data-integrity bug, not user-facing breakage — the page still loads and shows *a* date).

## Two market-feature candidates (speculative, not verified against Linear — dedupe first)

Grounded in `openspec/project.md`'s vision ("explore tools... through their relationships")
and non-negotiables (static, no backend, no auth). Cap is 3 per market-feature run; these
are only 2 — did not want to invent a filler third just to hit the cap, per
`agents/market-feature.md` step 9.

1. **🔗 Shareable filtered view (URL state)** — Encode active filters (search term,
   category, popularity/link-weight thresholds, selected node) into the URL query string
   so a filtered/focused view can be copy-pasted or linked, not just the raw homepage.
   Fits "Iterating in public" positioning in the README and needs zero backend — pure
   client-side `URLSearchParams`, consistent with the Out of Scope constraint against new
   infra. Ties to differentiation: most competing "landscape map" content is static
   images; a live, linkable, filtered view is something only this interactive format can
   do.
2. **🕰️ "How we got here" layer-history toggle** — Given the catalog already tracks a
   freshness/change date per entry (once the bug above is fixed), a lightweight toggle
   that dims nodes added before a chosen month lets readers see how a layer (e.g.
   Frameworks & Infra) grew over 2026. Speculative and depends on the freshness bug being
   fixed first to have real per-node dates, not just one whole-catalog stamp — flag that
   dependency to Sharad rather than treating it as ready to build.

## What was explicitly NOT done (blocked, not skipped)

- Issue Cap pre-flight for AI Landscape — not run (needs Linear MCP `list_issues`
  filtered by Linear Project ID `4ef7d096-f5bb-44f4-bac5-417e4488cdb8`).
- Linear dedupe search for the candidate above and the two feature ideas — not run.
- Filing any issue, or posting any first comment — not run.
- spec-drift step 10 (stale-issue sweep on AI Landscape's open Backlog issues) — not run,
  needs Linear MCP.
- spec-drift steps 11–12 (preview-branch cleanup, openspec archive sweep in AI-Workspace)
  — not attempted this run; both already have a live, unresolved handover
  (`handovers/preview-branch-cleanup-linear-api-key.md`) tracking a separate blocker
  (`LINEAR_API_KEY` secret + proxy blocking mutating git operations) — no new information
  to add there this run.
- bug-error (Vercel runtime logs + live-site check) — not run at all: no Vercel MCP tools
  were loaded in this session and direct network egress to
  `https://ai-landscape-ten.vercel.app/` was blocked by the session's own proxy policy
  (`EGRESS_BLOCKED`). Do not read this run's "0 bugs" as a clean bill of health for
  production errors — it's an untested surface.
- Mandatory Playwright screenshots (`agents/shared/visual-self-qa.md`) — not possible, no
  browser/Playwright tool was available in this session's toolset.

## Also fixed directly this run (no Linear needed, low-risk factual correction)

`projects.md`'s "Vercel Prod" column for AI Landscape 2026 listed
`https://rohrasharad-ship-it.github.io/ai-landscape/` (a GitHub Pages URL). That's stale —
`openspec/specs/deployment/spec.md`, `README.md`, and `AGENTS.md` in the target repo all
agree the real production URL is `https://ai-landscape-ten.vercel.app/`, and `vercel.json`
confirms the project actually deploys to Vercel. Corrected in the same commit as this
handover. If the GitHub Pages URL is intentional and separate infra, ignore/revert this
row — but nothing in the target repo referenced it, so it read as leftover from before the
project moved to Vercel.

## Instructions for receiving agent

1. Confirm Linear MCP tools are available (they weren't for this session).
2. Run the Issue Cap check for AI Landscape (Project ID `4ef7d096-f5bb-44f4-bac5-417e4488cdb8`).
3. If under cap: search Linear for the freshness-stamp candidate above; if not already
   tracked, verify current production behavior (view source or screenshot of the title
   area) before filing, then file per the Payload section, with the mandatory screenshot.
4. Optionally search + consider filing the two feature ideas (dedupe first; these are
   genuinely speculative, feel free to judge them not worth filing).
5. Run spec-drift step 10 (stale-issue sweep) for AI Landscape's open Backlog issues —
   this session could not do this at all.
6. Delete this handover file once the above is complete and tracked in Linear — until
   then it's the record of what this run found and couldn't act on.
