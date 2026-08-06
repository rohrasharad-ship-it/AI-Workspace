Handover: preview-branch-cleanup.yml has never succeeded — missing LINEAR_API_KEY repo secret

**For:** Any agent/human with repo Settings → Secrets access on `rohrasharad-ship-it/AI-Workspace`
**From:** spec-drift housekeeping (step 11), idea-sweep routine run for AI Landscape 2026, 2026-08-02
**Blocked by:** `.github/workflows/preview-branch-cleanup.yml` requires `secrets.LINEAR_API_KEY`, which is not set on this repo. All 3 runs to date (2026-07-21, 2026-07-27, and the one I triggered manually on 2026-08-02, run IDs 29878193147 / 30266096565 / 30772723638) failed identically at the same line: `error: LINEAR_API_KEY is required`. This session also has no Linear API key as a Bash env var (only Linear MCP tool access, which the shell script can't use), no working `git push` (proxy returns 403 on `push --delete`), and no MCP tool that deletes a git ref — so neither the automated path nor a manual fallback could complete this session.
**Action:** Add `LINEAR_API_KEY` as a repository secret (Settings → Secrets and variables → Actions → New repository secret), then either re-run the workflow via `workflow_dispatch` or wait for the next Monday 09:00 UTC schedule. That single fix clears the entire backlog below — no per-branch manual work needed once the secret exists.

## Payload

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

## Update — 2026-08-06 (idea-sweep for Usercon, spec-drift step 11)

Still blocked, same root cause: no `LINEAR_API_KEY` secret for the Action, no
`LINEAR_API_KEY` env var in this session either, `git push origin --delete`
still returns `HTTP 403` from this session's egress proxy (org policy blocks
raw git-over-HTTPS push to github.com — see `/root/.ccr/README.md`, "403/407
from the proxy... report the blocked host, do not retry or route around it"),
and the GitHub MCP server available here still has no branch/ref-delete tool
(`create_branch`, `delete_file`, `create_or_update_file` exist; nothing to
delete a ref). Confirmed both blockers are still open as of today, four days
after the original handover.

**This time I paginated Linear MCP `list_issues` workspace-wide to completion
(2 pages, no project filter, 250/page) and cross-referenced against the full,
current `origin/preview/*` branch list (125 branches).** This closes the gap
the original handover flagged ("SHA-18/19/20/24/26/28/29/30 predate the range
I paginated through"). Full re-derived result, current as of 2026-08-06:

- **101 branches confirmed safe to delete** — this is the original list above
  **plus** `preview/SHA-18-v1, SHA-19-v1, SHA-20-v1, SHA-24-v1, SHA-26-v1,
  SHA-28-v1, SHA-29-v1, SHA-30-v1` (all Canceled or Done in Linear, none
  `spec-needed`).
- **20 branches to keep** — unchanged from the original list (SHA-251 through
  SHA-272, still Backlog + `spec-needed`).
- **One correction to the original list:** `preview/sha-169-v1`,
  `preview/sha-170-v1`, `preview/sha-171-v1` (lowercase `sha-` prefix) are
  semantically safe to delete (their issues are Canceled) but the actual
  script's branch-name regex (`^preview/([A-Z]+-[0-9]+)-v([0-9]+)$`) is
  case-sensitive and will **skip** them without evaluating, same as
  `preview/SHA-25-build` (wrong suffix shape, no `-vN`). If someone runs the
  script itself rather than deleting by hand, expect these 4 to survive the
  run and need a manual `git push origin --delete` (or a regex fix in the
  script as a small follow-up).

No new branches need creating or updating this run — this update only
confirms and completes the existing backlog list. The fix is still the same
single action: add the `LINEAR_API_KEY` repo secret.
