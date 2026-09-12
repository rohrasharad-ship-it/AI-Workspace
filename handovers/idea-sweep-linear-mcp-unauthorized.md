# Handover: Linear MCP is unauthorized this session — idea-sweep cannot file, search, or count issues

**For:** Sharad (to reconnect Linear) and the next agent with working Linear MCP access
**From:** Claude Code, `idea-sweep` routine run for AI Landscape 2026, 2026-09-12
**Blocked by:** The Linear MCP server is not authorized for this session at all — every Linear
tool (`list_issues`, `search`, `create_issue`, comment, `list_projects`, etc.) is unavailable,
not just the specific `LINEAR_API_KEY`/shell-script gap already tracked in
`handovers/preview-branch-cleanup-linear-api-key.md`. This is a new, more fundamental blocker:
prior idea-sweep sessions clearly had working Linear MCP (see `data/sweep-runs.jsonl` entries
through 2026-08-19, and the extensive `list_issues` cross-referencing done in the
`preview-branch-cleanup-linear-api-key.md` update chain) — something has since disconnected
the Linear connector for this account/session.
**Action:** Reconnect the Linear connector for this account (claude.ai → Settings →
Connectors → Linear → reauthorize), then re-run `idea-sweep` for AI Landscape 2026 (and any
other project whose scheduled run lands while Linear is disconnected — they'll hit the same
wall).
**Issue:** N/A — no driving Linear issue exists; this blocked the routine before any issue
could be looked up or created.

---

## Payload

Per `routines/idea-sweep.md`, this run should have executed spec-drift → bug-error →
market-feature against **AI Landscape 2026**
(`rohrasharad-ship-it/ai-landscape`, Linear Project ID
`4ef7d096-f5bb-44f4-bac5-417e4488cdb8`). Instead:

- **Issue Cap pre-flight** (`agents/shared/issue-cap.md`, mandatory before any role acts)
  requires `list_issues` filtered by Linear Project ID — unavailable. Could not confirm the
  project is under the 5-issue active-pipeline cap.
- **spec-drift** steps 4–9 (Linear search, file up to 5 issues, attach visuals, first
  comment) — blocked, no Linear write/search access.
- **spec-drift** step 10 (stale-issue sweep, up to 3 comments on Backlog issues) — blocked,
  needs `list_issues` + comment.
- **bug-error** steps 3–7 (Linear search, file up to 5 issues) — blocked. (Vercel MCP tools
  themselves are available this session — the blocker here is Linear only.)
- **market-feature** steps 4–8 (Linear search, file up to 3 issues) — blocked.
- **spec-drift** steps 11–12 (preview-branch cleanup / OpenSpec archive housekeeping in
  AI-Workspace) — separately blocked by the pre-existing, already fully-documented
  `LINEAR_API_KEY` repo-secret + proxy git-push-403 issue in
  `handovers/preview-branch-cleanup-linear-api-key.md`. Confirmed no `LINEAR_API_KEY` env var
  in this session either. That file's own last update says re-verifying this specific point
  again "wastes tokens with no new information" — so no new update was added there; the fix
  it names (add the repo secret) is still the only outstanding step for steps 11–12
  specifically.

**What I did without Linear (read-only, no write path needed):**
- Read `rohrasharad-ship-it/ai-landscape`'s `openspec/project.md` — 6 capability specs exist
  (`radial-map`, `relationship-path-finder`, `search-filters`, `detail-panels`,
  `mobile-experience`, `data-catalog`), all under `openspec/specs/`.
- Did **not** do a full spec-vs-`index.html` diff or read Vercel runtime logs this run.
  Reasoning: any candidate gaps/bugs found would need a fresh Linear dedupe search
  immediately before filing anyway (per every role file), so front-loading that research now
  just goes stale by the time Linear access is restored — no durable value for the extra
  token cost. The next session with working Linear access should just run the full routine
  from scratch.

**Side note, not blocking, worth a human look sometime:** `projects.md` in AI-Workspace lists
AI Landscape 2026's Vercel Prod URL as the GitHub Pages address
`https://rohrasharad-ship-it.github.io/ai-landscape/`, but the project's own
`openspec/project.md` says hosting is Vercel at `https://ai-landscape-ten.vercel.app/` (and
the repo has a `vercel.json`). Didn't change `projects.md` myself since I couldn't verify
live which is currently authoritative without more digging — flagging for whoever has
context.

## Instructions for receiving agent / Sharad

1. **Sharad:** reconnect the Linear connector (claude.ai → Settings → Connectors → Linear).
2. **Next agent with working Linear MCP:** re-run `idea-sweep` for AI Landscape 2026 as if
   this run never happened — it produced no findings and filed nothing (see the
   `"blocked": true` ledger line for 2026-09-12 in `data/sweep-runs.jsonl`, which is
   deliberately not marked `"clean": true` since nothing was actually checked).
3. Optionally reconcile the `projects.md` Vercel Prod URL discrepancy noted above.
4. Delete this handover file once a routine run completes successfully with Linear access
   restored.
