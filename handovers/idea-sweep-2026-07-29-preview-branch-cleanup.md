# Handover: Orphaned preview branch cleanup (105 branches)

**For:** Any agent/session with `git push --delete` access to `rohrasharad-ship-it/AI-Workspace` (or a human with GitHub branch-delete permissions)
**From:** spec-drift role, idea-sweep routine, Resume Website run — 2026-07-29
**Blocked by:** This session's git remote goes through a policy-enforcing proxy that returns `HTTP 403` on any `git push origin --delete <branch>`, including a branch this same session created and pushed moments earlier (confirmed as a hard non-retriable policy denial, not a transient failure — see `/root/.ccr/README.md`: "do not retry organization policy denials (403/407) — report them instead"). Regular branch creation/push works fine; only ref deletion is blocked. No GitHub MCP tool for branch/ref deletion is available either (`mcp__github__*` has create_branch, list_branches, but no delete equivalent).
**Action:** Delete the 105 orphaned `preview/*` branches listed below from `rohrasharad-ship-it/AI-Workspace`.
**Issue:** Not tied to a single Linear issue — this is the `agents/spec-drift.md` step 11 housekeeping sweep (preview-branch cleanup), run as part of the `idea-sweep` routine for the Resume Website project.

## Payload

Full team-wide sweep was run (per `scripts/cleanup-preview-branches.sh` semantics — the script normally needs `LINEAR_API_KEY`, which this session also lacked as a raw env var; the check below was done manually via the Linear MCP `list_issues` tool against the whole `Sharad Rohra` team instead, fetching every issue's `status` + `labels` in two paginated calls and cross-referencing against `git ls-remote --heads origin | grep preview/`).

**Rule applied** (from `agents/spec-drift.md` step 11 / `agents/shared/conventions.md`): delete a `preview/<issue-id>-v<n>` branch when the issue is no longer `spec-needed` (moved to `agent-ready`, `In Review`, `Done`, `Canceled`, or `Duplicate`), or when it's an older version than the latest branch for that issue (no multi-version conflicts were found — every branch below is the only version for its issue).

**14 branches confirmed still active — do NOT delete these:**
```
preview/SHA-251-v1
preview/SHA-252-v1
preview/SHA-253-v1
preview/SHA-254-v1
preview/SHA-255-v1
preview/SHA-256-v1
preview/SHA-258-v1
preview/SHA-259-v1
preview/SHA-260-v1
preview/SHA-261-v1
preview/SHA-262-v1
preview/SHA-263-v1
preview/SHA-264-v1
preview/SHA-265-v1
```
(All are Backlog + `spec-needed` only, no `agent-ready` label, as of 2026-07-29.)

**105 orphaned branches to delete** (issue status noted; re-verify status hasn't changed since 2026-07-29 before deleting if this handover sits for a while):

```
preview/SHA-100-v1   Done, agent-ready
preview/SHA-101-v1   Canceled
preview/SHA-102-v1   Canceled
preview/SHA-103-v1   Done, agent-ready
preview/SHA-104-v1   Canceled
preview/SHA-115-v1   Done, agent-ready
preview/SHA-116-v1   Done, agent-ready
preview/SHA-117-v1   Done, agent-ready
preview/SHA-123-v1   Canceled
preview/SHA-124-v1   Canceled
preview/SHA-125-v1   Canceled
preview/SHA-126-v1   Duplicate
preview/SHA-128-v1   Duplicate
preview/SHA-129-v1   Duplicate
preview/SHA-130-v1   Duplicate
preview/SHA-131-v1   Duplicate
preview/SHA-132-v1   Duplicate
preview/SHA-133-v1   Duplicate
preview/SHA-134-v1   Duplicate
preview/SHA-135-v1   Canceled
preview/SHA-138-v1   Done, agent-ready
preview/SHA-139-v1   Done, agent-ready
preview/SHA-140-v1   Done, agent-ready
preview/SHA-141-v1   Canceled
preview/SHA-142-v1   Canceled
preview/SHA-143-v1   Done, agent-ready
preview/SHA-144-v1   Canceled
preview/SHA-145-v1   Canceled
preview/SHA-147-v1   Canceled
preview/SHA-148-v1   Canceled
preview/SHA-149-v1   Canceled
preview/SHA-152-v1   Canceled
preview/SHA-158-v1   Canceled
preview/SHA-159-v1   Canceled
preview/SHA-160-v1   Canceled, agent-ready
preview/SHA-161-v1   Canceled
preview/SHA-163-v1   Canceled
preview/SHA-164-v1   Canceled
preview/SHA-173-v1   Done, agent-ready
preview/SHA-176-v1   Canceled
preview/SHA-18-v1    Canceled
preview/SHA-19-v1    Canceled
preview/SHA-20-v1    Canceled
preview/SHA-201-v1   Canceled, agent-ready
preview/SHA-202-v1   Canceled
preview/SHA-231-v1   Done, agent-ready+spec-needed
preview/SHA-232-v1   Canceled
preview/SHA-235-v1   Canceled
preview/SHA-236-v1   Canceled
preview/SHA-237-v1   Canceled
preview/SHA-238-v1   Canceled
preview/SHA-239-v1   Done, agent-ready
preview/SHA-24-v1    Canceled
preview/SHA-240-v1   Canceled
preview/SHA-241-v1   Canceled
preview/SHA-242-v1   Canceled
preview/SHA-243-v1   Done, agent-ready
preview/SHA-244-v1   Canceled
preview/SHA-25-build Canceled (non-standard branch name, not preview/<id>-v<n>, but same repo/issue — safe to delete, issue is Canceled)
preview/SHA-26-v1    Canceled
preview/SHA-28-v1    Canceled
preview/SHA-29-v1    Done
preview/SHA-30-v1    Canceled
preview/SHA-31-v1    Canceled
preview/SHA-33-v1    Done
preview/SHA-37-v1    Canceled
preview/SHA-38-v1    Canceled
preview/SHA-44-v1    Done
preview/SHA-47-v1    Canceled
preview/SHA-48-v1    Canceled
preview/SHA-50-v1    Canceled
preview/SHA-51-v1    Canceled
preview/SHA-55-v1    Canceled
preview/SHA-56-v1    Canceled
preview/SHA-57-v1    Canceled
preview/SHA-58-v2    Canceled
preview/SHA-64-v1    Done, agent-ready
preview/SHA-65-v1    Done, agent-ready
preview/SHA-66-v1    Canceled
preview/SHA-71-v1    Canceled
preview/SHA-72-v1    Done, agent-ready
preview/SHA-73-v1    Canceled
preview/SHA-74-v1    Done, agent-ready
preview/SHA-75-v1    Done, agent-ready
preview/SHA-76-v1    Done, agent-ready
preview/SHA-81-v1    Done, agent-ready
preview/SHA-83-v1    Canceled
preview/SHA-84-v1    Canceled
preview/SHA-85-v1    Canceled
preview/SHA-86-v1    Canceled
preview/SHA-87-v1    Canceled
preview/SHA-88-v1    Canceled
preview/SHA-89-v1    Canceled
preview/SHA-91-v1    Canceled
preview/SHA-92-v1    Canceled
preview/SHA-93-v1    Canceled
preview/SHA-94-v1    Canceled
preview/SHA-95-v1    Canceled
preview/SHA-96-v1    Done, agent-ready
preview/SHA-97-v1    Canceled
preview/SHA-98-v1    Canceled
preview/SHA-99-v1    Canceled
preview/sha-169-v1   Canceled
preview/sha-170-v1   Canceled
preview/sha-171-v1   Done, agent-ready
```

**One unrelated stray branch** from this session's own proxy-restriction test (not a `preview/*` branch, safe to delete any time): `test-proxy-check-delete-me`. Created and pushed by this session to confirm delete was policy-blocked and not transient; the push succeeded but the delete of the same branch also 403'd, confirming the block is on deletion specifically. Harmless if left, but should be cleaned up whenever a session with delete access next touches this repo.

## Instructions for receiving agent

1. Confirm `git push --delete` (or GitHub UI/API branch delete) actually works in your session before starting — don't assume.
2. For each branch in the 105-branch list, re-check its Linear issue hasn't moved back to a still-open `spec-needed`-only state since 2026-07-29 (unlikely, but cheap to skip re-verifying only if you trust this handover is fresh). If unchanged, delete:
   ```bash
   git push origin --delete "preview/SHA-100-v1"
   # ...repeat, or batch multiple refspecs in one push command
   ```
3. Also delete `test-proxy-check-delete-me`.
4. Do **not** touch any branch in the 14-branch "still active" list above, `main`, or any `claude/*` dev branch.
5. Once done, delete this handover file (`git rm handovers/idea-sweep-2026-07-29-preview-branch-cleanup.md`) since the work will be fully complete and tracked only in git branch state at that point.
