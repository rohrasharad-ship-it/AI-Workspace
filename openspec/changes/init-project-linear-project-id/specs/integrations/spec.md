## MODIFIED Requirements

### Requirement: Project registry in projects.md
`projects.md` MUST be the single source of truth for every project an agent or routine operates on, including repo, Linear project name, Linear Project ID (UUID), Slack channel, and Vercel prod URL.

#### Scenario: Routine resolves project
- **WHEN** a routine trigger names "Resume Website"
- **THEN** the orchestrator looks up the row in `projects.md` for repo, Linear Project ID, Slack channel, and prod URL

#### Scenario: New project onboarded
- **WHEN** `/init-project` completes
- **THEN** a new row is added to `projects.md` with all six columns filled, including the Linear Project ID UUID captured from the `save_project` response in Step D (or confirmed via `list_projects` if needed)
