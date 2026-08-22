# Handover: idea-sweep routine for Usercon — Linear MCP not connected this session

**For:** Any agent/session with working Linear MCP access (or Sharad, to authorize the Linear connector for scheduled/automated sessions)
**From:** Scheduled idea-sweep trigger, Claude Code (Usercon), 2026-08-22
**Blocked by:** No Linear tools available at all in this session — not a missing `LINEAR_API_KEY` env var (that's the separate, already-tracked blocker in `handovers/preview-branch-cleanup-linear-api-key.md`), but the Linear MCP connector itself returning no callable tools.
**Action:** Re-run the `idea-sweep` routine for Usercon (`routines/idea-sweep.md`) from a session that has working Linear MCP access, once the connector issue below is resolved.
**Issue:** N/A — no Linear issue could be created or referenced; this session had no way to search, create, or comment on Linear issues at all.

## Payload

Trigger was:
```
Run the "idea-sweep" routine for usercon
Follow rohrasharad-ship-it/AI-Workspace/routines/idea-sweep.md exactly.
```

I read `routines/idea-sweep.md`, `routines/README.md`, `agents/shared/issue-cap.md`,
`agents/spec-drift.md`, `agents/bug-error.md`, `agents/market-feature.md`, and
`agents/shared/conventions.md` in full before starting, and resolved Usercon
against `projects.md`:

- Repo: `rohrasharad-ship-it/Usercon`
- Linear Project: UserCon
- Linear Project ID: `47ebefac-a4f4-4bdd-a382-4506f7e79b6b`
- Slack: `#usercon`
- Vercel Prod: `TBD` (no prod URL on record — bug-error would have nothing to
  read even if Linear worked, but that's separate from this blocker)

Every one of the three roles' Step 0 (Issue Cap pre-flight, mandatory before
anything else — see `agents/shared/issue-cap.md`) requires `list_issues` via
Linear MCP. Every subsequent step (dedupe search, `save_issue`, comments,
stale-issue sweep) also requires Linear MCP. None of it could run.

**What I checked to confirm this is a hard wall, not a fixable mistake in my
own session:**

1. `ListConnectors(keywords: ["Linear"])` → returns the Linear connector with
   `enabledInChat: true` and `installState: "unknown"` — it looks like it
   *should* be available.
2. `ToolSearch` for any `Linear`-prefixed tool (`list_issues`,
   `create_issue`, `search_issues`, plain keyword `"Linear"`) → **no matching
   tools found**, every time. The session's own system reminders explicitly
   listed `Linear` under "MCP servers require authentication before their
   tools can be used" and stated this session is non-interactive so the OAuth
   flow can't run here.
3. `env | grep -i LINEAR` → nothing. No `LINEAR_API_KEY` fallback either, so
   even the shell-script paths (stale-issue sweep, cleanup script) had no
   alternate route.

This is a different failure mode from the connector working-but-secret-missing
issue already tracked in `handovers/preview-branch-cleanup-linear-api-key.md`
(step 11's `LINEAR_API_KEY` for the GitHub Action / shell script). That one is
about a repo secret for a script. This one is about the **Linear MCP connector
itself not exposing any tools to this scheduled session** — it needs a human
to authorize it (per the session's own guidance: "via claude.ai connector
settings") since a non-interactive session cannot complete OAuth.

**What I deliberately did not do:** attempt any Linear-dependent step with
fabricated/guessed data, or record a `clean: true` entry in
`data/sweep-runs.jsonl` — previous clean runs for Usercon (e.g. 2026-08-12)
actually searched Linear and openspec/codebase and found nothing; this run
never got to look, so logging it as clean would misrepresent that a real
sweep happened. No ledger entry was written for this cycle.

Also not attempted: `agents/spec-drift.md` steps 11–12 housekeeping
(preview-branch cleanup, openspec archive sweep) — step 11 needs
`LINEAR_API_KEY` (already blocked per the existing handover) and step 12
needs the `gh` CLI, which this session's own operating instructions say not
to use (GitHub MCP only). Neither is a new finding; noted here only for
completeness of what this cycle covered (nothing).

## Instructions for receiving agent

1. Confirm Linear MCP tools are actually callable in your session (try
   `list_issues` with the Usercon Linear Project ID above) before doing
   anything else.
2. If working, run the full `idea-sweep` routine for Usercon per
   `routines/idea-sweep.md`: Issue Cap pre-flight, then spec-drift →
   bug-error → market-feature in order (bug-error will likely have nothing to
   read given Vercel Prod is `TBD` for Usercon — confirm that's still
   accurate in `projects.md` first).
3. If still not working, this is a connector-authorization problem outside
   any agent's control — flag it to Sharad directly rather than re-attempting
   from another automated session (re-running won't fix an unauthorized
   OAuth connector).
4. Delete this handover file once a session successfully completes an
   idea-sweep run for Usercon with working Linear access — no need to keep it
   around after that, this note is just a record of the gap in coverage.
