## ADDED Requirements

### Requirement: PM OS has its own OpenSpec baseline
AI-Workspace MUST maintain `openspec/project.md` and per-capability specs so idea-generation sweeps can compare planned process against actual instruction files.

#### Scenario: Spec-drift sweeps PM OS
- **WHEN** idea-sweep runs spec-drift against AI-Workspace
- **THEN** it reads `openspec/project.md` and all files under `openspec/specs/` as the planned baseline
