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

### Requirement: Spec-drift flags stale issues
On every spec-drift run (independent of gap-filing and issue-cap skips), the role MUST sweep open Backlog issues in the target Linear project for high-confidence "already shipped" candidates. It MUST post at most 3 comments per run (oldest Backlog first), skip issues flagged within the last 30 days, and MUST NOT close, cancel, or relabel any issue — comment only.

#### Scenario: Stale Backlog issue flagged
- **WHEN** spec-drift finds a Backlog issue whose described work appears already shipped in the codebase or OpenSpec, and no prior comment containing `Spec-drift check — this may already be done` was posted within 30 days
- **THEN** it posts a comment using the template: header `🔍 Spec-drift check — this may already be done`, cross-check date, **What I looked at**, **Why it looks resolved**, and asks whether it is safe to close — without closing or relabeling the issue

#### Scenario: Active or recently flagged issues skipped
- **WHEN** an issue is In Progress, In Review, Done, or already received a stale-issue comment within 30 days
- **THEN** spec-drift does not flag it in this run

#### Scenario: Cap reached mid-sweep
- **WHEN** spec-drift has already posted 3 stale-issue comments in the current run
- **THEN** it stops flagging additional issues until the next run

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

### Requirement: Defer filing during multi-project sweeps
When idea-sweep triggers against two or more projects, each idea-generation role MUST NOT call Linear `save_issue` during per-project scanning. Instead, each role MUST append a grouping candidate (Issue Brief fields, execution detail, attachments) to the run ledger for the orchestrator to group and file after that role finishes all projects.

#### Scenario: Multi-project deferral
- **WHEN** bug-error scans three projects in one idea-sweep run
- **THEN** it produces candidates for the orchestrator and files zero issues until the grouping step completes

#### Scenario: Single-project immediate filing
- **WHEN** market-feature runs for one project only
- **THEN** it files issues directly in that project's Linear project as today

### Requirement: Grouping candidate contents
Each deferred candidate MUST include: role name, project name from `projects.md`, normalized title, full Issue Brief fields, execution-detail payload for the first comment, and any screenshots or visual previews collected for that project.

#### Scenario: Orchestrator receives complete candidate
- **WHEN** spec-drift defers a gap from Resume Website during a multi-project sweep
- **THEN** the candidate includes enough detail to file a grouped issue without re-scanning the repo
