# Handover: idea-sweep routine can't run — Linear MCP not authenticated in this session type

**For:** Sharad (needs to authorize the Linear connector) — no agent can self-fix this
**From:** idea-sweep routine run for Usercon, scheduled trigger, 2026-08-27
**Blocked by:** The Linear MCP server is present in this session's tool list but requires
an OAuth authorization that has not been completed. Every Linear MCP tool call in this
session type fails before it can even be attempted — the harness reports Linear as
"requires authentication before its tools can be used" and explicitly states the session
is non-interactive so it cannot run the OAuth flow itself.
**Action:** Authorize the Linear connector for this workspace/account (via claude.ai
connector settings, or `claude mcp` / `/mcp` in an interactive session — whichever surface
manages this account's Linear connection) so future scheduled/automated sessions inherit a
working Linear MCP connection.
**Issue:** none — this blocks the routine's Step 0 (Issue Cap pre-flight) before any issue
exists to comment on.

## Payload

This is a different, more fundamental blocker than the one already tracked in
`handovers/preview-branch-cleanup-linear-api-key.md` (that one is about the
`LINEAR_API_KEY` **repo secret** used by the `cleanup-preview-branches.sh` shell script and
`generate-routine-log.mjs`, and about the proxy blocking `git push --delete`). This session
had **no Linear MCP access at all** — not even read-only `list_issues` — so nothing in
`routines/idea-sweep.md` that touches Linear could run:

- **Step 0 (Issue Cap pre-flight, `agents/shared/issue-cap.md`)** — could not count
  Usercon's active pipeline issues, so could not confirm the project is under the 5-issue
  cap before letting spec-drift/bug-error/market-feature file anything.
- **spec-drift, bug-error, market-feature steps 1–9** — all require `list_issues` (dedupe
  search) and issue creation; none could run.
- **spec-drift step 10 (stale-issue sweep)** — requires reading and commenting on Linear
  issues; could not run.
- **spec-drift step 11 (preview-branch cleanup)** — already independently blocked by the
  missing `LINEAR_API_KEY` repo secret (see the other handover, 7 prior updates,
  root-caused to a proxy that blocks mutating git/GitHub-API calls) — moot this run since
  Linear access failed first regardless.
- **spec-drift step 12 (openspec archive sweep)** — the only step **not** gated on Linear.
  I ran this directly: cloned AI-Workspace, checked `openspec/changes/` — only the
  `archive/` subfolder exists, no active (non-archived) change folders. Same clean-0 result
  as the last several runs' notes in the other handover. Nothing to archive.

I did not attempt any Linear MCP tool call beyond what the harness already reported as
unavailable — there is no partial-credential state here to probe (unlike the
`LINEAR_API_KEY` case, where the MCP tools worked but a separate shell-level secret was
missing). Retrying Linear MCP calls in a future session with the same auth state will fail
identically; this is purely an authorization gap, not a flaky connection.

## Instructions for receiving agent / human

1. Authorize the Linear connector for whatever account/session type runs scheduled
   `idea-sweep` triggers (this was a scheduled/automated session — no live user to click
   through an OAuth prompt interactively).
2. Once authorized, re-run `idea-sweep` for Usercon (and check whether other
   scheduled projects hit the same wall — this may not be Usercon-specific, it's whatever
   session/account context scheduled triggers run under).
3. This handover file can be deleted once a scheduled idea-sweep session successfully
   completes a Step 0 Issue Cap check via Linear MCP.
4. Do not confuse this with the `LINEAR_API_KEY` secret handover — fixing one does not fix
   the other. Both need to be resolved for spec-drift's steps 10–11 to fully succeed.
