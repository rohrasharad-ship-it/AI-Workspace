## Purpose

Three routine-triggered roles that file Backlog issues for Sharad to triage: spec-drift, bug-error, and market-feature.
## Requirements
### Requirement: Idea-generation roles are routine-triggered only
Spec-drift, bug-error, and market-feature agents MUST NOT be woken by Linear assignment. They run only via named routines (default: `idea-sweep`) or equivalent standalone triggers.

#### Scenario: Weekly idea sweep
- **WHEN** the `idea-sweep` routine runs for a project
- **THEN** spec-drift, bug-error, and market-feature execute in that order against the target repo

### Requirement: Spec-drift compares OpenSpec to codebase
The spec-drift role MUST read `openspec/project.md` and every file under `openspec/specs/`, then compare against the actual codebase to find meaningful gaps (planned but unbuilt or half-built).

#### Scenario: Gap found
- **WHEN** spec-drift finds a specced capability missing from the codebase
- **THEN** it files a Backlog issue with `spec-needed` label, assignee Sharad Rohra, Issue Brief description, and execution detail in the first comment

#### Scenario: Preview branch housekeeping
- **WHEN** spec-drift completes its scan (regardless of issues filed)
- **THEN** it lists remote `preview/*` branches and deletes orphans whose issues are no longer `spec-needed`

### Requirement: Bug-error reads production logs
The bug-error role MUST read Vercel production runtime errors/logs from the last 24 hours and file issues for real, actionable errors — filtering bot noise and self-resolved blips.

#### Scenario: Recurring runtime error
- **WHEN** production logs show a repeatable error affecting a core flow
- **THEN** bug-error files a `spec-needed` issue with High priority and log evidence in the first comment

### Requirement: Market-feature proposes new ideas from vision
The market-feature role MUST read `openspec/project.md` (including Out of Scope) and all capability specs, then propose up to 3 features not yet specced or tracked — always with a visual preview.

#### Scenario: New feature proposed
- **WHEN** market-feature identifies an opportunity aligned with project vision
- **THEN** it files a `spec-needed` issue with a minimal-effort visual preview and respects Out of Scope boundaries

### Requirement: Idea-generation never sets agent-ready
All three roles MUST create issues as Backlog + `spec-needed` only. They MUST NEVER set `agent-ready` or assign an agent.

#### Scenario: Issue created by spec-drift
- **WHEN** any idea-generation role creates an issue
- **THEN** assignee is Sharad Rohra, label is `spec-needed`, and title starts with one relevant emoji

### Requirement: Issue cap enforced before scanning
Before any idea-generation role runs for a project, the orchestrator MUST count issues in that project's active pipeline stages (cap: 5 per project using Linear Project ID). Active stages are Backlog, Todo, In Progress, and In Review only. At or over cap, all three roles skip that project.

#### Scenario: Backlog at cap
- **WHEN** a project has 5 or more issues in Backlog, Todo, In Progress, or In Review
- **THEN** the routine posts a skip message to Slack and does not run spec-drift, bug-error, or market-feature for that project

#### Scenario: Done or canceled issues excluded
- **WHEN** a project has Done, Canceled, or Duplicate issues
- **THEN** those issues do not count toward the cap of 5

#### Scenario: Wrong project excluded
- **WHEN** an issue belongs to a different Linear project than the target
- **THEN** it does not count toward that project's cap

