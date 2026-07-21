## Purpose

The entry point that routes every agent session to the correct role file and shared modules.

## Requirements

### Requirement: AGENTS.md acts as a thin router
The repo root `AGENTS.md` MUST be the single entry point every agent reads before any work. It MUST NOT contain full role instructions — only a dispatch table pointing to `agents/<role>.md` files and mandatory shared modules.

#### Scenario: Builder assigned to a Linear issue
- **WHEN** an agent starts a session on a product or infra repo whose `AGENTS.md` is a thin pointer
- **THEN** the agent fetches and follows `rohrasharad-ship-it/AI-Workspace/AGENTS.md` (main branch) as mandatory instructions
- **AND** reads `agents/builder.md` plus `agents/shared/conventions.md`

#### Scenario: Unknown trigger
- **WHEN** an agent cannot determine its role from the dispatch table
- **THEN** it MUST read only `agents/shared/conventions.md` and stop without writing code

### Requirement: Hub model prevents instruction drift
Full process instructions MUST live only in this repo. Product repos MUST contain a thin `AGENTS.md` with project facts (repo, Linear project, Slack channel, tech stack) and a pointer to this hub.

#### Scenario: New project onboarding
- **WHEN** `/init-project` runs for a new repo
- **THEN** the target repo gets a thin pointer `AGENTS.md`, not a copy of the full ruleset
- **AND** the project is registered in `projects.md`

### Requirement: Role dispatch table covers all agent types
`AGENTS.md` MUST map each trigger type to exactly one role file: builder (Linear assignment), reviewer (approval/feedback comment), spec-conversation (`@mention` on `spec-needed`), spec-drift/bug-error/market-feature (routine trigger).

#### Scenario: Idea-sweep routine fires
- **WHEN** an external trigger invokes a routine by name
- **THEN** the orchestrator reads `routines/<name>.md` and runs the listed role files against named projects from `projects.md`
