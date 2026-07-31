# Handover: Preview-branch cleanup — Linear check done, but this session's git access cannot delete branches

**For:** Any agent/session with git push access to `rohrasharad-ship-it/AI-Workspace` broad enough to delete arbitrary `preview/*` branches (not just push to one designated feature branch)
**From:** spec-drift role (steps 10–11), `idea-sweep` routine run for project "Resume Website" (Linear project `b01a99ac-46a3-4b00-9139-31e00fae781d`), 2026-07-31 — Resume Website was at the issue cap (7 active pipeline issues, cap 5), so only steps 10–11 ran this cycle.
**Blocked by:** `git push origin --delete <branch>` returns `HTTP 403` / `RPC failed` for **every** `preview/*` branch tried, including a single-branch test (`git push origin --delete preview/SHA-100-v1`), even though normal fetch/push to this session's own designated branch (`claude/vibrant-faraday-f6dm08`) works fine. This session's local git credential proxy appears scoped to push only the designated branch, not to delete other refs. This is a **different** blocker than the earlier `handover/preview-cleanup-linear-api-key` branch documented (missing `LINEAR_API_KEY`) — that one is now moot for the *analysis* step (see below), but the *deletion* step is blocked here by push scope, not by a missing secret.
**Action:** From an environment with real delete-capable push access to this repo (e.g. `LINEAR_API_KEY` set + unrestricted git push, as in a standalone Cursor/cloud session), run `bash scripts/cleanup-preview-branches.sh --dry-run`, diff its output against the reviewed list below as a sanity check, then run it for real (without `--dry-run`).
**Issue:** No single Linear issue drives this — routine housekeeping (`agents/spec-drift.md` step 11), not a product gap. Do not file a Linear issue for this.

## Payload

- `LINEAR_API_KEY` was **not** available in this session's shell env either (confirmed via `env | grep -i linear`, and via `node scripts/generate-routine-log.mjs` failing with `error: LINEAR_API_KEY is required` — that dashboard-refresh step from `routines/idea-sweep.md` is also blocked this run for the same reason).
- However, this session **did** have working Linear MCP tool access, so instead of the script's raw GraphQL calls it fetched every issue on the shared `SHA` team (`teamId 4d02f6ce-cd9a-4dd9-97d1-86b17bdf83b8`, 250-per-page, paginated, `includeArchived: true` — 2 pages, ~250 issues total) and replicated the script's exact decision rules in a local Node script against the live `origin/preview/*` branch list (125 branches as of this run):
  - delete if a lower version exists for the same issue than another branch for that issue (found: none this run — no issue currently has more than one preview branch)
  - delete if the issue's `statusType` is `completed`, `canceled`, or `duplicate`
  - delete if the issue no longer has the `spec-needed` label (regardless of state)
  - otherwise keep
  - branches not matching `preview/<UPPERCASE-TEAM>-<n>-v<n>` (case-sensitive, matching the script's own regex) are skipped as unrecognized — this includes `preview/SHA-25-build` and three lowercase `preview/sha-169-v1` / `-170-v1` / `-171-v1` branches, exactly as the script itself would skip them.
- **Result: 101 eligible for deletion, 20 to keep, 4 skipped as unrecognized.** Full delete list (branch names only, one per line) is below — cross-check this against the script's real run rather than trusting it blind, per the caution in the earlier LINEAR_API_KEY handover about not mixing ad hoc checks with real deletions:

<details>
<summary>101 branches reviewed as delete-eligible</summary>

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
```

</details>

**Kept (20)** — all still `spec-needed` and active, includes every current Resume Website Backlog issue (SHA-251 through SHA-272 range spanning multiple projects on the shared team): `preview/SHA-251-v1` … `preview/SHA-272-v1` (see script or Linear for the exact set — not reproduced here since these should *not* be touched).

**Skipped (4, unrecognized naming — script would also skip these):** `preview/SHA-25-build`, `preview/sha-169-v1`, `preview/sha-170-v1`, `preview/sha-171-v1`.

**Zero branches were actually deleted this run** — every `git push origin --delete` attempt failed with 403 before any branch was removed.

## Instructions for receiving agent

1. Confirm you have real delete-capable push access: `git push origin --delete <any-known-stale-branch>` should succeed, not 403.
2. Get `LINEAR_API_KEY` into your shell env and run `bash scripts/cleanup-preview-branches.sh --dry-run` from a fresh clone.
3. Compare its delete list to the 101 branches above. They should match exactly (same team, same rules, same branch snapshot modulo any branches created/issues changed since 2026-07-31). Investigate any mismatch before deleting — don't just take the larger list.
4. Run the script for real (drop `--dry-run`) once satisfied.
5. Also re-run `node scripts/generate-routine-log.mjs` with `LINEAR_API_KEY` set — it failed here for the same missing-secret reason and `data/routine-log.json` is stale.
6. Report final deleted/kept/skipped counts wherever this routine's results are tracked, then delete this handover file and the older `handover/preview-cleanup-linear-api-key` branch's file reference (that branch's content is now superseded by this one for the analysis portion, though the LINEAR_API_KEY gap it reported is still real and repeated in point 5 above).

**Do not** attempt to work around the git push-delete restriction (e.g. via raw REST calls with scraped credentials, or by trying alternate ref-deletion syntaxes) — if delete-capable push access isn't available in a given session's environment, that's a structural scope limit of that sandbox, not a bug to route around.
