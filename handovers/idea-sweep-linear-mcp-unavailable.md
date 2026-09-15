# Handover: idea-sweep routine cannot run — Linear MCP is entirely unauthorized in this session

**For:** Any agent/human who can authorize the Linear MCP connector for this account, or who is running the next idea-sweep session with working Linear access.
**From:** idea-sweep routine run (scheduled trigger) for Resume Website, 2026-09-15.
**Blocked by:** This session has **no Linear MCP tool access at all** — not a missing `LINEAR_API_KEY` for a shell script (the known, already-documented blocker in `handovers/preview-branch-cleanup-linear-api-key.md`), but the Linear MCP server itself reporting "requires authentication before its tools can be used." `ToolSearch` for Linear tools returns nothing; there is no `list_issues`/`create_issue`/`comment` tool of any kind available. This is a non-interactive scheduled session, so the OAuth authorization flow (`claude mcp` / `/mcp`) cannot be run from here — it requires an interactive session or the claude.ai connector settings.
**Action:** Authorize the Linear MCP connector for this account (via claude.ai connector settings, or `claude mcp` / `/mcp` in an interactive session), then re-run the `idea-sweep` routine for Resume Website (and check whether other scheduled idea-sweep runs hit the same wall — this is an account-level connector auth issue, not project-specific).
**Issue:** N/A — this is a routine trigger, not an existing Linear issue. No Linear issue could be created or referenced from this session for the reason above.

## Payload

`routines/idea-sweep.md` for Resume Website requires Linear MCP access at the
very first step (the Issue Cap pre-flight in `agents/shared/issue-cap.md`
calls `list_issues`), before any of the three roles (spec-drift, bug-error,
market-feature) can even start. With zero Linear tool access, none of the
following were possible this run:

- Issue Cap pre-flight count for Resume Website (`b01a99ac-46a3-4b00-9139-31e00fae781d`)
- spec-drift steps 1–9 (gap-filing) and step 10 (stale-issue sweep — needs to
  read/comment on existing issues)
- bug-error (entirely gated on the cap check)
- market-feature (entirely gated on the cap check)
- Posting the required Linear comment on this handover per the standard
  "Session steps (blocked agent)" procedure in `agents/shared/conventions.md`
  — that step itself needs Linear access, which is exactly what's missing, so
  it could not be completed this run.

What **was** confirmed as *not* blocked, in case it's useful context for
whoever picks this up: GitHub MCP access (read the resume-website repo,
`openspec/project.md`, `openspec/specs/`) works fine, and this AI-Workspace
branch could be created and pushed to normally. So the block is scoped
specifically to the Linear connector, not to MCP/tool access generally.

This is a different failure mode than the long-running
`preview-branch-cleanup-linear-api-key.md` handover (7+ runs): that one is
about a missing `LINEAR_API_KEY` **repo secret** for a shell script and a
`git push --delete` proxy block, in sessions that otherwise had full Linear
MCP tool access (search/create/comment all worked). This run had none of
that — the Linear MCP server itself was unauthorized, so even the most basic
`list_issues` call for the cap check was unavailable.

No sweep-ledger line was appended to `data/sweep-runs.jsonl` for this run.
The ledger's `clean: true` / filed-count fields mean "the roles ran and
verified nothing to file" — that would misrepresent what happened here,
since no role reached the point of checking anything. This handover is the
record instead, per `agents/shared/conventions.md`'s Blocked-agent handover
convention.

## Instructions for receiving agent

1. Authorize the Linear MCP connector for this account (outside this
   session — interactive `claude mcp`/`/mcp`, or claude.ai connector
   settings).
2. Confirm Linear tools are callable (e.g. a `list_issues` call against the
   Resume Website Linear Project ID succeeds).
3. Re-run the `idea-sweep` routine for Resume Website from
   `routines/idea-sweep.md`, starting from the Issue Cap pre-flight.
4. If other scheduled idea-sweep triggers (for other projects) have been
   silently producing no ledger entries or no filed issues around this same
   date, they likely hit the identical connector-auth wall — worth checking
   `data/sweep-runs.jsonl` for a gap starting 2026-09-15 across projects, not
   just Resume Website.
5. Delete this handover file once a confirmed-working idea-sweep run has
   completed for Resume Website with real Linear access.

Do not attempt to work around this by hand-writing to
`data/sweep-runs.jsonl` with fabricated "clean" results, and do not guess at
Resume Website's current Linear backlog from memory or stale handovers —
wait for real Linear access and let the routine's own pre-flight count it.
