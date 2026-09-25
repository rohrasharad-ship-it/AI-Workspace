# Handover: idea-sweep for Resume Website could not file — no Linear MCP in this session

**For:** Any agent/session with working Linear MCP access (and, for the mandatory
screenshot step, a Playwright/browser tool)
**From:** idea-sweep routine (spec-drift + bug-error + market-feature), run against
Resume Website, 2026-09-25
**Blocked by:** Linear MCP requires an OAuth flow this session is non-interactive
and cannot run (confirmed via tool search — no `mcp__Linear__*` tools were
available, and the harness explicitly flagged Linear as "requires authentication").
No Playwright/browser tool was available either, so the mandatory Visual
Self-QA screenshot (`agents/shared/visual-self-qa.md`) could not be taken for
any candidate below.
**Action:** Run the Issue Cap pre-flight for Resume Website
(`agents/shared/issue-cap.md`, Linear Project ID
`b01a99ac-46a3-4b00-9139-31e00fae781d`), then decide whether to file the
candidate(s) below — dedupe against Linear first, take a real screenshot per
role file, then file per `agents/shared/issue-brief.md` /
`agents/shared/conventions.md`.
**Issue:** N/A — this is a routine-triggered run (`idea-sweep`), not driven by
a single Linear issue.

---

## What did and didn't run

Per `routines/idea-sweep.md` all three roles were attempted against Resume
Website (repo `rohrasharad-ship-it/resume-website`, prod
`meet-sharad.vercel.app`). GitHub read access and Vercel log access were both
available and used; Linear (search/cap-check/create/comment) and a real
browser/Playwright were not.

### Issue Cap pre-flight — NOT DONE
Could not call `list_issues` — no Linear MCP tool present. **The receiving
agent must run this check first**, before filing anything below, per
`agents/shared/issue-cap.md`. If Resume Website is already at/over 5 active
pipeline issues, skip filing entirely this cycle (spec-drift steps 10–11 —
also skipped here, see below — would still be the only thing allowed to run).

### Bug/error — ran, clean
Called `mcp__Vercel__get_runtime_errors` for the Resume Website project
(`prj_P1V3fzfZ1QwZcVvUNHzdq1DQRtGt`, team `team_P5vgMhFNfh2d4fCe2YkRLjey`) over
the last 7 days. **No runtime errors found.** Per `agents/bug-error.md` step 8,
this role creates nothing — no action needed.

### Spec-drift — steps 1–3 done, 4–9 blocked (Linear), 10–12 blocked (Linear/tools)
Read `openspec/project.md` and every file under `openspec/specs/` in
resume-website, and diffed against the actual codebase (page composition,
component source). One real gap found — see Candidate 1 below. Steps 4 (Linear
dedupe search) through 9 (screenshot/comment) could not run. Steps 10–11
(stale-issue sweep, preview-branch cleanup) need Linear read access and were
skipped. Step 12 (openspec archive sweep,
`scripts/archive-merged-openspec-changes.sh --sweep`) was deliberately **not**
run even though it doesn't strictly need Linear: it shells out to `gh` to check
for open PRs before archiving a completed change, `gh` isn't available in this
session, and the script's own fallback when `gh` is missing is to skip the
open-PR check and archive anyway — that's a real risk of archiving an
in-progress change's spec folder out from under someone. Left for a session
that actually has `gh` (or equivalent open-PR visibility).

### Market/feature — steps 1–3 done (reasoning only, no web search used), 4–9 blocked
Read `openspec/project.md` in full (vision, non-negotiables, Out of Scope).
Two speculative ideas below — **explicitly unverified against Linear**, so
treat them as drafts to sanity-check for dedupe before filing, not
pre-approved.

## Sweep ledger

Deliberately **not** appended to `data/sweep-runs.jsonl` this run. That file's
schema (`{"at","project","filed","clean"}`) has no way to represent "blocked by
tooling" — writing `clean: true` would misrepresent this as "checked, found
nothing" (untrue for spec-drift and market-feature), and `clean: false` with
zero counts would misrepresent it as "checked, found things, chose not to
file" (also untrue). Whoever completes the filing below should append the
real line once counts are final.

---

## Candidate 1 — spec-drift (high confidence, verified against code)

**Finding:** The "Currently" section (`components/sections/Currently.tsx`) —
the Usercon "Building" card, rendered live in production between About and
Contact (`app/page.tsx`) and read by the voice agent's fact catalog per
CLAUDE.md — has **no capability file under `openspec/specs/`**. The
capability index in `openspec/project.md` lists Hero, Journey, About,
Contact, Voice Agent, Design System, and Site Meta only. Contact's own spec
file is also silent on the WhatsApp deep-link chip
(`NEXT_PUBLIC_WHATSAPP_NUMBER` / `wa.me` link) that's already built and live
in `Contact.tsx` — a second, smaller instance of the same pattern (built,
not specced).

This is the reverse of spec-drift's usual direction (specced-but-unbuilt) —
it's built-but-unspecced — so it doesn't cleanly fit "file a Backlog issue for
Sharad to triage" (there's no product decision here, just a docs gap). Recommend
**not** filing this as a Linear issue; instead have any future session with repo
write access add `openspec/specs/currently/spec.md` (documenting the Usercon
card, its manual "Reading" placeholder, and the Building-card update process
already described in CLAUDE.md) and a short WhatsApp-chip addendum to
`openspec/specs/contact/spec.md`, as a direct docs PR — no spec-needed
triage required. Flagging here so it isn't lost, not as an Issue Brief.

**Separate, smaller observation (also doc-only, also not filed):**
`openspec/specs/voice-agent/spec.md`'s "Avatar Photo" section and CLAUDE.md's
Pending Items table both describe a still-pending `avatar.jpeg` headshot for
"the voice agent's 56px circle" — but the same spec file's own "Floating SVG
Avatar" section (and the actual code in `VoiceAgent.tsx`) shows the voice
agent already uses an illustrated SVG face, not a photo. No source file in
the repo references `avatar.jpeg` at all (checked via repo-wide grep) — Hero,
About, and the OG image all use `IMG_3242.jpeg` directly. This pending item
looks abandoned/stale, not actually blocking anything. Worth a direct doc
cleanup (drop the Pending Items row + the dead Avatar Photo section) rather
than a Linear issue.

## Candidate 2 — market-feature (speculative, draft — verify dedupe first)

**In short:** Follow-up prompt chips

**Problem:** After the voice agent answers, a visitor has to think up their own
next question — most people don't know what else Sharad's portfolio can tell
them.

**Solution:** After each answer, show 2–3 tappable follow-up chips (e.g. "Compare
to ISB", "How do I reach him") generated from the same segment/citation data the
agent already produces.

**Why:** The whole pitch of this portfolio is a living AI product demo — a chat
surface that doesn't suggest its own next move is a missed chance to show that
same product instinct, and it directly lowers the effort for a time-pressed
recruiter to keep exploring instead of leaving after one answer.

**What it looks like:** 2–3 small pill buttons under the command bar after a
response finishes speaking, each one a short question; tapping one submits it
exactly like typing/speaking it would.

## Candidate 3 — market-feature (speculative, draft — verify dedupe first)

**In short:** 60-second recruiter mode

**Problem:** A recruiter skimming on their phone between calls may not have
time to ask the voice agent anything — they either scroll past everything or
bounce.

**Solution:** One extra CTA next to the existing mic button that starts a fixed,
short guided tour (under ~60 seconds of speech) hitting only the single highest
metric from each era, ending at Contact.

**Why:** The site is explicitly built for an active PM job search where the
audience is time-pressured recruiters — a zero-typing, zero-thinking "give me
the highlights" path serves that audience more directly than the open-ended
voice agent does today.

**What it looks like:** A second, smaller button beside the mic labeled
something like "60-sec tour" that immediately starts `runTour()` with a
fixed script instead of waiting for a transcript.

---

## Instructions for receiving agent

1. Run the Issue Cap check for Resume Website
   (`agents/shared/issue-cap.md`, project ID
   `b01a99ac-46a3-4b00-9139-31e00fae781d`). If at/over cap, stop — do not file
   anything below this cycle.
2. Candidate 1 (spec-drift): do **not** file as a Linear issue. If you have
   repo write access, open a docs-only PR adding
   `openspec/specs/currently/spec.md`, the WhatsApp addendum to
   `openspec/specs/contact/spec.md`, and the avatar.jpeg cleanup described
   above. If you don't have repo write access either, leave this handover in
   place and note that in your own follow-up.
3. Candidates 2–3 (market-feature): search Linear for anything already
   covering "follow-up prompts", "suggested questions", "recruiter mode", or
   "quick tour" in Resume Website before filing either. If genuinely new,
   file up to these 2 (market-feature's own cap is 3 per run, and bug-error/
   spec-drift are contributing 0 filed issues this cycle) as Backlog +
   `spec-needed`, assignee Sharad Rohra, title starting with one relevant
   emoji, using the Issue Brief text above as the description. Take a real
   Playwright screenshot of the current homepage/voice-agent area per
   `agents/shared/visual-self-qa.md` and attach it (signed-upload flow, never
   base64). Post the mandatory first comment per `agents/shared/issue-brief.md`
   rule 9 (vision/spec references, Linear search terms used, why not a
   duplicate) on each issue you create.
4. Append the real sweep ledger line to `data/sweep-runs.jsonl` once you know
   final filed counts, then run `node scripts/generate-routine-log.mjs`
   (needs `LINEAR_API_KEY`).
5. Delete this handover file once the above is resolved (or superseded by a
   docs PR + whatever Linear issues you filed) — until then it's the source
   of truth for this run.

**Do not** re-run spec-drift/bug-error/market-feature's research steps from
scratch — the findings above already reflect a full read of
`openspec/project.md`, every `openspec/specs/*/spec.md` file, the relevant
component source, and 7 days of Vercel runtime logs for this project.
