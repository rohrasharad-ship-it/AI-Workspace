# Handover: idea-sweep for Resume Website — Linear MCP unavailable this session, candidates ready to file

**For:** Any agent/session with working Linear MCP tool access (create + search issues, comment, attachments)
**From:** idea-sweep routine (spec-drift + bug-error + market-feature), Resume Website, Claude Code (web), 2026-08-31
**Blocked by:** This session's Linear MCP connector was never authorized (system-level notice: "the following MCP servers require authentication before their tools can be used: Linear" — non-interactive session, cannot run the OAuth flow itself). `ToolSearch` for Linear tools returned nothing. This is distinct from the already-tracked `LINEAR_API_KEY` repo-secret blocker in `handovers/preview-branch-cleanup-linear-api-key.md` (that one only affects the shell script / dashboard generation) — this session had **no Linear access of any kind**, so it could not do the Issue Cap pre-flight, dedupe search, issue creation, comments, or the stale-issue sweep. Everything Linear-shaped below is fully investigated and drafted, just not filed.
**Action:** Once Linear MCP access works: (1) run the Issue Cap check for Resume Website (`agents/shared/issue-cap.md`, Linear Project ID `b01a99ac-46a3-4b00-9139-31e00fae781d`) — not yet known this run; (2) dedupe-search each candidate below and file the ones still not tracked; (3) run the stale-issue sweep note on SHA-11 below; (4) attach the visual/context screenshots noted below once network access to the live site is also available (see network note).
**Issue:** N/A — this is a routine sweep run, not a single Linear issue.

## Also blocked: no outbound network access to the live site this session

Separately from Linear, this session's egress proxy denied outbound HTTPS to
`meet-sharad.vercel.app` (and to `www.google.com`) with a `403` policy
denial (`connect_rejected`, confirmed via
`curl -x $HTTPS_PROXY https://meet-sharad.vercel.app/` and via Playwright
with the proxy configured) — an organization policy block for this session,
not a retriable error. Per `agents/shared/visual-self-qa.md`'s network-policy
fallback: no screenshot was fabricated or skipped silently. Vercel's runtime
error/log APIs (MCP, not raw HTTPS) were reachable fine, so the bug-error
role's data source was not affected — only the mandatory live screenshots for
market-feature (and any live-site cross-check for spec-drift) were.

## Payload

### 1. Issue Cap pre-flight — NOT performed

Could not run `list_issues` (no Linear MCP). **The next session must run this
first**, before filing anything below, per `agents/shared/issue-cap.md`
(Linear Project ID `b01a99ac-46a3-4b00-9139-31e00fae781d`, cap 5 active
pipeline issues). If Resume Website is already at/over cap, do not file the
market-feature candidates below this cycle — carry them to the next run
instead of discarding them.

### 2. Spec-drift (steps 1–9) — investigated, nothing new to file

Read `openspec/project.md` and all 7 files under `openspec/specs/` in full,
and cross-checked each against the current codebase (local clone,
`claude/trusting-ramanujan-509oks`). Findings:

- **No new meaningful gaps found.** The two known pending items are already
  tracked and correctly left unbuilt: emoji scroll-morph (design-system spec,
  SHA-13) and Cal.com/Calendly booking button (contact spec, SHA-14) — both
  explicitly say "do not build until resolved" / "blocked on Sharad providing
  the URL." Correctly not re-proposed.
- **In-flight, not a gap:** PR #21 (`cursor/colleague-signal-wall-d002`,
  open, draft, SHA-30 "Colleague Signal Wall") already adds a testimonials
  section to About + updates `about/spec.md` — confirmed via
  `list_pull_requests` on `rohrasharad-ship-it/resume-website`. Nothing to
  file here either.
- **Doc drift (not a code gap — flag, don't file):**
  `openspec/project.md`'s capability table still lists **Site Meta** as "In
  progress, see SHA-11," but `openspec/specs/site-meta/spec.md` says "Live —
  SHA-173," and the code confirms it's fully shipped
  (`app/opengraph-image.tsx` exists, `app/fonts/` has the bundled DM
  Sans/Mono WOFFs, `app/layout.tsx` has `metadataBase` + full `openGraph`/
  `twitter` metadata blocks). The `social-share-preview` openspec change
  folder (proposal for exactly this work) is also still sitting unarchived
  in `openspec/changes/` in this repo, consistent with the work being done
  but not closed out.
  - **Stale-issue sweep candidate:** if SHA-11 is still open in Linear, post
    the standard `🔍 Spec-drift check — this may already be done` comment on
    it (per `agents/spec-drift.md` step 10 template) — evidence: the three
    code locations above.
  - Separately, `openspec/project.md`'s capability table row for Site Meta
    should be hand-corrected to "Live — SHA-173" to match `site-meta/spec.md`
    — small doc fix, not something to route through Linear.
- **Housekeeping steps 11–12: not run.**
  - Step 11 (`scripts/cleanup-preview-branches.sh`) needs `LINEAR_API_KEY` as
    a shell env var — not set this session. This is the same long-standing
    blocker tracked in `handovers/preview-branch-cleanup-linear-api-key.md`
    (7 prior updates) — see that file, not duplicated here.
  - Step 12 (`scripts/archive-merged-openspec-changes.sh --sweep`) could not
    run: `openspec` is in `resume-website/package.json` but **not installed**
    (`node_modules` was empty this session — needs `npm install` first), and
    the script's own open-PR safety check silently degrades to "assume no
    open PR" when `gh` isn't available (confirmed: this session has no `gh`
    CLI, GitHub access is MCP-only), which is unsafe to run blind. Manual
    substitute check via GitHub MCP: the only open PR touching
    `openspec/changes/` is #21 (SHA-30, touches `about/spec.md`, not any
    `openspec/changes/*` folder directly) — so a `--sweep --dry-run` run
    first (after `npm install`) to confirm exactly which change folders are
    `complete` before archiving for real is the safe next step, not
    something this session should guess at.

### 3. Bug-error (steps 1–8) — clean, nothing to file

Checked via Vercel MCP directly against the production project
(`prj_P1V3fzfZ1QwZcVvUNHzdq1DQRtGt`, team `team_P5vgMhFNfh2d4fCe2YkRLjey`):
`get_runtime_errors` for the last 24h returned **no runtime errors**. Did not
need to fall back to raw log scanning. Nothing actionable — correctly filing
nothing per step 8.

### 4. Market-feature (steps 1–9) — 3 candidates drafted, ready to file after dedupe

Read `openspec/project.md`'s vision/non-negotiables/out-of-scope in full.
None of the three below are Out of Scope (no CMS, no auth, no contact form,
no multi-language — none apply). None appear already built in the codebase
(checked: no `@vercel/analytics` dependency, no text-input element in
`components/VoiceAgent.tsx`, no JD-paste flow anywhere in `lib/voice/` or
`app/api/agent/`). **Not yet dedupe-searched against Linear** — do that
before filing. Capped at 3 per `agents/market-feature.md`.

Each is written in the exact Issue Brief format
(`agents/shared/issue-brief.md`) so it can be pasted directly into
`create_issue` once cap + dedupe are cleared. Title emoji chosen per
`agents/shared/conventions.md` (one relevant emoji, not a generic default).

---

#### Candidate A — 💬 Quiet-mode text chat for the voice agent

**In short:** Text chat fallback

**Problem:** The voice agent is mic-only — a recruiter in an open office, on
a call, or who simply doesn't want to talk out loud has no way to ask it
anything.

**Solution:** A typed-input option alongside the mic in the command bar that
sends the same transcript through the existing agent pipeline and shows the
tour as readable text instead of (or alongside) speech.

**Why:** The voice agent is the site's single biggest differentiator, but a
voice-only entry point excludes exactly the audience — recruiters mid-workday
— most likely to actually visit.

**What it looks like:** A small keyboard icon next to the mic in the command
bar toggles a text field; the agent's answer still scrolls/spotlights the
page, but appears as text bubbles near the command bar instead of requiring
audio.

**Suggested priority:** Medium

**First-comment execution detail (post after creating):** Vision check:
`openspec/project.md` doesn't list accessibility/quiet-mode as out of scope.
Spec check: `openspec/specs/voice-agent/spec.md` documents only
SpeechRecognition (STT) and TTS output — no text-input path exists today.
Codebase check: no `<input>`/`<textarea>` in `components/VoiceAgent.tsx`
(grepped `type.*question|text input|textarea` — no matches). Linear dedupe
terms to search before filing: "text chat", "text input", "quiet mode",
"accessibility voice". Visual preview: build per
`agents/shared/visual-specs.md` minimal tier (single static frame showing
the keyboard-icon toggle + text field next to the existing command bar)
before filing, at `previews/<new-issue-id>-v1.html` on branch
`preview/<new-issue-id>-v1`.

---

#### Candidate B — 🎯 Paste-a-JD fit check

**In short:** Paste-a-JD fit check

**Problem:** Recruiters have to read the whole site themselves to work out
whether Sharad fits a specific role they're hiring for.

**Solution:** A "paste a job description" prompt the voice agent can accept,
which then summarizes Sharad's closest-matching experience and metrics
against that JD.

**Why:** Turns the portfolio from a static story into a live tool a recruiter
actually uses inside their own hiring workflow — the kind of sharp,
product-thinking flourish most portfolios never attempt, which is exactly
the site's stated positioning ("a living product demo").

**What it looks like:** A "Check my fit" chip near the voice command bar
opens a paste box; the agent's answer tour highlights the 2–3 most relevant
Journey eras/metrics for that specific JD instead of a generic tour.

**Suggested priority:** Medium

**First-comment execution detail (post after creating):** Vision check:
directly matches `project.md`'s "living product demo" framing and the
existing segmented-tour agent architecture (`app/api/agent/route.ts`,
`lib/voice/pageController.ts`) — this reuses that pipeline rather than
requiring a new one. Spec check: not mentioned anywhere in
`openspec/specs/voice-agent/spec.md`. Codebase check: no JD/job-description
handling anywhere in `lib/voice/` or `app/api/agent/`. Linear dedupe terms:
"JD", "job description", "fit check", "resume match". Visual preview: build
per `agents/shared/visual-specs.md` minimal tier (static frame showing the
"Check my fit" chip + paste box near the command bar) before filing.

---

#### Candidate C — 📈 Live traction ticker

**In short:** Live visit/question ticker

**Problem:** The site calls itself "a living product demo," but once loaded
it shows no actual live product signal — it's fully static.

**Solution:** A small, understated stat (via lightweight analytics) near the
hero or footer — e.g. "X visits this week" or "Y questions asked to the
voice agent."

**Why:** A PM portfolio that visibly tracks its own real usage demonstrates
product instinct more convincingly than any paragraph describing it —
directly reinforces the site's own stated positioning.

**What it looks like:** A small mono-font stat chip, same visual language as
the existing "PM @ Amadeus" / "AI Builder" hero pills, showing a live-ish
number that updates on reload.

**Suggested priority:** Low

**First-comment execution detail (post after creating):** Vision check: not
listed Out of Scope; reinforces the "living product demo" line in
`project.md` directly. Spec check: no analytics/traction mention anywhere in
`openspec/specs/`. Codebase check: `package.json` has no `@vercel/analytics`
or similar dependency; `project.md`'s non-negotiables require a spec proposal
before any new dependency, so flag that explicitly in the issue for whoever
picks it up. Linear dedupe terms: "analytics", "traction", "visit counter",
"live stat". Visual preview: build per `agents/shared/visual-specs.md`
minimal tier (static frame showing the stat chip placement near the hero)
before filing.

---

## Instructions for receiving agent

1. Confirm Linear MCP tool access actually works (`list_issues` against
   `b01a99ac-46a3-4b00-9139-31e00fae781d` should return real data, not an
   auth error).
2. Run the Issue Cap check for Resume Website. If at/over cap, stop — leave
   this handover in place for the next cycle, don't file anything.
3. Dedupe-search each of Candidates A/B/C in the Resume Website Linear
   project using the search terms listed per-candidate above. File only the
   ones not already tracked, using the Issue Brief text verbatim (edit only
   if dedupe reveals overlap with something existing).
4. Post the SHA-11 stale-issue comment (section 2 above) if that issue is
   still open.
5. Build and attach the minimal-tier visual preview for each filed candidate
   (`agents/shared/visual-specs.md`) plus the mandatory live-homepage context
   screenshot (`agents/shared/visual-self-qa.md`) — confirm outbound network
   access to `meet-sharad.vercel.app` works in the new session first; if it's
   still blocked, follow the same network-policy fallback comment shape
   documented in `visual-self-qa.md` rather than skipping silently.
6. Once steps 3–5 are done for all three (filed, skipped-as-duplicate, or
   carried over at cap), delete this handover file.
7. Separately, whenever convenient (not blocking): hand-correct
   `openspec/project.md`'s Site Meta row in `resume-website` to "Live —
   SHA-173," and run `npm install` + `npx openspec list --json` in
   `resume-website` to check whether `social-share-preview` (and any other
   change folder) is `complete` and safe to archive via
   `scripts/archive-merged-openspec-changes.sh --sweep --dry-run` first.

## Sweep ledger

This run is logged as `"clean": false` (real candidates found, not filed —
see `data/sweep-runs.jsonl`, run at 2026-08-31T23:42:21Z) rather than as a
skip, since spec-drift and bug-error genuinely found nothing to file, while
market-feature has 3 real candidates blocked purely on tooling, not on
substance.
