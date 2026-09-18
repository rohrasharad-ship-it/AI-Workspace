# Handover: idea-sweep (Usercon) — no Linear MCP access this session, candidates drafted but not filed

**For:** Any agent with Linear MCP access
**From:** idea-sweep routine run for Usercon, 2026-09-18 (Claude Code scheduled session)
**Blocked by:** This session has zero Linear access — no Linear MCP tool is loaded or deferred (confirmed via tool search), and no `LINEAR_API_KEY` env var is set, so not even a raw API fallback was possible. This is a harder blocker than the one already tracked in `handovers/preview-branch-cleanup-linear-api-key.md` (that one has Linear MCP for reads/creates/comments but lacks the API key for the standalone shell script) — this session could not do the Issue Cap pre-flight, search for duplicates, create issues, or comment, at all.
**Action:** For each candidate below, first do the Issue Cap check (`agents/shared/issue-cap.md`, Linear Project ID `47ebefac-a4f4-4bdd-a382-4506f7e79b6b` for Usercon) — if Usercon is already at/over 5 active pipeline issues, do not file any of these this cycle. Otherwise search Linear first per the dedupe notes on each candidate, then create whichever aren't already tracked, following `agents/shared/issue-brief.md` + `agents/shared/conventions.md` exactly (Backlog, `spec-needed`, assignee Sharad Rohra, one emoji-led title each).
**Issue:** N/A — no Linear issue exists yet for any of this; Usercon is a single-project trigger, so a Linear-enabled session would normally file these directly instead of writing a handover.

## Also blocked: no Playwright/browser tool this session

Separately from Linear, this session has no Playwright/browser MCP tool available (confirmed via tool search — only `WebFetch`, a text-summarizing fetch, not a real screenshot). Visual Self-QA (`agents/shared/visual-self-qa.md`) is mandatory for every idea-generation issue and requires an actual screenshot, actually looked at with vision. **None of the candidates below have a screenshot attached.** Whichever agent files these must capture and attach the Visual Self-QA screenshot itself (production URL: the live Vercel deployment for project `usercon`, e.g. `https://usercon-220vjualt-rohrasharad-5924s-projects.vercel.app` or the current production alias) before or right after creating each issue, per the normal role steps — and, for the three market-feature candidates (#5–7), also build the mandatory Visual Specs mockup (`agents/shared/visual-specs.md`, minimal-effort tier) since all three have a UI component. Do not skip either to save time — `agents/shared/conventions.md` rule 12 says never skip silently.

## Bug/Error role: ran clean, nothing to file

Checked Vercel production runtime errors for the `usercon` project (`prj_MAkmwIEkHssO8BH1DfYLbPTNNKxU`, team `team_P5vgMhFNfh2d4fCe2YkRLjey`) over the last 7 days via `get_runtime_errors` — **no runtime errors found**. Per `agents/bug-error.md` step 8, this role creates nothing this cycle. Noting it here only so the sweep ledger entry below makes sense; no action needed from the receiving agent for bug-error.

**Small aside, not worth its own issue:** `projects.md` lists Usercon's Vercel Prod as "TBD" — it isn't; the Vercel project exists and is reachable (`usercon`, latest production deployment `READY` as of 2026-09-15, commit "Simplified menu overlay with Stitch nav map (SHA-214)"). Worth fixing that row next time anyone touches `projects.md`.

## Research basis (read in full this session, via GitHub MCP against `rohrasharad-ship-it/Usercon`)

`openspec/project.md`, all 8 files under `openspec/specs/` (`agent-api`, `context-graph`, `context-receipt`, `context-review`, `context-usage-insights`, `drive-storage`, `mcp-oauth`, `settings-screen`), `PRD.md`, `SPEC.md`, `STRATEGY.md`, `DECISIONS.md`, `NEXT.md`, `HANDOFF.md`, plus the relevant application code under `src/` for each candidate (paths noted per candidate below). Usercon is a solo-builder "context layer for AI agents" — it stores the user's personal context (goals, preferences, habits) and lets trusted agents (Claude, Codex, any MCP client) read/write it via OAuth-gated MCP, so the user doesn't re-explain themselves to every agent. It has no built-in chatbot and is explicitly not an acting agent itself. Currently mid a scoped 2-week self-test with a kill/ship decision gate (per `STRATEGY.md`).

**Explicit Out of Scope (from `openspec/project.md` + `PRD.md`) — do not propose against these:** built-in chatbot/LLM, native iOS/Android app, full permission dashboard, conflict/duplicate resolution workflow, payment/billing, browser clipboard flow or full manual questionnaire onboarding, hard delete (see Gap 3 below — already partially breached by a shipped feature), custom life areas in v1, preset context bundles, TestFlight/app-store release.

---

## Payload — draft candidates (Issue Brief format, ready to paste)

### Spec-drift candidates (from `agents/spec-drift.md`, cap 5 — 4 found)

#### 1. ✏️ [Feature] Inline chip editing for context corrections

**In short:** Inline chip editing

**Problem:** Correcting a saved memory means retyping it in a plain text box, not the tappable chips used elsewhere in the app.

**Solution:** Let people tap and adjust chip-style fields when editing an existing memory, the same way they already do when adding a new one.

**Why:** Usercon's whole design pitch is quick, tappable input instead of generic forms — a plain text box for corrections breaks that promise on one of the most common actions.

**What it looks like:** Editing an item shows the same chip-based sentence builder used for adding new preferences, not a generic multi-line text box.

**Suggested priority:** Medium

**Dedupe search terms for receiving agent:** "chip editing", "inline edit", "context item detail", "correction mechanic"

**First-comment execution detail (post after creating):** Spec basis: `PRD.md` Input Mechanics Direction ("never collapse every input into a generic textarea") and `openspec/specs/context-review/spec.md` ("Future correction mechanics (not yet built)"). Code checked: `src/components/context-item-detail.tsx` (current edit path is a plain title/body/tags form) vs. `src/components/contextual-rule-sheet.tsx` + `src/lib/contextual-rule.ts` (the "sentence slot machine" chip pattern already built and proven for new-preference creation, which the edit path could reuse). 5 of the 7 prioritized shaped-input mechanics in the PRD have no code anywhere in the repo yet; this candidate only covers the edit-path gap, the most visible one. No existing Linear issue found in this session (Linear unreachable) — receiving agent must do the real dedupe search before filing.

---

#### 2. 🔒 [Bug] Agents can self-approve their own pending memories

**In short:** Approval gate bypass

**Problem:** When review is required before a memory goes live, a connected agent can silently approve or reject its own submission instead of waiting for the user to look at it.

**Solution:** Only the user's own screen — never a connected agent — should be able to approve or reject a pending memory.

**Why:** This quietly defeats the entire point of requiring a human look before agent-written memories become active context.

**What it looks like:** Agents can still add and search memories as before, but an agent's request to approve or reject is refused outright — those actions only work from the user's own screen.

**Suggested priority:** High (core trust/review flow)

**Dedupe search terms for receiving agent:** "approve_context", "reject_context", "MCP tool filter", "approval bypass", "review gate"

**First-comment execution detail (post after creating):** Spec basis: `openspec/specs/agent-api/spec.md`'s own "Required Tools/Endpoints" list for agents pointedly omits `approve_context`/`reject_context` (framed elsewhere, e.g. PRD Core Use Case 2 and `DECISIONS.md`, as user-only actions). Code checked: `src/app/api/mcp/route.ts` (`tools/list` handler returns the full, unfiltered `contextTools` array from `src/lib/context-tools.ts`) and `src/lib/mcp-tool-runtime.ts` (executes `approve_context`/`reject_context` for any authenticated MCP caller with no extra gate). Concretely: an agent can write a pending item in `approval_required` mode and immediately self-approve it in the same MCP session. No existing Linear issue found in this session (Linear unreachable) — receiving agent must do the real dedupe search before filing; flag as High given the security/trust implication.

---

#### 3. 📄 [Docs] Non-negotiables don't mention the archived-item permanent-delete exception

**In short:** Delete-policy doc gap

**Problem:** The project's own ground rules say memories are never permanently deleted, but there's already a screen that permanently deletes archived items forever.

**Solution:** Update the ground-rules doc to spell out that only the user, from their own screen, can permanently delete an already-archived item — agents still can never delete anything.

**Why:** Right now the written rules and the real, shipped product disagree, which is confusing for anyone (including a future agent) reading the rules as ground truth.

**What it looks like:** The non-negotiables list gets one added line describing the browser-only archived-purge exception; no change to the actual purge feature or its behavior.

**Suggested priority:** Medium

**Dedupe search terms for receiving agent:** "hard delete", "archived purge", "non-negotiables", "permanent delete"

**First-comment execution detail (post after creating):** `openspec/project.md`'s Non-Negotiables list states "Archive, never hard delete," and `PRD.md`'s Out of Scope list says "Hard delete." But `openspec/changes/sha-182-archived-context-purge` (all tasks checked, fully shipped) plus `src/lib/archived-purge.ts`, `src/components/archived-purge-panel.tsx`, and `POST`/`GET /api/context/archived/purge` let the browser-side user permanently delete archived items — hard delete by any normal definition. `SPEC.md` §9 and `openspec/specs/context-review/spec.md` do document this as an intentional, agent-excluded, browser-only exception, but `project.md`/`PRD.md` (the stated top-level sources of truth) were never amended. No existing Linear issue found in this session (Linear unreachable) — receiving agent must do the real dedupe search before filing.

---

#### 4. 🗂️ [Chore] Spec files are missing several already-shipped features

**In short:** Specs out of date

**Problem:** The official spec docs don't mention some features that are already fully built and live, like exporting your memories or the guided way to add a new preference — and in one case a spec file still lists an already-shipped feature as "not yet built."

**Solution:** Fold the finished change proposals back into the main spec files (and archive the mobile-shell capability spec that's still sitting in a change folder) so the specs match what's actually shipped.

**Why:** Anyone reading the specs to understand what exists today — including this exact ideation exercise — gets a wrong picture, risking re-proposing or re-building things that already work.

**What it looks like:** No visible change for the user — this is a documentation catch-up so future planning starts from an accurate baseline.

**Suggested priority:** Low

**Dedupe search terms for receiving agent:** "openspec archive", "spec drift", "context packet export spec", "mobile-shell spec"

**First-comment execution detail (post after creating):** `openspec/changes/` has 20+ change proposals with every task checked (fully implemented) that were never archived into `openspec/specs/`. Two concrete examples: `portable-context-packet-export` (fully built — "Copy visible packet" + per-collection export in `context-workspace.tsx` / `src/lib/context-packet.ts`) has zero mention in `openspec/specs/context-review/spec.md`; `sha-220-contextual-manual-rule-input` (the sentence-slot-machine "Add rule" flow, fully built) is still listed in that same spec file as a "Future correction mechanic (not yet built)." Separately, a 9th capability (`mobile-shell`, referenced from `openspec/project.md`) has its spec only under `openspec/changes/sha-204-mobile-tab-nav/specs/mobile-shell/spec.md`, never archived. No existing Linear issue found in this session (Linear unreachable) — receiving agent must do the real dedupe search before filing.

---

### Market/feature candidates (from `agents/market-feature.md`, cap 3 — 3 found)

#### 5. 🎯 [Feature] Show whether a memory was stated by you or guessed by an agent

**In short:** Confidence tags on memories

**Problem:** A memory an agent guessed from something you said looks exactly the same as something you typed yourself, so judging which ones need a closer look is hard.

**Solution:** Tag each memory as "you said this" or "agent inferred this," shown right alongside the existing source details.

**Why:** This directly supports fast, careful review of what agents are writing about you — the core trust question this whole project is testing.

**What it looks like:** A small label next to the existing "why Usercon believes this" note, e.g. "Inferred from your message" vs. "Stated directly." See preview link below once built.

**Suggested priority:** Medium

**Dedupe search terms for receiving agent:** "confidence", "inferred", "source card", "provenance"

**First-comment execution detail (post after creating):** Vision basis: `STRATEGY.md`'s trust/review bottleneck (Sharad manually reviewing dozens of agent-written items during the 2-week self-test). Fits by adding a lightweight `confidence: "explicit" | "inferred"` field to existing context items, settable by the writing agent at `add_context` time, surfaced in the current "Why Usercon believes this" source-card breakdown — no new UI paradigm, nothing in Out of Scope touched. No similar idea found tracked in Linear this session (unreachable) — receiving agent must do the real dedupe search, including against anything spec-drift may have filed.

---

#### 6. 🤝 [Feature] Give newly connected agents a starter set of your key facts

**In short:** New-agent starter context

**Problem:** When you connect a brand-new agent, it has no idea what matters most about you yet and has to fish around before it becomes useful.

**Solution:** The moment a new agent connects, automatically hand it a short, ranked list of your most important existing facts.

**Why:** This is the core promise of the product — that switching agents shouldn't mean starting over — and nothing today actually delivers that at the moment of first connection.

**What it looks like:** No new screen for the user; a newly connected agent's very first response already reflects the user's top facts instead of starting blank. See preview link below once built.

**Suggested priority:** Medium

**Dedupe search terms for receiving agent:** "starter context", "onboarding agent", "new MCP client", "first connection"

**First-comment execution detail (post after creating):** Vision basis: `STRATEGY.md`'s "neutrality × plurality" thesis (horizontal facts should follow the user between agents rather than each agent starting cold). Proposed as a `get_starter_context()` MCP tool/API endpoint returning a small, priority-ranked slice of existing approved `You`-level and top-tagged context the moment a new OAuth grant is issued — deliberately distinct from the Out-of-Scope "preset context bundles" (that's canned content; this surfaces the user's own existing data). No similar idea found tracked in Linear this session (unreachable) — receiving agent must do the real dedupe search.

---

#### 7. 📊 [Feature] Weekly recap of facts that helped across different agents

**In short:** Weekly cross-agent recap

**Problem:** Proving Usercon is actually useful across agents right now means digging through activity logs by hand.

**Solution:** A short weekly summary in Settings showing which facts got reused across more than one type of agent that week.

**Why:** This turns the project's own success test (does a horizontal fact actually get reused across agents?) into something glanceable, instead of a manual log-mining exercise.

**What it looks like:** A small card in Settings, e.g. "This week: 3 facts reused across 2 areas," built entirely from data already being tracked. See preview link below once built.

**Suggested priority:** Low

**Dedupe search terms for receiving agent:** "weekly recap", "cross-vertical digest", "usage insights", "activity summary"

**First-comment execution detail (post after creating):** Vision basis: `STRATEGY.md`'s stated 2-week self-test success criterion (naming concrete cases where a horizontal fact informed a different vertical task). Buildable entirely from data already logged by the existing activity log / cross-vertical tagging (`SHA-166`, `GET /api/activity?crossVertical=true`, `cross-vertical-hits-panel`) — no new storage or schema needed. No similar idea found tracked in Linear this session (unreachable) — receiving agent must do the real dedupe search.

---

## Instructions for receiving agent

1. Read this file in full.
2. Do the Issue Cap pre-flight for Usercon (Linear Project ID `47ebefac-a4f4-4bdd-a382-4506f7e79b6b`, per `agents/shared/issue-cap.md`). If Usercon is at/over 5 active pipeline issues, stop — do not file any of these this cycle.
3. For each of the 7 candidates above, search Linear first using the noted dedupe terms; skip anything already tracked (open or recently closed).
4. Create surviving candidates as Backlog + `spec-needed`, assignee Sharad Rohra, title exactly as given (one emoji, already chosen to fit), description exactly as given (already in Issue Brief format) — per `agents/shared/issue-brief.md` and `agents/shared/conventions.md`. Respect each role's own cap even though this is one combined handover: max 5 from the spec-drift group (#1–4, all 4 survive that cap), max 3 from the market-feature group (#5–7, all 3 survive that cap).
5. Attach a real Playwright screenshot (Visual Self-QA, per `agents/shared/visual-self-qa.md`) to every created issue. For #1, #5, #6, #7 (real UI component), also build and attach a Visual Specs mockup (`agents/shared/visual-specs.md`, minimal-effort tier) and link it in the description's "What it looks like" line before finalizing.
6. Post the first-comment execution detail given above on each created issue (already drafted per candidate).
7. Once all 7 candidates are resolved (filed or explicitly skipped as duplicate), delete this handover file.
8. Also see `agents/spec-drift.md` steps 10–12 (stale-issue sweep, preview-branch housekeeping, openspec archive sweep) — this session could not run any of those either: step 10 needs the same Linear access that's missing here; steps 11–12 need `LINEAR_API_KEY` as a raw env var, already tracked as a separate, older blocker in `handovers/preview-branch-cleanup-linear-api-key.md`. Fold Usercon's stale-issue sweep into whichever future run has real Linear access; no need to duplicate the LINEAR_API_KEY tracking here.
