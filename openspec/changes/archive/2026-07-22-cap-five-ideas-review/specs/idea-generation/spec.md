## MODIFIED Requirements

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
