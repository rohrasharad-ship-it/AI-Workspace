# Handover: idea-sweep for Application Agent could not run — Linear MCP not authorized in this session

**For:** Sharad (connector authorization is an account-level action, not something any
agent session can do), or any future agent session confirming the fix
**From:** Claude Code, scheduled `idea-sweep` trigger for Application Agent, 2026-09-21
**Blocked by:** The Linear MCP connector was not authorized/connected for this session at
all — not the `LINEAR_API_KEY` repo-secret gap already tracked in
`handovers/preview-branch-cleanup-linear-api-key.md`. This is a different, more
fundamental blocker: no Linear tool of any kind (search, create, comment, list) was
available, so nothing in the routine that touches Linear could even be attempted.
**Action:** Reconnect/authorize the Linear connector for this account (claude.ai connector
settings), then re-run: "Run the idea-sweep routine for Application Agent. Follow
rohrasharad-ship-it/AI-Workspace/routines/idea-sweep.md exactly."
**Issue:** none — this run had no driving Linear issue; it was a scheduled routine trigger.

## Payload

Ran through `routines/idea-sweep.md`, `routines/README.md`, and every module it points to
(`agents/spec-drift.md`, `agents/bug-error.md`, `agents/market-feature.md`,
`agents/shared/issue-cap.md`, `agents/shared/issue-brief.md`, `agents/shared/openspec.md`,
`agents/shared/visual-specs.md`, `agents/shared/visual-self-qa.md`,
`agents/shared/conventions.md`, `agents/shared/linear-slack.md`) before starting, per the
routine's own instructions.

**Confirmed before doing anything else:**
- `ToolSearch` for `"Linear"` and for `"list_issues save_issue create_attachment_from_upload
  prepare_attachment_upload"` returned **zero** Linear-related tools — only GitHub's own
  `list_issues` (a different tool, for GitHub issues, not Linear).
- The session's own tool listing explicitly named `Linear` under "The following MCP
  servers require authentication before their tools can be used" and stated this session
  is non-interactive, so the OAuth flow can't run here.
- `env | grep -i linear` and `echo $LINEAR_API_KEY` — no `LINEAR_API_KEY` env var either,
  so there was no raw-API fallback.

**What this blocks, concretely, for Application Agent this cycle:**
- **Issue Cap pre-flight** (`agents/shared/issue-cap.md`) — needs `list_issues` against the
  Application Agent Linear Project ID (`7dc5202c-a586-4bed-b2d3-fba10f2dd913` per
  `projects.md`). Could not run, so the at-cap/under-cap state for this project is
  **unknown** this cycle (previous logged runs — 2026-07-11, 2026-08-06, 2026-08-19 — were
  all `clean:true`, so it was likely under cap as of three weeks ago, but that's not
  verified as of today).
- **spec-drift steps 1–9** (gap-filing) — step 4 (dedupe search) and step 5 (create) need
  Linear. Not attempted past the read-only openspec/codebase comparison (see below).
- **spec-drift step 10** (stale-issue sweep) — needs `list_issues` + comment. Not run.
- **spec-drift step 11** (preview-branch housekeeping) — needs Linear MCP or
  `LINEAR_API_KEY` to look up each issue's label/status before deciding whether a
  `preview/*` branch is an orphan. Not run — this is on top of the already-tracked
  `LINEAR_API_KEY` repo-secret gap in `handovers/preview-branch-cleanup-linear-api-key.md`;
  don't conflate the two, they're separate root causes that happen to block the same step.
- **spec-drift step 12** (openspec archive housekeeping) — does **not** need Linear. Checked
  independently: `openspec/changes/` in AI-Workspace currently has only the `archive/`
  directory, no active (non-archived) change folders, and `list_pull_requests` (open) on
  AI-Workspace returned none. So this step is a genuine clean 0 this run, unrelated to the
  Linear blocker.
- **bug-error** (entire role) — needs Linear to create/dedupe. Also independently N/A this
  cycle regardless: `projects.md` lists Application Agent's Vercel Prod as `TBD` — there is
  no deployed prod URL to pull runtime errors from yet.
- **market-feature** (entire role) — read `openspec/project.md` and vision would have been
  possible, but step 4 (dedupe against Linear) and step 5 (create) need Linear, so no
  issues were proposed or filed. Did not do the vision read since filing was impossible
  either way and speculative ideas without a dedupe check are exactly what the routine
  guards against.

**Did not touch:** no Linear issues created, updated, or commented on (none were possible);
no `preview/*` branches deleted (would require the same missing Linear access as step 11);
no entry appended to `data/sweep-runs.jsonl` — a `clean:true` entry there would misrepresent
this run as "checked, found nothing" when in fact nothing could be checked. Logging a false
clean run would also suppress the Issue Cap pre-flight signal for whoever reads the ledger
next.

## Instructions for receiving agent / Sharad

1. Reconnect the Linear MCP connector for this account (claude.ai connector settings) —
   this is the actual fix; no agent session can do this itself.
2. Re-run the trigger: "Run the idea-sweep routine for Application Agent. Follow
   rohrasharad-ship-it/AI-Workspace/routines/idea-sweep.md exactly." Once Linear tools are
   available, the routine runs as normal — nothing else in this repo needs to change.
3. This handover file can be deleted once a normal (non-blocked) idea-sweep run for
   Application Agent completes and logs to `data/sweep-runs.jsonl`.
4. Do not confuse this with `handovers/preview-branch-cleanup-linear-api-key.md` — that one
   is about the `LINEAR_API_KEY` GitHub Actions secret being unset (blocks the scheduled
   cleanup workflow and step 11's script path specifically). This one is about the Linear
   *connector* not being authorized for a given interactive/scheduled session at all
   (blocks every Linear MCP call in that session). Both can be true at once; fixing one
   does not fix the other.
