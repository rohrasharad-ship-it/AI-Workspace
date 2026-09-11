# Handover: idea-sweep for Resume Website could not run — this session has zero Linear access

**For:** Any agent/session with Linear MCP access (or a human who can authorize the Linear connector for this account)
**From:** idea-sweep routine run for Resume Website, Claude Code on the web, 2026-09-11
**Blocked by:** No Linear MCP tool at all — not a broken call, not a missing shell env var (the narrower blocker other handovers in this directory describe), but the tool itself absent from this session's toolset. The system explicitly reported: "The following MCP servers require authentication before their tools can be used: Linear" and that this non-interactive session cannot run the OAuth flow to connect it.
**Action:** Authorize the Linear connector for this account (via `claude mcp` / `/mcp` in an interactive session, or the account's connector settings), then re-run the `idea-sweep` routine for Resume Website from `routines/idea-sweep.md`.
**Issue:** N/A — this is a routine-level blocker with no target Linear issue yet (nothing could be searched or created).

---

## What this run was asked to do

Trigger: "Run the 'idea-sweep' routine for Resume Website. Follow
`rohrasharad-ship-it/AI-Workspace/routines/idea-sweep.md` exactly." — a
single-project run, so all three idea-generation roles (spec-drift,
bug-error, market-feature) should have run directly against the Resume
Website Linear project (`b01a99ac-46a3-4b00-9139-31e00fae781d` per
`projects.md`), filing issues themselves (no cross-project grouping needed).

## What actually happened

Every step in `routines/idea-sweep.md` and its three role files that touches
Linear was unreachable this session:

- **Issue Cap pre-flight** (`agents/shared/issue-cap.md`) — needs
  `list_issues` filtered by Linear Project ID. Not callable.
- **spec-drift steps 1–9** (gap-filing) — needs Linear search + create.
- **spec-drift step 10** (stale-issue sweep) — needs Linear list + comment.
- **spec-drift step 11** (preview-branch housekeeping,
  `scripts/cleanup-preview-branches.sh`) — the script itself hard-requires
  `LINEAR_API_KEY` as a shell env var and exits immediately without it
  (`error: LINEAR_API_KEY is required`); confirmed absent from this
  session's environment too. This is the same underlying gap as
  `handovers/preview-branch-cleanup-linear-api-key.md`, which has been open
  since 2026-08-02 across 7+ independent idea-sweep runs on other projects —
  still unresolved, still the fix needed for this step to ever complete from
  an agent session.
- **bug-error** (all steps) — needs Linear cap check + search + create.
- **market-feature** (all steps) — needs Linear cap check + search + create.

**What did run:** step 12 (OpenSpec archive housekeeping), which needs only
git/GitHub, not Linear. I ran `npm install` (openspec CLI wasn't installed
in this checkout yet) then
`bash scripts/archive-merged-openspec-changes.sh --sweep` in AI-Workspace.
Result: `sweep: no completed active changes` — a genuine clean 0, nothing to
archive, no new blocker here.

I deliberately did **not** append a `data/sweep-runs.jsonl` entry for this
run. The ledger schema (`{"filed":{"bugs":N,"features":M},"clean":bool}`)
represents a run that actually checked and found nothing — that's not what
happened here for spec-drift/bug-error/market-feature; they never ran at
all. Logging `clean:true` would misrepresent a total tool blocker as a clean
sweep. This handover file is the record instead.

## Instructions for receiving agent

1. Confirm Linear MCP is authorized and its tools (e.g. `list_issues`,
   `create_issue`, `search_issues`) are actually callable in your session.
2. Re-run the full `idea-sweep` routine for **Resume Website** per
   `routines/idea-sweep.md`: Issue Cap pre-flight first, then spec-drift →
   bug-error → market-feature in order (single-project run, file directly,
   no grouping step needed).
3. Step 12 (OpenSpec archive) does not need re-running for this — it already
   completed cleanly this session with nothing to do.
4. Step 11 (preview-branch cleanup) will still fail even with Linear MCP
   restored, unless `LINEAR_API_KEY` is also available as a shell env var in
   your session — see `handovers/preview-branch-cleanup-linear-api-key.md`
   for the full standing blocker and branch classification (last verified
   2026-08-12, likely stale by now — re-derive rather than trust it blindly
   given a month has passed).
5. Once this run completes normally, append the `data/sweep-runs.jsonl`
   entry per `routines/idea-sweep.md` and delete this handover file.
