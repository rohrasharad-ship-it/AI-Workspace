# Handover: idea-sweep for Resume Website blocked — no Linear MCP tool access in this session

**For:** Any agent/session with working Linear MCP access (create + search issues, comment, attach files)
**From:** idea-sweep routine run for Resume Website (all three roles: spec-drift, bug-error, market-feature), 2026-09-21
**Blocked by:** This session has no Linear MCP tools at all — not "missing API key for a shell script" (that's the separate, already-documented blocker in `handovers/preview-branch-cleanup-linear-api-key.md`), but zero `mcp__Linear__*` tools present in the toolset. The system context explicitly listed Linear as an MCP server "requiring authentication before its tools can be used," and this is a non-interactive session that cannot run the OAuth connector flow. Confirmed by `ToolSearch` returning no Linear-related tools at all.
**Action:** Once Linear MCP is connected/authorized for a session (via claude.ai connector settings, per the standard non-interactive-session guidance), re-run `agents/spec-drift.md` steps 1–11 and `agents/market-feature.md` steps 1–9 for Resume Website (Linear Project ID `b01a99ac-46a3-4b00-9139-31e00fae781d`) using the pre-verified research below so the next run doesn't have to redo it from scratch.
**Issue:** N/A — this is a routine pre-flight blocker, not tied to one Linear issue (the routine itself has no Linear issue; it's triggered by schedule, not assignment).

## What this session could and couldn't do

Every one of the three idea-generation roles requires Linear MCP for at least
one mandatory step (Issue Cap pre-flight, search-before-file dedupe, issue
creation, or stale-issue commenting) before it's allowed to file anything.
With zero Linear tools available, none of the three roles could complete
their job end-to-end. Rather than go silent, this session did the part of
each role's research that doesn't require Linear, so the receiving agent can
finish fast instead of re-deriving all of this.

### Bug/error role — genuinely complete, not just blocked

This one **did** reach a real conclusion without needing Linear at all:

- Checked `mcp__Vercel__get_runtime_errors` for project `prj_P1V3fzfZ1QwZcVvUNHzdq1DQRtGt` (resume-website), team `team_P5vgMhFNfh2d4fCe2YkRLjey`, window `since: "24h"` (checked 2026-09-21).
- Result: **"No runtime errors found in the selected time range."** Zero grouped error clusters.
- Per `agents/bug-error.md` step 8 ("If the site is clean, create nothing"), this role's cycle is done — clean, nothing to file, no Linear access was even needed to reach that conclusion. No further action needed for bug-error this cycle.

### Spec-drift role — steps 1–3 done, steps 4–11 blocked

Read `openspec/project.md` and every file under `openspec/specs/` (about,
contact, design-system, hero, journey, site-meta, voice-agent) plus every
**active (non-archived) change proposal** under `openspec/changes/` in the
resume-website repo. Seven change proposals are currently active — i.e.
already planned, already presumably tracked as Linear issues (`project.md`
references SHA-11 through SHA-14 and SHA-173 by name), and **should not be
re-proposed as "new" spec-drift gaps** without first confirming their Linear
status:

| Change folder | What it's for | Referenced issue (per `project.md`) |
|---|---|---|
| `fix-mobile-voice-audio` | iOS/Android TTS silent-audio bug (AudioContext suspend) | — |
| `journey-chapter-scrubber` | Fixed chapter scrubber for desktop pinned Journey scroll | — |
| `mobile-qa-pass` | Mobile layout/voice-agent QA across Hero/Journey/About/voice agent | SHA-12 |
| `save-contact-vcard` | "Save Contact" pill → `.vcf` download | — |
| `social-share-preview` | OG/Twitter meta tags + dynamic OG image | SHA-173 (site-meta) |
| `suggested-prompt-chips` | Tappable suggested-question chips above voice bar | — |
| `warmer-chatbot-avatar` | Softer/warmer voice-agent avatar face | — |

`project.md`'s own capability table also separately flags two **pending**
items with known issue numbers, independent of the folders above: Cal.com
booking button for Contact (SHA-14) and emoji scroll-morph for the design
system (SHA-13).

**What's still needed from steps 4–11** (all require Linear):
- Search the Resume Website Linear project for each of the 7 folders above (and SHA-11–14/173) to confirm they're still open and not stale — do **not** re-file any of them as new gaps.
- Beyond these 7, I did not find any additional planned-but-unbuilt gap between `openspec/specs/` and the current codebase worth a fresh issue — the spec tree is otherwise consistent with what's live per `CLAUDE.md`/`SPEC.md`. So there is likely **nothing new** for spec-drift to file this cycle beyond confirming the above — but the Issue Cap pre-flight (step 0) and the search-before-file step (step 4) still need to run for real before that's certain.
- Step 10 (stale-issue sweep — cross-check open Backlog issues against the current codebase, comment on up to 3 that look already resolved) needs Linear read+comment access; not attempted.
- Steps 11–12 (preview-branch cleanup, openspec archive sweep): **do not re-investigate** — this is the same, extensively-documented standing blocker (`LINEAR_API_KEY` repo secret missing + proxy blocks mutating git pushes) already confirmed independently 7 times in `handovers/preview-branch-cleanup-linear-api-key.md`. That file states re-verifying again "wastes tokens with no new information." Skipped for that reason, not because this session didn't try.

### Market-feature role — vision read, but no proposals filed (by design)

Read `openspec/project.md`'s vision, non-negotiables, and Out of Scope
section (no blog/CMS, no auth, no contact form, no multi-language). Given
that Resume Website already has **7 active change proposals** covering a
wide swath of near-term differentiation ideas (voice UX polish, mobile QA,
social sharing, contact convenience, avatar warmth), and given this role's
explicit guardrail — *"Search the target Linear project first; skip anything
already proposed or tracked, including things filed by the spec-drift
agent"* — this session deliberately did **not** invent or propose new
features. Doing so without any way to check Linear risks filing a duplicate
of something already tracked, which is exactly the failure mode the
guardrail exists to prevent. Left for the receiving agent to run steps 3–9
fresh once Linear access exists (their research context: the 7 folders above
are the current frontier of "not yet built"; anything beyond that is fair
game for a genuinely new proposal, capped at 3 issues, always with a visual).

## Issue Cap pre-flight — not run

Could not run `agents/shared/issue-cap.md`'s count (needs `list_issues`
filtered by Linear Project ID `b01a99ac-46a3-4b00-9139-31e00fae781d`, i.e.
Resume Website). The receiving agent must run this once, per that module,
before filing anything from spec-drift or market-feature.

## Sweep ledger

**Deliberately not appended to `data/sweep-runs.jsonl`.** The ledger schema
(`{"filed": {...}, "clean": bool}`) is meant for a run that actually reached
a real outcome (found real gaps and filed, or genuinely found nothing across
all three roles). This run didn't reach either state for two of three roles
— it was blocked, not clean — and a `clean: true` or a bare 0/0 line would
misrepresent that in the dashboard. Once the receiving agent finishes
spec-drift + market-feature for real, they should append the ledger line
for this cycle themselves with the real outcome.

## Instructions for receiving agent

1. Get Linear MCP access (ask Sharad to authorize the connector if working
   non-interactively).
2. Run the Issue Cap pre-flight for Resume Website (Linear Project ID
   `b01a99ac-46a3-4b00-9139-31e00fae781d`) per `agents/shared/issue-cap.md`.
3. If under cap: search Linear for each of the 7 openspec change folders
   listed above (and SHA-11/12/13/14/173) to confirm none need re-filing,
   then decide if spec-drift has anything genuinely new to file (this
   session found nothing beyond those 7). Run spec-drift step 10 (stale-issue
   sweep) and steps 11–12 (skip re-verifying the LINEAR_API_KEY blocker —
   see `handovers/preview-branch-cleanup-linear-api-key.md`).
4. If under cap: run market-feature steps 3–9 fresh (vision already read,
   summarized above).
5. Bug-error is done for this cycle — no action needed (confirmed clean via
   Vercel, see above). No need to re-check Vercel logs again this same
   cycle.
6. Append the real ledger line to `data/sweep-runs.jsonl` once spec-drift and
   market-feature actually conclude.
7. Delete this handover file once steps 2–4 are complete and tracked in
   Linear — until then, it's the source of truth for what's already been
   researched.
