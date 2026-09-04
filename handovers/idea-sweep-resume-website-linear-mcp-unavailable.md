# Handover: idea-sweep for Resume Website blocked — no Linear MCP access this session

**For:** Any agent/session with Linear MCP access
**From:** `idea-sweep` routine, Resume Website project, scheduled Claude Code session, 2026-09-04
**Blocked by:** Linear MCP connector unauthenticated/unavailable this session — the system
prompt explicitly flagged `Linear` as requiring authentication that a non-interactive
session cannot complete, and no `mcp__Linear__*` tool of any kind showed up under
`ToolSearch` (confirmed by searching for "linear issue create list" — only GitHub/Slack
tools matched).
**Action:** Once Linear access is available, run the Issue Cap pre-flight and the
Linear-dependent steps of `agents/spec-drift.md` (step 10, stale-issue sweep — hasn't run
for this project since 2026-08-05), `agents/bug-error.md`, and `agents/market-feature.md`
for **Resume Website**. The read-only analysis below is already done, so what's left is
mostly Linear I/O, not re-research.
**Issue:** N/A — this is a scheduled routine run (`idea-sweep`), not driven by a single
Linear issue.

---

## What happened

This was an automated firing of the `idea-sweep` routine
(`routines/idea-sweep.md`) for **Resume Website** only (single-project run — no
cross-project grouping applies). GitHub MCP and Vercel MCP were both available and used;
the **Linear MCP server was not connected/authorized in this session**.

This looks like a **one-off session/connector auth gap, not a structural blocker**:
`data/sweep-runs.jsonl` shows a prior Resume Website idea-sweep run on 2026-08-05
completed cleanly with real Linear access (0 filed, `clean: true`), so this exact routine
has worked with Linear before. Recommend checking the Linear connector's authorization
status (claude.ai Settings → Connectors) rather than treating this as the same class of
issue as the long-running `LINEAR_API_KEY` GitHub Actions secret gap documented in
`handovers/preview-branch-cleanup-linear-api-key.md` — that one is unrelated (it blocks a
shell script's env var on a scheduled GitHub Action runner, not this session's MCP tool
access).

Because every idea-generation step that touches Linear (Issue Cap pre-flight, dedupe
search, filing, stale-issue comments) requires the Linear MCP, **steps 0/4/5/8/10 in
`agents/spec-drift.md`, `agents/bug-error.md`, and `agents/market-feature.md` could not
run this cycle.** No issues were filed, searched, or commented on.

## What I *was* able to complete (no Linear needed)

**Bug/error (Vercel):**
- `mcp__Vercel__get_runtime_errors` on `prj_P1V3fzfZ1QwZcVvUNHzdq1DQRtGt` (resume-website),
  last 7 days → **no runtime errors**.
- `mcp__Vercel__get_runtime_logs` grouped by `statusCode`, last 7 days → **no log entries
  at all** (nothing to group).
- Conclusion: production is clean. Per `agents/bug-error.md` step 8, this role would
  create nothing regardless of Linear access — **no action needed from the receiving
  agent for bug-error this cycle**, beyond re-checking if a meaningful amount of time has
  passed since 2026-09-04.

**Spec-drift (OpenSpec vs. codebase):**
- Read `openspec/project.md`'s capability index. All 7 capabilities (`hero`, `journey`,
  `about`, `contact`, `voice-agent`, `design-system`, `site-meta`) are `Live` or `In
  progress`, and the only 3 flagged gaps (Cal.com booking button, emoji scroll-morph,
  site-meta OG/SEO work) are **already tracked** — referenced inline as SHA-14, SHA-13,
  and SHA-11 respectively. Did not re-propose these.
- Cross-checked against `resume-website/CLAUDE.md`'s own Pending Items table (avatar
  headshot upload; Impact Analytics/DTU demo videos; Cal.com link). The first two are
  **assets Sharad needs to supply** (a photo, videos), not code gaps an agent can build —
  not valid spec-drift candidates. Cal.com is the already-tracked SHA-14.
- Found no new, meaningful, high-confidence gap worth filing this cycle. This mirrors the
  historical pattern in `data/sweep-runs.jsonl` — every prior run across every project has
  filed 0 and been clean.
- **Stale-issue sweep (spec-drift step 10) could not run at all** — it needs `list_issues`
  + comment access. This is the one piece of spec-drift's job that a Linear outage fully
  blocks even when there's nothing new to file, and it hasn't run for Resume Website since
  2026-08-05 — the receiving agent should prioritize running it once Linear is back.

**Market-feature:**
- Re-read `openspec/project.md`'s vision, non-negotiables, and out-of-scope list. Nothing
  came to mind that's both genuinely differentiated *and* not already speculatively close
  to what's built (voice agent + spotlighting + pinned horizontal Journey scroll are
  already fairly novel for a portfolio site). Per `agents/market-feature.md` step 9 ("do
  not invent filler ideas to hit the cap"), proposing nothing would be the right call
  regardless — but treat this as **provisional, not confirmed**, since it couldn't be
  dedupe-checked against the current Linear backlog either way.

**Housekeeping (spec-drift steps 11–12):** Already extensively documented as blocked in
`handovers/preview-branch-cleanup-linear-api-key.md` (missing `LINEAR_API_KEY` repo secret
+ proxy blocks git-ref deletion from any agent session) — 7 independent confirmations to
date, explicitly marked "no further action needed... re-verifying wastes tokens." Did not
re-touch the preview-branch question. Did confirm one cheap, still-relevant fact: this
session's `openspec/changes/` in AI-Workspace currently holds only the `archive/` folder,
no active change folders — step 12 is a clean 0 regardless of the secret.

## Instructions for receiving agent

1. Confirm Linear MCP is actually available in your session (e.g. `list_issues` for
   Resume Website's Linear Project ID `b01a99ac-46a3-4b00-9139-31e00fae781d`).
2. Run the Issue Cap pre-flight (`agents/shared/issue-cap.md`) for Resume Website.
3. If under cap: run spec-drift step 10 (stale-issue sweep) first, since it's the most
   overdue piece. Steps 1–9 of spec-drift and market-feature can lean on the analysis
   above rather than re-reading everything from scratch, but do re-run the Linear dedupe
   search before filing anything, since backlog state may have changed since 2026-08-05.
4. Bug-error: nothing to do — production was clean as of 2026-09-04 (re-check
   `get_runtime_errors`/`get_runtime_logs` if several days have passed).
5. Append the real outcome to `data/sweep-runs.jsonl` for this run once the Linear-
   dependent steps complete — I've added a placeholder line marked `"clean":false` with a
   `"blocked"` note; treat it as superseded once you log the actual result.
6. Delete this handover file once the above is done.
