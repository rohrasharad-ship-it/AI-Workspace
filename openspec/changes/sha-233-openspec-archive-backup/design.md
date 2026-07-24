## Context

The reviewer role archives OpenSpec changes manually after merge (`agents/reviewer.md` step B.3). Agents skip this step reliably enough that merged, fully-checked-off folders accumulate in `openspec/changes/`. Preview-branch cleanup already solved the same class of problem with a script + weekly GitHub Action + spec-drift housekeeping pass.

## Goals / Non-Goals

**Goals:**
- Archive completed change folders automatically when their merge lands on `main`
- Catch orphans via a weekly sweep and during spec-drift housekeeping
- Match the preview-branch-cleanup pattern (script, workflow, conventions doc, spec-drift step)

**Non-Goals:**
- Replacing the reviewer's manual `openspec archive` step (keep both paths)
- Linear-native automation (archive is a git operation; no Linear equivalent exists)
- Archiving incomplete changes or changes with open PRs

## Decisions

### 1. Push-triggered archive from merge diff

On every push to `main`, parse changed paths for `openspec/changes/<name>/` (excluding `archive/`). For each unique change name that `openspec list --json` reports as `complete`, run `openspec archive <name> -y --skip-specs`.

**Why `--skip-specs`:** Builders sync delta specs to main specs before opening the PR (tasks include "Sync main specs"). Re-syncing at archive time is redundant and can conflict.

### 2. Weekly sweep catches orphans

List active changes via `openspec list --json`. Archive any with `status: complete` that:
- Has no open GitHub PR touching `openspec/changes/<name>/`, and
- Either appears in the push diff on a prior merge, or is older than 24 hours (builder sessions that died after checking tasks but before opening a PR are rare; the age gate avoids archiving in-flight work).

Uses `gh` CLI (available in GitHub Actions) for open-PR detection.

### 3. Workflow commits back to main

Unlike preview cleanup (branch deletes), archive moves files within the repo. The workflow must commit and push archive moves to `main` when changes are made.

### 4. Schedule offset from preview cleanup

Monday 09:05 UTC — five minutes after preview-branch cleanup (09:00) so both housekeeping jobs don't contend.

## Risks / Trade-offs

- **[Double archive]** Reviewer and Action both archive → `openspec archive` is idempotent (folder already gone = no-op). Safe.
- **[Push loop]** Archive commit triggers another push → second run finds no active changes in diff. Safe.
- **[Incomplete change archived on sweep]** Mitigated by open-PR check + 24h age gate on sweep-only path.

## Migration Plan

1. Ship script + workflow
2. This PR includes one-time archive of three stuck folders
3. No manual steps for Sharad
