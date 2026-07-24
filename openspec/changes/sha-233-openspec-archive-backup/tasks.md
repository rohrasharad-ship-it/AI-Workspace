## 1. One-time cleanup

- [x] 1.1 Archive stuck folders: `cross-project-pattern-grouping`, `init-project-linear-project-id`, `sha-196-stale-issue-sweep-spec`

## 2. Archive automation

- [x] 2.1 Create `scripts/archive-merged-openspec-changes.sh` (push mode + sweep mode)
- [x] 2.2 Create `.github/workflows/openspec-archive.yml`

## 3. Documentation

- [x] 3.1 Add structural backup section to `agents/shared/conventions.md`
- [x] 3.2 Note backup in `agents/reviewer.md` step B.3
- [x] 3.3 Extend `agents/spec-drift.md` housekeeping with archive sweep

## 4. Sync main specs

- [x] 4.1 Apply delta to `openspec/specs/build-loop/spec.md`
- [x] 4.2 Apply delta to `openspec/specs/shared-conventions/spec.md`

## 5. Verify

- [x] 5.1 Run `npm run build` (openspec validate)
- [x] 5.2 Dry-run archive script locally
