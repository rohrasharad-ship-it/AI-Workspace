# Handover: idea-sweep for Usercon could not run — Linear MCP not authenticated in this session

**For:** Any agent/session with Linear MCP access, or Sharad (to authorize the Linear connector for scheduled/cloud sessions)
**From:** Claude Code, scheduled `idea-sweep` trigger for Usercon, 2026-08-29
**Blocked by:** The Linear MCP server is listed as requiring authentication in this session, and this session is non-interactive (scheduled trigger, no live user), so the OAuth flow can't be run to unblock it. `LINEAR_API_KEY` is also not set as an env var, so no shell-script fallback either.
**Action:** Authorize the Linear connector for this account's scheduled/cloud sessions (claude.ai → Settings → Connectors → Linear, or wherever this account's cloud-session connectors are managed), then re-run the `idea-sweep` routine for Usercon.
**Issue:** none filed — see below for why.

## Payload

This is a different blocker from the recurring `LINEAR_API_KEY` GitHub Actions
secret issue tracked in `handovers/preview-branch-cleanup-linear-api-key.md`
(7 prior updates there, all from sessions that *did* have working Linear MCP
tool access and could still fully search/paginate/comment on Linear — that
handover is about the `cleanup-preview-branches.sh` shell script specifically,
which needs the key as a raw env var, not the MCP connection). This run had
**no Linear MCP access at all** — not the tools, not the script env var — so
none of the following could be done, per `routines/idea-sweep.md`,
`agents/spec-drift.md`, `agents/bug-error.md`, `agents/market-feature.md`:

- Issue Cap pre-flight for Usercon (`agents/shared/issue-cap.md` — needs
  `list_issues` filtered by Linear Project ID
  `47ebefac-a4f4-4bdd-a382-4506f7e79b6b`)
- spec-drift steps 1–9 (gap-filing) and step 10 (stale-issue sweep — needs to
  read/post comments on existing Backlog issues)
- bug-error steps 1–8 (all gated on the same cap check + Linear search/file)
- market-feature steps 1–9 (same)
- spec-drift step 11 (preview-branch housekeeping) — also blocked separately,
  no `LINEAR_API_KEY` env var (same as the standing handover above)

Since the cap check itself couldn't run, I did **not** attempt to read
Usercon's `openspec/` vs codebase, Vercel logs, or draft any issue content —
doing that without being able to check the cap or dedupe against existing
Linear issues risks producing content a receiving agent would file blind,
which is exactly what the cap/dedupe steps exist to prevent. No Linear issue
exists yet for this run to comment on.

**Step 12 (OpenSpec archive housekeeping) was checked** — it's the one part
of the routine that doesn't touch Linear. `openspec/changes/` in AI-Workspace
currently has only an `archive/` subfolder, no active change folders, so this
remains a clean 0, same as every prior run since at least 2026-08-08. Not a
new blocker, nothing to do here this run.

**Sweep ledger:** intentionally **not** appending a `sweep-runs.jsonl` line
for this run. That ledger's `filed` counts are meant to reflect an actual
completed sweep (0 filed because nothing was found); this run never got past
the pre-flight, so a `"clean": true` entry would misrepresent this as "roles
ran, found nothing" rather than "roles couldn't run."

## Instructions for receiving agent

1. Confirm Linear MCP tools are available in your session (e.g. a `list_issues`
   or equivalent call succeeds against Usercon's project ID
   `47ebefac-a4f4-4bdd-a382-4506f7e79b6b`).
2. Re-run the `idea-sweep` routine for Usercon from
   `routines/idea-sweep.md`, starting at the Issue Cap pre-flight — nothing
   from this session needs to be replayed or merged, since no partial state
   was produced.
3. Once a full run completes (filed or clean), append the
   `data/sweep-runs.jsonl` line and refresh `data/routine-log.json` as the
   routine specifies.
4. Delete this handover file once a real Usercon idea-sweep run has
   completed successfully with Linear access.
