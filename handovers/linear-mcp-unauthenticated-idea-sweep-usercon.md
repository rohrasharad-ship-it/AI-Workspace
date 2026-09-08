# Handover: Linear MCP entirely unavailable this session — idea-sweep for Usercon could not run

**For:** Any agent/human who can authorize the Linear connector for this account (claude.ai Settings → Connectors), or the next idea-sweep session once Linear access is restored
**From:** idea-sweep routine run (all three roles: spec-drift, bug-error, market-feature), triggered for Usercon, 2026-09-08
**Blocked by:** Linear MCP server requires re-authentication. This session's tool list explicitly flagged Linear as needing OAuth before its tools can be used, and a live `ToolSearch` for Linear tools (list/search/create issue) returned zero Linear tools — only unrelated GitHub issue tools matched. `LINEAR_API_KEY` is also not present as a Bash env var (consistent with the pre-existing, still-unresolved blocker documented in `handovers/preview-branch-cleanup-linear-api-key.md`).
**Action:** Reconnect/authorize the Linear MCP connector for this account (claude.ai → Settings → Connectors → Linear). This session could not run the OAuth flow itself (non-interactive). Once reconnected, re-run `idea-sweep` for Usercon — nothing below needs to be manually replayed, the routine is idempotent per its own dedupe-search step.

## Payload

This is a **different, more severe blocker** than the one tracked in
`handovers/preview-branch-cleanup-linear-api-key.md` (which is about a missing
`LINEAR_API_KEY` *repository secret* for the GitHub Action script only). That
one blocks steps 11–12 (preview-branch cleanup / openspec archive
housekeeping). This one — no Linear MCP tool access at all in this session —
blocks everything upstream of that:

- **Issue Cap pre-flight** (`agents/shared/issue-cap.md`) — cannot call
  `list_issues` scoped to the Usercon Linear Project ID
  (`47ebefac-a4f4-4bdd-a382-4506f7e79b6b`), so the active-pipeline count for
  Usercon could not be verified at all this run.
- **spec-drift steps 1–9** (gap-filing) — blocked: needs Linear search-first
  dedupe and issue creation.
- **spec-drift step 10** (stale-issue sweep) — blocked: needs to list/read/
  comment on existing Backlog issues.
- **bug-error** — blocked at its own step 0 (cap check) and step 3 (dedupe
  search)/step 4 (create).
- **market-feature** — blocked at the same points.

What I checked instead, since Linear was unreachable:
- `openspec/changes/` in AI-Workspace currently has only the `archive/`
  subdirectory — no active (non-archived) change folders — so step 12
  (openspec archive housekeeping) has nothing to do regardless of tooling.
  Not a new blocker, just a clean 0, consistent with the last few runs.
- Step 11 (preview-branch cleanup) remains separately blocked per the
  existing handover (`LINEAR_API_KEY` secret still not configured on the
  GitHub Action, confirmed again here since the env var is also absent
  locally) — did not re-attempt the git-push-403 investigation since that
  handover's 2026-08-12 update already concluded further re-verification
  wastes tokens with no new information.

No Linear read/write of any kind happened this run — zero issues filed,
zero comments posted, zero cap check performed. This is a full skip, not a
"clean" result: unlike the `"clean": true` entries in
`data/sweep-runs.jsonl` (which mean all three roles ran and found nothing),
this run never got past pre-flight. I did **not** append a `sweep-runs.jsonl`
line for this reason — that ledger's schema has no "blocked" state, and
writing `"clean": true` would misrepresent that verification actually
happened. Treat this handover file as the record for the 2026-09-08 Usercon
run instead.

## Instructions for receiving agent

1. Reconnect the Linear MCP connector for this account (human action, outside
   any agent session — see claude.ai Settings → Connectors → Linear; the
   system prompt for non-interactive sessions cannot run this OAuth flow
   itself).
2. Once reconnected, re-run the `idea-sweep` routine for Usercon from
   scratch — `routines/idea-sweep.md` step-by-step, starting at the Issue Cap
   pre-flight. Nothing from this run needs replaying since nothing succeeded.
3. If Linear reconnects but the preview-branch-cleanup secret is still
   unresolved, that's the separate, already-tracked blocker — see
   `handovers/preview-branch-cleanup-linear-api-key.md`, do not duplicate
   effort re-diagnosing it here.
4. Delete this handover file once a subsequent idea-sweep run for Usercon
   completes normally (Linear reachable, cap check performed) — until then it
   is the record that this cycle produced nothing because the tool, not the
   project, was the problem.
