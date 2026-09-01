# Handover: idea-sweep routine for Resume Website — Linear MCP entirely unavailable this session

**For:** Any agent/session with working Linear MCP access for this account (or Sharad, to check the Linear connector's auth status in claude.ai connector settings)
**From:** idea-sweep routine, triggered for Resume Website, 2026-09-01
**Blocked by:** No Linear MCP tools loaded at all this session. `ListConnectors` reports the Linear connector with `installState: "unknown"`; no `mcp__Linear__*` tool exists in this session's tool list or via `ToolSearch`; the session's own system context states Linear "require[s] authentication before [its] tools can be used" and that a non-interactive session cannot run the OAuth flow. This is a different, more severe blocker than the long-standing `handovers/preview-branch-cleanup-linear-api-key.md` issue — that one is about the `LINEAR_API_KEY` **repo secret** used by a shell script (step 11 only); this one is the **Linear MCP connector itself** being unauthenticated, which blocks every Linear-touching step of every idea-generation role (issue cap pre-flight, search, create, comment) for this entire run.
**Action:** Once Linear MCP access is confirmed working (e.g. `list_issues` succeeds), pick up the idea-sweep routine for Resume Website using the research payload below so it doesn't have to be redone from scratch, per `routines/idea-sweep.md` and `agents/spec-drift.md` / `agents/bug-error.md` / `agents/market-feature.md`.
**Issue:** N/A — this is a routine-level blocker with no driving Linear issue (this session had no Linear access to create one).

## What I could and couldn't do this session

I have working GitHub MCP access (scoped to `rohrasharad-ship-it/resume-website` and `rohrasharad-ship-it/AI-Workspace`), a local checkout of both repos, and Vercel MCP access, so I completed all the *read-only* research each role needs before it touches Linear. I did not — and could not — do the issue cap pre-flight, search Linear for dupes, create any issue, or comment on anything. **No Linear issues were created or should be assumed created by this run.**

## Payload

### Bug-error (step 1 done, steps 3+ blocked)
`mcp__Vercel__get_runtime_errors` for project `prj_P1V3fzfZ1QwZcVvUNHzdq1DQRtGt` (resume-website), `since: 24h`: **no runtime errors found.** Nothing to file — but re-check freshness rather than trusting this stale by the time this is picked up (checked 2026-09-01).

### Spec-drift (steps 1-2 done, steps 3+ blocked pending Issue Cap + Linear dedupe search)
Read `openspec/project.md` and all 7 capability specs (`hero`, `journey`, `about`, `contact`, `voice-agent`, `design-system`, `site-meta`) against the current codebase (via `CLAUDE.md` and direct source reads — local checkout at `resume-website/`, HEAD `3276cd3`, branch `claude/trusting-ramanujan-8ql0md`).

**One real, high-confidence finding:** `openspec/specs/voice-agent/spec.md` is significantly stale relative to the actual implementation. Verified directly against source, not just CLAUDE.md's summary:

| Spec says | Actual code says |
|---|---|
| Groq model `llama-3.1-8b-instant` | `app/api/agent/route.ts:149` — `model: "openai/gpt-oss-20b"` |
| TTS = ElevenLabs (`/api/tts`) + browser fallback only | `app/api/tts/route.ts` — Sarvam Bulbul (`bulbul:v3`) tried first, ElevenLabs second, browser `speechSynthesis` last |
| Static one-paragraph "System Prompt" block | System prompt is built dynamically from `lib/content/factCatalog.ts`; agent returns an ordered list of **segments** (`{say, focus, cite}`), not a single response — see CLAUDE.md "Voice Agent Pipeline" |
| No mention of page highlighting | `components/PageSpotlight.tsx` + `triggerSpotlightForCitations()` in `lib/voice/pageController.ts` — dark-mask cutout system driven by each segment's `cite` field, entirely unspecced |
| No mention of a keyboard shortcut | ⌘K / Ctrl+K opens the voice bar and starts listening (`components/VoiceAgent.tsx`) |
| No mention of conversation memory | `historyRef` (last 3 turns) sent as `history` with each request, validated server-side by `sanitizeHistory()` |

The `FloatingAvatar` SVG face and its warm/friendly expression *are* real and current (confirmed at `components/VoiceAgent.tsx:204` and the `voice-float` idle-bob keyframe) — that part of the spec is accurate, and there's already an **active, unarchived** openspec change, `openspec/changes/warmer-chatbot-avatar/`, covering exactly that avatar-expression work. **Do not re-propose the avatar** — only the agent-pipeline/TTS/spotlight/shortcut/memory drift above is a genuine unspecced gap.

Suggested issue if filed: something like `📝 [Docs] Update voice-agent openspec to match the tour/spotlight/memory pipeline` — Backlog, `spec-needed`, Sharad Rohra, Medium priority (it's a documentation-accuracy gap, not user-facing breakage).

**Before filing:** search Linear for anything already tracking this (dedupe), and check `openspec/changes/` isn't already covering it — as of this run the active (non-archived) change folders were: `fix-mobile-voice-audio`, `journey-chapter-scrubber`, `mobile-qa-pass`, `save-contact-vcard`, `social-share-preview`, `suggested-prompt-chips`, `warmer-chatbot-avatar`. None of these cover the agent-pipeline spec drift above (they're feature/QA proposals, not spec-accuracy fixes), so it's likely not a duplicate, but confirm via Linear search per role step 4 before creating.

The other 6 capability specs (`hero`, `journey`, `about`, `contact`, `design-system`, `site-meta`) read consistent with the codebase — no other drift found. The two pending items each spec already flags (Cal.com booking → SHA-14, emoji scroll-morph → SHA-13) are already tracked; do not re-file either.

**Issue Cap:** NOT checked — Linear MCP unavailable, so Resume Website's current active-issue count (Backlog/Todo/In Progress/In Review vs. the cap of 5) is unknown this run. Run `agents/shared/issue-cap.md` (Linear Project ID `b01a99ac-46a3-4b00-9139-31e00fae781d`) before filing anything above.

**Stale-issue sweep (spec-drift step 10) and preview-branch/openspec-archive housekeeping (steps 11-12):** not attempted — step 10 needs Linear MCP directly; step 11's script needs the still-missing `LINEAR_API_KEY` repo secret (see `handovers/preview-branch-cleanup-linear-api-key.md`, unresolved across 7+ prior runs) or working Linear MCP as an alternative read path; step 12 (openspec archive sweep) doesn't need Linear but wasn't run this session — check `openspec/changes/` in this repo for anything `complete` and orphaned if picking this up.

### Market-feature (not run)
Read `openspec/project.md`'s vision/non-negotiables/out-of-scope section (living product demo, PM portfolio demonstrating product thinking; no blog/CMS/auth/contact-form/multi-language). Did not complete ideation or the Linear dedupe search — no point proposing features I can't check against existing Linear issues for duplicates. Defer the full market-feature pass to the next session with Linear access.

## Instructions for receiving agent

1. Confirm Linear MCP tools are actually loaded and authenticated (e.g. a `list_issues` call succeeds) before doing anything else.
2. Run the Issue Cap pre-flight for Resume Website (`agents/shared/issue-cap.md`, Linear Project ID `b01a99ac-46a3-4b00-9139-31e00fae781d`).
3. If under cap: search Linear for the voice-agent spec-drift finding above; if not a duplicate, file it per `agents/spec-drift.md` steps 5-8 (Issue Brief format, screenshot, first comment).
4. Re-run bug-error's Vercel check fresh (don't trust the 2026-09-01 "clean" result as still current) and run the full market-feature ideation + dedupe pass (steps 3-9 of `agents/market-feature.md`) — neither was completed this run.
5. Run spec-drift steps 10-12 (stale-issue sweep, preview-branch housekeeping, openspec archive sweep) for Resume Website.
6. Delete this handover file once a session with working Linear MCP access has completed the above for Resume Website.
