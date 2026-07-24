## Why

Merged OpenSpec change folders keep sitting in `openspec/changes/` because reviewer step B.3 (`npx openspec archive`) depends on an agent remembering it after every merge. SHA-174 cleaned up two stuck folders manually; three more piled up within days — the same failure mode, so a one-time fix is not enough.

## What Changes

- Add `scripts/archive-merged-openspec-changes.sh` — archives completed active changes when a merge lands on `main`, with a weekly sweep for orphans (mirrors `scripts/cleanup-preview-branches.sh`).
- Add `.github/workflows/openspec-archive.yml` — runs the script on every push to `main` and weekly (Monday 09:05 UTC, after preview-branch cleanup).
- Document the structural backup in `agents/shared/conventions.md` (same pattern as preview-branch cleanup).
- Extend `agents/spec-drift.md` housekeeping to run the archive sweep during idea-sweep.
- One-time cleanup: archive the three stuck folders (`cross-project-pattern-grouping`, `init-project-linear-project-id`, `sha-196-stale-issue-sweep-spec`).

## Capabilities

### New Capabilities

_None — archive automation is a structural backup for existing build-loop behavior._

### Modified Capabilities

- `build-loop`: Document that OpenSpec archive runs on merge via GitHub Action in addition to reviewer step B.3.
- `shared-conventions`: Document the scheduled + spec-drift backup for OpenSpec archive, parallel to preview-branch cleanup.

## Impact

- `scripts/archive-merged-openspec-changes.sh` — new script
- `.github/workflows/openspec-archive.yml` — new workflow (requires `contents: write` to push archive commits)
- `agents/shared/conventions.md`, `agents/reviewer.md`, `agents/spec-drift.md` — backup documentation
- `openspec/specs/build-loop/spec.md`, `openspec/specs/shared-conventions/spec.md` — requirement deltas
- `openspec/changes/archive/` — three folders moved from active changes (one-time cleanup)
