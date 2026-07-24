## ADDED Requirements

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
