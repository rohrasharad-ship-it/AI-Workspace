# Routine: idea-sweep

**Read `routines/README.md` first** for the general routine/orchestration model
— this file only defines what *this* routine bundles.

**Multi-project runs:** when the trigger names two or more projects (or "all
projects"), also read `agents/shared/cross-project-grouping.md` — roles defer
filing until the orchestrator groups matching gaps at the end of each role.

## What it runs

All three idea-generation roles, in this order, against each target project:

1. `agents/spec-drift.md`
2. `agents/bug-error.md`
3. `agents/market-feature.md`

Each role file is self-contained (it names its own `Read first:` shared
modules) — this routine does not duplicate their instructions, it only says
*run all three, for these projects, then summarize*.

## Project selection

The trigger names one or more projects by their `projects.md` name (e.g.
"Resume Website"), or says "all projects" to run against every row in
`projects.md`. Resolve each name to its repo, Linear project, Linear project ID,
and prod URL before running the roles.

## Pre-flight, per project

Before running any of the three roles for a given project, do the Issue Cap
check from `agents/shared/issue-cap.md` **once** for that project (use the
**Linear Project ID** from `projects.md`, not the display name). If it's at or
over the cap (5 active pipeline issues in Backlog, Todo, In Progress, or In
Review), **still run spec-drift steps 10–11 only** (stale-issue sweep +
preview-branch housekeeping — these shrink the backlog and do not file new
issues). Skip spec-drift steps 1–9 and skip bug-error and market-feature
entirely for this project this cycle. Projects under the cap proceed normally
below.

## Cadence (default, when set up as a recurring trigger)

- spec-drift: weekly, Monday 9am
- bug-error: daily, 9am
- market-feature: weekly, Monday 9am

A single `idea-sweep` trigger can run all three on the same cadence if that's
simpler to schedule (e.g. one daily firing that always runs bug-error, and
only runs spec-drift + market-feature on Mondays) — or set up as separate
triggers per role if independent cadences matter more than a single firing.
Either is a scheduling choice made where the trigger lives (co-work trigger,
cron), not something this file needs to enforce.

## Cross-project grouping (multi-project triggers only)

When the trigger names **two or more projects** (or "all projects"):

1. Resolve the full project list from `projects.md` before starting any role.
2. For each role in order (spec-drift → bug-error → market-feature):
   - Run that role against every under-cap project, but **do not file issues yet**
     — each role appends grouping candidates to the run ledger (see
     `agents/shared/cross-project-grouping.md`).
   - After the role finishes all projects, run the grouping step: cluster
     matching candidates, file one issue per cluster (PM OS when 2+ projects
     share a gap; otherwise the single project's Linear project).
3. Single-project triggers skip this section entirely — roles file directly.

## Output

- **Single-project run:** each role files its own Linear issues directly, per
  its own file.
- **Multi-project run:** the orchestrator files after each role's grouping step;
  roles supply candidates only.
- **No Slack updates.** The routine does not post a summary (or a skip
  notice) to Slack — Linear is the record. Filed issues, stale-issue comments,
  and the sweep ledger below are the only output.
- If a role found nothing, note it in the run's own output (e.g. to the user
  or session log) rather than silently doing nothing — but this no longer
  goes to Slack.
- **Sweep ledger (routine run log):** after finishing each project, append one
  JSON line to `data/sweep-runs.jsonl` in
  AI-Workspace (commit on the same branch if you have repo access, or note it
  for the next infra touch):
  ```json
  {"at":"<ISO8601>","project":"<projects.md name>","filed":{"bugs":N,"features":M},"clean":false}
  ```
  Set `"clean": true` and zero counts when all three roles filed nothing.
  Bugs = issues whose titles start with 🐛; features = spec-drift + market
  combined. Then run `node scripts/generate-routine-log.mjs` (needs
  `LINEAR_API_KEY`) to refresh `data/routine-log.json` for the sandbox
  dashboard at `/routine-log.html`.
- **A project skipped at the pre-flight step (see above)** still gets a partial
  spec-drift summary (`stale issues flagged`, `preview branches deleted`) if
  steps 10–11 ran — never the full run with bug-error/market-feature counts,
  since those roles did not run.

## Example trigger

```
Run the "idea-sweep" routine for Resume Website.
Follow rohrasharad-ship-it/AI-Workspace/routines/idea-sweep.md exactly.
```

```
Run the "idea-sweep" routine for all projects.
Follow rohrasharad-ship-it/AI-Workspace/routines/idea-sweep.md exactly.
```
