# Handover: preview-branch-cleanup.yml has never succeeded — missing LINEAR_API_KEY repo secret

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

## Update — 2026-08-06 (spec-drift housekeeping, idea-sweep run for Application Agent)

Still unresolved. The scheduled Monday run (2026-08-03, run ID 30813814116) also failed
with the identical `LINEAR_API_KEY is required` error — 4 failures now. This session hit
the same wall independently: no `LINEAR_API_KEY` env var, `git push origin --delete` on a
confirmed-safe branch (`preview/SHA-100-v1`) still returns HTTP 403 from the proxy, and no
GitHub MCP tool exists to delete a ref. Also newly confirmed: `node
scripts/generate-routine-log.mjs` (the routine-log dashboard refresh, also referenced from
`routines/idea-sweep.md`) fails at the same line for the same reason — so the missing
secret is now blocking two structural-backup paths, not just this one. No new branches
deleted this run; the payload list above has not been re-verified but is likely still
accurate since nothing else can act on it. Fix remains: add the repo secret.

## Update — 2026-08-07 (spec-drift housekeeping, idea-sweep run for Usercon — skipped at cap)

Still unresolved, 5th failed attempt. Usercon was at the issue cap (5/5 active Backlog
issues) this run, so steps 1–9 were skipped entirely, but step 11 housekeeping still ran
as required. Re-derived the full branch/issue cross-reference from scratch this session
(Linear MCP `list_issues` across the whole `Sharad Rohra` team, both pages, 272 issues
total, matched against all 125 `preview/*` branches currently on the remote). Result
matches the shape of the payload above with the branch set now larger (more issues have
gone terminal since 2026-08-06):

**Confirmed safe to delete (101 branches, terminal issue state or no longer spec-needed):**
SHA-100, SHA-101, SHA-102, SHA-103, SHA-104, SHA-115, SHA-116, SHA-117, SHA-123, SHA-124,
SHA-125, SHA-126, SHA-128, SHA-129, SHA-130, SHA-131, SHA-132, SHA-133, SHA-134, SHA-135,
SHA-138, SHA-139, SHA-140, SHA-141, SHA-142, SHA-143, SHA-144, SHA-145, SHA-147, SHA-148,
SHA-149, SHA-152, SHA-158, SHA-159, SHA-160, SHA-161, SHA-163, SHA-164, SHA-173, SHA-176,
SHA-18, SHA-19, SHA-20, SHA-201, SHA-202, SHA-231, SHA-232, SHA-235, SHA-236, SHA-237,
SHA-238, SHA-239, SHA-24, SHA-240, SHA-241, SHA-242, SHA-243, SHA-244, SHA-26, SHA-28,
SHA-29, SHA-30, SHA-31, SHA-33, SHA-37, SHA-38, SHA-44, SHA-47, SHA-48, SHA-50, SHA-51,
SHA-55, SHA-56, SHA-57, SHA-58-v2, SHA-64, SHA-65, SHA-66, SHA-71, SHA-72, SHA-73, SHA-74,
SHA-75, SHA-76, SHA-81, SHA-83, SHA-84, SHA-85, SHA-86, SHA-87, SHA-88, SHA-89, SHA-91,
SHA-92, SHA-93, SHA-94, SHA-95, SHA-96, SHA-97, SHA-98, SHA-99

**Do NOT delete (20, still Backlog + `spec-needed`):** SHA-251, SHA-252, SHA-253, SHA-254,
SHA-255, SHA-256, SHA-258, SHA-259, SHA-260, SHA-261, SHA-262, SHA-263, SHA-264, SHA-265,
SHA-267, SHA-268, SHA-269, SHA-270, SHA-271, SHA-272 — same set as 2026-08-02, unchanged.

**Skip, not `preview/<ISSUE>-v<N>` shaped — do not touch:** `preview/SHA-25-build`,
`preview/sha-169-v1`, `preview/sha-170-v1`, `preview/sha-171-v1` (lowercase `sha-` doesn't
match the script's branch-name regex; `SHA-25-build` doesn't match the `-v<n>` suffix
pattern — both are exactly what the cleanup script itself would also skip as
"unrecognized branch name", not something blocked by the missing key).

Attempted `git push origin --delete` on all 101 anyway as a fallback in case the proxy
scope had changed since 2026-08-06 — all 101 failed identically: `HTTP 403`, `send-pack:
unexpected disconnect while reading sideband packet`. Zero branches deleted this run.
`node scripts/generate-routine-log.mjs` was not re-attempted (same missing-secret failure
already reconfirmed twice; re-running it a third time in the same session adds nothing).
Fix remains exactly as above: add `LINEAR_API_KEY` as a repo secret, one time, to unblock
both the weekly Action and every future idea-sweep housekeeping step at once.
