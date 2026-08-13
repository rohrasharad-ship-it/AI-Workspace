## Purpose

External service wiring: project registry, Linear Project ID resolution, and
Linear's (optional, not agent-managed) Slack bell.
## Requirements
### Requirement: Project registry in projects.md
`projects.md` MUST be the single source of truth for every project an agent or routine operates on, including repo, Linear project name, Linear Project ID (UUID), Slack channel, and Vercel prod URL.

#### Scenario: Routine resolves project
- **WHEN** a routine trigger names "Resume Website"
- **THEN** the orchestrator looks up the row in `projects.md` for repo, Linear Project ID, Slack channel, and prod URL

#### Scenario: New project onboarded
- **WHEN** `/init-project` completes
- **THEN** a new row is added to `projects.md` with all six columns filled, including the Linear Project ID UUID captured from the `save_project` response in Step D (or confirmed via `list_projects` if needed)

### Requirement: Linear Project ID used for MCP queries
Agents MUST filter Linear `list_issues` by Linear Project ID (UUID), not display name — name filters silently return empty for some projects.

#### Scenario: Issue cap check
- **WHEN** idea-sweep checks open issue count
- **THEN** it uses the UUID from `projects.md`, paginates all results, verifies each issue's `projectId` matches, and counts only issues whose status is Backlog, Todo, In Progress, or In Review

### Requirement: Agents never post to Slack for idea-generation
Idea-generation routines and roles MUST NOT post any message to Slack — no routine summary, no cap-skip notice, no per-issue message. Linear is the only surface these roles write to.

#### Scenario: New issue filed by spec-drift
- **WHEN** spec-drift creates an issue during idea-sweep
- **THEN** the agent posts nothing to Slack; Linear's own project bell (a separate, Linear-side setting) may independently post a per-issue card if a human has enabled it

#### Scenario: Agents do not post per-issue Slack
- **WHEN** an idea-generation role creates an issue
- **THEN** the role does NOT post a separate Slack message

### Requirement: Linear bell is optional and not agent-managed
Linear's per-project Slack bell (Issue created events) is a Linear workspace setting, not something any routine or role in this repo configures or depends on. It MAY be enabled or disabled per project at Sharad's discretion, independent of routine behavior.

#### Scenario: Bell verification (only if intentionally enabled)
- **WHEN** a human has enabled the bell for a project and wants to confirm it works
- **THEN** a throwaway test issue confirms a Linear bot card appears in the project's Slack channel within ~1 minute

### Requirement: PM OS project registered
AI-Workspace (PM OS) MUST be registered in `projects.md` with Linear project "PM OS", Slack `#pm-ops`, and Vercel sandbox URL `ai-workspace-blond.vercel.app`.

#### Scenario: Idea-sweep on PM OS
- **WHEN** idea-sweep runs against PM OS
- **THEN** spec-drift can read this repo's `openspec/` and compare against the instruction files in the codebase

