# Handover: idea-sweep routine for Usercon could not run — Linear MCP connector is unauthenticated in this session

**For:** Sharad (needs to re-authorize the Linear connector), or any future agent session with a working Linear MCP connection
**From:** idea-sweep routine, scheduled run for Usercon, 2026-08-24
**Blocked by:** The Linear MCP connector (`ListConnectors` reports `installState: "unknown"`, `enabledInChat: true`) has no valid OAuth session in this cloud/scheduled session. No `mcp__Linear__*` tools were loaded at all — `ToolSearch` for "Linear" returned zero matches, and the system prompt explicitly states the server "requires authentication before its tools can be used." There is also no `LINEAR_API_KEY` env var available as a shell fallback (checked and confirmed absent).
**Action:** Re-authorize the Linear connector for this account (claude.ai → Settings → Connectors → Linear → reconnect), then re-run this routine: "Run the 'idea-sweep' routine for Usercon."
**Issue:** N/A — this is a routine-level blocker, not tied to a specific Linear issue (Linear itself is unreachable, so none could be created/read).

## Payload

Per `routines/idea-sweep.md` and `agents/shared/conventions.md` rule 17 (blocked-agent handover), this session could not perform any step that touches Linear:

- **Step 0 (Issue Cap pre-flight)** — could not run at all; requires `list_issues` filtered by Usercon's Linear Project ID (`47ebefac-a4f4-4bdd-a382-4506f7e79b6b` per `projects.md`).
- **spec-drift steps 1–9, bug-error steps 1–8, market-feature steps 1–9** — all require searching/creating/commenting on Linear issues. None ran.
- **spec-drift step 10 (stale-issue sweep)** — requires reading + commenting on Linear issues. Did not run.
- **spec-drift step 11 (preview-branch housekeeping)** — this is a **separate, already well-documented** blocker (missing `LINEAR_API_KEY` repo secret + a proxy that blocks mutating git operations for any agent session) — see `handovers/preview-branch-cleanup-linear-api-key.md`, which has 7 independent confirmations as of 2026-08-12 and explicitly says no further re-verification is needed. Not re-attempted this run — would fail identically even if Linear MCP were authenticated, since the script needs the shell-level `LINEAR_API_KEY`, not MCP access.
- **spec-drift step 12 (OpenSpec archive housekeeping)** — does **not** need Linear. Checked directly via GitHub MCP: `openspec/changes/` in AI-Workspace contains only the `archive/` subdirectory — no active, non-archived change folders. Consistent with the 2026-08-12 note in the preview-cleanup handover ("step 12 remains a clean 0"). No action needed, script not run (nothing for it to do).
- **Usercon's own `openspec/`** was confirmed to exist (`openspec/project.md`, `openspec/specs/`, `openspec/changes/` all present) — so once Linear access is restored, spec-drift/market-feature steps 1–2 have real material to read against.
- **Sweep ledger** (`data/sweep-runs.jsonl`) — deliberately **not** appended this run. A `"clean": true` / zero-count entry would misrepresent this as "ran and found nothing" when in fact none of the Linear-dependent steps executed at all. Do not backfill a ledger line for this run; the next successful run's own entry is the accurate record.

## Instructions for receiving agent

1. If you are Sharad: reconnect the Linear connector in claude.ai connector settings, then just re-trigger the routine — no other setup needed, this handover file can be deleted once the next run completes normally.
2. If you are a future agent session and Linear MCP tools **are** available to you (confirm via `ToolSearch` for "Linear" or by checking `ListConnectors`): run the full `idea-sweep` routine for Usercon from scratch per `routines/idea-sweep.md` — do not assume any partial progress from this session, since nothing was checked or filed.
3. Do not attempt to work around the missing Linear access by guessing issue state, fabricating a cap count, or filing issues via any non-Linear path — per `agents/shared/conventions.md`, Linear is the system of record.
4. Once the routine runs successfully, append the real `sweep-runs.jsonl` entry for this cycle and delete this handover file.

---
_Filed by the idea-sweep routine (Claude Code) — Linear connector reauthorization required to proceed._
