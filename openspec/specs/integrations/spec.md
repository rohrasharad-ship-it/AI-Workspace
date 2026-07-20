## Purpose

External service wiring: project registry and Linear → Slack notifications.

## Requirements

### Requirement: Project registry in projects.md
`projects.md` MUST be the single source of truth for every project an agent or routine operates on, including repo, Linear project name, Linear Project ID (UUID), Slack channel, and Vercel prod URL.

#### Scenario: Routine resolves project
- **WHEN** a routine trigger names "Resume Website"
- **THEN** the orchestrator looks up the row in `projects.md` for repo, Linear Project ID, Slack channel, and prod URL

#### Scenario: New project onboarded
- **WHEN** `/init-project` completes
- **THEN** a new row is added to `projects.md` with the Linear Project ID from `list_projects`

### Requirement: Linear Project ID used for MCP queries
Agents MUST filter Linear `list_issues` by Linear Project ID (UUID), not display name — name filters silently return empty for some projects.

#### Scenario: Issue cap check
- **WHEN** idea-sweep checks open issue count
- **THEN** it uses the UUID from `projects.md`, paginates all results, and counts non-terminal statuses

### Requirement: Dual Slack notification paths
Idea-generation MUST use two independent Slack paths: (1) routine summary posted by the orchestrating agent at end of run, (2) per-issue Linear bot cards via project bell integration.

#### Scenario: New issue filed by spec-drift
- **WHEN** spec-drift creates an issue during idea-sweep
- **THEN** the routine summary mentions it at end of run AND Linear's bell posts a per-issue card (if configured)

#### Scenario: Agents do not post per-issue Slack
- **WHEN** an idea-generation role creates an issue
- **THEN** the role does NOT post a separate Slack message — only Linear's bell handles per-issue notifications

### Requirement: Linear bell configured per project
Each Linear project MUST have Slack bell notifications enabled for at least "Issue created" events, pointing to the channel in `projects.md`. Smoke test required after setup.

#### Scenario: Bell verification
- **WHEN** onboarding a new project or verifying cron health
- **THEN** a throwaway test issue confirms a Linear bot card appears in the project's Slack channel within ~1 minute

### Requirement: PM OS project registered
AI-Workspace (PM OS) MUST be registered in `projects.md` with Linear project "PM OS", Slack `#pm-ops`, and Vercel sandbox URL `ai-workspace.vercel.app`.

#### Scenario: Idea-sweep on PM OS
- **WHEN** idea-sweep runs against PM OS
- **THEN** spec-drift can read this repo's `openspec/` and compare against the instruction files in the codebase
