## ADDED Requirements

### Requirement: Cross-project gap grouping on multi-project sweeps
When idea-sweep runs against two or more projects in one trigger, the orchestrator MUST collect gap candidates from each role per project, group candidates that describe the same underlying gap within the same role, and file one Linear issue per group instead of one per project.

#### Scenario: Same gap in three projects
- **WHEN** spec-drift finds "No PR template" in Resume Website, AI Landscape, and Usercon during one multi-project sweep
- **THEN** one Backlog issue is filed (not three) with an **Affects:** list naming all three projects

#### Scenario: Single-project sweep unchanged
- **WHEN** idea-sweep runs for only Resume Website
- **THEN** roles file issues directly in that project's Linear project with no grouping step

#### Scenario: Unique gaps not grouped
- **WHEN** two projects have different gaps in the same run
- **THEN** each gap files as its own issue in the appropriate Linear project (or PM OS for grouped cross-repo items only)

### Requirement: Grouped issues filed in PM OS
Cross-project grouped issues MUST be created in the PM OS Linear project with standard Issue Brief format plus an **Affects:** line listing every affected project name from `projects.md`.

#### Scenario: Grouped issue location
- **WHEN** a gap is grouped across multiple product projects
- **THEN** the issue is filed in PM OS, not duplicated into each product project's backlog

### Requirement: Per-role grouping boundary
Grouping MUST only combine candidates from the same idea-generation role within the same run. Spec-drift, bug-error, and market-feature candidates MUST NOT be merged with each other.

#### Scenario: Same symptom, different roles
- **WHEN** spec-drift and bug-error both surface a related problem in the same run
- **THEN** they remain separate issues (one per role), even if descriptions overlap
