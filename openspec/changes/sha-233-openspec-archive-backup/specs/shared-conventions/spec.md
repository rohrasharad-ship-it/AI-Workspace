## ADDED Requirements

### Requirement: Structural backup for OpenSpec archive
AI-Workspace MUST maintain a non-agent-dependent path that archives completed OpenSpec change folders after merge: (1) a scheduled GitHub Action (`.github/workflows/openspec-archive.yml`) running `scripts/archive-merged-openspec-changes.sh` on every push to `main` and weekly (Monday 09:05 UTC), and (2) spec-drift housekeeping during idea-sweep running the same script in sweep mode.

#### Scenario: Merge lands without reviewer archive
- **WHEN** a merged PR leaves a completed change folder in `openspec/changes/`
- **THEN** the push-triggered GitHub Action moves it to `openspec/changes/archive/` within the same push cycle or the next weekly sweep

#### Scenario: Spec-drift weekly housekeeping
- **WHEN** idea-sweep runs spec-drift against AI-Workspace
- **THEN** step 11+ housekeeping includes running `archive-merged-openspec-changes.sh --sweep` and reporting archived count
