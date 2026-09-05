# Handover: idea-sweep (Resume Website) blocked — no Linear MCP access this session

**For:** Any agent/session with working Linear MCP access
**From:** Claude Code cloud session running the scheduled `idea-sweep` routine for Resume Website, 2026-09-05
**Blocked by:** No Linear MCP tools available this session. `ListConnectors` shows the Linear connector `enabledInChat: true` but `installState: "unknown"`, and the harness explicitly reported: "The following MCP servers require authentication before their tools can be used: Linear." This is a non-interactive scheduled session, so it cannot complete the OAuth/re-authorization flow itself. This looks like a session/connector-auth state issue, not a structural absence — prior idea-sweep runs (see `data/sweep-runs.jsonl` and other `handovers/` files) clearly did have working Linear MCP access, including full-workspace `list_issues` pagination.
**Action:** Once Linear MCP access is restored (Sharad re-authorizes the Linear connector via claude.ai connector settings, or a session with a working connection picks this up), re-run the `idea-sweep` routine for **Resume Website** per `routines/idea-sweep.md`, using the research below as a head start rather than starting from zero.
**Issue:** No driving Linear issue — this is a routine-level blocker, not an issue-level one.

---

## What this session could NOT do (all require Linear MCP)

- Issue Cap pre-flight (`agents/shared/issue-cap.md`) — could not count active pipeline issues for Resume Website (Linear Project ID `b01a99ac-46a3-4b00-9139-31e00fae781d`), so **it is unknown whether this project is at cap**.
- Dedupe search against existing Linear issues for any candidate below.
- File any Backlog issue, or comment on any existing issue.
- Spec-drift step 10 (stale-issue sweep) — could not list/read open Backlog issues to check if they look already resolved.
- Spec-drift steps 11–12 (preview-branch cleanup / OpenSpec archive housekeeping) — these also need Linear (issue status lookups) and, per `handovers/preview-branch-cleanup-linear-api-key.md`, are separately blocked on a missing `LINEAR_API_KEY` repo secret regardless of MCP access. Not re-verified this run.

Also no Playwright/browser tool was available in this session's toolset, so even if Linear had worked, the mandatory Visual Self-QA screenshot (`agents/shared/visual-self-qa.md`) could not have been attached to any new issue. Both blockers compound — a fully working session needs both restored.

Because filing/dedupe/cap-check are all blocked, **no issues were created and no `data/sweep-runs.jsonl` entry was appended** for this run — appending a `"clean": true` entry would misrepresent a run that didn't actually execute its Linear-dependent steps. The receiving session should append the ledger line once it completes the real run.

## What this session COULD still do (read-only, no Linear needed) — findings below

### 1. Bug-error role: clean, nothing to file

Checked Vercel production runtime errors for Resume Website (`projectId: prj_P1V3fzfZ1QwZcVvUNHzdq1DQRtGt`, `teamId: team_P5vgMhFNfh2d4fCe2YkRLjey`) over the last 7 days via `mcp__Vercel__get_runtime_errors`: **no runtime errors found**. Nothing to file this cycle.

### 2. Market-feature role: not run

Skipped doing real ideation this run — even a great idea can't be filed without Linear (dedupe + create) and can't carry the mandatory current-state screenshot without Playwright. Re-run this role properly once both tools are back rather than trusting any idea I'd guess at now.

### 3. Spec-drift role: one real, high-confidence finding

**`openspec/specs/voice-agent/spec.md` is significantly out of date vs. what's actually shipped.** This is exactly the kind of drift `project.md` warns matters — it tells future agents "read this file plus only the ONE relevant capability file," so a stale voice-agent spec would feed wrong context into any future spec-conversation or builder session that touches the voice agent.

Confirmed by reading the current code directly (not just `CLAUDE.md`, which already documents the real architecture and agrees with the code):

| Spec says (`openspec/specs/voice-agent/spec.md`) | Actually shipped (verified in code) |
|---|---|
| Agent model: Groq `llama-3.1-8b-instant` | `app/api/agent/route.ts`: Groq `openai/gpt-oss-20b`, `reasoning_effort: "medium"` |
| Hardcoded system prompt (~6 lines, no dynamic facts) | `buildSystemPrompt()` in `route.ts` injects `factCatalogText()` from `lib/content/factCatalog.ts` — the agent's knowledge is generated from `eras.ts`/`projects.ts`/`eraCaseStudies.ts`/`usercon.ts`, not hand-written |
| Single-response model: agent just answers, no structured multi-stop behavior described | Real implementation returns an ordered list of up to 3 **segments**, each with `{say, focus: {section}|{eraId}, cite}` — a "tour" the page walks through (`sanitizeSegments()` in `route.ts`) |
| No mention of conversation memory | Real implementation sanitizes and forwards a `history` array (`sanitizeHistory()`, capped at 3 turns / 6 messages), used to resolve follow-up questions |
| No mention of citation/spotlighting | Real implementation validates `cite` ids against the fact catalog server-side and drives `PageSpotlight.tsx` client-side — entirely undocumented in this spec |
| TTS stack: "ElevenLabs (`/api/tts`)" as the primary/only listed provider | Per `CLAUDE.md` (checked into the repo, authoritative): Sarvam Bulbul (`bulbul:v3`) is the **primary** TTS provider, ElevenLabs is a backup, browser `speechSynthesis` is the last resort — the reverse priority of what the spec implies |
| "Floating SVG Avatar" — 120×138px illustrated South Asian face, lip-synced via Web Audio `AnalyserNode`, blinking eyelid ellipses, idle float keyframe | `CLAUDE.md` describes the shipped avatar as a 56px `public/photo/avatar.jpeg` photo circle instead — no illustrated SVG face component is referenced anywhere in current docs or `components/` |
| Command bar / state machine described (idle/listening/thinking/speaking pill) | Broadly still plausible/consistent — **not** contradicted, likely still accurate, did not attempt to fully re-verify this part |

I did not open `components/VoiceAgent.tsx` line-by-line to double-check the command-bar visuals and avatar claims pixel-for-pixel (that's normal implementation-detail work for whoever picks up the actual issue) — but the model name, system-prompt construction, segment/tour/citation architecture, and TTS provider order are confirmed directly from `app/api/agent/route.ts` and `lib/content/factCatalog.ts`, cross-checked against `CLAUDE.md`.

**Suggested issue** (for the receiving agent to dedupe-search first, then file if not already tracked):

- **Title:** `📝 [Chore] voice-agent openspec doc doesn't match shipped implementation`
- **Priority:** Medium (doesn't block anything today, but will actively mislead the next agent who reads it before touching the voice agent)
- **Problem:** `openspec/specs/voice-agent/spec.md` describes an old architecture (ElevenLabs-primary TTS, `llama-3.1-8b-instant`, hardcoded prompt, SVG avatar, no tour/segments/citation/history) that no longer matches what's live.
- **Solution:** Rewrite the spec section-by-section against `app/api/agent/route.ts`, `lib/content/factCatalog.ts`, `lib/voice/pageController.ts`, `components/VoiceAgent.tsx`, `components/PageSpotlight.tsx`, and `CLAUDE.md`'s "Voice Agent Pipeline" / "Voice Agent Spotlighting" sections (already accurate — could be the primary source to port from).
- **Why:** `openspec/project.md` explicitly tells future single-issue agents to read only the one relevant capability file, not the whole spec tree — a wrong voice-agent spec actively misdirects that shortcut.
- **What it looks like:** Doc-only change, no screenshot strictly necessary for the issue itself, though the receiving agent should still follow the mandatory Visual Self-QA convention if the role file requires it for every idea-generation issue regardless of content type.
- **Dedupe terms to search first:** "voice-agent spec", "openspec drift", "factCatalog", "SHA-1" through recent SHA numbers referencing voice agent doc work.

Minor, lower-confidence secondary observation (probably not worth its own issue, mention only in the above issue's first comment if filed): `openspec/project.md`'s capability table lists Site Meta as "In progress, see SHA-11" while `openspec/specs/site-meta/spec.md` itself says "Status: Live — SHA-173" — a small status mismatch between the index and the capability file, not necessarily worth a separate Backlog issue on its own (cosmetic).

## Instructions for receiving agent

1. Confirm Linear MCP is working (`list_issues` against project ID `b01a99ac-46a3-4b00-9139-31e00fae781d` returns real data, not an empty list).
2. Run the Issue Cap pre-flight (`agents/shared/issue-cap.md`) for Resume Website before filing anything.
3. If under cap: dedupe-search Linear for the voice-agent spec-drift finding above; if not already tracked, file it per `agents/spec-drift.md` steps 5–8 (Issue Brief format, Sharad as assignee, emoji title, first-comment execution detail, screenshot per Visual Self-QA if a Playwright tool is available this time).
4. Run spec-drift steps 10–12 (stale-issue sweep, preview-branch housekeeping, OpenSpec archive sweep) properly — none of them ran this cycle.
5. Run market-feature fresh (this session did no real ideation) — remember the mandatory visual per `agents/shared/visual-specs.md`.
6. Append the `data/sweep-runs.jsonl` line for this Resume Website run once it actually completes, with real filed counts.
7. Delete this handover file once the above is done and tracked in Linear/git — until then it's the record of what this run found and couldn't act on.
