# Handover: idea-sweep routine for AI Landscape 2026 could not run — no Linear MCP access at all this session

**For:** Any agent with Linear MCP access, or Sharad
**From:** Claude Code (cloud/remote session), idea-sweep routine trigger for AI Landscape 2026, 2026-08-30
**Blocked by:** This session has **zero Linear MCP tools** — not just the missing `LINEAR_API_KEY` env var
  documented in `handovers/preview-branch-cleanup-linear-api-key.md`. The Linear connector itself is
  unauthenticated for this session; no `mcp__Linear__*` (or equivalent) tool appears anywhere in the
  available toolset, and there is no interactive way for this session to complete an OAuth flow.
**Action:** Authorize the Linear connector for this account/session type (via `claude mcp` / the relevant
  connector settings — outside what an agent session can do for itself), then re-run the `idea-sweep`
  routine for AI Landscape 2026. Nothing below needs to be re-derived once Linear access exists — just
  run the routine fresh.
**Issue:** N/A — no driving Linear issue; this is a routine-trigger session, not an issue-assigned one.

## Payload

Followed `routines/idea-sweep.md` for **AI Landscape 2026**
(`rohrasharad-ship-it/ai-landscape`, Linear Project ID `4ef7d096-f5bb-44f4-bac5-417e4488cdb8`) exactly as
written, in order:

1. **Issue Cap pre-flight** (`agents/shared/issue-cap.md`) — requires `list_issues` filtered by
   Linear Project ID. **Could not run at all** — no Linear MCP tool available. Confirmed via `ToolSearch`
   with multiple queries ("linear issue create search", "mcp Linear list_issues create_issue") — no
   Linear tool surfaced. This is a harder blocker than prior runs hit: earlier idea-sweep sessions
   (see updates in `handovers/preview-branch-cleanup-linear-api-key.md`, 2026-08-02 through 2026-08-12)
   all had working Linear MCP for reads/writes and only lacked the raw `LINEAR_API_KEY` **environment
   variable** needed by the `cleanup-preview-branches.sh` / `generate-routine-log.mjs` shell scripts.
   This session has neither the MCP tool nor the env var — the cap could not even be checked, so
   spec-drift steps 1–9, bug-error, and market-feature could not run (all depend on Linear search/file),
   and spec-drift step 10 (stale-issue sweep) could not run either (also Linear-dependent).
2. **Spec-drift steps 1–9, bug-error, market-feature** — **skipped entirely**, not attempted. All three
   require searching Linear for dedupe and filing/commenting on issues; none of that is possible without
   the MCP tool. Attempting the read-only halves (reading `openspec/specs/`, reading the live site,
   proposing candidate gaps/bugs/features) without the ability to dedupe against existing Linear issues
   or actually file anything would risk either silently dropping real findings or hallucinating a "clean"
   result — neither is safe to report, so nothing was proposed or evaluated this run.
3. **Spec-drift step 10 (stale-issue sweep)** — **skipped**, same reason (needs `list_issues` +
   `add_comment` on the target Linear project).
4. **Spec-drift step 11 (preview-branch housekeeping)** — **skipped**. Same root cause as the existing
   `handovers/preview-branch-cleanup-linear-api-key.md` handover (no `LINEAR_API_KEY`), now compounded by
   no Linear MCP either. Not re-verifying that handover's branch classification again this run — it
   states its list is complete/verified as of 2026-08-12 and asks future sessions not to re-derive it.
5. **Spec-drift step 12 (OpenSpec archive housekeeping)** — this one does **not** need Linear. Checked:
   `openspec/changes/` in AI-Workspace currently contains only the `archive/` directory, no active
   change folders. Nothing to archive — consistent with the 2026-08-12 update's "clean 0" note.
6. **Sweep ledger** — deliberately **not** appended to `data/sweep-runs.jsonl` this run. Every existing
   entry there records `"clean":true` for a run where the roles actually executed and genuinely found
   nothing. That is not what happened here — the roles never ran, so a `"clean":true` entry would
   misrepresent this as a verified-clean sweep when nothing was actually checked. The ledger schema in
   `routines/idea-sweep.md` has no field for "blocked before any role ran"; rather than force a
   misleading entry into it, this handover is the record instead. Whoever fixes the Linear access gap
   should consider whether the ledger schema ought to support a `"blocked"` state, but that's a judgment
   call for a human/spec conversation, not something to invent unilaterally here.

## Instructions for receiving agent

1. Confirm Linear MCP tools are present in your session (any `list_issues`/`create_issue`-equivalent
   Linear tool). If not, this handover still applies — stop and re-raise rather than guessing.
2. Re-run `routines/idea-sweep.md` for **AI Landscape 2026** from the top — Issue Cap pre-flight first,
   then spec-drift → bug-error → market-feature per the routine.
3. Once that run completes (whether clean or with filed issues), append its own ledger line to
   `data/sweep-runs.jsonl` as normal.
4. Delete this handover file once a real (non-blocked) idea-sweep run for AI Landscape 2026 has
   completed — it will supersede this one.
5. Do **not** treat the absence of a ledger entry for 2026-08-30 as evidence the site was checked and
   found clean — it was not checked at all this run.
