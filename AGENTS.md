# PM OS — Agent Operating Instructions (Router)

This file is the entry point for how AI agents operate across all of Sharad's
projects. Every agent (Cursor, Claude, Codex, or otherwise) reads this before
starting work — but this file itself is deliberately thin. It tells you which
role you're in and which file to read next; the actual process lives in
`agents/` and `routines/`.

## Why it's split this way

A single flat instructions file means every agent — whether it's building a
feature, discussing a spec, or scanning for bugs — reads the entire ruleset,
including sections it will never act on. That wastes tokens and increases the
chance of drift/confusion from irrelevant context. So this repo is structured
like OpenSpec is structured for product specs (see `agents/shared/openspec.md`):
one small file everyone reads, then per-role files that only the relevant
agent reads.

```
AGENTS.md              — this file: router only
agents/
  builder.md            — Role 1: assigned a Linear issue, builds it
  reviewer.md            — Role 2: re-woken by Sharad's feedback/approval comment
  spec-conversation.md   — Role 3: @mentioned on a spec-needed issue
  spec-drift.md          — Role 4a: idea-generation, routine-triggered
  bug-error.md           — Role 4b: idea-generation, routine-triggered
  market-feature.md      — Role 4c: idea-generation, routine-triggered
  shared/                — modules referenced by name from role files above
routines/               — named, git-stored jobs an external trigger invokes
                           by name; see routines/README.md
projects.md             — repo / Linear / Slack / prod URL per project
design/                 — UI animation & component copy-paste reference system
```

## Hub model: this repo is the only place instructions live

All process — for every project, every role, every routine — lives once, in
`rohrasharad-ship-it/AI-Workspace`. A project repo (e.g. resume-website) never
gets a full copy; it gets a **thin pointer `AGENTS.md`** that fetches and
follows this repo's files. Nothing is stored in Cursor Settings, Claude
project config, Codex config, or any other outside tool — an outside trigger
(co-work, cron) only ever needs to name a routine and a project; see
`routines/README.md` for exactly what that trigger should say.

**Thin `AGENTS.md` template for a new project repo** (created automatically by
`/init-project`):
```markdown
# Agent Instructions — <Project Name>

STEP 0 — before doing anything else: fetch and follow the full process from
rohrasharad-ship-it/AI-Workspace/AGENTS.md (main branch). Treat it as mandatory,
not optional context. This file only adds project-specific facts.

## Project Facts
- Repo: <owner/repo>
- Linear project: <name>
- Slack channel: <#channel>
- Tech stack: <one line>
```

**Requirement:** AI-Workspace must be reachable by whatever agent is doing the
fetch. Since this file has no secrets in it, keep AI-Workspace **public** so
any agent (Cursor cloud agent, Claude, Codex via GitHub Action) can fetch it
with zero special repo grants. If AI-Workspace must stay private, use a git
submodule in each project repo instead — more setup, but works without a
public repo.

## Core Concept: Trigger vs Gate

- **Trigger** = what *wakes* an agent (Linear assignment, an @mention, or a
  routine firing). Nothing else wakes an agent.
- **Gate** = what the woken agent checks before proceeding (e.g. the
  `agent-ready` label for the builder role).

Full detail: `agents/shared/loop.md`.

## Dispatch table — find your role, read its file, nothing else

| You were triggered by... | You are... | Read |
|---|---|---|
| Assigned to a Linear issue | **Builder** | `agents/builder.md` |
| Sharad commented on an issue with an open PR (feedback or "approved") | **Reviewer** | `agents/reviewer.md` |
| @mentioned in a comment on a `spec-needed` issue | **Spec Conversation** | `agents/spec-conversation.md` |
| The `idea-sweep` routine (or a spec-drift-only trigger) | **Spec-Drift** | `agents/spec-drift.md` |
| The `idea-sweep` routine (or a bug-error-only trigger) | **Bug/Error** | `agents/bug-error.md` |
| The `idea-sweep` routine (or a market-feature-only trigger) | **Market/Feature** | `agents/market-feature.md` |

Every role above also reads `agents/shared/conventions.md` — that file holds
the rules that apply regardless of role (new-issue conventions, the "always
apply" rule list, what Sharad does vs what agents do). It is the one file
every agent reads no matter what.

## Routines: how idea-generation actually gets triggered

Roles 1–3 above are woken directly by Linear. The three idea-generation roles
are not — something external has to trigger them, on a schedule or on demand.
That's what `routines/` is for: a routine is a named bundle (which roles, which
projects, what output) that an external trigger invokes by name, with the real
instructions living here in git, not pasted into any outside tool. Start at
`routines/README.md`.

## Projects

Every project this file's roles and routines can operate on — repo, Linear
project, Slack channel, prod URL — is in `projects.md`. Add new projects via
the `/init-project` skill, which also creates a project's thin pointer
`AGENTS.md` automatically.

## UI design reference

When building or speccing anything with a visual or motion component, read
`design/README.md` first. It catalogs external copy-paste sources (React Bits,
Aceternity UI, Anime.js, etc.), local snippets, and the workflow for adapting
them — **don't write UI animations from scratch** when a reference exists.
Full detail lives in `design/resources.md` and `design/workflow.md`.
