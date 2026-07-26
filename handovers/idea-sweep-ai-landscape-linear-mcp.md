# Handover: idea-sweep routine for AI Landscape could not run — Linear MCP unavailable

**For:** Any agent/session with an authorized Linear MCP connection
**From:** idea-sweep orchestrator (scheduled trigger), AI Landscape 2026, 2026-07-26
**Blocked by:** No Linear MCP tools available in this session (Linear connector shows as "requires authentication before its tools can be used"; no `LINEAR_API_KEY` env var present either)
**Action:** Authorize the Linear connector for this account, then re-run the `idea-sweep` routine for AI Landscape (and check whether other projects' scheduled sweeps hit the same wall)
**Issue:** none created — the routine never got past the mandatory Issue Cap pre-flight, which requires Linear

## Payload

The scheduled trigger fired correctly:

```
Run the "idea-sweep" routine for AI Landscape.
Follow rohrasharad-ship-it/AI-Workspace/routines/idea-sweep.md exactly.
```

This session read `routines/idea-sweep.md`, `routines/README.md`, `projects.md`,
`agents/shared/issue-cap.md`, `agents/spec-drift.md`, `agents/bug-error.md`,
`agents/market-feature.md`, `agents/shared/linear-slack.md`, and
`agents/shared/conventions.md` in full, and resolved the project row:

| Field | Value |
|---|---|
| Project | AI Landscape 2026 |
| Repo | `rohrasharad-ship-it/ai-landscape` |
| Linear Project | AI Landscape |
| Linear Project ID | `4ef7d096-f5bb-44f4-bac5-417e4488cdb8` |
| Slack Channel | `#ai-landscape` |
| Prod URL | https://rohrasharad-ship-it.github.io/ai-landscape/ (repo also has a `vercel.json`) |

Every idea-generation role (spec-drift, bug-error, market-feature) requires the
**Issue Cap pre-flight** (`agents/shared/issue-cap.md`) before it's allowed to
file anything, and that pre-flight requires `list_issues` against the Linear
Project ID above. No Linear MCP tools were present in this session's tool
list (confirmed via tool search — only GitHub, Slack, and Vercel MCP tools
resolved), and no `LINEAR_API_KEY` was set in the environment, so:

- The cap count could not be computed at all (not "cap reached" — genuinely
  unknown).
- No dedupe search against existing Linear issues was possible.
- Spec-drift steps 1–9 (gap-filing), bug-error, and market-feature could not
  run — all three write to Linear.
- Spec-drift steps 10–11 (stale-issue sweep, preview-branch housekeeping) also
  could not run: step 10 needs to read/post issue comments via Linear MCP,
  and step 11's `cleanup-preview-branches.sh` needs `LINEAR_API_KEY` to look
  up each preview branch's issue label/state before deciding whether to
  delete it — running it without that key would be an unsafe guess, not a
  housekeeping pass.

No Linear reads, writes, or comments were attempted while blocked, and no
issues were fabricated or assumed. This is a full block on the routine, not a
partial run.

## Instructions for receiving agent

1. Confirm the Linear MCP connector is authorized for this account (Sharad:
   claude.ai connector settings; or `/mcp` in an interactive Claude Code
   session) and that a Linear MCP tool (e.g. `list_issues`/`search_issues`
   equivalent) actually resolves via tool search before re-running anything.
2. Re-run the `idea-sweep` routine for **AI Landscape** from
   `routines/idea-sweep.md`, starting from the Issue Cap pre-flight in
   `agents/shared/issue-cap.md` — nothing from this session can be resumed or
   skipped, since none of it ran.
3. While you're in there, it's worth checking whether the same Linear
   auth gap affects other scheduled `idea-sweep` runs (Resume Website, PM OS,
   Application Agent, Usercon) — this session only checked AI Landscape.
4. Delete this handover file once a Linear-connected run completes
   successfully for AI Landscape (per the receiving-agent convention in
   `agents/shared/conventions.md`).

## Do not

- Do not mark this as "Idea-sweep skipped — cap reached" anywhere; the cap was
  never measured.
- Do not invent Linear issue links or a "0 filed" summary that implies the
  roles actually ran — they did not execute at all.
