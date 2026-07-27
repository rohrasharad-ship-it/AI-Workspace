## ADDED Requirements

### Requirement: Routine run log dashboard on sandbox
AI-Workspace MUST host a static `routine-log.html` page showing idea-sweep pipeline health: global pending bugs/features, created today, and per-project cards for every row in `projects.md`.

#### Scenario: Page loads with generated data
- **WHEN** a user opens `/routine-log.html` on a deployed branch
- **THEN** the page fetches `/data/routine-log.json` and renders pipeline KPIs and one card per registered project

#### Scenario: Zero-pending project visible
- **WHEN** a project has no pending pipeline issues
- **THEN** its card still appears with an "all clear" or zero state

#### Scenario: Clean sweep visible
- **WHEN** a sweep run logged zero findings for a project
- **THEN** the project's recent sweeps section shows a clean state for that run

### Requirement: Routine log data generation
AI-Workspace MUST provide `scripts/generate-routine-log.mjs` that reads `projects.md`, queries Linear (via `LINEAR_API_KEY`), merges `data/sweep-runs.jsonl`, and writes `data/routine-log.json`.

#### Scenario: Script run with API key
- **WHEN** `LINEAR_API_KEY` is set and the script runs
- **THEN** `data/routine-log.json` is updated with current pending counts and recent sweep history

### Requirement: Idea-sweep appends sweep ledger
After each idea-sweep run per project, the orchestrator MUST append one JSONL line to `data/sweep-runs.jsonl` recording filed bug/feature counts or a clean run.

#### Scenario: Clean sweep logged
- **WHEN** all three roles file nothing for a project
- **THEN** a ledger entry with `clean: true` and zero counts is appended
