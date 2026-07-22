## Purpose

Cross-cutting rules and formats that every agent role must follow regardless of task.
## Requirements
### Requirement: Issue Brief format for all created issues
Every agent that creates a Linear issue MUST use the five-field Issue Brief format: In short, Problem, Solution, Why, What it looks like — each exactly one line, plain language, no implementation detail.

#### Scenario: Idea-generation files issue
- **WHEN** spec-drift creates a new issue
- **THEN** the description follows Issue Brief format with execution detail in the first comment, not the description

### Requirement: Status Snapshot on every meaningful touch
Agents MUST maintain a four-line Status Snapshot block at the top of issue descriptions: Phase, Last update, PR, Preview — refreshed on every spec reply, PR open, self-QA fix, approval, or merge.

#### Scenario: Builder opens PR
- **WHEN** a PR is created for an infra/docs change
- **THEN** Status Snapshot shows Phase: In Review, PR link, and Preview: N/A (for AI-Workspace)

### Requirement: Always-apply rules enforced
All agents MUST follow the rules in `agents/shared/conventions.md`: no direct push to main, spec before code, no auto-merge, Vercel preview as review surface, feedback on Linear not PR, visual self-QA when applicable.

#### Scenario: Any agent session
- **WHEN** an agent starts work in any role
- **THEN** it reads `agents/shared/conventions.md` in addition to its role file

### Requirement: New issues assigned to Sharad with emoji titles
New issues MUST have assignee Sharad Rohra (never an agent at creation), title starting with one relevant emoji, and Issue Brief description.

#### Scenario: Reviewer spillover
- **WHEN** a reviewer notices an out-of-scope gap during a build
- **THEN** it files a separate Backlog `spec-needed` issue without blocking the current PR

### Requirement: OpenSpec per-capability structure mandated
Every repo MUST use OpenSpec with `openspec/project.md` and per-capability `openspec/specs/<name>/spec.md` files — not a single flat spec file.

#### Scenario: Agent reads spec for single feature
- **WHEN** a builder works one capability
- **THEN** it reads `openspec/project.md` plus only the relevant capability's `spec.md` — not the entire specs tree

### Requirement: PM OS has its own OpenSpec baseline
AI-Workspace MUST maintain `openspec/project.md` and per-capability specs so idea-generation sweeps can compare planned process against actual instruction files.

#### Scenario: Spec-drift sweeps PM OS
- **WHEN** idea-sweep runs spec-drift against AI-Workspace
- **THEN** it reads `openspec/project.md` and all files under `openspec/specs/` as the planned baseline

