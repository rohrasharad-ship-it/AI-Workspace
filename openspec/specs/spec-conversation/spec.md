## Purpose

The spec-phase role for refining `spec-needed` issues before any code is written.

## Requirements

### Requirement: Spec conversation is @mention triggered only
The spec-conversation role MUST NOT be Linear-assigned. It activates only when Sharad `@mentions` an agent in a comment on a `spec-needed` issue.

#### Scenario: Sharad asks for input
- **WHEN** Sharad `@mentions` an agent on a `spec-needed` issue
- **THEN** the agent reads the issue, `openspec/project.md`, and relevant capability specs
- **AND** replies in the Linear comment thread with understanding, questions, and alternatives

### Requirement: No code during spec phase
During spec conversation, the agent MUST NOT write code in the real project repo or run OpenSpec propose/apply commands.

#### Scenario: Active spec discussion
- **WHEN** an issue remains labeled `spec-needed`
- **THEN** the agent may create visual spec previews per `visual-qa` capability but MUST NOT open feature PRs or modify product code

### Requirement: Status snapshot refreshed every reply
On every spec-conversation reply, the agent MUST update the Status Snapshot block at the top of the issue description.

#### Scenario: Back-and-forth discussion
- **WHEN** the agent posts any reply during spec conversation
- **THEN** the Status Snapshot reflects current phase ("Spec discussion"), date, and one-sentence summary

### Requirement: Agent locks spec and flips label on approval
When Sharad gives any affirmative signal ("yes", "go ahead", "sounds good", "ship it", "approved", "lgtm", or similar), the agent MUST finalize the issue description, swap `spec-needed` → `agent-ready`, and assign the builder — all in the same turn.

#### Scenario: Sharad approves spec
- **WHEN** Sharad replies affirmatively to the agent's readiness check
- **THEN** the agent updates spec text, changes label to `agent-ready`, assigns the builder agent, and does NOT require Sharad to manually change label or assignee

### Requirement: Visual features get full-effort spec previews
When a proposed feature has a meaningful visual or motion component, the spec-conversation agent MUST attach a full-effort visual preview link per the visual-qa capability.

#### Scenario: Animated hero proposed
- **WHEN** the spec conversation discusses a scroll-linked animation
- **THEN** the agent provides a working HTML preview on a `preview/<issue-id>-v<n>` branch with the real interaction demonstrated
