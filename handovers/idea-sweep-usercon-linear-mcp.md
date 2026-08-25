# Handover: idea-sweep routine could not run for Usercon — no Linear MCP access this session

**For:** Any agent/session with Linear MCP tools authorized for this account
**From:** idea-sweep routine (Claude Code, scheduled run), Usercon project, 2026-08-25
**Blocked by:** This session has no Linear MCP connector at all — not a missing secret or
API key, the connector itself is unauthorized. The harness reported: "The following MCP
servers require authentication before their tools can be used: Linear" and that OAuth
cannot be completed from this non-interactive scheduled session. A `ToolSearch` for
Linear tools (create/search/list issue) returned zero matches — confirmed nothing is
loaded under any name.
**Action:** Once the Linear connector is authorized for this account (claude.ai →
Settings → Connectors → Linear, or via `claude mcp`/`/mcp` in an interactive session),
re-run the `idea-sweep` routine for Usercon from the top per
`routines/idea-sweep.md` — nothing from this run can be reused or resumed from, since
every role's Step 0 (Issue Cap pre-flight, `agents/shared/issue-cap.md`) itself requires
Linear and could not be evaluated.

## Payload

- **Project resolved from `projects.md`:** Usercon → repo
  `rohrasharad-ship-it/Usercon`, Linear Project "UserCon",
  Linear Project ID `47ebefac-a4f4-4bdd-a382-4506f7e79b6b`, Slack `#usercon`,
  Vercel Prod TBD.
- **What this session had:** GitHub MCP (read/write), Vercel MCP, Slack MCP — all
  connected and usable.
- **What this session lacked:** Linear MCP entirely (no tool of any kind — not
  `list_issues`, `create_issue`, `search_issues`, nor any comment/attachment tool), and no
  `LINEAR_API_KEY` as a raw env var either (checked — unset), so no fallback script path
  was available.
- **Consequence:** Could not perform the Issue Cap pre-flight for Usercon (needs
  `list_issues` filtered by Linear Project ID `47ebefac-a4f4-4bdd-a382-4506f7e79b6b` —
  see `agents/shared/issue-cap.md`). Without knowing cap status, none of the three roles'
  Step 0 could be satisfied, so **no issues were filed, no comments posted, no dedupe
  search run** for spec-drift, bug-error, or market-feature.
- **Step 12 (OpenSpec archive housekeeping) checked anyway since it doesn't need
  Linear:** `openspec/changes/` in AI-Workspace currently has only the `archive/`
  directory, no active (non-archived) change folders — clean 0, nothing to do. Not a new
  blocker, matches the state reported in prior runs (see
  `handovers/preview-branch-cleanup-linear-api-key.md`, 2026-08-12 updates).
- **Steps 10–11 (stale-issue sweep, preview-branch cleanup) not attempted:** both need
  either Linear MCP or `LINEAR_API_KEY`, neither available. Note this is a *different*
  and more complete blocker than the one tracked in
  `handovers/preview-branch-cleanup-linear-api-key.md` — that file's prior sessions all
  had working Linear MCP (they ran `list_issues` cross-referenced against branches) and
  were only missing the repo secret for the *script/Action* path. This session had
  neither. Do not treat this handover as a duplicate of that one; they document different
  failure modes. That file's LINEAR_API_KEY / proxy-write-block issue is still separately
  open and unrelated to this blocker.
- **Sweep ledger:** not appended to `data/sweep-runs.jsonl` — the routine's own log
  format expects filed counts, and this run never reached a state where "clean: true,
  filed: 0" would be accurate; it's a hard block, not a clean pass. Leaving the ledger
  untouched rather than logging a misleading "clean" entry.

## Instructions for receiving agent

1. Confirm Linear MCP tools are actually loaded this time (e.g. search for a
   `list_issues`/`create_issue`-style Linear tool) before starting.
2. Run `routines/idea-sweep.md` for Usercon from step 1 of the pre-flight — do the Issue
   Cap check fresh using Linear Project ID `47ebefac-a4f4-4bdd-a382-4506f7e79b6b`.
3. Nothing to reconcile or roll back — this session made zero Linear writes.
4. Delete this handover file once a full idea-sweep run completes successfully for
   Usercon.
