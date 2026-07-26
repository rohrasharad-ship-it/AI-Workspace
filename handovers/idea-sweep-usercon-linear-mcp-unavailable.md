# Handover: idea-sweep routine (Usercon) blocked — Linear MCP not authenticated

**For:** Any agent/session with an authenticated Linear MCP connection
**From:** Claude, scheduled `idea-sweep` trigger session, 2026-07-26
**Blocked by:** Linear MCP server requires OAuth authorization; this session is
non-interactive (scheduled task) and cannot complete the OAuth flow. No other
Linear access path was available.
**Action:** Once Linear MCP is authorized, run the full `idea-sweep` routine
for **Usercon** per `routines/idea-sweep.md` — nothing below has been filed.
**Routine:** `routines/idea-sweep.md` — trigger was "Run the idea-sweep routine
for usercon"

---

## Why this file exists

The scheduled trigger asked me to run `idea-sweep` for Usercon. I read
`routines/idea-sweep.md`, `routines/README.md`, `agents/spec-drift.md`,
`agents/bug-error.md`, `agents/market-feature.md`, `agents/shared/issue-cap.md`,
and `agents/shared/conventions.md` as required. Every path through this
routine needs Linear MCP:

- The mandatory Issue Cap pre-flight (`agents/shared/issue-cap.md`) requires
  `list_issues` against the Usercon Linear Project ID.
- Dedup search ("search the target Linear project first") in all three roles.
- Issue creation (spec-drift up to 5, bug-error up to 5, market-feature up to 3).
- Spec-drift's stale-issue sweep (steps 10) requires reading and commenting on
  existing Linear issues.

This session's Linear MCP tool is present but gated behind an OAuth flow this
non-interactive session cannot complete. Per `agents/shared/conventions.md`
("Blocked-agent handover" — "no Linear MCP" is the literal example given),
this is a hard tool-access wall, not a "wait and retry" situation. I did not
attempt any workaround (e.g. filing via GitHub Issues instead of Linear,
guessing at cap status) since that would violate the routine's own guardrails.

**Nothing was filed, searched, or commented on in Linear for this run.** No
issue cap count exists for Usercon from this session — treat it as unknown,
not zero.

## Payload — context gathered so the next session can move fast

Project resolved from `projects.md`:

| Field | Value |
|---|---|
| Repo | `rohrasharad-ship-it/Usercon` |
| Linear Project | UserCon |
| Linear Project ID | `47ebefac-a4f4-4bdd-a382-4506f7e79b6b` |
| Slack Channel | `#usercon` (`C0BF843AFK6`) |
| Vercel Prod | **TBD** in `projects.md` — see note below |

**Note — Vercel Prod is unset for Usercon.** `bug-error` needs a production URL
to read runtime logs/errors; with `Vercel Prod: TBD`, that role has no
deployment to inspect regardless of Linear access. Worth flagging to Sharad
(or updating `projects.md`) separately from this handover — a bug-error run
against Usercon can't do anything until that field is filled in.

**openspec/project.md summary (Usercon):** user-owned context layer for AI
agents — stores structured personal context, lets trusted agents (Claude,
Codex) read/write it via MCP+OAuth. Next.js 16 App Router, React 19 +
TypeScript, Google Drive-backed storage. Non-negotiables include: archive
never hard-delete, no unauthenticated MCP writes in prod, every PR needs a
Vercel preview URL, no new deps without a spec proposal. Out of scope:
built-in chatbot/LLM, native mobile app, full permission dashboard,
conflict/duplicate resolution UI, billing, hard delete, custom life areas.

**openspec/specs/ capabilities present (8):** `agent-api`, `context-graph`,
`context-receipt`, `context-review`, `context-usage-insights`,
`drive-storage`, `mcp-oauth`, `settings-screen`. I did not diff these against
`src/` line-by-line — that's `spec-drift` steps 1–3, which need to run in the
same session that can also do step 4 (Linear dedup search) and step 5 (file),
so doing a shallow read-only pass here without Linear access risked producing
low-confidence gaps ahead of the guardrail ("meaningful gaps only, ignore
cosmetic nitpicks"). Better to run steps 1–9 fresh, together, once unblocked.

## Instructions for receiving agent

1. Confirm Linear MCP is authenticated (try `list_projects` or `list_issues`
   for the ID above).
2. Run `agents/shared/issue-cap.md`'s count for Usercon using the Project ID
   above (not the display name — `issue-cap.md` calls out Usercon by name as
   a project where name-based filtering silently returns zero).
3. If under cap, run `agents/spec-drift.md` steps 1–12, `agents/bug-error.md`
   (only meaningful once `projects.md` has a real Vercel Prod URL for
   Usercon), and `agents/market-feature.md` in full, per `routines/idea-sweep.md`.
4. Post the consolidated per-project Slack summary to `#usercon` per the
   template in `routines/idea-sweep.md`.
5. Delete this handover file once a full idea-sweep cycle has actually run
   for Usercon.

## What I did instead this session

Posted to `#usercon` explaining the sweep did not run and why (Linear MCP
unavailable in this automated session), so Sharad isn't left thinking a clean
sweep happened. No Slack notification silently skipped.
