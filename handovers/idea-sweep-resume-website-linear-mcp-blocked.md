# Handover: idea-sweep (Resume Website) blocked at Issue Cap pre-flight — Linear MCP not authenticated

**For:** Any agent/session with Linear MCP access
**From:** Claude (idea-sweep routine, scheduled trigger, 2026-07-25, non-interactive session)
**Blocked by:** No Linear MCP access this session — the Linear connector requires an interactive OAuth flow (`claude mcp` / `/mcp`) that a non-interactive scheduled session cannot run
**Action:** Run the Issue Cap pre-flight for Resume Website, then dedupe-search and file the surviving candidates below, run the stale-issue comment, and run the two housekeeping scripts — none of which this session could do
**Issue:** N/A — this handover covers a full `idea-sweep` routine run, not one pre-existing Linear issue

---

## Why this exists

The scheduled trigger asked this session to run `routines/idea-sweep.md` for
**Resume Website**. Every load-bearing step of that routine needs Linear:
the mandatory Issue Cap pre-flight (`agents/shared/issue-cap.md`), the
dedupe search before filing, issue creation, first-comment posting, the
stale-issue sweep, and the preview-branch cleanup script (needs
`LINEAR_API_KEY`). This session had `github`, `Vercel`, and `Slack` MCP
access but Linear was unauthenticated and this session cannot complete
OAuth. Per `agents/shared/conventions.md` → "Blocked-agent handover," this
is a hard tool-access wall, not something to route around — so this session
did every part of the routine that does **not** require Linear (research via
GitHub + Vercel, no fabricated Linear actions) and stopped there.

**This will recur on every future scheduled idea-sweep firing** (daily
bug-error, weekly spec-drift/market-feature, across all 5 projects in
`projects.md`) until the Linear MCP connector is re-authorized outside a
scheduled session. Flagging this distinctly in #pm-ops as well, since it's
a structural automation-health issue, not specific to this one project.

---

## What this session verified / did

- **Project resolved:** Resume Website → repo `rohrasharad-ship-it/resume-website`,
  Linear Project ID `b01a99ac-46a3-4b00-9139-31e00fae781d`, Slack `#resume-website`,
  prod `meet-sharad.vercel.app` (Vercel project `prj_P1V3fzfZ1QwZcVvUNHzdq1DQRtGt`,
  team `team_P5vgMhFNfh2d4fCe2YkRLjey`).
- **Bug/error role — ran fully (needed only GitHub + Vercel):** checked
  `mcp__Vercel__get_runtime_errors` for the last 7 days — **zero runtime
  errors**. Nothing to file. This role's output is final, not blocked.
- **Spec-drift role — research only:** read `openspec/project.md` and every
  `openspec/specs/*/spec.md`, cross-checked against the live codebase. See
  candidates below. Steps 4–9 (Linear dedupe search + filing + comment +
  screenshot) NOT done.
- **Market-feature role — research only:** read `openspec/project.md` vision/
  non-negotiables/out-of-scope, proposed 3 candidates. Steps 4–8 (Linear
  dedupe search + filing + comment + screenshot) NOT done.
- **Stale-issue sweep (spec-drift step 10):** could not run at all — requires
  listing/reading open Linear issues. However, while reading `openspec/project.md`'s
  capability table during gap research, this session noticed the **SHA-11**
  reference ("Site Meta — In progress, see SHA-11") looks stale against the
  code — see "Possibly stale" below.
- **Preview-branch housekeeping (spec-drift step 11):** NOT run — the cleanup
  script needs `LINEAR_API_KEY` to check each issue's label/state, which this
  session doesn't have. While listing branches in this repo to create the
  working branch for this handover, this session noticed **~50
  `preview/SHA-*-v*` branches** already exist here, several sharing identical
  commit SHAs (e.g. SHA-50/51/55/56/57 all point at the same commit). Worth a
  priority run of `scripts/cleanup-preview-branches.sh` once Linear access is
  back — this may be a bigger backlog than a normal weekly sweep expects.
- **OpenSpec archive housekeeping (spec-drift step 12):** NOT run — no shell
  environment with the AI-Workspace repo cloned in this session. Unclear
  whether the scheduled GitHub Action backup has been keeping this current;
  worth a manual `--sweep` check.
- **No Linear search, no issue creation, no comments, no attachments, no
  Playwright screenshots were performed or fabricated anywhere in this run.**

---

## Payload: candidates for the receiving agent to triage

**First, mandatory:** run the Issue Cap pre-flight
(`agents/shared/issue-cap.md`) against Linear Project ID
`b01a99ac-46a3-4b00-9139-31e00fae781d` before filing anything below. If at/over
cap (≥5 active pipeline issues), post the skip message to `#resume-website`
and stop — do not file any of the candidates below this cycle.

### Spec-drift candidates (cap 5 — 4 found)

1. **Voice agent never speaks its spec'd Contact closing line**
   - In short: Contact closing line never fires
   - Problem: `contact/spec.md` says the voice agent speaks a closing line when Contact is entered; no scroll/visibility trigger exists anywhere in the code (confirmed: no `IntersectionObserver`, no such trigger in `VoiceAgent.tsx` or `Contact.tsx`).
   - Solution: fire the existing TTS `speak()` pipeline once when `#contact` enters view.
   - Why: most visitors scroll or nav-jump straight to Contact and never trigger any agent behavior there — the spec'd moment simply never happens.
   - What it looks like: avatar/command bar animates and speaks a short sign-off line the first time Contact is visible.
   - Suggested priority: Medium
   - Spec ref: `openspec/specs/contact/spec.md`; code checked: `components/VoiceAgent.tsx`, `components/sections/Contact.tsx`, `lib/voice/pageController.ts`, `app/page.tsx`

2. **Journey's built media/case-study system has no real media**
   - In short: Era media is 100% built, 0% populated
   - Problem: `Era.media` fields (`gifSrc`/`videoSrc`/`posterSrc`) in `lib/content/eras.ts` are unset for all 4 eras, so `EraMediaBox.tsx` always shows "Preview coming soon" instead of the spec'd looping clip, and mobile tap-to-play never exercises.
   - Solution: source/produce short clips per era, wire into `eras.ts`.
   - Why: `journey/spec.md` calls this section "highest craft investment," but its centerpiece never fires for any visitor — `CaseStudyModal.tsx` and `EraMediaBox.tsx` are fully functional but dead weight today.
   - What it looks like: real looping clip per era; tapping opens the already-built Problem/Approach/Trade-off/Outcome modal with real video.
   - Suggested priority: Medium
   - Spec ref: `openspec/specs/journey/spec.md`, `openspec/specs/design-system/spec.md` (mobile table); code checked: `lib/content/eras.ts`, `components/EraMediaBox.tsx`, `components/CaseStudyModal.tsx`, `lib/content/eraCaseStudies.ts`

3. **Voice-agent system prompt contradicts its own spec**
   - In short: spec says ≤3 sentences, deployed prompt says 3–5
   - Problem: `voice-agent/spec.md` documents "under 3 sentences unless asked to elaborate"; `app/api/agent/route.ts`'s actual system prompt says "3-5 sentences... build a mini narrative." They directly disagree.
   - Solution: sync the spec to the real deployed prompt (or vice versa) so future prompt edits don't drift against a wrong baseline.
   - Why: anyone tuning against the spec today would double the intended response length.
   - What it looks like: docs-only fix, no visitor-facing change.
   - Suggested priority: Low
   - Spec ref: `openspec/specs/voice-agent/spec.md`; code checked: `app/api/agent/route.ts`

4. **Spec'd "Avatar Photo" fallback chain doesn't correspond to any code**
   - In short: spec describes a photo avatar that was never built
   - Problem: `voice-agent/spec.md`'s "Avatar Photo" section describes an `avatar.jpeg`/`IMG_3242.jpeg` fallback chain; `VoiceAgent.tsx` actually renders a hand-drawn SVG `FloatingAvatar` exclusively — zero code references `avatar.jpeg`/`avatar.png` anywhere. `CLAUDE.md`'s Pending Items table separately still lists the avatar headshot as "Pending upload," which is misleading since nothing would consume it even if uploaded.
   - Solution: delete the stale "Avatar Photo" section from the spec; correct/close the CLAUDE.md pending row.
   - Why: an actionable-looking pending item that would waste a contributor's time chasing a dead feature.
   - What it looks like: documentation-only cleanup.
   - Suggested priority: Low
   - Spec ref: `openspec/specs/voice-agent/spec.md`, `CLAUDE.md` Pending Items; code checked: `components/VoiceAgent.tsx`, `public/photo/` listing

**Verified still genuinely pending (no action needed, FYI only):** SHA-14
(Cal.com booking button — confirmed absent from `Contact.tsx`), SHA-13 (emoji
scroll-morph — confirmed not built, and the spec explicitly says not yet).

**Possibly stale — needs Linear cross-check, comment don't re-file:**
SHA-11. `openspec/project.md`'s capability table says "Site Meta — In
progress, see SHA-11," but `openspec/specs/site-meta/spec.md` itself is
headed "Status: Live — SHA-173," and the code (`app/layout.tsx` OG/Twitter
meta, `app/opengraph-image.tsx` dynamic image) fully satisfies every spec'd
requirement. This looks done. Per `agents/spec-drift.md` step 10, comment on
SHA-11 with the standard "Spec-drift check — this may already be done"
template (don't file a new issue, don't close it yourself).

### Market-feature candidates (cap 3 — 3 found)

1. **🎯 Voice agent role-fit pitch generator**
   - In short: agent tailors its pitch live per recruiter context
   - Problem: the agent gives the same tour/Q&A to every visitor regardless of the role/company they're evaluating for.
   - Solution: extend the Groq prompt so a spoken cue ("I'm hiring for a Senior PM, AI Products") reframes the next answer around the most relevant era/metric.
   - Why: directly serves the stated vision ("a live voice agent that can... answer recruiter questions") — live personalization per conversation would be genuinely memorable.
   - What it looks like: same command bar; optionally a small state label like "Tailoring for AI Product roles."
   - Suggested priority: Medium
   - Risk notes: low — voice-only input, stays inside the existing voice-agent capability; main risk is Groq 8B prompt reliability holding the sentence-count rule while personalizing.

2. **📊 Self-instrumented "living metrics" badge**
   - In short: a badge showing real live usage stats of the site itself
   - Problem: the site calls itself "a living product demo" but nothing on it proves that with real data.
   - Solution: a small `badge`-type sticker showing aggregate stats (e.g. "1,204 visitors · 89 questions answered").
   - Why: turns Sharad's PM/metrics instinct into visible proof on the page itself.
   - What it looks like: one small sticker near Hero or Contact.
   - Suggested priority: Low
   - Risk notes: needs a lightweight analytics dependency → per Non-Negotiables ("no new dependencies without a spec proposal first") this needs a spec proposal before build, not just a Backlog issue; keep aggregate-only, no per-visitor tracking, to stay clear of anything auth-adjacent.

3. **🛠️ "Behind the Build" auto-generated changelog**
   - In short: read-only feed of recent shipped changes, auto-generated from deploys/commits
   - Problem: the site's spec-driven, agent-assisted build process is invisible to visitors.
   - Solution: a compact, auto-generated strip of recent changes (dates + commit titles), zero manual authoring.
   - Why: makes "living" in "living product demo" literal — proof of shipping velocity is a strong signal to a PM-hiring audience.
   - What it looks like: small collapsed strip, maybe folded into Contact.
   - Suggested priority: Low
   - **Risk notes — highest risk of the three:** an editorial-feeling feed of entries risks reading as a blog, which is explicitly **Out of Scope** in `openspec/project.md`. Only file/build this if it can be framed as strictly auto-generated from deploy metadata with zero freeform text — otherwise raise it as a question to Sharad rather than filing as a straightforward Backlog issue.

---

## Instructions for receiving agent

1. Read `agents/shared/issue-cap.md` and run the Issue Cap pre-flight for
   Resume Website (Linear Project ID `b01a99ac-46a3-4b00-9139-31e00fae781d`).
   If at/over cap, post the skip message to `#resume-website` and stop here.
2. If under cap: for each candidate above, search the Resume Website Linear
   project first and skip anything already tracked (open or recently closed) —
   none of this was pre-checked against Linear.
3. File surviving spec-drift candidates (up to 5) and market-feature
   candidates (up to 3, separate cap) per `agents/shared/conventions.md` New
   Issue Conventions + `agents/shared/issue-brief.md` format: Backlog +
   `spec-needed`, assignee Sharad Rohra, emoji-led title. For the changelog
   idea, apply the Out-of-Scope scrutiny noted above before filing.
4. Attach a visual preview for any issue with a UI component
   (`agents/shared/visual-specs.md`) and a real Playwright screenshot per
   `agents/shared/visual-self-qa.md` — neither was done in this pass.
5. Post the first-comment execution detail on each new issue per
   `agents/shared/issue-brief.md` rule 9 (spec refs/code paths are listed
   above per candidate).
6. Comment on **SHA-11** with the stale-issue-sweep template from
   `agents/spec-drift.md` step 10 (don't file a new issue for it).
7. Once Linear access allows it, run
   `bash scripts/cleanup-preview-branches.sh` (there's a real backlog — see
   above) and `bash scripts/archive-merged-openspec-changes.sh --sweep` in
   AI-Workspace.
8. Post the consolidated Slack summary to `#resume-website` per
   `routines/idea-sweep.md`'s template once steps 1–7 are done.
9. Delete this handover file once everything above is filed/tracked in
   Linear and Slack — until then it's the source of truth for this cycle's
   findings.

**Do not** re-run the GitHub/Vercel research above from scratch — the
candidates in this file are the output of that research; re-verify against
Linear for dedupe, don't redo the codebase/spec reading.
