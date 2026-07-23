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

### Requirement: Blocked-agent handover convention
When an agent cannot complete assigned work because a required tool integration is definitively unavailable (e.g. no Linear MCP, no push access to the target repo), it MUST write a handover under `handovers/` in AI-Workspace using the path and template in `agents/shared/conventions.md` (Blocked-agent handover section), comment on the Linear issue with the handover link, and refresh the Status Snapshot noting the blocker.

#### Scenario: Cloud builder lacks Linear MCP
- **WHEN** a builder session finishes implementation but cannot create a follow-up Linear issue
- **THEN** it writes `handovers/<ISSUE-ID>-<short-slug>.md` with the required header and body sections, commits to its branch, and comments on the driving issue with the GitHub link

#### Scenario: Builder cannot push to private target repo
- **WHEN** a builder finishes code locally but lacks push access to the production repo
- **THEN** it writes `handovers/<ISSUE-ID>/README.md` with apply instructions and any artifacts, commits to AI-Workspace, and comments on the Linear issue with the bundle path

#### Scenario: Receiving agent picks up handover
- **WHEN** an agent with the missing tool access is woken to continue blocked work
- **THEN** it reads the handover file from the linked path and follows the numbered Instructions for receiving agent before improvising its own approach

