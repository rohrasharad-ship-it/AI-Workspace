# Handover: idea-sweep for Resume Website blocked on Linear MCP access

**For:** Any agent/session with Linear MCP access
**From:** Scheduled `idea-sweep` routine run, Resume Website, 2026-09-22 (cloud session, no Linear MCP connector authorized)
**Blocked by:** The Linear MCP server is not authorized in this session ("requires authentication before its tools can be used"). This is a non-interactive scheduled session, so the OAuth flow that would connect it can't run here.
**Action:** Run the Issue Cap pre-flight, dedupe, and file (or discard) the candidates below for the Resume Website Linear project — then close out this handover.
**Issue:** none yet — nothing could be created without Linear access. This *is* the pre-Linear output of the run.

---

## Why this covers the whole routine, not one step

`routines/idea-sweep.md` was run against **Resume Website**
(`rohrasharad-ship-it/resume-website`, Linear Project ID
`b01a99ac-46a3-4b00-9139-31e00fae781d`) per
`rohrasharad-ship-it/AI-Workspace/routines/idea-sweep.md`. Nearly every
consequential step in all three role files depends on Linear MCP tools:

- Issue Cap pre-flight (`agents/shared/issue-cap.md`) — needs `list_issues`
- Dedup search in each role's step 3/4 — needs Linear search
- Issue creation — needs `save_issue` / create
- spec-drift steps 10–11 (stale-issue sweep, comments) — needs Linear read/comment
- spec-drift step 11 preview-branch housekeeping also needs `LINEAR_API_KEY` for
  `scripts/cleanup-preview-branches.sh` (same underlying gap, different surface —
  see existing handover `handovers/preview-branch-cleanup-linear-api-key.md`)

None of that could run. What follows is everything from each role that
**doesn't** require Linear, done in full, so the receiving agent only needs
to do the Linear-side pre-flight + dedupe + filing, not redo the analysis.

## Payload

### 1. Bug/Error — clean, nothing to file

Checked Vercel runtime errors for the `resume-website` project
(`prj_P1V3fzfZ1QwZcVvUNHzdq1DQRtGt`) over the last 24h via
`get_runtime_errors`: **no runtime errors found.** Per
`agents/bug-error.md` step 8, this role needs nothing filed. No Linear
action needed here at all — this part of the run is actually complete.

### 2. Spec-Drift — 2 candidates, need dedupe + cap check before filing

Read `openspec/project.md` and every file under `openspec/specs/` in
`resume-website` (hero, journey, about, contact, voice-agent, design-system,
site-meta) and compared against the live implementation as documented in the
repo's own `CLAUDE.md` (checked into the repo, kept current per its own
conventions).

**Candidate A — "Currently" section has no OpenSpec capability at all**

- **What I looked at:** `openspec/project.md` Capabilities table (lists only
  Hero, Journey, About, Contact, Voice Agent, Design System, Site Meta) vs.
  `CLAUDE.md`'s page architecture, which renders `Currently` as live section
  04 (`components/sections/Currently.tsx`) between About and Contact — two
  cards ("Reading" placeholder + "Building", the latter linking out to
  Usercon, with its own content documented directly in `Currently.tsx`, not
  a separate content file).
- **Why it looks like a real gap, not a nitpick:** `openspec/shared` reading
  rule (`agents/shared/openspec.md`) has builder/spec-conversation agents
  read `project.md` + only the one relevant capability file for a
  single-issue task. There is no `openspec/specs/currently/spec.md` and no
  row for it — a future agent asked to touch the Currently section has
  nothing to read.
- **Suggested issue:** in short "Document Currently section spec"; problem:
  the live Reading/Building section has no OpenSpec capability file, so
  future agents can't find its spec; solution: add a `currently` capability
  (spec.md + project.md table row) describing the two cards and the Usercon
  link; why: prevents drift/guesswork next time this section changes; no
  visual needed (spec-only, not a UI change) — skip Visual Specs per its own
  "skip entirely for changes with no visual/UI component" carve-out... but
  note the underlying section *is* visual, so use judgment: a screenshot of
  the current Currently section for context is still worth attaching per
  Visual Self-QA once filed.
- Suggested priority: Low–Medium (docs gap, not a functional gap).

**Candidate B — `voice-agent/spec.md` is substantially stale vs. the live build**

- **What I looked at:** `openspec/specs/voice-agent/spec.md` "Technology
  Stack" and "System Prompt" sections vs. `CLAUDE.md`'s "Voice Agent
  Pipeline" and "Environment Variables" sections.
- **Why it looks like a real gap:** the spec file says TTS is ElevenLabs
  (primary) with browser fallback, and the agent model is Groq
  `llama-3.1-8b-instant` answering with a single freeform response. The
  actual live system per `CLAUDE.md` is materially different: Sarvam Bulbul
  is the *primary* TTS provider (ElevenLabs is now the backup, browser
  speech is third), the model is `openai/gpt-oss-20b` with
  `reasoning_effort: "medium"`, and the agent returns an ordered list of
  **segments** (`{say, focus, cite}`) driving a multi-stop "tour" with
  scroll-settle waiting, `PageSpotlight` citation highlighting, and a
  3-turn conversation-history memory (`⌘K`/`Ctrl+K` shortcut too) — none of
  which appear in the spec file at all.
- **Confidence:** high — this is a straight text comparison between the
  spec file and the repo's own current-state doc, not a guess about intent.
- **Suggested issue:** in short "Update voice-agent spec to match build";
  problem: the OpenSpec voice-agent capability describes a TTS
  provider/model/response-shape that's no longer what's running, so a future
  agent editing this capability would work from a wrong mental model;
  solution: rewrite the Technology Stack + System Prompt sections of
  `voice-agent/spec.md` to match the current Sarvam/segments/spotlight/memory
  architecture; why: prevents a real implementation regression next time
  someone touches voice-agent from the spec alone; no visual needed (spec
  text only).
- Suggested priority: Medium (risk of a future agent actively reverting
  working behavior to match the stale spec).

**Dedupe note:** I could not search Linear to confirm these aren't already
tracked. `openspec/changes/` has no active change folder for either topic
(checked: `fix-mobile-voice-audio`, `journey-chapter-scrubber`,
`mobile-qa-pass`, `save-contact-vcard`, `social-share-preview`,
`suggested-prompt-chips`, `warmer-chatbot-avatar` — none overlap). Still
run the mandatory Linear search before filing.

### 3. Market/Feature — 1 speculative candidate, low confidence on novelty

Read `openspec/project.md`'s vision/differentiation framing ("living product
demo," "founder-pitched" voice agent) and cross-checked against the 9
ideas already in flight (`openspec/changes/*` above, plus SHA-13 emoji
scroll-morph and SHA-14 Cal.com booking, both noted as pending directly in
the specs) to avoid re-proposing those.

**Candidate — shareable one-pager per era case study**

- **In short:** Exportable case-study one-pager
- **Problem:** A recruiter who likes one era's story (e.g. Amadeus) has no
  way to save or forward just that Problem/Approach/Trade-off/Outcome
  narrative — they'd have to screenshot the modal.
- **Solution:** A "Save this story" action inside each era's case-study
  modal that generates a clean, single-page PDF or shareable link from the
  same case-study data already structured for the voice agent's fact
  catalog (`lib/content/`).
- **Why:** Differentiates from a static portfolio — the same narrative data
  already exists in a structured form (case studies feed the voice agent
  today per `CLAUDE.md`); this reuses it in a recruiter-forwardable form.
- **Confidence this is genuinely new:** Medium — I could not search Linear
  to rule out something similar already being tracked or previously
  rejected. Verify via Linear search before treating as novel.
- Suggested priority: Low (speculative, per market-feature's own cap-3/Low
  default).

Only one candidate — didn't want to invent filler to hit market-feature's
cap of 3 (its own step 9 says not to).

### 4. Housekeeping (spec-drift steps 10–12) — also blocked

- **Stale-issue sweep (step 10):** needs Linear to list/read/comment on
  Backlog issues — not attempted.
- **Preview-branch cleanup (step 11):** `scripts/cleanup-preview-branches.sh`
  needs `LINEAR_API_KEY` — same underlying gap as
  `handovers/preview-branch-cleanup-linear-api-key.md` (already filed,
  still open as far as this session could tell — it couldn't check Linear
  to confirm). Don't file a duplicate infra issue for this specifically;
  that handover already covers it.
- **OpenSpec archive sweep (step 12):** `scripts/archive-merged-openspec-changes.sh --sweep`
  doesn't need Linear — this *could* have been run, but this session has no
  shell/clone access to AI-Workspace (GitHub-MCP-only cloud session, not a
  local checkout). Flagging so the receiving agent (or the weekly GitHub
  Action `.github/workflows/openspec-archive.yml`) covers it instead of it
  silently being skipped.

## Instructions for receiving agent

1. Read this file in full (payload above has everything already analyzed).
2. Run the Issue Cap pre-flight (`agents/shared/issue-cap.md`) for Resume
   Website (`b01a99ac-46a3-4b00-9139-31e00fae781d`). If at/over cap (5),
   stop — don't file any of the below this cycle.
3. If under cap: search the Resume Website Linear project for each
   candidate above (spec-drift A, spec-drift B, market-feature one-pager).
   Skip any already tracked.
4. File the survivors as Backlog + `spec-needed`, assignee Sharad Rohra,
   Issue Brief format, title with one leading emoji, per each role's own
   file (`agents/spec-drift.md`, `agents/market-feature.md`) — including the
   mandatory first-comment execution detail and Visual Self-QA screenshot
   for each.
5. Optionally run spec-drift steps 10–12 (stale-issue sweep + housekeeping)
   for Resume Website while you have Linear access, since this session
   couldn't.
6. Consider (separately, not blocking the above): whether the recurring gap
   — Linear MCP unavailable to scheduled cloud `idea-sweep` sessions — is
   itself worth a PM OS infra issue. Check first whether
   `handovers/linear-issue-vercel-preview-blocker.md`'s root cause (or a
   Linear issue already filed from it) covers this, since both stem from
   "cloud/scheduled agent sessions lack certain integrations." Don't file
   a duplicate if it's already tracked there.
7. Delete this handover file once the above is done — the candidates will
   live on as Linear issues (or be explicitly rejected), so this file stops
   being the source of truth at that point.

**Do not** implement any of the candidates above — all three are
`spec-needed` for triage only, per the idea-generation routine's guardrails.
