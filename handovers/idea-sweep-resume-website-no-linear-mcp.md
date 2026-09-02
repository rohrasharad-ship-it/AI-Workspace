# Handover: idea-sweep for Resume Website blocked — no Linear MCP tool this session

**For:** Any agent/session with working Linear MCP tool access
**From:** idea-sweep routine (orchestrating session, all three roles), triggered
for Resume Website, 2026-09-02
**Blocked by:** This session has **no Linear MCP tool at all** — not a missing
`LINEAR_API_KEY` env var (that's a separate, already-tracked blocker, see
`handovers/preview-branch-cleanup-linear-api-key.md`), but the Linear MCP
connector itself reporting "requires authentication before its tools can be
used," with no OAuth flow available in this non-interactive session. A
deferred-tool search for `linear` and for generic issue/project-management
tool names returned zero Linear tools — only GitHub, Vercel, and Slack MCP
tools are reachable. This is more severe than what prior idea-sweep sessions
hit (they had working `list_issues`/`create_issue`/comment tools and only
lacked shell-level `LINEAR_API_KEY` or git ref-delete permission for the
housekeeping script) — here, the Issue Cap pre-flight, Linear dedupe search,
issue creation, and issue commenting are **all** unavailable, for every one
of the three idea-generation roles. No Playwright/browser MCP tool is
available in this session either, so the mandatory visual-self-QA screenshot
step (`agents/shared/visual-self-qa.md`) also could not run.
**Action:** Once Linear MCP access is available, run the Issue Cap pre-flight
for Resume Website (Linear Project ID `b01a99ac-46a3-4b00-9139-31e00fae781d`
from `projects.md`), then dedupe-search and file whichever of the candidates
below are still relevant and not already tracked. Take the mandatory
Playwright screenshots at filing time (not from this handover — the repo
state may have moved since 2026-09-02).
**Issue:** N/A — this is a routine run (`idea-sweep` → Resume Website), not
tied to a single pre-existing Linear issue.

## What this session *could* still do without Linear/Playwright, and did

- Read `openspec/project.md` and every file under `openspec/specs/` in
  `rohrasharad-ship-it/resume-website` (hero, journey, about, contact,
  voice-agent, design-system, site-meta) via GitHub MCP.
- Read Vercel production runtime errors for the project
  (`prj_P1V3fzfZ1QwZcVvUNHzdq1DQRtGt`) via Vercel MCP, last 7 days.
- Could **not**: check the Issue Cap, search Linear for existing/duplicate
  issues, create issues, comment on issues, run the stale-issue sweep (step
  10), or take Playwright screenshots. Preview-branch housekeeping (step 11)
  and OpenSpec archive housekeeping (step 12) were not attempted this
  session either — step 11 needs `LINEAR_API_KEY` (confirmed unset, see the
  existing tracked blocker) and step 12 needs `gh` CLI (not available in
  this session per its own operating instructions) — both are already
  covered by the standing `preview-branch-cleanup-linear-api-key.md`
  handover, so not duplicated here.

## Bug/error role — result: clean, nothing to file

`get_runtime_errors` for the last 7 days on `meet-sharad.vercel.app` returned
**no runtime errors**. Per `agents/bug-error.md` step 8, this role creates
nothing. No further action needed for this role.

## Spec-drift role — candidates (unverified against Linear — dedupe before filing)

Everything with an explicit `SHA-##` reference already inside a spec file was
**excluded** below since it's already tracked (Cal.com/Calendly booking →
SHA-14 in `openspec/specs/contact/spec.md`; emoji scroll-morph → SHA-13 in
`openspec/specs/design-system/spec.md`). The two candidates below have no
`SHA-##` reference anywhere in the specs, so they may or may not already be
tracked — **search Linear first**.

1. **Avatar headshot still pending.** `openspec/specs/voice-agent/spec.md`
   ("Avatar Photo" section) and the repo's `CLAUDE.md` Pending Items table
   both say `/public/photo/avatar.jpeg` is a pending upload, with
   `IMG_3242.jpeg` as the current fallback. If not already tracked, this is a
   real, low-effort content gap (not a code gap) — suggested priority Low,
   since it's blocked on Sharad supplying a photo, not on any agent building
   something.
2. **Project demo videos pending for two of four eras.** `CLAUDE.md`'s
   Pending Items table lists "Amadeus, ISB live — Impact Analytics, DTU
   pending" for the Journey section's era media boxes
   (`openspec/specs/journey/spec.md` "Era Media Box" — `media.videoSrc`).
   Same caveat: this may be content-blocked on Sharad providing footage
   rather than an agent-buildable gap — check before filing as `agent-ready`-
   track work (it should stay `spec-needed`/Backlog either way per
   conventions).

## Separate observation — stale spec, not a new-issue candidate

`openspec/specs/voice-agent/spec.md` describes an **outdated** version of the
voice agent (SVG-illustrated floating face avatar, ElevenLabs as the primary
TTS provider, Groq `llama-3.1-8b-instant`, a single freeform system prompt,
no mention of the segment/tour architecture). The repo's own `CLAUDE.md` (the
more current, detailed source) describes a materially different, more
advanced implementation: a 56px photo avatar in Hero, Sarvam Bulbul as
primary TTS with ElevenLabs as backup, `openai/gpt-oss-20b`, multi-segment
tours with `focus`/`cite`, `factCatalog.ts`, `PageSpotlight`, conversation
history, and the ⌘K/Ctrl+K shortcut — none of which appear in
`openspec/specs/voice-agent/spec.md`. This reads as the spec having fallen
behind several rounds of shipped code (conventions.md rule 7 says "spec
update before code change — always," which appears not to have been
followed consistently here). This isn't a "plan it, build it" gap in the
sense spec-drift normally files — the functionality is already live — so
it's flagged here as a documentation/spec-hygiene note for whoever next
touches `voice-agent/spec.md`, not filed as a Backlog issue.

## Market/feature role — 2 speculative candidates (not already built, not Out of Scope)

Per `agents/market-feature.md`, capped at 3, and "do not invent filler to hit
the cap" — only 2 came out cheaply differentiated enough to propose:

1. **Recruiter-tailored deep-link tours.** A URL param (e.g.
   `?focus=amadeus` or a small set of named presets) that, on load, has the
   voice agent auto-play a short 1–2 segment tour tailored to that link
   without requiring a mic tap — e.g. Sharad shares a link with an AI-startup
   recruiter that opens already narrating the Impact Analytics + Amadeus
   AI-systems angle. Ties directly to the stated vision ("living product
   demo" for an active PM job search) and is a natural next step after the
   already-shipped ⌘K shortcut — same "cheap, real improvement" spirit
   `CLAUDE.md` uses to justify that shortcut, and distinct from the
   ElevenLabs widget the project explicitly rejected (this is first-party,
   personalized, and link-driven rather than a generic embedded widget).
2. **Idle re-engagement nudge from the voice command bar.** After a period
   of no scroll/interaction post-load, the command bar surfaces a small,
   dismissible one-line hint pulled from `factCatalog.ts`
   (e.g. "💬 Ask me about the $4M ARR launch") instead of sitting silently at
   the bottom of the screen. Reinforces the "AI-native personality"
   differentiation goal in `openspec/project.md` and gives skimming
   recruiters a nudge toward the agent instead of scrolling past it
   untouched. Needs restraint (one-shot, respects
   `prefers-reduced-motion`, no popup/modal) to avoid becoming the kind of
   intrusive widget the project has already said no to.

Both would need a visual mockup + Playwright screenshot per
`agents/shared/visual-specs.md` / `visual-self-qa.md` before filing — not
attempted this session (no browser tool available).

## Instructions for receiving agent

1. Confirm Linear MCP access works (try a `list_issues` call against Resume
   Website's Linear Project ID before anything else).
2. Run the Issue Cap pre-flight for Resume Website. If already at/over cap,
   stop — do not file any of the candidates below this cycle.
3. For each candidate above, search Linear first; skip anything already
   tracked (the SHA-13/SHA-14 style references inside the specs strongly
   suggest this team already tracks known gaps directly in Linear, so check
   carefully before filing to avoid duplicates).
4. File only what survives dedupe, following `agents/shared/issue-brief.md`,
   `agents/shared/conventions.md` (Backlog + `spec-needed`, assignee Sharad
   Rohra, emoji-led title), and the mandatory Playwright screenshot / visual
   preview steps this session couldn't perform.
5. Run spec-drift steps 10 (stale-issue sweep) and, if `LINEAR_API_KEY`/`gh`
   access exists in your session, 11–12 (housekeeping) — see the existing
   `preview-branch-cleanup-linear-api-key.md` handover for the current state
   of that separate, still-unresolved blocker before re-deriving it.
6. Delete this handover file once its candidates have been triaged (filed,
   explicitly rejected, or confirmed duplicates) — it does not need to
   persist once a Linear-enabled run has acted on it.
