## ADDED Requirements

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
