# Handover: idea-sweep routine has no Linear access in scheduled/non-interactive sessions

**For:** Sharad, or any agent that can authorize the Linear connector for this account
**From:** Claude Code, scheduled `idea-sweep` run for Resume Website, 2026-08-25
**Blocked by:** Linear MCP tools are not authorized for this session, and this session is
non-interactive (a scheduled trigger) so it cannot run the OAuth flow itself. The harness's
own tool listing states this explicitly: *"The following MCP servers require authentication
before their tools can be used: Linear... This session is non-interactive, so Claude cannot
run the OAuth flow here."* No `LINEAR_API_KEY` env var is present either (checked `env`),
so there is no fallback path for the shell-script-based housekeeping steps.
**Action:** Authorize the Linear connector for this account at
claude.ai → Settings → Connectors (or wherever the scheduled `idea-sweep` trigger's identity
is configured), so future scheduled runs inherit a working Linear session the same way an
interactive session would. Separately/additionally, add `LINEAR_API_KEY` as available to
scheduled sessions if that's a distinct credential from the interactive connector.
**Issue:** none — this run never reached the point of creating one; see below.

---

## What this blocked, concretely

Following `routines/idea-sweep.md` for **Resume Website** only (single-project trigger):

- **Pre-flight Issue Cap check** (`agents/shared/issue-cap.md`) — needs `list_issues` via
  Linear MCP filtered by Resume Website's Linear Project ID
  (`b01a99ac-46a3-4b00-9139-31e00fae781d`). Could not run at all, so I don't know whether
  Resume Website is at/over the 5-issue active-pipeline cap.
- **spec-drift steps 1–9** (gap-filing) — blocked at "search the target Linear project
  first" (step 4) and issue creation (step 5).
- **spec-drift step 10** (stale-issue sweep) — blocked; can't list/read/comment on Backlog
  issues.
- **spec-drift step 11** (preview-branch housekeeping) — blocked; the cleanup script needs
  `LINEAR_API_KEY`, not present. (This specific sub-blocker is already exhaustively
  documented in `handovers/preview-branch-cleanup-linear-api-key.md` across 7+ prior runs —
  not re-investigating it further here, per that file's own note that re-verifying wastes
  tokens. Root cause is the same missing credential either way.)
- **spec-drift step 12** (OpenSpec archive sweep) — *not* blocked by Linear, so I checked it
  directly via GitHub MCP: `openspec/changes/` in this repo currently contains only the
  `archive/` folder, no active change folders. Nothing to archive this run — genuinely clean,
  not blocked.
- **bug-error steps 3–4** (search/create) — blocked. (Steps 1–2, reading Vercel logs, were
  not attempted since the run can't act on anything found without Linear access — no point
  reading logs I can't file issues against.)
- **market-feature steps 4–5** (search/create) — blocked, same reasoning as bug-error.

So: **no issue-cap check, no search, no create, no comment, no stale-issue sweep** happened
for Resume Website this run. This is not the same as "clean" (roles ran and found nothing)
— nothing was actually checked.

## A pattern worth flagging

`data/sweep-runs.jsonl` currently shows a long unbroken streak of `"clean":true,
"filed":{"bugs":0,"features":0}` entries across every project, going back to 2026-07-11 —
13 entries, never once a nonzero fill. Given that Linear access has now been independently
confirmed missing in *this* session, and the preview-branch-cleanup handover shows a
parallel `LINEAR_API_KEY` gap that's persisted since at least 2026-07-21, it's worth Sharad
(or a session with working Linear access) spot-checking whether any of those 13 "clean"
runs were actually blocked runs that mis-logged themselves as clean, rather than genuinely
finding nothing across 5 active projects for 6+ weeks straight. I did not overwrite or
"correct" any of those past entries — I don't have enough information to know which, if
any, were true blocks vs. genuinely clean — but the streak itself is a signal.

I'm logging *this* run honestly below (not as `clean:true`) rather than following the
existing entries' apparent pattern.

## Instructions for receiving agent / Sharad

1. Authorize the Linear connector for whatever identity scheduled `idea-sweep` runs use, so
   the next scheduled fire has real Linear MCP access.
2. Once authorized, a Resume Website idea-sweep can just be re-run from
   `routines/idea-sweep.md` — nothing here needs to be manually replayed, this handover is
   informational, not a payload of pre-drafted issues.
3. If/when you're spot-checking the "clean" streak in `data/sweep-runs.jsonl`, the honest
   way to tell blocked-vs-clean apart in hindsight is probably: was Linear MCP available to
   that specific session type at that time? There's no in-band signal in the ledger itself
   today — that's arguably a gap in the ledger schema worth fixing (e.g. a `"blocked"`
   field) but I'm not making that schema change unilaterally in a routine-run session.
4. Delete this handover once Linear access is confirmed working for scheduled runs and at
   least one subsequent idea-sweep has completed normally.
