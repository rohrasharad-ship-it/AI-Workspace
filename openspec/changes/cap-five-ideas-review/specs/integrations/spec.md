## MODIFIED Requirements

### Requirement: Linear Project ID used for MCP queries
Agents MUST filter Linear `list_issues` by Linear Project ID (UUID), not display name — name filters silently return empty for some projects.

#### Scenario: Issue cap check
- **WHEN** idea-sweep checks open issue count
- **THEN** it uses the UUID from `projects.md`, paginates all results, verifies each issue's `projectId` matches, and counts only issues whose status is Backlog, Todo, In Progress, or In Review
