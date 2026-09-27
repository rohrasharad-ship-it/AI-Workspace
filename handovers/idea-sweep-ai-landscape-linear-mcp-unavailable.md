# Handover: idea-sweep for AI Landscape 2026 — Linear MCP unavailable this session

**For:** Any agent/session with working Linear MCP access (this is a different, more
severe blocker than `handovers/preview-branch-cleanup-linear-api-key.md` — that one is
about a missing `LINEAR_API_KEY` *repo secret* for two shell scripts, while this session
had no Linear MCP *tool* connected at all, so it couldn't even count issues or search
Linear, let alone file anything)
**From:** idea-sweep routine run (all three roles) for AI Landscape 2026, scheduled/automated run, 2026-09-27
**Blocked by:** The Linear MCP server was listed as requiring OAuth authorization
("This session is non-interactive, so Claude cannot run the OAuth flow here") — no
`mcp__Linear__*` tools were available at any point in the session. Every step that needs
Linear was skipped as a result:
- Issue Cap pre-flight (`agents/shared/issue-cap.md`) — could not count active pipeline issues for AI Landscape (Linear Project ID `4ef7d096-f5bb-44f4-bac5-417e4488cdb8`).
- spec-drift steps 4–9 (dedupe search + file) — skipped, no gaps found anyway (see below).
- spec-drift step 10 (stale-issue sweep) — could not list/comment on open Backlog issues.
- market-feature steps 4–9 (dedupe search + file) — 3 draft ideas below are **not** deduped against Linear.
- bug-error steps 3–7 (dedupe + file) — moot, production is clean (see below), nothing to file.

**Action:** Once Linear MCP is reconnected (user reconnects via claude.ai connector
settings, since this can't be done from a non-interactive session), a session with
working Linear access should: (1) run the Issue Cap check for AI Landscape, (2) if under
cap, search Linear and file whichever of the 3 market-feature drafts below aren't already
tracked, each with a screenshot per `agents/shared/visual-self-qa.md`, (3) run the
spec-drift stale-issue sweep on AI Landscape's open Backlog issues.

## What I could still verify without Linear (repo + Vercel access both worked fine)

**Vercel production (bug-error, steps 1–2):** `get_runtime_errors` on project
`prj_qCYQn9V1nrGNrUYdar5L0KVuqyu0` (team `team_P5vgMhFNfh2d4fCe2YkRLjey`), last 24h —
**zero runtime errors.** Nothing for bug-error to file even once Linear is back.

**Spec vs. code (spec-drift, steps 1–3):** Read `openspec/project.md` and all six
capability specs (`radial-map`, `relationship-path-finder`, `search-filters`,
`detail-panels`, `mobile-experience`, `data-catalog`), plus `deployment/spec.md`. Cross-
checked the two currently-active (non-archived) OpenSpec changes against the shipped
code via `search_code`/grep on `index.html`:
- `presentation-mode` — tasks all checked off; confirmed `presentMode` and `Find Path`
  strings are actually present in `index.html` (11 and 2 occurrences respectively). Shipped.
- `last-updated-freshness-stamp` — tasks all checked off; confirmed
  `scripts/inject-catalog-freshness.js` exists and the corresponding requirements are
  already written into `radial-map/spec.md` and `mobile-experience/spec.md`. Shipped.

**No new spec-drift gap found** — the six capability specs read as accurate descriptions
of what's actually built; nothing meaningfully planned-but-unbuilt turned up.

**Housekeeping opportunity (not executed this run):** Both change folders above look
ready for `npx openspec archive <name> -y --skip-specs` per
`agents/spec-drift.md` step 12. I did **not** attempt this myself because:
1. `agents/spec-drift.md` step 12 says completed change folders "live in AI-Workspace,"
   but for this project they live in `rohrasharad-ship-it/ai-landscape` itself
   (`openspec/changes/last-updated-freshness-stamp`, `.../presentation-mode`) — the
   routine doc's step 12 instructions don't match this repo's actual layout. Worth fixing
   in `agents/spec-drift.md` (either generalize step 12 to "run in the target repo" or
   clarify it's AI-Workspace-specific).
2. The sweep script (`scripts/archive-merged-openspec-changes.sh`) needs `gh` CLI for its
   open-PR check, which isn't available in this session's tool access, and running
   `npx openspec archive` + pushing to `ai-landscape` without that safety check felt like
   more risk than a scheduled/unattended run should take on someone else's spec directory.
   A session with real shell + `gh` access should run
   `bash scripts/archive-merged-openspec-changes.sh --sweep` **inside a clone of
   `ai-landscape`** (not AI-Workspace) to archive both.

**Small fix I did make directly (no Linear needed):** `projects.md` listed AI Landscape's
Vercel Prod as a GitHub Pages URL (`https://rohrasharad-ship-it.github.io/ai-landscape/`),
but `README.md`, `openspec/project.md`, and `openspec/specs/deployment/spec.md` in the
target repo all agree the real production URL is `https://ai-landscape-ten.vercel.app/`
(confirmed live via Vercel's own project listing). Corrected in this same commit.

## Market-feature candidates (drafted, NOT deduped against Linear — search before filing)

Read `openspec/project.md`'s vision/non-negotiables/out-of-scope. All three respect
"no backend," "no real-time ingestion," and "don't replatform."

### 1. 🔗 Shareable deep link to a selection or path

**In short:** Shareable map links

**Problem:** Anyone who finds an interesting path or node on the map has no way to send
someone straight to that exact view — they can only share the bare homepage URL.

**Solution:** Encode the current selection or Find-Path result in the URL so opening the
link reproduces the same focused view.

**Why:** The map's best moments (e.g. "here's how Nvidia connects to Claude in 3 hops")
are exactly what people want to screenshot or tweet — a working link makes it a click
instead of a screenshot.

**What it looks like:** A "Copy link" action next to the existing "Copy LinkedIn blurb"
button that copies a URL like `?path=Nvidia,Claude` or `?node=Claude`; opening it restores
that selection/path automatically.

### 2. ⚖️ Compare two tools side-by-side

**In short:** Side-by-side tool compare

**Problem:** Deciding between two similar tools (e.g. two image-gen models) means
clicking each one's panel separately and remembering what the first one said.

**Solution:** A compare view that shows two nodes' detail panels side by side.

**Why:** Comparison is one of the most common reasons someone explores a landscape map in
the first place — the current single-panel flow makes it more work than it needs to be.

**What it looks like:** Selecting a second node while holding a modifier (or a small "+compare"
button on the open panel) splits the side panel into two columns, same fields as today.

### 3. 🖼️ Export current view as a shareable image

**In short:** Export map as image

**Problem:** The only way to share what the map currently shows (a filtered view, a found
path, a presentation-mode shot) is an ad hoc OS screenshot.

**Solution:** A one-click "Save image" that exports the current SVG view as a PNG.

**Why:** This is a visual product built to be shown off (talks, social posts) — presentation
mode already optimizes for showing it live, but there's no matching way to take a piece of
it away afterward.

**What it looks like:** A camera-icon button near the existing zoom controls that downloads
a PNG snapshot of the current canvas, cropped to the visible viewport.

## Instructions for receiving agent

1. Confirm Linear MCP is connected (try `list_issues` on project ID `4ef7d096-f5bb-44f4-bac5-417e4488cdb8`).
2. Run the Issue Cap check (`agents/shared/issue-cap.md`) for AI Landscape before filing anything.
3. If under cap: search Linear for each of the 3 ideas above; file whichever aren't already
   tracked, in Issue Brief format, with a screenshot per `agents/shared/visual-self-qa.md`
   and a minimal-effort visual preview per `agents/shared/visual-specs.md`.
4. Run spec-drift step 10 (stale-issue sweep) on AI Landscape's open Backlog issues.
5. Consider running `scripts/archive-merged-openspec-changes.sh --sweep` inside a clone of
   `ai-landscape` (not AI-Workspace) to archive `presentation-mode` and
   `last-updated-freshness-stamp` — both look fully shipped.
6. Delete this handover file once Linear filing + stale-sweep are done for this cycle.
