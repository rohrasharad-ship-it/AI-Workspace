# Handover: idea-sweep for AI Landscape 2026 blocked — no Linear MCP access this session

**For:** Any agent/session with Linear MCP access
**From:** idea-sweep routine run for AI Landscape 2026, Claude Code (web/scheduled session), 2026-09-19
**Blocked by:** This session's Linear MCP server is listed as requiring authorization it
cannot complete (non-interactive session — no OAuth flow available). Every idea-generation
role needs Linear for the issue-cap pre-flight, dedupe search, filing, and the stale-issue
sweep (`agents/shared/issue-cap.md`, `routines/idea-sweep.md` steps 1–10 across all three
roles). None of that could run. This is a different, more fundamental gap than the
`LINEAR_API_KEY`-for-GitHub-Action problem tracked in
`handovers/preview-branch-cleanup-linear-api-key.md` — that one blocks a shell script;
this one blocks the Linear MCP tool itself, so no session-side Linear call of any kind was
possible (not `list_issues`, not `create_issue`, not `create_comment`).
**Action:** Whoever restores or has Linear MCP access should (a) run the Issue Cap
pre-flight for the **AI Landscape** Linear project (ID `4ef7d096-f5bb-44f4-bac5-417e4488cdb8`
from `projects.md`), then (b) dedupe-search and file the 3 market-feature candidates below
if still under cap and still not already tracked, each with a visual preview + live-site
screenshot per `agents/shared/visual-specs.md` / `agents/shared/visual-self-qa.md` (neither
was produced this session — no Playwright/browser tool was available either).
**Issue:** N/A — this is a routine-triggered run, not a Linear-issue-driven session, so
there is no driving issue ID to link.

## Payload — this run's findings, per role

### bug-error — clean, nothing to file

Checked `mcp__Vercel__get_runtime_errors` for project `prj_qCYQn9V1nrGNrUYdar5L0KVuqyu0`
(team `team_P5vgMhFNfh2d4fCe2YkRLjey`), last 24h: **no runtime errors**. Vercel access
worked fine this session (unlike Linear) — this part of the role isn't blocked, it's just
genuinely clean. No dedupe/filing needed either way.

### spec-drift — no meaningful built-vs-specced product gaps found

Read `openspec/project.md` and all 7 capability specs (`radial-map`,
`relationship-path-finder`, `search-filters`, `detail-panels`, `mobile-experience`,
`data-catalog`, `deployment`) against the current `index.html`. Spot-checked several
specific requirements end-to-end (LinkedIn-blurb copy button, mobile capped-connections
"show more" control, generative-media node connections for Midjourney/Runway/Udio) — all
present in code as specced. This matches the last 5 sweep-ledger entries for this project
(all `clean:true`, 2026-08-02 through 2026-08-15) — AI Landscape's spec is well-maintained.
Per step 9, nothing meaningful → **nothing to file**, independent of the Linear blocker.

**Non-Linear housekeeping note (not a filed issue, just flagging):** two change folders in
**ai-landscape's own** `openspec/changes/` are fully implemented (all tasks checked, merged
2026-07-23, PR #17/#18, no open PR since) but never archived:

- `last-updated-freshness-stamp` — its spec delta **was** already manually merged into
  `openspec/specs/radial-map/spec.md` and `openspec/specs/mobile-experience/spec.md`, so
  this one is a pure folder-move once someone runs `npx openspec archive
  last-updated-freshness-stamp` (or the equivalent sweep script) with real push access to
  `ai-landscape`.
- `presentation-mode` — the feature is fully shipped in `index.html` (`presentMode` state,
  `setPresentMode`, the `#present-toggle` button all present and wired), but its spec delta
  was **never** merged: there's no `openspec/specs/presentation-mode/spec.md`, no
  present-mode requirement in `radial-map/spec.md`, and `openspec/project.md`'s Capabilities
  list doesn't mention it. Archiving this one needs the actual `openspec archive` merge
  step, not just a folder move — otherwise the capability stays permanently undocumented.

This is outside `agents/spec-drift.md` step 12's literal scope (that step only sweeps
**AI-Workspace's own** `openspec/changes/`, which I confirmed is still empty/clean — see the
update I added to `handovers/preview-branch-cleanup-linear-api-key.md`). I did not attempt
to move or edit these files myself: this session only has GitHub MCP file read/write (no
`openspec` CLI, no arbitrary shell+git push to `ai-landscape`), and hand-editing a spec
delta without the CLI's merge logic risks getting `presentation-mode`'s spec wrong. Whoever
picks this up should run the real `openspec archive` command against `ai-landscape` for
both change folders.

### market-feature — 3 candidates, ready to file once Linear access exists

Read `openspec/project.md` (vision: public interactive AI-ecosystem map; non-negotiables:
stay static/no-backend, preserve search/filter/selection/connection exploration; out of
scope: accounts/auth, real-time backend/API ingestion, replatforming off static HTML) and
all 7 specs. None of these three appear already built or specced. **Not filed** — Linear
dedupe search against the AI Landscape project's existing backlog still needs to run before
filing (I could not do it this session); treat these as candidates to verify, not
pre-cleared.

1. **In short:** Shareable map permalink
   **Problem:** The existing "Copy LinkedIn blurb" button shares text about one tool, but
   there's no way to link someone straight into the *interactive state* you're looking at —
   a filtered view, a selected node, an active path — they land on the default map.
   **Solution:** Encode the current selection/filter/path state into the URL (query string)
   so a copied link reopens the map exactly as it was shared.
   **Why:** A map you can deep-link into is far more shareable on social/Slack than one that
   always resets to the same default view — directly extends a feature that already exists.
   **What it looks like:** A "Copy link to this view" action next to the existing LinkedIn
   button; opening the copied URL restores the same selection/filters/path.
   Suggested priority: Medium. Fits the static/no-backend constraint (pure client-side URL
   state) and doesn't touch anything Out of Scope.

2. **In short:** Compare two tools
   **Solution:** A side-by-side view of two selected nodes' descriptions, popularity, and
   connections — reusing existing detail-panel data, no new data model.
   **Problem:** Readers exploring competitors (e.g. two image-gen tools) have to click back
   and forth between detail panels and hold the comparison in their head.
   **Why:** Direct tool-vs-tool comparison is a common way readers actually use landscape
   maps and isn't offered by most static ecosystem infographics — a real differentiator.
   **What it looks like:** Selecting a second node while one is already selected offers a
   "Compare" option that opens a two-column panel instead of replacing the first selection.
   Suggested priority: Low. Speculative and a UI-interaction-model change (how selection
   works today) — good candidate for spec-conversation to scope down.

3. **In short:** Market-emergence timeline
   **Problem:** The map only shows the ecosystem as it looks today — it doesn't tell the
   story of *when* each layer or tool emerged, even though "how fast this moved" is a big
   part of the AI story in 2026.
   **Solution:** An optional timeline control that reveals nodes progressively by a
   first-appeared year/quarter, turning the static snapshot into a "how we got here" replay.
   **Why:** Differentiates from single-point-in-time competitor landscape maps and fits the
   product's own framing ("AI Landscape 2026").
   **What it looks like:** A slider or play button that animates nodes appearing in
   chronological order, dimming everything not yet "arrived."
   Suggested priority: Low. Flagging the main cost honestly: needs a first-appeared
   date/quarter added to all ~156 catalog nodes — a real data-entry lift, not just UI — so
   this is the most speculative of the three; good candidate to scope down or drop in
   spec-conversation if the data cost isn't worth it.

None of these have a visual preview or live-site screenshot yet (mandatory before filing,
per the shared guardrails) — this session had no Playwright/browser tool available on top
of the Linear gap.

## Instructions for receiving agent

1. Confirm Linear MCP access works, then run the Issue Cap pre-flight for **AI Landscape**
   (`projects.md` Linear Project ID `4ef7d096-f5bb-44f4-bac5-417e4488cdb8`) per
   `agents/shared/issue-cap.md`.
2. If under cap: dedupe-search the 3 market-feature candidates above against the AI
   Landscape Linear project; file whichever aren't already tracked as Backlog +
   `spec-needed`, assignee Sharad Rohra, title with one leading emoji, Issue Brief
   description (content above), suggested priority as noted. Attach a visual preview
   (`agents/shared/visual-specs.md`) and a real Playwright screenshot of the current
   homepage (`agents/shared/visual-self-qa.md`) to each before creating it, and post the
   first-comment execution detail (this handover as the source, vision/spec files read,
   Linear search terms used) per `agents/shared/issue-brief.md` rule 9.
3. Also run the stale-issue sweep (`agents/spec-drift.md` step 10) for AI Landscape — this
   session could not touch it at all.
4. Optionally file a small chore issue (or just run it directly) to archive the two
   `ai-landscape` OpenSpec change folders described above, with real `openspec` CLI access
   to that repo.
5. Delete this handover file once Linear-side filing (or a decision not to file) for this
   run is complete — the candidates above are then tracked in Linear, not here.
