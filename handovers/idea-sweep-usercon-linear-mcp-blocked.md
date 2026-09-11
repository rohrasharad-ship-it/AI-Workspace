# Handover: idea-sweep routine for Usercon — blocked on Linear MCP access

**For:** Any agent/session with Linear MCP access
**From:** Claude (scheduled `idea-sweep` trigger, session 2026-09-11)
**Blocked by:** Linear MCP was not authorized in the triggering session (connector
requires an interactive OAuth flow this non-interactive session cannot run).
No `list_issues`, `save_issue`, or comment access was available at any point.
**Action:** Run the Issue Cap pre-flight for Usercon, dedupe the candidates
below against existing Linear issues, then file whatever survives per
`agents/shared/issue-cap.md`, `agents/shared/issue-brief.md`, and
`agents/shared/conventions.md`.
**Issue:** N/A — no Linear issue exists yet for this handover itself (Linear
was unreachable). File the candidates below directly; there is nothing to
comment on.

---

## Why this handover exists

The scheduled trigger asked to run `routines/idea-sweep.md` for **Usercon**
(repo `rohrasharad-ship-it/Usercon`, Linear project `UserCon`, ID
`47ebefac-a4f4-4bdd-a382-4506f7e79b6b`). Per `agents/shared/conventions.md`
("Blocked-agent handover"), this session hit a hard tool-access wall rather
than mere uncertainty, so it stopped and wrote this handover instead of
guessing at Linear state or fabricating results:

- **Issue Cap pre-flight** (`agents/shared/issue-cap.md`) could not be run —
  it requires `list_issues` filtered by the Linear Project ID. **The count for
  Usercon is unknown this cycle** — do not assume it's under cap; check it
  first, same as any normal run.
- **spec-drift** steps 1–3 (read-only: openspec vs. code) were run manually
  from GitHub (see Payload below) since they don't need Linear. Steps 4–9
  (dedupe search + filing + screenshots) were **not** attempted — no Linear,
  and no live browser/Playwright session against a deployed Usercon URL was
  set up for this research pass.
- **spec-drift** steps 10–11 (stale-issue sweep, preview-branch housekeeping)
  were **not** run — step 10 needs to read/comment on existing Linear issues;
  step 11's cleanup script needs `LINEAR_API_KEY`, which this session doesn't
  have.
- **spec-drift** step 12 (OpenSpec archive housekeeping) does **not** need
  Linear, but was skipped in this pass to keep this handover focused — a
  future session can run `bash scripts/archive-merged-openspec-changes.sh --sweep`
  in AI-Workspace independent of this handover.
- **bug-error** could not run at all — `projects.md` lists Usercon's Vercel
  Prod as `TBD`, so there is no known production URL to pull runtime
  logs/errors from, separate from the Linear blocker.
- **market-feature** steps 1–3 (read-only vision research) were run manually
  from GitHub; steps 4–9 (dedupe + filing + screenshots) were not attempted,
  same reason as spec-drift.

**Important correction surfaced by this research:** Usercon is **not** a
user-conference/event-networking app despite the name — it's a personal,
portable, cross-agent context store ("a user-owned context layer for AI
agents"). Anyone filing these issues should use that framing, not a
conference/events framing.

## Payload — candidate issues for a Linear-enabled agent to dedupe and file

Each candidate below still needs, before filing: a Linear search for
duplicates in the UserCon project, a title emoji per
`agents/shared/conventions.md`, the full Issue Brief format
(`agents/shared/issue-brief.md`), a first comment with execution detail, and
(mandatory) a real Playwright screenshot attached via
`prepare_attachment_upload` → PUT → `create_attachment_from_upload` per
`agents/shared/visual-self-qa.md`. None of that was done here — treat
everything below as raw research input, not issue-ready text.

### Spec-drift gaps (cap 5 per `agents/spec-drift.md`; 4 found)

1. **Shaped input mechanics beyond inline editing and contextual rules** — Medium priority.
   `PRD.md` ("Input Mechanics Direction") and `DECISIONS.md` ("Input Mechanics
   Priority") lock a 7-step build order for capturing context (inline
   chip/text edit → "Tell me more" voice/text sheet → floating voice capture →
   this-or-that comparative pairs → spectrum dials → sentence slot machine →
   30-second onboarding voice memo). Only steps 1 (inline edit) and 6
   (`ContextualRuleSheet`) are built. Steps 2, 3, 4, 5, 7 don't exist anywhere
   in `src/components` or `src/lib`. `NEXT.md` Build Order item 10 repeats the
   same pending list. Checked: `PRD.md`, `DECISIONS.md`, `NEXT.md`,
   `src/components/context-item-detail.tsx`, `context-workspace.tsx`,
   `contextual-rule-sheet.tsx`, full `src/components/` listing.

2. **MCP OAuth connected-Drive consent path is a self-flagged, unverified blocker** — High priority.
   `HANDOFF.md` ("What Is Not Done Yet") states verbatim that the hosted MCP
   OAuth connected-Drive consent page still needs verification with a real
   Claude custom connector or a browser with a connected Drive cookie, and
   that if Claude connects without showing the Usercon/Google consent screens
   when needed, that's a blocker. This touches the project Non-Negotiable
   "Hosted MCP access requires OAuth by default; no unauthenticated MCP writes
   in production" (`openspec/project.md`). Checked: `HANDOFF.md`,
   `openspec/specs/mcp-oauth/spec.md`, `openspec/project.md`.

3. **Mobile Safari rendering issue flagged but never closed out** — Low–Medium priority.
   `HANDOFF.md` states Sharad's phone Safari issue "still needs device-side
   verification" even though automated checks (HTTP 200, automated mobile
   viewport rendering) pass. No later doc confirms it was fixed or re-triaged.
   Matters because Usercon is meant to be a daily-use PWA. Checked:
   `HANDOFF.md`, `openspec/changes/sha-204-mobile-tab-nav/specs/mobile-shell/spec.md`.

4. **No path to convert a Note into a Goal/Project/Preference** — Low priority.
   `DECISIONS.md` locks in "Notes are loose context that can later become a
   Goal, Project, or Preference," but no UI or tool exists for this — the edit
   surface only touches title/body/tags, `type` isn't editable in the UI, and
   there's no promotion endpoint in `context-tools.ts`/`context-validation.ts`
   (the generic `PATCH /api/context/[id]` could technically accept it, so
   it's a UI/tool gap, not a schema block). Checked: `DECISIONS.md`,
   `SPEC.md` §4.1, `src/components/context-item-detail.tsx`,
   `src/lib/context-validation.ts`, `src/app/api/context/[id]/route.ts`.

*(A 5th candidate was deliberately not forced — every other openspec change
folder checked (`sha-179` through `sha-243`, `portable-context-packet-export`,
etc.) is fully implemented in code even where its own `tasks.md` has stale
unchecked boxes. Anything explicitly marked Out of Scope in
`openspec/project.md` — conflict/duplicate resolution, full permission
dashboard, custom life areas, hard delete, browser clipboard flow, native
packaging, built-in chatbot — was excluded; those are deliberate non-goals,
not gaps.)*

### Market-feature ideas (cap 3 per `agents/market-feature.md`; 3 found)

All three are grounded in Usercon's actual differentiation thesis
(portability/neutrality across multiple agents, per `STRATEGY.md`) rather than
a conference-app comparison — see the correction note above.

1. **Cross-vertical reuse digest ("what Usercon actually did for you")** — High priority.
   `STRATEGY.md`'s 2-week decision gate requires naming ≥2 concrete cases of a
   horizontal fact correctly informing a different vertical task than the one
   it was captured under. The raw data already exists (`crossVertical` flag on
   activity entries, `GET /api/activity?crossVertical=true`, per-item usage
   history) but there's no rollup that answers this question directly — today
   it requires manually scanning raw activity/receipts. Low-cost (no new
   dependencies, reuses existing logging). Checked:
   `openspec/specs/context-usage-insights/spec.md`,
   `openspec/specs/context-receipt/spec.md`,
   `openspec/specs/agent-api/spec.md`,
   `src/components/cross-vertical-hits-panel.tsx` (raw list only),
   `src/components/home-activity-panel.tsx` (recent receipts only, no rollup).

2. **Agent-plurality / portability-health indicator** — Medium priority.
   The existing "agent contribution breakdown" only counts who *wrote*
   context (`sourceAgent`, from `sha-143`). Nothing surfaces who *reads*
   context over time per agent — the actual "plurality" variable
   `STRATEGY.md` says the product's value depends on (if Sharad silently
   consolidates to one agent, that's the strategic kill signal). Read-agent
   data already exists per activity entry, so this is aggregation/display,
   not new plumbing. Checked: `STRATEGY.md` ("The thesis"),
   `openspec/specs/context-usage-insights/spec.md`, `src/lib/activity-log.ts`,
   `src/lib/usage-insights.ts`, `src/components/context-workspace.tsx`.

3. **Unused-context staleness signal** — Low–Medium priority.
   `STRATEGY.md` cites the "Notion Life OS signal" — Sharad's prior
   self-context system rotted from silent disuse — as a hard design
   constraint ("zero-maintenance or it repeats the Notion failure"). Usage
   insights show *if* an item was read in the last 30 days per-item, but
   there's no proactive "never read" / "not read in N days" rollup across
   items — exactly the decay pattern that killed the Notion system. Purely
   observational (surfaces candidates for archiving, doesn't auto-archive),
   consistent with archive-never-delete and the no-conflict-resolution
   Out-of-Scope boundary. Checked: `STRATEGY.md` ("The Notion Life OS
   signal"), `openspec/specs/context-usage-insights/spec.md`,
   `src/lib/usage-insights.ts`, `src/components/context-item-detail.tsx`.

## Instructions for receiving agent

1. Run the Issue Cap pre-flight for Usercon (`agents/shared/issue-cap.md`,
   Linear Project ID `47ebefac-a4f4-4bdd-a382-4506f7e79b6b`). If already at or
   over 5 active pipeline issues, stop — do not file any of the candidates
   above this cycle.
2. If under cap, search the UserCon Linear project for each candidate above;
   drop anything already tracked.
3. File what survives following `agents/spec-drift.md` steps 5–8 (gaps) and
   `agents/market-feature.md` steps 5–8 (feature ideas) — Issue Brief format,
   emoji title, Sharad Rohra as assignee, `spec-needed` label, a visual
   preview/screenshot per `agents/shared/visual-self-qa.md`, and a first
   comment with execution detail.
4. Separately, if you have Vercel access and can find/confirm a Usercon
   production URL, run `agents/bug-error.md` for real — it was skipped
   entirely in this pass (see Payload note above) and `projects.md` should be
   updated with the real prod URL once known (currently `TBD`).
5. Append a line to `data/sweep-runs.jsonl` in AI-Workspace once filing is
   done, reflecting the actual counts filed (not this handover's candidate
   counts) — e.g. `{"at":"<ISO8601>","project":"Usercon","filed":{"bugs":0,"features":N},"clean":false}`.
6. Delete this handover file once filing is complete and tracked in Linear —
   until then, it's the source of truth for this cycle's Usercon idea-sweep.
