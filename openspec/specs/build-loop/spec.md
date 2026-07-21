## Purpose

The core development cycle from approved spec through PR, review, and merge.

## Requirements

### Requirement: Trigger vs gate separation
Linear assignment or `@mention` MUST wake an agent (trigger). The `agent-ready` label MUST be the only gate for whether a builder proceeds. Issue status MUST NOT be used as a gate because Linear auto-sets "In Progress" on assignment.

#### Scenario: Builder wakes on spec-needed issue
- **WHEN** a builder agent is assigned to an issue labeled `spec-needed`
- **THEN** it posts a refusal comment and stops without writing code

#### Scenario: Builder wakes on agent-ready issue
- **WHEN** a builder agent is assigned to an issue labeled `agent-ready`
- **THEN** it proceeds with cleanup, OpenSpec workflow, implementation, and PR

### Requirement: Builder follows OpenSpec before coding
On `agent-ready` issues, the builder MUST install/verify OpenSpec, run propose, then apply before opening a PR. It MUST update specs before code changes.

#### Scenario: Feature implementation
- **WHEN** a builder implements an approved issue
- **THEN** it creates or updates OpenSpec change artifacts before modifying code
- **AND** runs the project build command before opening a PR

### Requirement: PR opens In Review immediately
After opening a PR, the builder MUST move the Linear issue to `In Review` as the next action — not gated on Vercel, screenshots, or Slack.

#### Scenario: PR created
- **WHEN** a builder opens a PR for an `agent-ready` issue
- **THEN** the issue status moves to `In Review` immediately
- **AND** the Status Snapshot block in the issue description is refreshed

### Requirement: Reviewer merges only on explicit approval
The reviewer role MUST NOT merge until Sharad comments an explicit approval (`@agent approved`, `lgtm`, etc.). On approval it MUST merge, run `openspec archive`, move to Done, and notify Slack.

#### Scenario: Sharad approves
- **WHEN** Sharad comments "@agent approved" on an issue with a green PR
- **THEN** the reviewer merges the PR, archives the OpenSpec change, and posts "🚀 live" to Slack

#### Scenario: Sharad gives feedback
- **WHEN** Sharad comments feedback on an open PR issue
- **THEN** the reviewer updates the spec first, then code, pushes to the same branch, and comments on Linear (not PR)

### Requirement: Preview branch cleanup on build start
When a builder starts on `agent-ready`, it MUST delete any leftover `preview/<issue-id>-*` branches from the spec phase.

#### Scenario: Spec preview branch exists
- **WHEN** a builder begins work and finds `preview/SHA-40-v1` on the remote
- **THEN** it deletes that branch before creating its feature branch
