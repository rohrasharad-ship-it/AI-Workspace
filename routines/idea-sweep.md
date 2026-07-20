# Routine: idea-sweep

**Read `routines/README.md` first** for the general routine/orchestration model
— this file only defines what *this* routine bundles.

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
`projects.md`. Resolve each name to its repo, Linear project, Slack channel,
and prod URL before running the roles.

## Pre-flight, per project

Before running any of the three roles for a given project, do the Issue Cap
check from `routines/README.md` **once** for that project. If it's at or over
the cap (5 open issues), post the skip message to that project's Slack
channel and move on to the next named project — do not run spec-drift,
bug-error, or market-feature for this one this cycle. Projects under the cap
proceed normally below.

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

## Output

- Each role files its own Linear issues directly, per its own file.
- After all roles finish for all named projects, post **one consolidated
  Slack message per project** (not per role) to that project's Slack channel:
  ```
  🧭 Idea sweep — [Project Name]
  Spec-drift: [N] issues filed
  Bug/error: [N] issues filed
  Market/feature: [N] issues filed
  [links to each new issue]
  ```
- If a role found nothing, say so ("Bug/error: clean, nothing filed") rather
  than omitting it — Sharad should be able to tell the sweep actually ran.
- If any issues were filed, note whether Linear per-issue notifications should
  have appeared in the channel (see `agents/shared/linear-slack.md`). If the
  bell was never smoke-tested, flag that rather than assuming it works.
- **A project skipped at the pre-flight step (see above) gets only the skip
  message, never the consolidated summary too** — no roles ran, so there's
  nothing to summarize. One Slack message per project, either the skip
  message or the summary, never both.

## Example trigger

```
Run the "idea-sweep" routine for Resume Website.
Follow rohrasharad-ship-it/AI-Workspace/routines/idea-sweep.md exactly.
```

```
Run the "idea-sweep" routine for all projects.
Follow rohrasharad-ship-it/AI-Workspace/routines/idea-sweep.md exactly.
```
