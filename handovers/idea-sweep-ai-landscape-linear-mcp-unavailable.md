# Handover: idea-sweep routine for AI Landscape 2026 blocked — Linear MCP not authenticated in this session

**For:** Any agent/session with a working, authenticated Linear MCP connection
**From:** idea-sweep routine run (spec-drift + bug-error + market-feature) for AI Landscape 2026, triggered 2026-09-09, Claude Code (web/scheduled session)
**Blocked by:** The Linear MCP server is not authenticated for this session. It doesn't appear in the callable tool list at all — the harness flagged it up front: "The following MCP servers require authentication before their tools can be used: Linear... This session is non-interactive, so Claude cannot run the OAuth flow here." A follow-up tool search for any Linear-shaped tool (list/search/create/comment issue) returned nothing. This is a **connector-auth gap for this session**, not a structural problem — `handovers/preview-branch-cleanup-linear-api-key.md` shows many prior idea-sweep sessions used Linear MCP successfully (list_issues, create, comment) across 270+ SHA issues, so this looks like the Linear connector simply needs to be reconnected/re-authorized for future automated/scheduled sessions (see claude.ai Settings → Connectors, or however this account's Linear connector is provisioned for scheduled runs).
**Action:** Re-authorize the Linear MCP connector for this account/session type, then have an agent resume the idea-sweep for AI Landscape 2026 using the prepared work below (no need to redo the analysis, just the Linear-side steps).
**Issue:** N/A — this is a routine-level block, not a single Linear issue (the routine never got far enough to check the issue cap, so no Linear issue was created or updated this run).

## What this blocks

Per `routines/idea-sweep.md` and the three role files, almost everything downstream of the pre-flight requires Linear MCP:
- The **Issue Cap pre-flight** itself (`agents/shared/issue-cap.md`) needs `list_issues` filtered by Linear Project ID — couldn't even confirm whether AI Landscape (`4ef7d096-f5bb-44f4-bac5-417e4488cdb8`) is under its cap of 5 active pipeline issues.
- Dedupe search, issue creation (`save_issue`/create), and first-comment posting for all three roles (spec-drift steps 4–9, bug-error steps 3–7, market-feature steps 4–8).
- Spec-drift's stale-issue sweep (step 10) and preview-branch cleanup (step 11) — both need to read issue status/labels from Linear.

**Not blocked**, and completed this run (see Payload): reading OpenSpec vs. the live codebase, reading Vercel runtime data, and one direct doc fix to `projects.md`.

## Payload

### 1. Bug-error — genuinely clean, no filing needed once Linear is back

Checked Vercel directly (project `prj_qCYQn9V1nrGNrUYdar5L0KVuqyu0`, team `team_P5vgMhFNfh2d4fCe2YkRLjey`):
- `get_runtime_errors` over the last 7 days: **zero runtime errors**.
- `list_deployments`: the 20 most recent deployments are all `state: READY` on `target: production` or clean preview builds — no failed builds.

There is nothing for bug-error to file this cycle for AI Landscape, independent of the Linear blocker. No further action needed here unless a future run finds new errors.

### 2. Spec-drift — no meaningful gap found; two housekeeping items flagged instead

Read `openspec/project.md` and all 7 capability specs (`radial-map`, `relationship-path-finder`, `search-filters`, `detail-panels`, `mobile-experience`, `data-catalog`, `deployment`). The specs are current and detailed — they already document the Relationship Path Finder, the "Updated Mon YYYY" freshness stamp, the ring-label z-order/Force-Radial toggle fix, mobile's capped connection pills with show-more, and the side panel's filter-aware connection list. Spot-checked the shipped `index.html` (fetched raw, grepped locally) and confirmed markers for all of these are actually present in code: `Find Path`, `Copy LinkedIn`, `freshness`, `showMore`, `No path found`. **No spec-to-code gap worth filing as a Backlog issue was found.**

Two things worth flagging instead of a gap issue:

- **Two shipped-but-unarchived OpenSpec changes**: `openspec/changes/last-updated-freshness-stamp/` and `openspec/changes/presentation-mode/` are both already merged to `main` (PR #17 and PR #18 — the latter, "Add presentation mode for talks and demos," is the current production deployment) but never archived into `openspec/specs/`. `AI-landscape` has no `.github/workflows/openspec-archive.yml` (checked `.github/` — only a PR template exists), so nothing archives these automatically the way `conventions.md`'s structural-backup section assumes. I did **not** run `npx openspec archive` myself this session — doing so means committing spec-file changes to the AI-landscape repo, which felt like it belonged on a reviewed branch/PR rather than an unattended push, and this session's designated AI-landscape branch (`claude/beautiful-ride-adi01j`) wasn't set up with that in mind. Recommend either: (a) a future spec-drift run's step 12 does this properly in a PR, or (b) Sharad runs `npx openspec archive last-updated-freshness-stamp -y --skip-specs && npx openspec archive presentation-mode -y --skip-specs` locally.
- **`projects.md` had a stale prod URL for AI Landscape** — see below, already fixed.

Steps 10–11 (stale-issue sweep, preview-branch cleanup) could not run at all — both need Linear.

### 3. `projects.md` data-quality fix (already applied, this repo, this branch)

`projects.md` listed AI Landscape 2026's "Vercel Prod" column as `https://rohrasharad-ship-it.github.io/ai-landscape/` (a GitHub Pages URL). That's wrong: the project is actually deployed on Vercel. Confirmed two ways — `openspec/specs/deployment/spec.md` in the ai-landscape repo names `https://ai-landscape-ten.vercel.app/` as the documented production URL, and Vercel MCP (`list_projects` under team `team_P5vgMhFNfh2d4fCe2YkRLjey`) shows a live `ai-landscape` project (`prj_qCYQn9V1nrGNrUYdar5L0KVuqyu0`) linked to this same GitHub repo, actively deploying (most recent production deploy is PR #18, today). I corrected the row in `projects.md` on this branch. This matters beyond cosmetics — bug-error's whole job is reading "the Vercel production runtime logs," and a routine that trusted the old GitHub Pages URL would have looked in the wrong place (or nowhere, since GitHub Pages has no runtime logs) every time it ran for this project.

### 4. Market-feature — 3 drafted candidates, not filed (need Linear dedupe search first)

Read `openspec/project.md`'s vision/non-negotiables/Out-of-Scope sections. All three respect "no backend," "no accounts," and "static single-file app." **These still need a Linear dedupe search before filing** — I have no way to confirm none of these (or something similar) is already tracked or was already rejected in triage.

**1. 🔗 Shareable view links**
- In short: Shareable map links
- Problem: A reader who finds an interesting filtered view or a traced path has no way to send that exact view to someone else — every link just opens the default blank map.
- Solution: Encode the current search, filters, selection, and any active path-finder route into the URL so opening a shared link restores the same view.
- Why: A landscape map is inherently something people want to reference and share (e.g. "look at this AI chip supply chain"); shareable views turn one visit into referral traffic with zero backend.
- What it looks like: A "Copy link to this view" action near the existing copy/share affordances; opening the copied URL reproduces the same filters, selection, and path.
- Suggested priority: Medium

**2. 🆕 "What's new" changelog**
- In short: Recent catalog changes
- Problem: Returning visitors have no way to tell what changed in the ecosystem since their last visit beyond the single "Updated Mon YYYY" stamp.
- Solution: A lightweight "What's new" panel listing the last several nodes/links added or changed, driven by the same git-history data that already powers the freshness stamp.
- Why: AI moves fast; a changelog gives returning visitors a concrete reason to check back instead of re-exploring the whole graph to find what's different.
- What it looks like: A small "What's new" link next to the freshness stamp opening a short list like "+ Added Sora 2 (Video Gen)" or "+ Connected Grok to xAI infra."
- Suggested priority: Medium

**3. ⚖️ Compare two tools side by side**
- In short: Compare two tools
- Problem: Readers evaluating two competing tools (e.g. two chip designers or two image generators) have to open each one's detail panel separately and hold the comparison in their head.
- Solution: A "+ Compare" action on the detail panel opens a second panel alongside it for a chosen second node.
- Why: Comparison is one of the most common reasons someone explores a competitive landscape map; side-by-side removes the memory burden of a single scrollable panel.
- What it looks like: A "+ Compare" button in the existing detail panel; a second panel appears showing both tools' category, popularity, description, and shared connections.
- Suggested priority: Low (speculative, and adds real UI complexity to a project whose spec explicitly says "keep the controls lightweight" — likely to get triaged out, but worth Sharad's call)

None of these have visual mockups or the mandatory Visual Self-QA screenshot yet — both require Linear (`prepare_attachment_upload`/`create_attachment_from_upload`) and, per `agents/shared/visual-specs.md`, a preview branch push to AI-Workspace, which only makes sense to do once an idea has survived the dedupe check and is actually going to be filed.

## Instructions for receiving agent

1. Confirm Linear MCP is working (`list_issues` on the AI Landscape project succeeds).
2. Run the Issue Cap pre-flight for AI Landscape 2026 (`agents/shared/issue-cap.md`, Linear Project ID `4ef7d096-f5bb-44f4-bac5-417e4488cdb8`). If at/over cap (5), stop — skip straight to stale-issue sweep + preview-branch cleanup below.
3. If under cap: dedupe-search Linear for each of the 3 market-feature candidates above. File the survivors as Backlog + `spec-needed`, assignee Sharad Rohra, Issue Brief description (text above is already in that format), minimal-effort visual mockup per `agents/shared/visual-specs.md`, and the mandatory Visual Self-QA screenshot per `agents/shared/visual-self-qa.md`. Bug-error and spec-drift gap-filing can be treated as clean for this cycle based on the findings above — re-verify only if a meaningful amount of time has passed since 2026-09-09.
4. Run spec-drift steps 10–11 (stale-issue sweep, preview-branch cleanup) for AI Landscape — neither ran this session.
5. Decide on archiving the two pending OpenSpec changes (`last-updated-freshness-stamp`, `presentation-mode`) in the ai-landscape repo — see item 2 above.
6. Delete this handover file once Linear access is confirmed restored and steps 2–4 have been carried out (or explicitly deferred) — it isn't needed once the routine can run normally again.
