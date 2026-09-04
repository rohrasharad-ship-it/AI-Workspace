# Handover: idea-sweep for AI Landscape 2026 could not file/search/comment — no Linear MCP tool in this session

**For:** Any agent session with working Linear MCP access
**From:** idea-sweep routine run for AI Landscape 2026 (Claude Code, scheduled trigger), 2026-09-04
**Blocked by:** No Linear MCP tool was available anywhere in this session's toolset. The
system explicitly listed `Linear` as an MCP server requiring authorization before its tools
can be used, and this is a non-interactive scheduled session — no OAuth flow could be run to
connect it. This is a different, more severe blocker than the long-running
`LINEAR_API_KEY` issue in `handovers/preview-branch-cleanup-linear-api-key.md` (that one is
about a *shell script's* env var; this session had no Linear tool access at all — not even
`list_issues`/`create_issue`/`create_comment`).
**Action:** Reconnect the Linear connector for whatever session/environment type ran this
scheduled trigger (claude.ai Settings → Connectors, or the relevant MCP config for
scheduled/cloud sessions), then re-run `idea-sweep` for AI Landscape 2026 from scratch
(Issue Cap pre-flight → all three roles). Treat this as a fresh run, not a continuation —
see Payload below for what's already been established vs. what still needs a real Linear
pass.
**Issue:** N/A — this was a routine trigger (`Run the "idea-sweep" routine for AI
landscape`), not a Linear-assigned issue.

## What this session could and could not do

This session also had **outbound network egress blocked** for arbitrary web domains
(`WebFetch` to both `rohrasharad-ship-it.github.io` and `ai-landscape-ten.vercel.app`
returned `EGRESS_BLOCKED`), so no live-site Playwright/browser check or screenshot was
possible either (mandatory per `agents/shared/conventions.md` #12 and every role's
screenshot step). GitHub MCP and Vercel MCP both worked fine.

Given no Linear (cap check, dedupe search, filing, commenting) and no live-site access, here
is what actually ran vs. what's still open, role by role:

### Issue Cap pre-flight — **not done**
Could not run — requires Linear `list_issues`. Do this first in the next session, using
Linear Project ID `4ef7d096-f5bb-44f4-bac5-417e4488cdb8` per `agents/shared/issue-cap.md`.
Do not assume this session's other findings mean the project is under cap.

### bug-error — analysis done, genuinely clean, nothing to file
Vercel MCP *does* work in this session (Linear does not). Found the correct Vercel project
for AI Landscape 2026 (see "Vercel Prod URL was stale" below) and pulled
`get_runtime_errors` for the last 7 days: **no runtime errors found**. Per
`agents/bug-error.md` step 8 ("If the site is clean, create nothing"), this role's job is
done for this cycle — no Linear access was even needed here since there was nothing to file
or dedupe. Re-running this role from scratch next time is fine but not urgent.

### spec-drift — **not attempted beyond reading project.md**
Read `openspec/project.md` in the target repo (capabilities: radial-map,
relationship-path-finder, search-filters, detail-panels, mobile-experience, data-catalog;
there's also an `openspec/specs/deployment/` folder not listed in project.md's Capabilities
section — worth a quick look, may be stale or may be a project.md omission). Deliberately
did **not** do the full gap-analysis (reading every spec file + the app code) this session,
because step 4's mandatory "search Linear first, skip anything already tracked" can't be
done without Linear — producing draft candidates here that can't be deduped against the ~20
issues already known to exist in this project's history (see sweep-runs.jsonl and prior
handovers) risks staging duplicate-issue work for the next session rather than saving it
time. Also could not run the stale-issue sweep (step 10) — needs Linear to list/read/comment
on existing issues. Next session should run steps 1–10 fresh.

### market-feature — **not attempted**
Same reasoning as spec-drift: proposing features without being able to check what's already
proposed/tracked in Linear isn't safe to stage. Next session should run steps 1–9 fresh.

### Housekeeping (spec-drift steps 11–12)
- **Step 11 (preview-branch cleanup in this repo):** still blocked, unchanged from
  `handovers/preview-branch-cleanup-linear-api-key.md` — confirmed the scheduled
  `preview-branch-cleanup.yml` Action is still failing as of its most recent run (run #9,
  2026-08-31, conclusion `failure`), so the missing `LINEAR_API_KEY` repo secret is still
  the blocker, 8+ runs in now. No need to re-verify the git-push-delete proxy block again —
  that's already been confirmed from three independent angles per that handover's log. Just
  fix the secret.
- **Step 12 (openspec archive sweep, this repo):** checked `openspec/changes/` in
  AI-Workspace directly via GitHub — it contains only the `archive/` subfolder, no active
  change folders. **Clean, 0 to archive**, confirmed without needing the script or
  `LINEAR_API_KEY`.

## Data fix made this session: stale Vercel Prod URL in `projects.md`

`projects.md`'s AI Landscape 2026 row listed `https://rohrasharad-ship-it.github.io/ai-landscape/`
(a GitHub Pages URL) under "Vercel Prod" — but `openspec/project.md` in the target repo says
hosting is Vercel at `ai-landscape-ten.vercel.app`, and Vercel MCP's `list_projects` confirms
a real Vercel project (`ai-landscape`, id `prj_qCYQn9V1nrGNrUYdar5L0KVuqyu0`) linked to that
GitHub repo, with `ai-landscape-ten.vercel.app` as one of its production domains. Updated the
row to the correct Vercel URL in this same commit — bug-error and any other role reading
`projects.md` needs the real Vercel project's domain, not a GitHub Pages mirror, to find
runtime logs at all. Whether the GitHub Pages deployment is still an intentionally
maintained secondary mirror is unknown — didn't touch GitHub Pages settings, just corrected
the routine's own project-index field.

## Ledger

Did **not** append a `"clean":true` line to `data/sweep-runs.jsonl` for this run, because
that would misrepresent a run where 2 of 3 roles never executed (vs. ran and found nothing).
The next full run's ledger line is the first accurate one since 2026-08-19.

## Instructions for receiving agent

1. Confirm Linear MCP is reachable in your session (try `list_issues` for the AI Landscape
   project ID above) before doing anything else.
2. Run the Issue Cap pre-flight for AI Landscape 2026 (Linear Project ID
   `4ef7d096-f5bb-44f4-bac5-417e4488cdb8`) per `agents/shared/issue-cap.md`.
3. If under cap: run spec-drift steps 1–10 and market-feature steps 1–9 fresh (bug-error is
   already confirmed clean this cycle via Vercel logs — feel free to skip re-running it, or
   re-run it too if you want fresh data since some time will have passed).
4. Append the real `data/sweep-runs.jsonl` line for this cycle once the roles actually run.
5. Delete this handover file once the above is done.
