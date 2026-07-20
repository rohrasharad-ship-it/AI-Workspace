# Routines

A **routine** is a named, git-stored job that an external trigger (a co-work
schedule, a cron, a manual "run this") can invoke by name, without pasting any
real instructions into that outside tool. The outside trigger only ever needs
to say two things: **which routine** and **which project(s)**. Everything else
— which agent roles run, what they read, what they're allowed to do, where
output goes — lives here in git.

This solves the problem that used to exist with Cursor Automations: the
guardrails lived in `AGENTS.md` but the actual prompt lived only in Cursor's
UI, so nothing was fully version-controlled and nothing was reusable across
projects. Now the prompt *is* the routine file.

## Model

- **Role** (`agents/*.md`) = HOW a given kind of agent works — its process,
  its guardrails, what it's allowed to touch.
- **Routine** (`routines/*.md`) = WHICH roles run, against WHICH project(s),
  on what cadence, producing what output. A routine is a bundle, not new
  process — it composes existing roles.
- **Hub model**: this file and every routine in this directory are generic —
  they never hardcode a specific project. Project-specific facts (repo, Linear
  project, Slack channel, prod URL) come from `projects.md` at trigger time,
  or from a project name/repo passed directly by the trigger.

## Idea-generation is the routine case

Roles 1–3 (builder, reviewer, spec-conversation) are event-triggered — Linear
assignment or an @mention wakes them directly, so they don't need a routine
wrapper. The three idea-generation roles (`agents/spec-drift.md`,
`agents/bug-error.md`, `agents/market-feature.md`) are different: nothing in
Linear wakes them, so something external has to. That's what a routine is for
— and because one routine can name multiple roles and multiple projects, this
is also the mechanism for **one trigger → many sub-agents → many repos**.

## How to write the external trigger

Keep the outside prompt (in co-work, a cron, wherever) to this shape:

```
Run the "<routine-name>" routine for <project name(s) or "all projects">.
Follow rohrasharad-ship-it/AI-Workspace/routines/<routine-name>.md exactly.
```

Nothing else needs to be pasted there. If the routine or its constituent roles
change, editing the files here is enough — no outside tool needs to be touched
again.

## How the orchestrating session executes a routine

1. Read the named routine file (e.g. `routines/idea-sweep.md`) — it lists
   which roles to run.
2. Resolve the named project(s) against `projects.md` (repo, Linear project,
   Linear project ID, Slack channel, prod URL). If the trigger says "all projects," loop over
   every row in `projects.md`.
3. For each (role × project) pair, run that role's file
   (`agents/spec-drift.md`, etc.) against that project — either inline in the
   same session, or by spawning one sub-agent per pair if the fan-out is large
   (multiple roles × multiple repos). Sub-agents work over MCP (GitHub read,
   Vercel logs, Linear, Playwright against the live URL) — no local clone of
   the target repo is required, so fan-out across repos doesn't require
   switching working directories.
4. Each role that creates issues does so directly in Linear, following its own
   file and `agents/shared/conventions.md`.
5. After all pairs finish, post one consolidated Slack summary (not one
   message per sub-agent) to the project's Slack channel: how many issues
   were filed by which role, with links.

## Pre-flight: Issue Cap (mandatory, before any idea-generation role creates issues)

Follow `agents/shared/issue-cap.md` exactly — that module has the full
counting procedure, skip message, and the known Linear MCP pitfall.

**In short:** count open issues per project (cap: 5). Filter `list_issues` by
the **Linear Project ID** from `projects.md`, not the display name — name
filters silently return zero for some projects. Paginate through every page and
count issues whose `statusType` is not `completed`, `canceled`, or `duplicate`.

**If that count is 5 or more, do not run any of the three idea-generation
roles for this project this cycle.**

**This check is per-project, not global** — a full backlog on one project
never blocks routines on another. With 5 active projects (see `projects.md`),
this keeps the steady-state ceiling across all of them around 25 total, not
unbounded.

**Check once per project per routine run, not once per role.** If `idea-sweep`
is running all three roles for a project, do this check a single time before
any of them start — skip all three together if the cap is hit, rather than
checking (and posting to Slack) three separate times for the same project.

## Shared guardrails (every idea-generation role, every routine)

- Create issues only as `Backlog` + `spec-needed` — **never `agent-ready`**
- Assignee is always Sharad Rohra, never an agent (see `agents/shared/conventions.md`)
- Title starts with one relevant emoji (see `agents/shared/conventions.md`)
- Description uses the Issue Brief format — five scannable one-liners, no long
  paragraphs (see `agents/shared/issue-brief.md`)
- Search Linear first — skip anything already tracked (open or recently closed)
- No implementation detail — that belongs to the later spec conversation
- Suggest a priority; Sharad overrides
- If the proposed issue has a meaningful visual/UI component, attach a visual
  preview per `agents/shared/visual-specs.md`, minimal-effort tier, and link
  it in the issue description
- Take a real screenshot per `agents/shared/visual-self-qa.md` and attach it
  to the issue — mandatory for every issue any of these three roles create

## Idea Feeder Sources

| Feeder | Role file | What it does | Default trigger |
|---|---|---|---|
| Spec-drift | `agents/spec-drift.md` | Reads openspec/specs/ vs actual code, files issues for what's specced but unbuilt | Weekly (Mon 9am) via `idea-sweep` |
| Bug/error | `agents/bug-error.md` | Reads Vercel runtime errors + logs, files issues for what's breaking in prod | Daily via `idea-sweep` |
| Market/feature | `agents/market-feature.md` | Reads project vision, proposes brand-new features not yet in the spec or Linear, always with a visual | Weekly (Mon 9am) via `idea-sweep` |
| Spillover | `agents/reviewer.md` | Agent notices a gap while building or reviewing, files a new Backlog issue, doesn't block current work | Per-issue, not a routine |
| Capture agent | — | Sharad drops a Slack message or voice note → becomes a clean Backlog issue | Not yet built |

## Available routines

| Routine | File | What it bundles |
|---|---|---|
| Idea sweep | `routines/idea-sweep.md` | spec-drift + bug-error + market-feature, one or more projects |

Add a new routine by creating a new `routines/<name>.md` file with the same
shape as `idea-sweep.md` — a role list, a default cadence, and an output
description. No code changes needed anywhere else.
