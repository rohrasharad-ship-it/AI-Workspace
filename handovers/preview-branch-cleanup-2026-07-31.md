# Handover: preview/* branch housekeeping blocked — no write access to AI-Workspace git refs

**For:** Any agent/session with real `git push` rights to `rohrasharad-ship-it/AI-Workspace` (or direct Linear API access via `LINEAR_API_KEY` to run `scripts/cleanup-preview-branches.sh` itself)
**From:** idea-sweep routine (spec-drift step 11, triggered for AI Landscape 2026), 2026-07-31
**Blocked by:** This session's git write access to AI-Workspace is denied (HTTP 403 on `git push origin --delete`, per the agent-proxy's egress/write policy — see `/root/.ccr/README.md`, "do not retry or route around it"). No GitHub MCP tool exists to delete a branch/ref either (only `create_branch`, no delete equivalent). Read access (clone, `git ls-remote`) and file-content commits via the GitHub MCP `create_or_update_file` API work fine — this is specifically a ref-deletion / raw-push wall. Separately, this session also has no `LINEAR_API_KEY` env var, so the script itself can't be run as-is either.
**Action:** Delete the 101 orphaned `preview/*` branches listed below from `rohrasharad-ship-it/AI-Workspace` (each is a fully-qualified `preview/<ISSUE-ID>-v<N>` branch — never touch `main` or anything else).
**Issue:** N/A — this is routine cross-project housekeeping (`agents/spec-drift.md` step 11), not scoped to one Linear issue. Filed here instead of the usual `<ISSUE-ID>-<short-slug>.md` path for that reason.

## Payload

This run reproduced `scripts/cleanup-preview-branches.sh`'s exact algorithm by hand, using Linear MCP (`get_issue`) instead of the script's `curl`-based GraphQL call, against the live `preview/*` branch list in AI-Workspace at the time (125 branches, checked with a fresh `git ls-remote origin 'refs/heads/preview/*'` immediately before classifying — no drift from an earlier snapshot). All 121 regex-matching branches were resolved via Linear lookup; 4 were left untouched as unrecognized names (see below). **Zero branches were deleted** — the very first delete attempt (`preview/SHA-100-v1`) got a 403, so per the safety rule ("stop, don't route around a policy block") nothing further was attempted, and `git ls-remote` confirmed `SHA-100-v1` is still present, i.e. no partial/inconsistent state.

**101 branches to delete** — each still exists as of this run, each an exact match of `preview/<ISSUE-ID>-v<N>` for an issue that is no longer `spec-needed` (state is `completed`/`canceled`/`duplicate`):

```
preview/SHA-100-v1   issue completed        preview/SHA-142-v1   issue canceled         preview/SHA-24-v1    issue canceled
preview/SHA-101-v1   issue canceled         preview/SHA-143-v1   issue completed        preview/SHA-240-v1   issue canceled
preview/SHA-102-v1   issue canceled         preview/SHA-144-v1   issue canceled         preview/SHA-241-v1   issue canceled
preview/SHA-103-v1   issue completed        preview/SHA-145-v1   issue canceled         preview/SHA-242-v1   issue canceled
preview/SHA-104-v1   issue canceled         preview/SHA-147-v1   issue canceled         preview/SHA-243-v1   issue completed
preview/SHA-115-v1   issue completed        preview/SHA-148-v1   issue canceled         preview/SHA-244-v1   issue canceled
preview/SHA-116-v1   issue completed        preview/SHA-149-v1   issue canceled         preview/SHA-26-v1    issue canceled
preview/SHA-117-v1   issue completed        preview/SHA-152-v1   issue canceled         preview/SHA-28-v1    issue canceled
preview/SHA-123-v1   issue canceled         preview/SHA-158-v1   issue canceled         preview/SHA-29-v1    issue completed
preview/SHA-124-v1   issue canceled         preview/SHA-159-v1   issue canceled         preview/SHA-30-v1    issue canceled
preview/SHA-125-v1   issue canceled         preview/SHA-160-v1   issue canceled         preview/SHA-31-v1    issue canceled
preview/SHA-126-v1   issue duplicate        preview/SHA-161-v1   issue canceled         preview/SHA-33-v1    issue completed
preview/SHA-128-v1   issue duplicate        preview/SHA-163-v1   issue canceled         preview/SHA-37-v1    issue canceled
preview/SHA-129-v1   issue duplicate        preview/SHA-164-v1   issue canceled         preview/SHA-38-v1    issue canceled
preview/SHA-130-v1   issue duplicate        preview/SHA-173-v1   issue completed        preview/SHA-44-v1    issue completed
preview/SHA-131-v1   issue duplicate        preview/SHA-176-v1   issue canceled         preview/SHA-47-v1    issue canceled
preview/SHA-132-v1   issue duplicate        preview/SHA-18-v1    issue canceled         preview/SHA-48-v1    issue canceled
preview/SHA-133-v1   issue duplicate        preview/SHA-19-v1    issue canceled         preview/SHA-50-v1    issue canceled
preview/SHA-134-v1   issue duplicate        preview/SHA-20-v1    issue canceled         preview/SHA-51-v1    issue canceled
preview/SHA-135-v1   issue canceled         preview/SHA-201-v1   issue canceled         preview/SHA-55-v1    issue canceled
preview/SHA-138-v1   issue completed        preview/SHA-202-v1   issue canceled         preview/SHA-56-v1    issue canceled
preview/SHA-139-v1   issue completed        preview/SHA-231-v1   issue completed        preview/SHA-57-v1    issue canceled
preview/SHA-140-v1   issue completed        preview/SHA-232-v1   issue canceled         preview/SHA-58-v2    issue canceled
preview/SHA-141-v1   issue canceled         preview/SHA-235-v1   issue canceled         preview/SHA-64-v1    issue completed
preview/SHA-236-v1   issue canceled         preview/SHA-65-v1    issue completed        preview/SHA-91-v1    issue canceled
preview/SHA-237-v1   issue canceled         preview/SHA-66-v1    issue canceled         preview/SHA-92-v1    issue canceled
preview/SHA-238-v1   issue canceled         preview/SHA-71-v1    issue canceled         preview/SHA-93-v1    issue canceled
preview/SHA-239-v1   issue completed        preview/SHA-72-v1    issue completed        preview/SHA-94-v1    issue canceled
                                             preview/SHA-73-v1    issue canceled         preview/SHA-95-v1    issue canceled
                                             preview/SHA-74-v1    issue completed        preview/SHA-96-v1    issue completed
                                             preview/SHA-75-v1    issue completed        preview/SHA-97-v1    issue canceled
                                             preview/SHA-76-v1    issue completed        preview/SHA-98-v1    issue canceled
                                             preview/SHA-81-v1    issue completed        preview/SHA-99-v1    issue canceled
                                             preview/SHA-83-v1    issue canceled
                                             preview/SHA-84-v1    issue canceled
                                             preview/SHA-85-v1    issue canceled
                                             preview/SHA-86-v1    issue canceled
                                             preview/SHA-87-v1    issue canceled
                                             preview/SHA-88-v1    issue canceled
                                             preview/SHA-89-v1    issue canceled
```

**20 branches confirmed KEEP** (still `Backlog` + `spec-needed` — do not delete): `preview/SHA-251-v1`, `SHA-252-v1`, `SHA-253-v1`, `SHA-254-v1`, `SHA-255-v1`, `SHA-256-v1`, `SHA-258-v1`, `SHA-259-v1`, `SHA-260-v1`, `SHA-261-v1`, `SHA-262-v1`, `SHA-263-v1`, `SHA-264-v1`, `SHA-265-v1`, `SHA-267-v1`, `SHA-268-v1`, `SHA-269-v1`, `SHA-270-v1`, `SHA-271-v1`, `SHA-272-v1`.

**4 branches left alone as unrecognized names** (don't match `preview/[A-Z]+-[0-9]+-v[0-9]+`, same as the real script would skip them): `preview/SHA-25-build`, `preview/sha-169-v1`, `preview/sha-170-v1`, `preview/sha-171-v1`.

Classification was done fresh against Linear (not cached) — re-verify state hasn't changed for any issue before deleting if much time has passed since 2026-07-31.

## Instructions for receiving agent

1. Confirm you actually have `git push --delete` rights (or equivalent) to `rohrasharad-ship-it/AI-Workspace` — test on one branch first (e.g. `preview/SHA-100-v1`, listed above as safe to delete) before batch-processing.
2. For each of the 101 branches in the delete list above: `git push origin --delete <branch>`. Do not re-derive the classification — it's already done and current as of this handover's date; just re-confirm nothing has moved if this handover is picked up much later.
3. Do **not** delete any of the 20 KEEP branches or the 4 unrecognized-name branches.
4. Once done, delete this handover file (per the standard convention) and note the final deleted/kept/skipped tally somewhere visible (e.g. reply in `#pm-ops` or update `data/sweep-runs.jsonl` context) so the next `idea-sweep` run doesn't redo this work from scratch.
5. Do not attempt to route around the 403 (e.g. via a different auth mechanism not sanctioned for this session) — if you also lack write access, extend this handover rather than guessing.
