# Handover: idea-sweep routine for Usercon could not run — no Linear MCP access this session

**For:** Any agent/session with Linear MCP tool access
**From:** Scheduled `idea-sweep` routine run, Usercon project, 2026-09-04
**Blocked by:** This session has zero Linear MCP tools available — not the previously-tracked `LINEAR_API_KEY` shell-secret gap (see `handovers/preview-branch-cleanup-linear-api-key.md`), but a harder wall: no `mcp__Linear__*` tools are registered in this session's toolset at all, and the platform reports Linear "requires authentication" via an interactive OAuth flow this non-interactive scheduled session cannot perform.
**Action:** Re-run the `idea-sweep` routine for Usercon (all three roles — spec-drift, bug-error, market-feature) from a session that has working Linear MCP access, following `routines/idea-sweep.md` exactly. Nothing below has been filed to Linear; this run did none of the Linear-dependent work.
**Issue:** N/A — this is a routine-level blocker, not tied to one pre-existing Linear issue.

## What was and wasn't possible this run

Per `agents/shared/issue-cap.md`, the Issue Cap pre-flight (count active pipeline
issues in the Usercon Linear project, ID `47ebefac-a4f4-4bdd-a382-4506f7e79b6b`)
requires `list_issues` via Linear MCP. That tool does not exist in this session,
so the pre-flight could not run, and per `routines/idea-sweep.md` none of the
three roles' Linear-dependent steps could run either:

- **spec-drift** steps 1–9 (gap-filing) and step 10 (stale-issue sweep, needs
  `list_issues` + reading/posting comments) — not attempted.
- **bug-error** steps 3–8 (Linear dedupe search, issue creation, comment) — not
  attempted. Step 1 (read Vercel production runtime errors) *was* done with
  Vercel MCP (project `prj_MAkmwIEkHssO8BH1DfYLbPTNNKxU`,
  `get_runtime_errors`, last 24h): **no runtime errors found**. So even with
  Linear access, bug-error would have filed nothing this cycle — that part of
  the run is genuinely clean, not just blocked.
- **market-feature** — not attempted at all. Read `openspec/project.md` for
  Usercon (vision/non-negotiables/out-of-scope, capabilities list) but did not
  go further into `openspec/specs/` or draft feature proposals, since any
  candidate would need a Linear dedupe search before it's safe to hand off as
  a real proposal, and that search isn't possible this session.
- **spec-drift steps 11–12** (preview-branch cleanup / OpenSpec archive sweep,
  shell-script based) were not re-attempted — this session also has no
  `LINEAR_API_KEY` env var, which is the already-documented, repeatedly
  confirmed blocker for those scripts (see
  `handovers/preview-branch-cleanup-linear-api-key.md`, 7 prior independent
  hits). No new information to add there; re-verifying would just waste
  tokens per that file's own note.

## Instructions for receiving agent

1. Confirm Linear MCP tools are actually available in your session
   (`list_issues` etc.) before starting.
2. Run the Issue Cap pre-flight for Usercon (Linear Project ID
   `47ebefac-a4f4-4bdd-a382-4506f7e79b6b`) per `agents/shared/issue-cap.md`.
3. If under cap, run all three roles per `routines/idea-sweep.md` and
   `agents/spec-drift.md` / `agents/bug-error.md` / `agents/market-feature.md`
   in full — this handover did none of their filing/search/comment work, so
   there is nothing to "resume," just a clean start.
4. Vercel runtime errors for Usercon were clean (0 errors, last 24h) as of
   2026-09-04 — worth a fresh check again since some time will have passed,
   but this run at least confirms production wasn't on fire that day.
5. Append the real sweep-runs.jsonl line for this project/date once the roles
   actually run (the line this session added is a `"blocked": true` placeholder,
   not a real "clean" result — replace/supplement it, don't treat it as
   already-covered).
6. Delete this handover file once a real idea-sweep run for Usercon has
   completed with Linear access.
