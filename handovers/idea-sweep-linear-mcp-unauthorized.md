# Handover: idea-sweep routine cannot run — Linear connector not authorized in this session

**For:** Sharad (one-click fix), or any future idea-sweep session once Linear is connected
**From:** idea-sweep routine run for Usercon, Claude Code (claude.ai/code) scheduled session, 2026-09-07
**Blocked by:** The Linear MCP server is configured for this account but **not authorized** —
the session's tool list explicitly says: *"The following MCP servers require authentication
before their tools can be used: Linear"* and *"This session is non-interactive, so Claude
cannot run the OAuth flow here."* No `list_issues`/`create_issue`/comment tool of any kind
resolved at runtime, and no `LINEAR_API_KEY` env var was present either (checked — empty),
so there is no direct-API fallback like the one `scripts/cleanup-preview-branches.sh` uses.
**Action:** Authorize the Linear connector for this account at claude.ai → Settings →
Connectors, then re-run (or let the next scheduled firing of) `idea-sweep` for Usercon.
**Issue:** none yet — every step that would create or look up a Linear issue is gated on
this, including the mandatory Issue Cap pre-flight (`agents/shared/issue-cap.md`), so no
issue exists to comment on for this run.

## Payload

This is a harder stop than the earlier `preview-branch-cleanup-linear-api-key.md` blocker:
that one still had a scripted fallback path (a repo secret + GitHub Action runner) that
didn't depend on this session's own tool access. Here, every single step of all three
idea-sweep roles for a single-project run depends on Linear:

- **Issue Cap pre-flight** (`routines/idea-sweep.md` pre-flight, `agents/shared/issue-cap.md`)
  — requires `list_issues` filtered by Usercon's Linear Project ID
  (`47ebefac-a4f4-4bdd-a382-4506f7e79b6b` per `projects.md`) to count active pipeline
  issues. Without it, there is no way to know whether Usercon is already at the 5-issue cap,
  so no role can safely proceed even to the dedupe-search step.
- **spec-drift** steps 4–9 (dedupe search, create, comment) and step 10 (stale-issue sweep —
  needs to read + comment on existing issues) — all Linear-dependent.
- **bug-error** — also independently blocked: Usercon's `Vercel Prod` in `projects.md` is
  still `TBD`, so there's no production URL to read runtime logs from regardless of Linear.
- **market-feature** steps 4–8 (dedupe search, create, comment) — Linear-dependent.

I deliberately did **not** do the read-only research portions (spec-drift steps 1–3,
market-feature steps 1–2 — reading `openspec/project.md`, `openspec/specs/`, and the
codebase to find gaps or propose features) and stage draft issues here, for two reasons:
1. Without the Issue Cap check, I don't know whether Usercon even has room for new issues
   this cycle — drafting candidates that can't be filed either way is speculative work.
2. Any draft would go stale by the time a Linear-enabled session picks this up (openspec
   specs and the codebase both change), so the receiving session should just re-run
   `idea-sweep` for Usercon from step 0, not resume from a partial draft.

`spec-drift` housekeeping steps 11–12 (preview-branch cleanup, openspec archive sweep) do
**not** require Linear issue creation, only Linear *reads* (to check each preview branch's
issue status) plus `LINEAR_API_KEY` for the script — also unavailable this session (checked,
empty env var) — so those were skipped too rather than run half-blind.

**Ledger:** appended one line to `data/sweep-runs.jsonl` for this run:
`{"project":"Usercon","filed":{"bugs":0,"features":0},"clean":false}` — `clean:false`
because this is a blocked run, not a genuinely clean sweep (0 issues found on a full read),
and the ledger schema has no separate "blocked" flag to distinguish the two. This handover
file is the source of truth for why the count is 0.

## Instructions for receiving agent / Sharad

1. If you're Sharad: go to claude.ai → Settings → Connectors and authorize Linear for this
   account. That's the entire fix — no code or infra change needed.
2. Once authorized, either wait for the next scheduled `idea-sweep` firing for Usercon, or
   trigger it manually with the standard trigger shape in `routines/README.md`.
3. The next run should execute the full routine from scratch (Issue Cap pre-flight through
   all three roles) — there is no partial state here to resume from.
4. Delete this handover file once a Usercon idea-sweep run completes successfully with
   working Linear access (i.e. once this specific blocker is confirmed cleared).
