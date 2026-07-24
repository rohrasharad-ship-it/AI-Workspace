## MODIFIED Requirements

### Requirement: Reviewer merges only on explicit approval
The reviewer role MUST NOT merge until Sharad comments an explicit approval (`@agent approved`, `lgtm`, etc.). On approval it MUST merge, run `npx openspec archive`, move to Done, and notify Slack. A GitHub Action on push to `main` (`.github/workflows/openspec-archive.yml`) MUST also archive any completed OpenSpec change folders touched by the merge as a structural backup — the same way preview-branch cleanup backs up agent-forgotten branch deletes.

#### Scenario: Sharad approves
- **WHEN** Sharad comments "@agent approved" on an issue with a green PR
- **THEN** the reviewer merges the PR, archives the OpenSpec change, and posts "🚀 live" to Slack

#### Scenario: Sharad gives feedback
- **WHEN** Sharad comments feedback on an open PR issue
- **THEN** the reviewer updates the spec first, then code, pushes to the same branch, and comments on Linear (not PR)

#### Scenario: Reviewer forgets archive step
- **WHEN** a PR with a completed OpenSpec change merges to `main`
- **THEN** the openspec-archive GitHub Action archives the change folder even if the reviewer agent skipped `npx openspec archive`
