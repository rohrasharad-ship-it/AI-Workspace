## Purpose

Named, git-stored job bundles that external triggers invoke by name without pasting instructions into outside tools.

## Requirements

### Requirement: Routines compose existing roles
A routine file MUST list which agent roles run, against which projects, and what consolidated output to produce. It MUST NOT duplicate role instructions — those live in `agents/<role>.md`.

#### Scenario: External trigger invokes routine
- **WHEN** a co-work schedule or cron says `Run the "idea-sweep" routine for Resume Website`
- **THEN** the orchestrator reads `routines/idea-sweep.md` and executes the listed roles against the named project from `projects.md`

### Requirement: Idea-sweep bundles three idea-generation roles
The `idea-sweep` routine MUST run spec-drift, bug-error, and market-feature in order for each target project, with a single issue-cap check per project before any role starts.

#### Scenario: All projects sweep
- **WHEN** the trigger says "all projects"
- **THEN** the orchestrator loops every row in `projects.md`, running the cap check and all three roles per project under cap

### Requirement: Consolidated Slack summary per project
After all roles finish for a project, the orchestrator MUST post one Slack message per project (not per role) summarizing issues filed or "clean" status per role.

#### Scenario: Sweep completes with findings
- **WHEN** idea-sweep finishes for Resume Website
- **THEN** one message posts to `#resume-website` with counts and links per role

#### Scenario: Project skipped at cap
- **WHEN** a project hits the issue cap
- **THEN** only the skip message posts — no consolidated summary

### Requirement: Cross-project gap grouping on multi-project sweeps
When idea-sweep runs against two or more projects in one trigger, the orchestrator MUST collect gap candidates from each role per project, group candidates that describe the same underlying gap within the same role, and file one Linear issue per group instead of one per project.

#### Scenario: Same gap in three projects
- **WHEN** spec-drift finds the same gap in Resume Website, AI Landscape, and Usercon during one multi-project sweep
- **THEN** one Backlog issue is filed (not three) with an **Affects:** list naming all three projects

#### Scenario: Single-project sweep unchanged
- **WHEN** idea-sweep runs for only Resume Website
- **THEN** roles file issues directly in that project's Linear project with no grouping step

#### Scenario: Grouped issues filed in PM OS
- **WHEN** a gap is grouped across multiple product projects
- **THEN** the issue is filed in PM OS, not duplicated into each product project's backlog

#### Scenario: Per-role grouping boundary
- **WHEN** spec-drift and bug-error both surface a related problem in the same run
- **THEN** they remain separate issues (one per role), even if descriptions overlap

### Requirement: New routines added by file only
Adding a routine MUST require only creating `routines/<name>.md` with the same shape as `idea-sweep.md`. No code changes elsewhere.

#### Scenario: New routine needed
- **WHEN** a new scheduled job is defined
- **THEN** a new markdown file in `routines/` documents roles, cadence, and output; external triggers reference it by name
