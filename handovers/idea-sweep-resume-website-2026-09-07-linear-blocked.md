# Handover: idea-sweep (Resume Website, 2026-09-07) — no Linear access this session

**For:** Any agent/session with Linear MCP access (or a valid `LINEAR_API_KEY`)
**From:** idea-sweep routine run (spec-drift + bug-error + market-feature), Resume Website, 2026-09-07
**Blocked by:** Linear MCP tool required OAuth authorization not granted to this session, and no `LINEAR_API_KEY` env var was available either — so the Issue Cap pre-flight, Linear dedupe search, issue creation, and issue commenting from `agents/shared/issue-cap.md` / `routines/idea-sweep.md` could not run at all.
**Action:** Run the Issue Cap check for Resume Website (Linear Project ID `b01a99ac-46a3-4b00-9139-31e00fae781d`), then dedupe-search and file the candidate issues below (only the ones the cap allows), post the stale-issue comment candidate, and take the mandatory Playwright screenshots/visual previews per role file before filing.
**Issue:** N/A — this is a scheduled `idea-sweep` routine run, not driven by a single Linear issue.

## What this session could and couldn't do

Repo (`rohrasharad-ship-it/resume-website`) and Vercel MCP were both available, so the
non-Linear parts of all three roles ran for real:

- **spec-drift steps 1–3** (read `openspec/project.md` + all `openspec/specs/*`, compare
  against the actual codebase): done — see findings below. No genuine unbuilt-planned-gap
  issue to file (steps 4–9 correctly produce 0 new issues).
- **spec-drift step 10** (stale-issue sweep): could not run — needs Linear MCP to list/read
  Backlog issues and comments. One candidate found by inference, not verified — see below.
- **spec-drift steps 11–12** (preview-branch cleanup, openspec archive housekeeping): step 11
  needs `LINEAR_API_KEY` (already tracked as a standing blocker in
  `handovers/preview-branch-cleanup-linear-api-key.md` — no new action needed there from this
  run). Step 12 has real, concrete findings this run — see "OpenSpec archive candidates"
  below; blocked on different tooling (no `gh` CLI, no local `openspec` CLI installed), not Linear.
- **bug-error steps 1–2** (Vercel prod runtime errors/logs, last 24h and 7d): done via Vercel
  MCP (`prj_P1V3fzfZ1QwZcVvUNHzdq1DQRtGt`, team `team_P5vgMhFNfh2d4fCe2YkRLjey`) —
  **zero runtime errors** in the last 7 days, all recent deployments `READY` on production.
  Per step 8, a clean site means create nothing. Bug-error needs no further action.
- **market-feature steps 1–3** (read vision, propose up to 3 features): done — 3 candidates
  drafted below, ready for dedupe search + filing.
- **Issue Cap pre-flight:** not run — requires Linear. Whoever picks this up must do it
  first, once, before filing any of the market-feature candidates (spec-drift has nothing to
  file regardless of cap).

## Candidate issues (market-feature) — dedupe-search then file if cap allows

Search the Resume Website Linear project first for anything matching before filing any of
these — none of them should duplicate `suggested-prompt-chips` (still unbuilt, already has
an open `openspec/changes/` proposal — do not re-propose it) or any of the already-shipped
change folders listed below.

### 1. 🧭 Recruiter Mode — 60-second guided tour

**In short:** One-tap fast path for time-pressed recruiters

**Problem:** A recruiter with 30–60 seconds may bounce before scrolling through the full editorial page to reach the Journey highlights and Contact section.

**Solution:** A small pill near the Hero CTA row ("⚡ 60-second tour") that fires the existing voice-agent tour pipeline (segments → `scrollToFocus` → spotlight → speak) through a canned sequence hitting only the highest-signal stops (top Journey metrics, Contact), without requiring a mic tap or a spoken question.

**Why:** Reuses 100% of the already-built tour/spotlight infrastructure (`lib/voice/pageController.ts`, `runTour()`) for a new high-value audience — no new scroll or animation machinery needed.

**What it looks like:** A small accent-bordered pill next to the existing Download Resume / LinkedIn / GitHub row in Hero; tapping it runs the same scroll+spotlight+speak sequence as a voice query, just pre-scripted instead of Groq-generated.

Suggested priority: Medium

### 2. 🗂️ "Paste a JD, check the fit"

**In short:** Job-description fit check via the voice agent

**Problem:** A recruiter has to manually cross-reference their JD against the page themselves — there's no fast way to ask "does Sharad fit THIS specific role."

**Solution:** A small text input under the voice command bar ("Paste a JD, I'll tell you the fit") that sends the pasted text through the existing `/api/agent` pipeline as context for a targeted 2–3 sentence fit answer, spoken and spotlighted exactly like any other tour segment.

**Why:** Turns the voice agent from a novelty into a tool that directly serves the stated goal in `openspec/project.md` ("active PM job search") — and reuses the entire existing agent/tour/TTS pipeline, no new backend surface.

**What it looks like:** A collapsed affordance under the command bar that expands into a textarea + "Check fit" button; answer plays through the same speaking/spotlight UX as a normal question.

**Note for spec conversation:** flag this explicitly against the project's "no contact form" non-negotiable during spec review — this collects no contact info and persists nothing, it's a one-shot utility input, but worth Sharad's explicit sign-off given how close it reads to the banned category.

Suggested priority: Medium

### 3. 📈 "Ship Log" — recently-shipped strip

**In short:** Small on-page changelog of the site's own recent iterations

**Problem:** The site's actual dev loop (OpenSpec proposals → spec conversation → PR → merge, shipping most weeks) is real evidence of product process, but it's completely invisible to a visitor — nothing on the page shows that this portfolio is itself an actively iterated product.

**Solution:** A compact "Latest ships" list (3–5 dated one-liners, e.g. "🎙️ Voice agent conversation memory — Sep 5") near the Currently/Contact section, generated from merged OpenSpec change history rather than hand-maintained.

**Why:** Directly reinforces the stated design philosophy in `openspec/project.md` ("not a traditional portfolio — a living product demo... demonstrates product thinking") with real, verifiable evidence instead of just claiming it in copy.

**What it looks like:** A small DM Mono-labelled list of 3–5 short dated entries in a cream card, sitting near the Currently section.

Suggested priority: Low

## Stale-issue sweep candidate (spec-drift step 10) — unverified, needs Linear to confirm

`openspec/project.md`'s capability table lists Site Meta as **"In progress, see SHA-11"**,
but `openspec/specs/site-meta/spec.md` itself says **"Status: Live — SHA-173"**, and the
actual code (`app/opengraph-image.tsx`, metadata in `app/layout.tsx`) matches everything the
spec describes as shipped. This looks like `project.md`'s capability table just wasn't
updated when site-meta actually shipped under a different issue number (SHA-173, not
SHA-11) — i.e. SHA-11 may already be resolved/superseded and safe to close, or may be a
stale duplicate. Could not verify SHA-11's actual Linear status or check for an existing
"may already be done" comment (30-day dedupe rule in `agents/spec-drift.md` step 10) without
Linear MCP. If SHA-11 is still open, post the standard stale-issue comment template pointing
to `site-meta/spec.md` and `app/opengraph-image.tsx` as evidence; if it's already closed,
also fix `project.md`'s capability table to stop pointing at it. No source with **at least
one Linear-status page seen for reference** issues — this is inferred from spec/code
divergence only, not fetched a Linear detail.

## OpenSpec archive candidates (spec-drift step 12) — blocked on `gh`/`openspec` CLI, not Linear

`scripts/archive-merged-openspec-changes.sh` doesn't need Linear at all (it uses the
`openspec` CLI + `gh search prs`), but this session has neither the `openspec` CLI installed
(`@fission-ai/openspec` is only a devDependency here in AI-Workspace, not installed, and
`resume-website`'s own `package.json` wasn't checked for it either) nor a `gh` binary (this
session's GitHub access is MCP-only per its own operating instructions). Also note the
change folders live in `resume-website/openspec/changes/`, not in AI-Workspace as
`agents/spec-drift.md` step 12 currently states — that instruction may be stale/written
before per-project OpenSpec trees existed; worth a quick correction to that file once
confirmed with Sharad.

Cross-checked each active change folder's proposal against the current `resume-website`
codebase and the "Live" openspec specs — **6 of 7 look fully shipped and archivable**:

| Change folder | Evidence it's shipped |
|---|---|
| `fix-mobile-voice-audio` | `unlockAudioContext()` + mobile audio-unlock-on-tap logic present in `components/VoiceAgent.tsx` |
| `journey-chapter-scrubber` | Matches `JourneyTimelineNav.tsx` exactly as documented Live in `journey/spec.md` (click-to-jump, arrow keys, continuous fill) |
| `mobile-qa-pass` | Referenced as done (SHA-12) in `design-system/spec.md`; Playwright mobile suite exists in `e2e/` |
| `save-contact-vcard` | `app/contact.vcf` route + `lib/contact/vcard.ts` present; matches `contact/spec.md` |
| `social-share-preview` | `app/opengraph-image.tsx` present; matches `site-meta/spec.md` (SHA-173) |
| `warmer-chatbot-avatar` | Smile/cheek-warmth expression code present in `components/VoiceAgent.tsx`; matches `voice-agent/spec.md`'s documented expression |

**Not shipped — leave active:** `suggested-prompt-chips` — no chip component found anywhere
in `components/`; this is a genuinely still-open proposal, not a gap to re-file.

## Instructions for receiving agent

1. Run the Issue Cap pre-flight for Resume Website (`agents/shared/issue-cap.md`, project ID
   `b01a99ac-46a3-4b00-9139-31e00fae781d`) once, before filing anything below.
2. Dedupe-search Linear, then file whichever of the 3 market-feature candidates the cap
   allows, each with the mandatory Playwright screenshot/visual preview and first comment
   per `agents/market-feature.md` steps 5–8.
3. Check SHA-11's current Linear status; if still open and unresolved, post the stale-issue
   comment per `agents/spec-drift.md` step 10 using the evidence above (skip if it already
   has a recent "may already be done" comment).
4. Once `gh`/`openspec` tooling is available, run
   `bash scripts/archive-merged-openspec-changes.sh --sweep` from inside a `resume-website`
   checkout (not AI-Workspace — see correction note above) to archive the 6 shipped change
   folders listed above.
5. Delete this handover file once the above is done and tracked in Linear/git.
