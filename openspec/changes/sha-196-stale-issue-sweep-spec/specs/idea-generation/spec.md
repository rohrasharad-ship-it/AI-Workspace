## ADDED Requirements

### Requirement: Spec-drift flags stale issues
On every spec-drift run (independent of gap-filing and issue-cap skips), the role MUST sweep open Backlog issues in the target Linear project for high-confidence "already shipped" candidates. It MUST post at most 3 comments per run (oldest Backlog first), skip issues flagged within the last 30 days, and MUST NOT close, cancel, or relabel any issue — comment only.

#### Scenario: Stale Backlog issue flagged
- **WHEN** spec-drift finds a Backlog issue whose described work appears already shipped in the codebase or OpenSpec, and no prior comment containing `Spec-drift check — this may already be done` was posted within 30 days
- **THEN** it posts a comment using the template: header `🔍 Spec-drift check — this may already be done`, cross-check date, **What I looked at**, **Why it looks resolved**, and asks whether it is safe to close — without closing or relabeling the issue

#### Scenario: Active or recently flagged issues skipped
- **WHEN** an issue is In Progress, In Review, Done, or already received a stale-issue comment within 30 days
- **THEN** spec-drift does not flag it in this run

#### Scenario: Cap reached mid-sweep
- **WHEN** spec-drift has already posted 3 stale-issue comments in the current run
- **THEN** it stops flagging additional issues until the next run
