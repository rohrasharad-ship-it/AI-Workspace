# Handover: idea-sweep (AI Landscape) blocked — Linear MCP not connected

**For:** Any agent/session with Linear MCP access to the AI Landscape project
**From:** idea-sweep routine (spec-drift + bug-error + market-feature), automated run, 2026-09-14
**Blocked by:** Linear connector not authorized in this session — `ListConnectors`
reports `{"name":"Linear","connected":false,"installState":"connect_incomplete"}`.
No Linear MCP tools were exposed at all, so the mandatory Issue Cap pre-flight,
dedupe search, issue creation, and stale-issue comment sweep could not run for
any of the three roles.
**Action:** Once Linear is connected, run the Issue Cap pre-flight for AI
Landscape (Linear Project ID `4ef7d096-f5bb-44f4-bac5-417e4488cdb8`), then
dedupe-search and file the candidates below.
**Issue:** N/A — no Linear issue exists yet for this handover; it is filed as
a repo handover precisely because Linear itself was the blocked tool.

## What ran / what didn't this cycle

- **Issue Cap pre-flight**: could not run (needs Linear `list_issues`). Do
  this first before filing anything below — if AI Landscape is already at 5
  active pipeline issues (Backlog/Todo/In Progress/In Review), stand down on
  filing per `agents/shared/issue-cap.md`.
- **bug-error**: ran cleanly, no blocker. Checked Vercel project
  `prj_qCYQn9V1nrGNrUYdar5L0KVuqyu0` (`ai-landscape`) runtime errors for the
  last 7 days via `get_runtime_errors` — **zero errors**. Nothing to file for
  this role.
  - Side-fix already pushed to this branch, independent of Linear:
    `projects.md` had a stale prod URL for AI Landscape (a GitHub Pages URL;
    the project is actually on Vercel at `https://ai-landscape-ten.vercel.app/`,
    confirmed against the target repo's own `openspec/project.md`, `AGENTS.md`,
    `README.md`, and `vercel.json`, plus a matching live Vercel project). Fixed
    in commit `31c4be8758b5f693bc0ea374a963dd73891056eb` on this branch — the
    stale entry would have made Vercel-log bug-error checks silently no-op for
    this project going forward.
- **spec-drift**: gap-filing steps 1–9 (Linear dedupe + create) blocked, but
  the full spec-vs-code comparison across all 7 capabilities was still done
  read-only (via a research subagent reading the live `index.html` in full
  against every capability's spec.md) — see candidates below. Steps 10–11
  (stale-issue Linear comment sweep, preview-branch cleanup) are also blocked
  — both need Linear (comment/read access, and `LINEAR_API_KEY` for the
  cleanup script's issue-state lookups). Step 12 (openspec archive sweep) was
  skipped this cycle: no local git checkout with push credentials was
  available in this session to run
  `scripts/archive-merged-openspec-changes.sh`; the weekly GitHub Action
  (`.github/workflows/openspec-archive.yml`) already covers this as the
  documented structural backup.
- **market-feature**: the proposal step (read vision + specs, pitch up to 3
  features) was completed read-only — see candidates below. Filing blocked by
  Linear.
- **Screenshots / visual previews** (mandatory for every filed issue) were
  not taken — no point capturing them before Linear is connected and dedupe
  search can rule out duplicates. The receiving agent should take fresh ones
  per `agents/shared/visual-self-qa.md` at filing time so they reflect the
  current site, not stale ones from this handover.

## Payload — candidates to file once Linear is connected

All candidates: status Backlog, label `spec-needed` (never `agent-ready`),
assignee Sharad Rohra, Issue Brief description format
(`agents/shared/issue-brief.md`).

### spec-drift candidates

1. **🔍 Mobile search doesn't match tool ID, unlike desktop**
   - Problem: Desktop search (`isVisible()` in `index.html`, ~line 1946)
     matches a query against `name`, `id`, `category`, and `subCat`. The
     mobile card-filtering predicate (~line 2273) only matches `name`,
     `category`, and `subCat` — it never checks `id`. Tools whose `id`
     differs meaningfully from their display `name` — e.g. id
     `"Runway Gen-4.5"` vs name `"Runway"`, id `"Google Veo 3.1"` vs name
     `"Google Veo"`, id `"Kling 2.6/3.0"` vs name `"Kling"` — are findable by
     that string on desktop but return nothing on mobile.
   - Spec basis: `openspec/specs/search-filters/spec.md`, Requirement
     "Desktop search matches category text" / Scenario "Desktop search
     parity with mobile" — explicitly requires the same result set on both
     surfaces for the same query.
   - Where: `index.html`, mobile `render()` filter predicate (~line 2273) vs
     desktop `isVisible()` (~line 1946).
   - Suggested priority: Medium — real, reproducible UX inconsistency; not
     core-flow breaking.

2. **📅 Freshness-stamp build script has drifted line ranges, may under-report catalog updates**
   - Problem: `scripts/inject-catalog-freshness.js` hardcodes
     `CATALOG_RANGES = [[271,465],[469,844]]` to `git blame` the
     `NODES`/`LINKS_RAW` arrays for the "Updated Mon YYYY" freshness stamp.
     The arrays have since moved to roughly lines 317–512 and 515–891 — about
     46 lines of drift — so the blame misses the tail of both arrays,
     including the most recently added Image/Video/Music-gen link fixes
     around lines 866–891. The displayed freshness date can be older than the
     true last catalog edit.
   - Spec basis: `openspec/specs/radial-map/spec.md` Requirement "Desktop
     title shows catalog freshness" and
     `openspec/specs/mobile-experience/spec.md` Requirement "Mobile header
     shows catalog freshness" — both require the stamp to reflect the latest
     catalog change date.
   - Where: `scripts/inject-catalog-freshness.js` (`CATALOG_RANGES` constant).
   - Note for the spec conversation (not an implementation instruction): a
     fix would need to locate the array boundaries dynamically (e.g. regex
     for the `const NODES = [` / `const LINKS_RAW = [` opening lines and
     their matching closing `];`) instead of hardcoded line numbers, so it
     can't silently drift again.
   - Suggested priority: Low/Medium — cosmetic date accuracy, not a
     functional break.

Everything else checked — radial-map (ring-label toggle survival, zoom
clipping), relationship-path-finder (resolve/BFS/animate/callout/clear),
detail-panels (visible-connections-only + live filter update), the mobile
14-pill connection cap and show-more/less control, data-catalog's
Image/Video/Music-gen `LINKS_RAW` coverage (Midjourney, Ideogram, Recraft,
Runway, Luma AI, Pika, Udio) and bubble-key resolution, and deployment
reachability/README link — all matched their spec. No gap to file for those.

### market-feature candidates (cap 3 — file only what survives dedupe)

1. **🔗 Shareable deep-link state** — Encode the current selection, active
   path-finder from/to, filters, and zoom transform into the URL
   (hash/query string) so any specific view (e.g. "the Nvidia → Bedrock
   chain") is copy-paste shareable. Fits the vision: turns the map into
   something people can point colleagues at instead of a one-shot
   exploration tool. Fully client-side — `history.replaceState` +
   `URLSearchParams` on every filter/select/path change, parsed back on
   load to replay `applyFilters()` / the path-finder / the zoom transform.
   No backend, no auth.
2. **⚖️ Compare-two-tools side-by-side view** — Pick any two nodes (e.g.
   Cursor vs. Windsurf) and see a split panel of their category,
   popularity, description, and shared-vs-distinct connections. Fits the
   vision: a new lens on data that already exists in `NODES`/`LINKS_RAW`,
   extending the existing side-panel/connection-exploration UX rather than
   adding new surface area. Reuses `#side-panel` markup and a shared
   connection-list renderer, triggered from a new "Compare" affordance on
   the tooltip/panel.
3. **⌨️ Keyboard-driven navigation** — Arrow keys step between sibling
   nodes in the current ring/category, Enter opens the panel, `/` focuses
   search, Esc clears selection, `?` shows a shortcuts overlay. Fits the
   "fast, interactive" positioning as a power-user/accessibility
   differentiator. Pure event-wiring on top of the existing
   `selectNode()` / `openSidePanel()` / `clearSelection()` functions — no
   new data or state model.

None of the three need a backend, auth, or personalization — all stay within
`openspec/project.md`'s Out of Scope constraints.

## Instructions for receiving agent

1. Connect/verify Linear MCP access, then run the Issue Cap pre-flight for AI
   Landscape (`agents/shared/issue-cap.md`, project ID
   `4ef7d096-f5bb-44f4-bac5-417e4488cdb8`).
2. If under cap: dedupe-search Linear for each candidate above, then file the
   ones that survive dedupe, following `agents/spec-drift.md` /
   `agents/market-feature.md` and the Issue Brief format
   (`agents/shared/issue-brief.md`), each with a fresh Playwright screenshot
   per `agents/shared/visual-self-qa.md` — do not reuse or fabricate a
   screenshot; none were taken during this run.
3. No need to re-run the bug-error Vercel check unless significant time has
   passed since 2026-09-14 — this cycle already confirmed zero runtime errors
   over the prior 7 days.
4. File spec-drift and market-feature candidates as `spec-needed`, never
   `agent-ready` — a spec conversation still needs to happen before either is
   built.
5. Once every candidate here is filed (or explicitly rejected as not worth
   filing), delete this handover file.
