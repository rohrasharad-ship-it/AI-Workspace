# Handover: preview-branch-cleanup.yml has never succeeded — missing LINEAR_API_KEY repo secret

**For:** Any agent/human with repo Settings → Secrets access on `rohrasharad-ship-it/AI-Workspace`
**From:** spec-drift housekeeping (step 11), idea-sweep routine run for Application Agent, 2026-08-05 (previously: AI Landscape 2026, 2026-08-02)
**Blocked by:** `.github/workflows/preview-branch-cleanup.yml` requires `secrets.LINEAR_API_KEY`, which is not set on this repo. All runs to date (2026-07-21, 2026-07-27, 2026-08-02 manual dispatch, run IDs 29878193147 / 30266096565 / 30772723638) failed identically at `error: LINEAR_API_KEY is required`. This blocker recurred identically on 2026-08-05: no Linear API key as a Bash env var (only Linear MCP tool access, which the shell script can't use), `git push --delete` returns 403 (the checked-out repo's credential can push commits but not delete refs), and no GitHub MCP tool deletes a git ref either (`create_branch` exists; nothing symmetric for delete) — so neither the automated path nor a manual fallback could complete, for the second run in a row.
**Action:** Add `LINEAR_API_KEY` as a repository secret (Settings → Secrets and variables → Actions → New repository secret), then either re-run the workflow via `workflow_dispatch` or wait for the next Monday 09:00 UTC schedule. That single fix clears the entire backlog below — no per-branch manual work needed once the secret exists.

## Payload

Using Linear MCP (`list_issues` filtered by `team: SHA`, all pages — 271 issues, full workspace) cross-referenced against all 125 `preview/*` branches in this repo (2026-08-05 pass), the following are confirmed safe to delete under the rule in `agents/spec-drift.md` step 11 (issue no longer `spec-needed`, or terminal status — Done/Canceled/Duplicate — or superseded by a newer version for the same issue). This supersedes the partial list below from 2026-08-02 — every issue that run flagged as "unconfirmed" (SHA-18, SHA-19, SHA-20, SHA-24, SHA-26, SHA-28, SHA-29, SHA-30) is now confirmed Canceled/Done and included:

```
SHA-18, SHA-19, SHA-20, SHA-24, SHA-26, SHA-28, SHA-29, SHA-30, SHA-31, SHA-33,
SHA-37, SHA-38, SHA-44, SHA-47, SHA-48, SHA-50, SHA-51, SHA-55, SHA-56, SHA-57,
SHA-58-v2, SHA-64, SHA-65, SHA-66, SHA-71, SHA-72, SHA-73, SHA-74, SHA-75, SHA-76,
SHA-81, SHA-83, SHA-84, SHA-85, SHA-86, SHA-87, SHA-88, SHA-89, SHA-91, SHA-92,
SHA-93, SHA-94, SHA-95, SHA-96, SHA-97, SHA-98, SHA-99, SHA-100, SHA-101, SHA-102,
SHA-103, SHA-104, SHA-115, SHA-116, SHA-117, SHA-123, SHA-124, SHA-125, SHA-126,
SHA-128, SHA-129, SHA-130, SHA-131, SHA-132, SHA-133, SHA-134, SHA-135, SHA-138,
SHA-139, SHA-140, SHA-141, SHA-142, SHA-143, SHA-144, SHA-145, SHA-147, SHA-148,
SHA-149, SHA-152, SHA-158, SHA-159, SHA-160, SHA-161, SHA-163, SHA-164, SHA-173,
SHA-176, SHA-201, SHA-202, SHA-231, SHA-232, SHA-235, SHA-236, SHA-237, SHA-238,
SHA-239, SHA-240, SHA-241, SHA-242, SHA-243, SHA-244
```
(101 issues total → delete the corresponding `preview/<id>-v1` branch for each, or `preview/SHA-58-v2`.)

**Still unresolved by naming, not by this script:** `preview/SHA-25-build`, `preview/sha-169-v1`, `preview/sha-170-v1`, `preview/sha-171-v1` don't match the script's `^preview/([A-Z]+-[0-9]+)-v([0-9]+)$` regex (lowercase `sha`, or `-build` suffix instead of `-vN`) — the script silently skips these as "unrecognized branch name" every run, so they will **never** self-clear even once the secret is added. Their issues (SHA-169, SHA-170, SHA-171) are Canceled, so they're just as safe to delete; someone needs to delete these 4 by hand once, or the script's regex needs a case-insensitive/alternate-suffix fix.

**Do NOT delete** (still Backlog + `spec-needed` or otherwise active, actively awaiting spec/triage): SHA-251, SHA-252, SHA-253, SHA-254, SHA-255, SHA-256, SHA-258, SHA-259, SHA-260, SHA-261, SHA-262, SHA-263, SHA-264, SHA-265, SHA-267, SHA-268, SHA-269, SHA-270, SHA-271, SHA-272.

Also present but **not** `preview/*` — do not touch: `test-proxy-check-delete-me`, `test-push-permission-check`, `test-push-scope-check` (out of scope for this cleanup; only `preview/*` branches are ever authorized for deletion per `agents/shared/visual-specs.md`).

## Instructions for receiving agent

1. Add the `LINEAR_API_KEY` repo secret.
2. Trigger `preview-branch-cleanup.yml` via `workflow_dispatch` (or let the Monday cron do it).
3. Confirm the run's conclusion is `success` and check the job log for the actual delete count (expect ~101, not 105 — the 4 non-standard-named branches above need a manual `git push origin --delete` regardless, since the script's regex will never match them).
4. If it succeeds, this handover file can be deleted — the backlog above will be cleared programmatically, no need to hand-verify my list against it.
