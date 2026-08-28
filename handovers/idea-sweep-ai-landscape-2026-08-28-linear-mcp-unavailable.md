# Handover: idea-sweep routine blocked for AI Landscape — no Linear access this session

**For:** Any agent/session with working Linear MCP access (or a `LINEAR_API_KEY` env var)
**From:** idea-sweep routine run for AI Landscape 2026, Claude Code (scheduled session), 2026-08-28
**Blocked by:** No Linear MCP tools connected this session — the Linear MCP server itself reports "requires authentication before its tools can be used," meaning every Linear tool (`list_issues`, `create_issue`, `search_issues`, comments, etc.) is unavailable this session, not just one call or one role. No `LINEAR_API_KEY` shell env var either. This is broader than the blocker already tracked in `handovers/preview-branch-cleanup-linear-api-key.md`, which assumes Linear MCP works for search/filing and only the raw API key (used by `cleanup-preview-branches.sh`) is missing — this session has neither.
**Action:** Re-run `idea-sweep` for AI Landscape 2026 (Linear Project ID `4ef7d096-f5bb-44f4-bac5-417e4488cdb8`) from a session with working Linear MCP or a raw `LINEAR_API_KEY` once available. Nothing below needs re-deriving — the routine's actual work (steps 1–10, for all three roles) never started, because step 0 (Issue Cap pre-flight) itself requires Linear.
**Issue:** None. This is a scheduled routine trigger, not an issue-driven session, so there is no Linear issue to comment on — and no Linear access to create one either.

## Payload

Ran `routines/idea-sweep.md` for **AI Landscape 2026** (`rohrasharad-ship-it/ai-landscape`, Linear Project ID `4ef7d096-f5bb-44f4-bac5-417e4488cdb8`) as a scheduled trigger. Read the routine file, `routines/README.md`, `agents/shared/issue-cap.md`, and all three role files (`agents/spec-drift.md`, `agents/bug-error.md`, `agents/market-feature.md`) before starting, per the routine's own instructions.

**What blocked immediately:** step 0 of the routine (Issue Cap pre-flight, `agents/shared/issue-cap.md`) requires `list_issues` via Linear MCP. This session's tool list shows Linear under "requires authentication before its tools can be used" — confirmed no fallback either: `LINEAR_API_KEY` is unset as a shell env var (`echo ${LINEAR_API_KEY:+yes}` → empty).

Because the cap check can't run, none of steps 1–9 could proceed for **any** of the three roles (spec-drift, bug-error, market-feature) — all three need Linear for search-before-file and for filing itself, not just for the cap count.

**Step 10 (spec-drift stale-issue sweep)** also needs Linear (`list_issues` + read comments) — blocked for the same reason.

**Step 11 (preview-branch housekeeping, `scripts/cleanup-preview-branches.sh` in AI-Workspace — this always runs against AI-Workspace regardless of which project triggered the sweep)** requires `LINEAR_API_KEY` as a shell env var; also unset. This is the **same root cause already tracked** in `handovers/preview-branch-cleanup-linear-api-key.md` (8 consecutive independent hits as of 2026-08-12, root-caused there to a missing `LINEAR_API_KEY` repo secret plus a proxy that blocks mutating git pushes as a manual fallback). Did not re-verify the branch classification list again — that handover already notes re-verifying wastes tokens with no new information. Fix is unchanged: add the `LINEAR_API_KEY` repository secret.

**Step 12 (openspec archive housekeeping)** — checked `openspec/changes/` in AI-Workspace directly (`ls openspec/changes/`): only `archive/` exists, no active/complete change folders. Clean 0, not a new blocker — matches the same clean-0 note in the 2026-08-08 and 2026-08-12 updates on the other handover.

**Two things worth flagging for whoever next runs this successfully** (found while reading context, not full role output — no role actually ran):

1. `projects.md`'s "Vercel Prod" column for AI Landscape 2026 lists the GitHub Pages URL (`https://rohrasharad-ship-it.github.io/ai-landscape/`), but the project's own `openspec/specs/deployment/spec.md` states the canonical production URL is `https://ai-landscape-ten.vercel.app/` (Vercel), and a `vercel.json` exists in the repo root. If `projects.md` is the routine's source of truth for "Vercel Prod," `agents/bug-error.md` step 1 ("read Vercel production runtime logs") would be pointed at the wrong host — GitHub Pages has no runtime-log surface at all, so bug-error would find nothing every run regardless of actual prod errors. Worth a `projects.md` correction (or confirming GitHub Pages is actually current and the openspec spec is stale) before bug-error next runs for this project. Did not fix it myself since this is a factual call about which host is really live, not a mechanical one.
2. AI Landscape's openspec content is present and looks current — `openspec/project.md` plus specs under `openspec/specs/{data-catalog,deployment,detail-panels,mobile-experience,radial-map,relationship-path-finder,search-filters}/`. spec-drift and market-feature have everything they need to run steps 1–3 as soon as Linear access exists; nothing about the repo itself is blocking.

## Instructions for receiving agent

1. Confirm Linear MCP works (or `LINEAR_API_KEY` is set) in your session.
2. Re-run `routines/idea-sweep.md` for AI Landscape 2026 from step 0 — nothing from this session can be reused, since no role actually executed.
3. Separately (not blocking step 2): resolve the `projects.md` Vercel-Prod-URL question above (item 1) — confirm with Sharad if needed — so `bug-error` reads the correct host next time it runs for this project.
4. Once Linear access is confirmed and `idea-sweep` completes (or legitimately finds nothing), append that run's own line to `data/sweep-runs.jsonl` as usual — this session did not, since no role ran and a `"clean": true` entry would misrepresent that idea-generation actually executed.
5. Delete this handover file once a future run for AI Landscape 2026 completes without hitting the Linear-access wall.
