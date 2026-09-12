# Handover: idea-sweep for Usercon blocked — Linear MCP not authenticated in this session

**For:** Sharad (connector authorization) — then any agent with Linear MCP access, to re-run the routine
**From:** `idea-sweep` routine run for Usercon (scheduled trigger), Claude Code cloud session, 2026-09-12
**Blocked by:** The Linear MCP server is configured for this session but **not authenticated** — no Linear tools were exposed at all (not even read-only ones), and there is no `LINEAR_API_KEY` (or similar) in the session environment as a fallback. This is a different, more severe blocker than the two existing handovers in this directory:
  - `preview-branch-cleanup-linear-api-key.md` is about the **GitHub Action** missing the `LINEAR_API_KEY` repo secret (a shell-script problem). That's unrelated to this session.
  - `linear-issue-vercel-preview-blocker.md` is about Vercel Deployment Protection. Also unrelated.
  - Prior idea-sweep sessions for Usercon (see updates dated 2026-08-06/08/12 in `preview-branch-cleanup-linear-api-key.md`) **did** have working Linear MCP access for querying/filing issues — they only hit the wall on the housekeeping shell script and `git push --delete`. This session has **no Linear MCP tool at all**, so the blocker is one step further upstream: nothing in `routines/idea-sweep.md` that touches Linear could run.
**Action:** Sharad needs to authorize the Linear connector for this account (claude.ai → Settings → Connectors → Linear → reconnect/authorize). Non-interactive sessions cannot complete an OAuth flow, so no agent can self-fix this. Once authorized, re-run: `Run the "idea-sweep" routine for Usercon. Follow rohrasharad-ship-it/AI-Workspace/routines/idea-sweep.md exactly.`

## What this session could and could not do

**Could not run at all (all require Linear):**
- Issue Cap pre-flight (`agents/shared/issue-cap.md`) — never checked, so no issues were filed by any role, out of caution (filing without a cap check is exactly what that pre-flight exists to prevent).
- `agents/spec-drift.md` steps 1–9 (gap-filing) and step 10 (stale-issue sweep — needs to read/comment on existing issues).
- `agents/bug-error.md` entirely (also separately blocked — see below).
- `agents/market-feature.md` steps 4–9 (dedupe search + filing).
- `agents/spec-drift.md` step 11 (preview-branch cleanup) — needs Linear to resolve each `preview/<id>-vN` branch's issue status; also still has the unresolved `LINEAR_API_KEY` secret problem from the other handover even when Linear access exists.

**Also structurally blocked independent of Linear:**
- `agents/bug-error.md` step 1 needs the Usercon production URL. `projects.md` lists Usercon's Vercel Prod as `TBD` — there is no Vercel project configured for this row yet, so bug-error cannot run for Usercon even once Linear is fixed, until that row is filled in (via Vercel MCP, which *is* connected in this session).
- `agents/spec-drift.md` step 12 (OpenSpec archive sweep) needs `gh` CLI (not available to this session — GitHub access here is MCP-only, no shell `gh`) plus a local clone with `npx openspec` — not attempted, since it's independent of Linear but still needs tooling this session lacks. (For reference: a 2026-08-08 run noted `openspec/changes/` had no active folders anyway — worth re-checking with a session that has `gh`.)

**Could do (read-only research, no Linear needed), so the next Linear-enabled run has a head start:**
- Read `openspec/project.md` and the `openspec/specs/` capability list for Usercon (8 capabilities: context-graph, context-review, agent-api, context-usage-insights, context-receipt, drive-storage, mcp-oauth, settings-screen; plus `mobile-shell` spec'd under an in-flight change `openspec/changes/sha-204-mobile-tab-nav/`).
- Spot-checked `context-usage-insights` and `mcp-oauth` specs against `src/app` structure. No confident, high-value gap or already-shipped item was found in this shallow pass — this was **not** a full-breadth read of all 8 spec files against the whole codebase (that's the actual job of `agents/spec-drift.md` step 1–3, and it deserves the real reading, not a partial one that risks filing something wrong). Do not treat this as "spec-drift already ran" — a Linear-enabled agent should still do the full read from scratch.
- No market-feature ideation was attempted for the same reason — `agents/market-feature.md` step 1–3 calls for reading `openspec/project.md` in full plus every spec file before proposing anything; a partial read produces exactly the kind of shallow, generic ideas that role is designed to avoid.

## Instructions for receiving agent (once Linear is authorized)

1. Confirm Linear MCP tools are present this session (e.g. `list_issues` resolves).
2. Re-run `idea-sweep` for Usercon from the top, following `routines/idea-sweep.md` exactly — this handover does not shortcut steps 0–9, only confirms nothing was filed yet for this cycle.
3. Before running `agents/bug-error.md`, check whether `projects.md`'s Usercon row still says Vercel Prod `TBD`. If a Usercon Vercel project now exists, update that row (repo, URL) so bug-error has a target; if not, skip bug-error again and note why, same as this run.
4. Delete this handover file once a full Linear-enabled idea-sweep cycle has completed successfully for Usercon.

## Not done

No `data/sweep-runs.jsonl` entry was appended for this run — the ledger schema records `filed` counts from roles that actually ran, and none did. Recording `clean:true` here would misrepresent this as a verified "nothing to file" cycle rather than a blocked one; this handover is the record instead.
