# Handover: idea-sweep routine for AI Landscape 2026 could not run — no Linear MCP in this session

**For:** Any agent session with working Linear MCP access, or Sharad
**From:** idea-sweep routine (orchestrator), scheduled run for AI Landscape 2026, 2026-09-07
**Blocked by:** This session has no Linear MCP tool loaded at all. The connector requires
an OAuth authorization flow that this session (a scheduled, non-interactive Claude Code on
the web run) cannot perform — there is no browser/user present to complete it. This is
distinct from the ongoing `LINEAR_API_KEY` repo-secret blocker tracked in
`handovers/preview-branch-cleanup-linear-api-key.md` (that one blocks *shell scripts* run
via a GitHub Actions secret; this one blocks the *MCP connector* itself, used for every
`list_issues`/`create_issue`/comment call an idea-generation role makes). Fixing the secret
does not fix this — this needs the Linear connector authorized for the account/session that
runs `idea-sweep`, via claude.ai Settings → Connectors (or `claude mcp` / `/mcp` in an
interactive session).
**Action:** Once Linear MCP is available in a session, re-run `idea-sweep` for AI Landscape
2026 following `routines/idea-sweep.md` exactly — do the Issue Cap pre-flight and Linear
dedupe search fresh (this handover's candidates are pre-screened against the codebase only,
**not** against Linear, since Linear couldn't be read at all this run).
**Issue:** N/A — this run is not tied to an existing Linear issue; it's the routine's own
scheduled trigger.

## What could and couldn't run this session

- **Step 0 (Issue Cap pre-flight), all three roles:** blocked — could not call `list_issues`.
- **spec-drift steps 1-4** (openspec vs. code): ran, using GitHub MCP + a local grep pass
  over `index.html` fetched from the repo. See candidates below — result was clean, no
  gaps found worth filing.
- **spec-drift steps 5-9** (file/screenshot/comment): N/A — no gaps found, and blocked on
  Linear regardless.
- **spec-drift step 10** (stale-issue sweep): blocked — needs to read/paginate open Linear
  issues and their comments.
- **spec-drift step 11** (preview-branch housekeeping): not attempted — already tracked as
  broken for a different reason (`LINEAR_API_KEY` secret missing) in
  `handovers/preview-branch-cleanup-linear-api-key.md`; that handover's 2026-08-12 update
  says re-verifying the same root cause a 4th+ time wastes tokens with no new information,
  so I deferred to it rather than re-diagnosing.
- **spec-drift step 12** (openspec archive housekeeping): same as step 11 — same missing
  secret, same script family. Not re-verified for the same reason.
- **bug-error step 1** (Vercel runtime logs): attempted via Vercel MCP
  (`mcp__Vercel__list_projects`) — returned `{"error": "Failed to list projects."}` with no
  further detail. Could not resolve a Vercel project ID for `ai-landscape-ten.vercel.app` to
  call `get_runtime_errors`. This is a **third**, separate blocker (Vercel MCP, not Linear) —
  whoever picks this up should check Vercel MCP auth/team scoping independently; it may
  already be fixed by the time Linear is sorted out.
- **bug-error steps 2-8:** N/A — blocked on both step 1 and Linear.
- **market-feature steps 1-3** (vision read + ideation): ran fully — see candidates below.
- **market-feature steps 4-9** (dedupe/file/screenshot/comment): blocked on Linear.

## Side finding already fixed (not part of this handover — no action needed)

While reading `openspec/specs/deployment/spec.md`, found `projects.md`'s "Vercel Prod"
column for AI Landscape 2026 pointed at the project's GitHub Pages mirror
(`rohrasharad-ship-it.github.io/ai-landscape/`) instead of the actual Vercel deployment
(`https://ai-landscape-ten.vercel.app/`) that the spec and `README.md` both document as
production. Fixed directly in `projects.md` on this branch (commit "Fix AI Landscape 2026
prod URL in project index") since it was a pure factual correction, not Linear-dependent.
Worth knowing about because the *old* wrong URL would have sent a working bug-error role's
Vercel-log lookup at a host that was never on Vercel to begin with (GitHub Pages has no
runtime-error API).

## Payload — candidates ready for Linear dedupe + filing once access exists

### Spec-drift (steps 1-4): clean, nothing to file

Read `openspec/project.md` and all six capability specs (`radial-map`,
`relationship-path-finder`, `search-filters`, `detail-panels`, `mobile-experience`,
`data-catalog`) plus `deployment/spec.md`, then spot-checked the corresponding behavior in
`index.html` (fetched via GitHub MCP, checked with local grep since it's a single ~150KB
file):

- Freshness label (`radial-map` + `mobile-experience` specs): implemented correctly — the
  source has a `__CATALOG_FRESHNESS__` placeholder that `scripts/inject-catalog-freshness.js`
  replaces at build time (derived from `git blame` on the `NODES`/`LINKS_RAW` ranges), wired
  into `vercel.json`'s `buildCommand`. Working as designed, not a placeholder bug.
- Sub-category search (`search-filters` spec, e.g. "GPU Makers"): present in `NODES` data
  (`"subCat":"GPU Makers"` under `Chip Designers` category) — spec requirement appears met.
- Mobile capped connection list + show-more/show-less (`mobile-experience` spec): found
  `.m-conn-show-more` button wired to expand/collapse — appears implemented.
- Path finder controls, "No path found" state (`relationship-path-finder` spec): found
  `#path-find-btn`, `#path-badge`, and the "No path found" string in the badge logic —
  appears implemented.
- Deployment spec's documented production URL matches `README.md` exactly.

None of this is exhaustive line-by-line verification of every Scenario in every spec (that
would mean reading the full 150KB file end-to-end, which felt disproportionate for a
routine run given the actual blocker is Linear, not code review) — but nothing surfaced a
credible "specced but unbuilt" gap worth an issue. Treat this as a light pass, not a full
audit; a future full spec-drift run should still do its normal full-breadth read.

### Market-feature (steps 1-3): 3 draft candidates, NOT yet deduped against Linear

Per `openspec/project.md`: static/no-backend is a hard non-negotiable, user accounts/auth
and real-time backend/APIs are explicitly Out of Scope. All three ideas below are pure
client-side additions consistent with that. **A receiving agent must still run
market-feature step 4 (search Linear for existing/duplicate ideas, including anything
spec-drift or a prior market-feature run already filed) before creating any of these** —
none of this was checked against Linear.

1. **🔗 Shareable deep-link state** — encode the current selection (selected node, active
   path-finder query, active filters) into the URL hash/query string, so a reader can copy
   the address bar and send someone straight to the same view. No backend needed (pure
   client-side `history.replaceState`/hash parsing). Ties to differentiation: this is a
   public reference map meant to be linked to and shared (LinkedIn blurb button already
   exists for individual nodes) — right now the *view itself* isn't shareable, only a
   description of one node is.
2. **🖼️ Export current view as an image** — a button that rasterizes the current filtered
   SVG/canvas view (via `canvas.toDataURL` or an SVG-to-PNG conversion) so a reader can save
   or share a snapshot of e.g. "everything connected to Anthropic." No backend, no new
   dependency needed beyond what D3/SVG already provides. Pairs naturally with idea #1.
3. **⚖️ Side-by-side compare for two nodes** — let a reader pick two nodes and see their
   detail-panel data (category, description, popularity, connections) side by side instead
   of one at a time. Reuses existing per-node data already in `NODES`; no backend, no new
   taxonomy.

None of these should be filed as-is without the Linear dedupe search and the mandatory
visual preview + live-site screenshot (`agents/shared/visual-specs.md`,
`agents/shared/visual-self-qa.md`) that market-feature step 6-7 require.

### Bug-error: no findings — logs unreachable this run

Could not read Vercel runtime logs (see blocker list above). No claim of a clean production
either way — this is an unresolved unknown, not a "nothing found."

## Instructions for receiving agent

1. Confirm Linear MCP is actually available (try any `list_issues`/`search` call) before
   doing anything else below.
2. Run the Issue Cap pre-flight for AI Landscape 2026 (`agents/shared/issue-cap.md`,
   Linear Project ID `4ef7d096-f5bb-44f4-bac5-417e4488cdb8`) fresh — do not assume this
   handover's absence of Linear data means the project is under cap.
3. If under cap: search Linear for each of the 3 market-feature candidates above and file
   whichever survive dedupe, following `agents/market-feature.md` steps 4-9 in full
   (visual preview + screenshot + first comment are still mandatory).
4. Separately check whether Vercel MCP (`mcp__Vercel__list_projects`) now resolves a
   project for `ai-landscape-ten.vercel.app` — if so, run `agents/bug-error.md` steps 1-8
   properly instead of relying on this handover (no bug findings exist here).
5. Run spec-drift step 10 (stale-issue sweep) properly now that Linear is readable — it
   did not run at all this session.
6. Do NOT re-attempt steps 11/12 (preview-branch cleanup, openspec archive sweep) as a way
   to "double check" the `LINEAR_API_KEY` secret blocker — that's tracked separately in
   `handovers/preview-branch-cleanup-linear-api-key.md` and confirmed multiple times over;
   only revisit it if that handover itself says the secret was added.
7. Delete this handover file once step 3 above has actually run (whether or not it filed
   anything) — the candidates here will be stale after that.
