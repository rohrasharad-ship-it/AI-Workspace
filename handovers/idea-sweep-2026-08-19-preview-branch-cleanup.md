# Handover: 106 orphaned preview/* branches ready to delete, but this session has no delete-ref access

**For:** Any agent/session with `git push --delete` rights on `rohrasharad-ship-it/AI-Workspace` (or GitHub admin/write access to delete refs via API), not just push-to-existing-branch rights
**From:** spec-drift housekeeping (step 11), running inside the `idea-sweep` routine for Resume Website, 2026-08-19
**Blocked by:** `git push origin --delete <branch>` returned `HTTP 403` for every branch tested (`RPC failed; HTTP 403 curl 22`) — this session's git credential can push commits to its own designated branch but cannot delete refs on `origin`. The GitHub MCP server available in this session also has no delete-branch/delete-ref tool (checked: `create_branch`, `list_branches`, `delete_file`, `create_or_update_file` — no ref-deletion tool exists in the toolset). `LINEAR_API_KEY` is also unset in this session, so `scripts/cleanup-preview-branches.sh` itself can't run either (it hard-requires the key even for `--dry-run`, since it looks up each issue's Linear status via curl).
**Action:** Delete exactly the 106 fully-qualified branches listed below from `origin` on `rohrasharad-ship-it/AI-Workspace`. Every one has already been individually verified against live Linear issue state (see Payload) — no re-verification needed, just execute the deletes.
**Issue:** N/A — this is routine infrastructure housekeeping (`agents/spec-drift.md` step 11 / `routines/idea-sweep.md`), not tied to a single Linear issue.

## Payload

Verification method used (in place of the blocked script): pulled every issue in the `Sharad Rohra` Linear team via `list_issues` (paginated, `includeArchived: true`, no project filter — the preview-branch convention isn't project-scoped), matched each `preview/<issue-id>-v<n>` branch's issue-id against that map, and applied the same rule the script itself uses: delete when the issue is no longer `spec-needed` in an active pre-build stage (i.e. its status is `Done`, `Canceled`, `Duplicate`, or its label moved off `spec-needed` to `agent-ready`) — since there were no cases of multiple versions for the same issue-id in the current branch list, no "older version" deletions applied.

**19 branches confirmed to KEEP (do NOT delete — active `Backlog` + `spec-needed` issues, single version each):**
`preview/SHA-251-v1`, `preview/SHA-252-v1`, `preview/SHA-253-v1`, `preview/SHA-254-v1`, `preview/SHA-255-v1`, `preview/SHA-258-v1`, `preview/SHA-259-v1`, `preview/SHA-260-v1`, `preview/SHA-261-v1`, `preview/SHA-262-v1`, `preview/SHA-263-v1`, `preview/SHA-264-v1`, `preview/SHA-265-v1`, `preview/SHA-267-v1`, `preview/SHA-268-v1`, `preview/SHA-269-v1`, `preview/SHA-270-v1`, `preview/SHA-271-v1`, `preview/SHA-272-v1`

**106 branches to DELETE** (fully-qualified, `origin/` prefix omitted — run exactly as `preview/...`, never a wildcard):

```
preview/SHA-100-v1
preview/SHA-101-v1
preview/SHA-102-v1
preview/SHA-103-v1
preview/SHA-104-v1
preview/SHA-115-v1
preview/SHA-116-v1
preview/SHA-117-v1
preview/SHA-123-v1
preview/SHA-124-v1
preview/SHA-125-v1
preview/SHA-126-v1
preview/SHA-128-v1
preview/SHA-129-v1
preview/SHA-130-v1
preview/SHA-131-v1
preview/SHA-132-v1
preview/SHA-133-v1
preview/SHA-134-v1
preview/SHA-135-v1
preview/SHA-138-v1
preview/SHA-139-v1
preview/SHA-140-v1
preview/SHA-141-v1
preview/SHA-142-v1
preview/SHA-143-v1
preview/SHA-144-v1
preview/SHA-145-v1
preview/SHA-147-v1
preview/SHA-148-v1
preview/SHA-149-v1
preview/SHA-152-v1
preview/SHA-158-v1
preview/SHA-159-v1
preview/SHA-160-v1
preview/SHA-161-v1
preview/SHA-163-v1
preview/SHA-164-v1
preview/SHA-173-v1
preview/SHA-176-v1
preview/SHA-18-v1
preview/SHA-19-v1
preview/SHA-20-v1
preview/SHA-201-v1
preview/SHA-202-v1
preview/SHA-231-v1
preview/SHA-232-v1
preview/SHA-235-v1
preview/SHA-236-v1
preview/SHA-237-v1
preview/SHA-238-v1
preview/SHA-239-v1
preview/SHA-24-v1
preview/SHA-240-v1
preview/SHA-241-v1
preview/SHA-242-v1
preview/SHA-243-v1
preview/SHA-244-v1
preview/SHA-25-build
preview/SHA-256-v1
preview/SHA-26-v1
preview/SHA-28-v1
preview/SHA-29-v1
preview/SHA-30-v1
preview/SHA-31-v1
preview/SHA-33-v1
preview/SHA-37-v1
preview/SHA-38-v1
preview/SHA-44-v1
preview/SHA-47-v1
preview/SHA-48-v1
preview/SHA-50-v1
preview/SHA-51-v1
preview/SHA-55-v1
preview/SHA-56-v1
preview/SHA-57-v1
preview/SHA-58-v2
preview/SHA-64-v1
preview/SHA-65-v1
preview/SHA-66-v1
preview/SHA-71-v1
preview/SHA-72-v1
preview/SHA-73-v1
preview/SHA-74-v1
preview/SHA-75-v1
preview/SHA-76-v1
preview/SHA-81-v1
preview/SHA-83-v1
preview/SHA-84-v1
preview/SHA-85-v1
preview/SHA-86-v1
preview/SHA-87-v1
preview/SHA-88-v1
preview/SHA-89-v1
preview/SHA-91-v1
preview/SHA-92-v1
preview/SHA-93-v1
preview/SHA-94-v1
preview/SHA-95-v1
preview/SHA-96-v1
preview/SHA-97-v1
preview/SHA-98-v1
preview/SHA-99-v1
preview/sha-169-v1
preview/sha-170-v1
preview/sha-171-v1
```

One-line command once you have delete rights (fully-qualified names only, no wildcards, never touches `main`):

```bash
cd AI-Workspace
git fetch origin --prune
xargs -a <(cat <<'EOF'
preview/SHA-100-v1
... (paste the 106 names above)
EOF
) -n 15 git push origin --delete
```

Or via GitHub's REST API per branch (if git push access is what's actually missing but API write access exists):
`DELETE /repos/rohrasharad-ship-it/AI-Workspace/git/refs/heads/preview/<name>`

## Instructions for receiving agent

1. Confirm you actually have delete-ref rights before starting (a quick `git push origin --delete` on one throwaway branch you create yourself is a safe test — do not test against one of the 106 real branches first in case something is wrong with your own read of this list).
2. Re-run `git branch -r | grep 'origin/preview/'` right before deleting — if the branch list has changed since 2026-08-19 (new preview branches created, or one of the 106 already gone), that's expected drift; just skip anything already gone and don't delete anything not on this list without re-verifying its Linear status yourself.
3. Delete the 106 branches listed above.
4. Delete this handover file once done — the cleanup is complete and doesn't need to stay tracked.
5. No Linear comment is needed for this one (it's infra housekeeping, not a Linear issue) — just delete the branches and this file.
