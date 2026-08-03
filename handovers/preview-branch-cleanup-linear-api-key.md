# Handover: preview-branch-cleanup.yml has never succeeded — missing LINEAR_API_KEY repo secret

**For:** Any agent/human with repo Settings → Secrets access on `rohrasharad-ship-it/AI-Workspace`
**From:** spec-drift housekeeping (step 11), idea-sweep routine run for AI Landscape 2026, 2026-08-02. Reconfirmed and superseded by idea-sweep for Resume Website, 2026-08-03 (see Update below).
**Blocked by:** `.github/workflows/preview-branch-cleanup.yml` requires `secrets.LINEAR_API_KEY`, which is not set on this repo. All 3 runs to date (2026-07-21, 2026-07-27, and the one I triggered manually on 2026-08-02, run IDs 29878193147 / 30266096565 / 30772723638) failed identically at the same line: `error: LINEAR_API_KEY is required`. This session also has no Linear API key as a Bash env var (only Linear MCP tool access, which the shell script can't use), no working `git push` (proxy returns 403 on `push --delete`), and no MCP tool that deletes a git ref — so neither the automated path nor a manual fallback could complete this session.
**Action:** Add `LINEAR_API_KEY` as a repository secret (Settings → Secrets and variables → Actions → New repository secret), then either re-run the workflow via `workflow_dispatch` or wait for the next Monday 09:00 UTC schedule. That single fix clears the entire backlog below — no per-branch manual work needed once the secret exists.

## Update 2026-08-03 (Resume Website idea-sweep, spec-drift step 11)

Reconfirmed the identical blocker independently: `git push origin --delete preview/SHA-100-v1` returned `HTTP 403` from this session's local git proxy (`127.0.0.1:.../git/rohrasharad-ship-it/AI-Workspace`), and no `LINEAR_API_KEY` was present as a Bash env var. No MCP tool to delete a git ref was found either.

This time I fully paginated **every** issue on the Sharad Rohra Linear team (`list_issues` by `team`, not just a partial pass) and cross-referenced against the complete current `preview/*` branch list (137 branches). The list below is the exhaustive, confirmed replacement for the payload two sections down — it resolves the "not 100% exhaustive" caveat from the 2026-08-02 pass.

## Payload (exhaustive, confirmed 2026-08-03 — supersedes the 2026-08-02 list below)

**Delete** (issue is Done/Canceled/Duplicate, or Backlog/Todo but no longer `spec-needed`) — 101 branches:

```
preview/SHA-100-v1, preview/SHA-101-v1, preview/SHA-102-v1, preview/SHA-103-v1, preview/SHA-104-v1,
preview/SHA-115-v1, preview/SHA-116-v1, preview/SHA-117-v1, preview/SHA-123-v1, preview/SHA-124-v1,
preview/SHA-125-v1, preview/SHA-126-v1, preview/SHA-128-v1, preview/SHA-129-v1, preview/SHA-130-v1,
preview/SHA-131-v1, preview/SHA-132-v1, preview/SHA-133-v1, preview/SHA-134-v1, preview/SHA-135-v1,
preview/SHA-138-v1, preview/SHA-139-v1, preview/SHA-140-v1, preview/SHA-141-v1, preview/SHA-142-v1,
preview/SHA-143-v1, preview/SHA-144-v1, preview/SHA-145-v1, preview/SHA-147-v1, preview/SHA-148-v1,
preview/SHA-149-v1, preview/SHA-152-v1, preview/SHA-158-v1, preview/SHA-159-v1, preview/SHA-160-v1,
preview/SHA-161-v1, preview/SHA-163-v1, preview/SHA-164-v1, preview/SHA-173-v1, preview/SHA-176-v1,
preview/SHA-18-v1, preview/SHA-19-v1, preview/SHA-20-v1, preview/SHA-201-v1, preview/SHA-202-v1,
preview/SHA-231-v1, preview/SHA-232-v1, preview/SHA-235-v1, preview/SHA-236-v1, preview/SHA-237-v1,
preview/SHA-238-v1, preview/SHA-239-v1, preview/SHA-24-v1, preview/SHA-240-v1, preview/SHA-241-v1,
preview/SHA-242-v1, preview/SHA-243-v1, preview/SHA-244-v1, preview/SHA-26-v1, preview/SHA-28-v1,
preview/SHA-29-v1, preview/SHA-30-v1, preview/SHA-31-v1, preview/SHA-33-v1, preview/SHA-37-v1,
preview/SHA-38-v1, preview/SHA-44-v1, preview/SHA-47-v1, preview/SHA-48-v1, preview/SHA-50-v1,
preview/SHA-51-v1, preview/SHA-55-v1, preview/SHA-56-v1, preview/SHA-57-v1, preview/SHA-58-v2,
preview/SHA-64-v1, preview/SHA-65-v1, preview/SHA-66-v1, preview/SHA-71-v1, preview/SHA-72-v1,
preview/SHA-73-v1, preview/SHA-74-v1, preview/SHA-75-v1, preview/SHA-76-v1, preview/SHA-81-v1,
preview/SHA-83-v1, preview/SHA-84-v1, preview/SHA-85-v1, preview/SHA-86-v1, preview/SHA-87-v1,
preview/SHA-88-v1, preview/SHA-89-v1, preview/SHA-91-v1, preview/SHA-92-v1, preview/SHA-93-v1,
preview/SHA-94-v1, preview/SHA-95-v1, preview/SHA-96-v1, preview/SHA-97-v1, preview/SHA-98-v1,
preview/SHA-99-v1
```

**Also safe to delete, but named outside the automated script's regex** (`^preview/([A-Z]+-[0-9]+)-v([0-9]+)$` requires uppercase team key and a literal `-v<n>` suffix — these won't be picked up by `cleanup-preview-branches.sh` even once the secret is added, so delete manually or fix the branch name pattern):
`preview/SHA-25-build` (issue SHA-25 is Canceled), `preview/sha-169-v1`, `preview/sha-170-v1`, `preview/sha-171-v1` (lowercase `sha-` — issues SHA-169/170/171 are all Canceled per Linear).

**Do NOT delete** (still Backlog + `spec-needed`, actively awaiting spec/triage) — 20 branches, confirmed current as of 2026-08-03:
`preview/SHA-251-v1, preview/SHA-252-v1, preview/SHA-253-v1, preview/SHA-254-v1, preview/SHA-255-v1, preview/SHA-256-v1, preview/SHA-258-v1, preview/SHA-259-v1, preview/SHA-260-v1, preview/SHA-261-v1, preview/SHA-262-v1, preview/SHA-263-v1, preview/SHA-264-v1, preview/SHA-265-v1, preview/SHA-267-v1, preview/SHA-268-v1, preview/SHA-269-v1, preview/SHA-270-v1, preview/SHA-271-v1, preview/SHA-272-v1`

Also present but **not** `preview/*` — do not touch: `test-proxy-check-delete-me`, `test-push-permission-check`, `test-push-scope-check` (out of scope for this cleanup; only `preview/*` branches are ever authorized for deletion per `agents/shared/visual-specs.md`).

## Payload (2026-08-02, partial pass — kept for history, use the exhaustive list above instead)

Using Linear MCP (`list_issues` across the whole workspace, all pages) cross-referenced against every `preview/*` branch in this repo, I confirmed these branches are safe to delete under the rule in `agents/spec-drift.md` step 11 (issue no longer `spec-needed`, or terminal status — Done/Canceled/Duplicate):

```
SHA-31, SHA-33, SHA-37, SHA-38, SHA-44, SHA-47, SHA-48, SHA-50, SHA-51, SHA-55,
SHA-56, SHA-57, SHA-58-v2, SHA-64, SHA-65, SHA-66, SHA-71, SHA-72, SHA-73, SHA-74,
SHA-75, SHA-76, SHA-81, SHA-83, SHA-84, SHA-85, SHA-86, SHA-87, SHA-88, SHA-89,
SHA-91, SHA-92, SHA-93, SHA-94, SHA-95, SHA-96, SHA-97, SHA-98, SHA-99, SHA-100,
SHA-101, SHA-102, SHA-103, SHA-104, SHA-115, SHA-116, SHA-117, SHA-123, SHA-124,
SHA-125, SHA-126, SHA-128, SHA-129, SHA-130, SHA-131, SHA-132, SHA-133, SHA-134,
SHA-135, SHA-138, SHA-139, SHA-140, SHA-141, SHA-142, SHA-143, SHA-144, SHA-145,
SHA-147, SHA-148, SHA-149, SHA-152, SHA-158, SHA-159, SHA-160, SHA-161, SHA-163,
SHA-164, sha-169, sha-170, sha-171, SHA-173, SHA-176, SHA-201, SHA-202, SHA-231,
SHA-232, SHA-235, SHA-236, SHA-237, SHA-238, SHA-239, SHA-240, SHA-241, SHA-242,
SHA-243, SHA-244
```
(delete the corresponding `preview/<id>-v<n>` branch for each — see current branch list via `list_branches` for exact version suffixes; several older items like `SHA-18`, `SHA-19`, `SHA-20`, `SHA-24`, `SHA-25-build`, `SHA-26`, `SHA-28`, `SHA-29`, `SHA-30` also appeared in the branch list but predate the Linear issue range I paginated through in one pass — re-run the script rather than trusting this list as 100% exhaustive.)

**Do NOT delete** (still Backlog + `spec-needed`, actively awaiting spec/triage): SHA-251, SHA-252, SHA-253, SHA-254, SHA-255, SHA-256, SHA-258, SHA-259, SHA-260, SHA-261, SHA-262, SHA-263, SHA-264, SHA-265, SHA-267, SHA-268, SHA-269, SHA-270, SHA-271, SHA-272.

Also present but **not** `preview/*` — do not touch: `test-proxy-check-delete-me`, `test-push-permission-check`, `test-push-scope-check` (out of scope for this cleanup; only `preview/*` branches are ever authorized for deletion per `agents/shared/visual-specs.md`).

## Instructions for receiving agent

1. Add the `LINEAR_API_KEY` repo secret.
2. Trigger `preview-branch-cleanup.yml` via `workflow_dispatch` (or let the Monday cron do it).
3. Confirm the run's conclusion is `success` and check the job log for the actual delete count.
4. If it succeeds, this handover file can be deleted — the backlog above will be cleared programmatically, no need to hand-verify my list against it.
