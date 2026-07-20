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

### Requirement: New routines added by file only
Adding a routine MUST require only creating `routines/<name>.md` with the same shape as `idea-sweep.md`. No code changes elsewhere.

#### Scenario: New routine needed
- **WHEN** a new scheduled job is defined
- **THEN** a new markdown file in `routines/` documents roles, cadence, and output; external triggers reference it by name
