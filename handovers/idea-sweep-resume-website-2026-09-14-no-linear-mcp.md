# Handover: idea-sweep for Resume Website — candidates ready to file, blocked on Linear MCP

**For:** Any agent/session with Linear MCP access
**From:** idea-sweep routine run (spec-drift + bug-error + market-feature), Resume Website, 2026-09-14
**Blocked by:** This session has GitHub MCP + Vercel MCP + local shell/git, but no Linear MCP connector authorized (session-level OAuth not completed) and no `LINEAR_API_KEY` env var. Every idea-generation step that needs Linear (Issue Cap pre-flight, dedupe search, `save_issue`, screenshot attachment, first comment, stale-issue sweep) could not run.
**Action:** Run the Issue Cap pre-flight for Resume Website, then file the candidate issues below (search-dedupe first), then run spec-drift's stale-issue sweep.
**Issue:** N/A — this is a routine-triggered handover (`idea-sweep`), not driven by an existing Linear issue.

---

## What I could and couldn't do this run

Per `agents/shared/conventions.md` → Blocked-agent handover: I did everything this session's tools allow before writing this up.

**Done (no Linear needed):**
- Spec-drift steps 1–3 (read `openspec/specs/`, read code, find gaps) — full breadth read, see candidate below.
- Spec-drift step 12 (OpenSpec archive housekeeping) — ran directly in `resume-website` (see note below on why not AI-Workspace).
- Bug-error steps 1–2 (Vercel runtime errors/logs) — clean, nothing to file.
- Market-feature steps 1–3 (read `project.md` + specs, propose features) — see 3 candidates below.

**Blocked (needs Linear):**
- Issue Cap pre-flight (`agents/shared/issue-cap.md`) — could not count Resume Website's active pipeline issues. **Do this first** before filing anything below — if the project is already at/over 5 active issues, hold all of these for next cycle except spec-drift's own housekeeping (already done).
- Dedupe search against existing Linear issues — the candidates below are deduped only against what's visible in the repo (open PRs, `openspec/changes/`, `CLAUDE.md` Pending Items table), **not** against Linear itself. Search Linear before filing each one.
- `save_issue`, screenshot attachment (`prepare_attachment_upload` → PUT → `create_attachment_from_upload`), first comment with execution detail — none of this ran.
- Spec-drift step 10 (stale-issue sweep / comment on Backlog issues that look resolved) — could not list or comment on issues.

**Not blocked, but explicitly not re-verified — see existing handover:** Spec-drift step 11 (preview-branch cleanup) requires `LINEAR_API_KEY` as a shell env var, which is absent in this session too. `handovers/preview-branch-cleanup-linear-api-key.md` already has 7 independent confirmations of this exact blocker (root cause: proxy blocks mutating git/GitHub REST calls; the real fix is adding the `LINEAR_API_KEY` repo secret so the scheduled GitHub Action, which runs on a real runner, can do the deletes). That file itself says re-verifying is a waste of tokens — I did not re-run the script or duplicate that finding. Nothing new to add there.

### Note on step 12 (OpenSpec archive) — ran in `resume-website`, not `AI-Workspace`

`agents/spec-drift.md` step 12 says completed change folders "live in AI-Workspace." For Resume Website that's not actually true — `resume-website/openspec/changes/` holds its own active changes; `AI-Workspace/openspec/changes/` has none (confirmed via `npx openspec list --json` in both repos). I ran the archive logic in `resume-website` itself since that's where the real files are; running it in AI-Workspace per the literal doc text would have been a silent no-op. Someone should double check whether that doc line is stale for multi-repo projects generally, or whether I'm missing a mechanism that mirrors project changes into AI-Workspace.

Result: archived `warmer-chatbot-avatar`, `suggested-prompt-chips`, `save-contact-vcard` (all tasks complete, no open PR references them — confirmed via `list_pull_requests`/`get_files` on the one open PR, #21, which only touches `components/`, `e2e/`, and `openspec/specs/about/spec.md`, not any `openspec/changes/` folder). Committed and pushed to `claude/trusting-ramanujan-ptqv0w` on `resume-website`.

**Not archived — needs a human/spec fix first:** `mobile-qa-pass` and `journey-chapter-scrubber` are both task-complete but `openspec archive` refuses them with validation errors: their delta spec sections (`## ADDED Requirements` / `## MODIFIED Requirements`) exist but contain no parsed `### Requirement:` blocks, so OpenSpec can't find any deltas to fold into `specs/`. This is a formatting issue in those two change folders, not a content dispute. Small candidate issue, low priority — see below or fix directly (`openspec/changes/mobile-qa-pass/specs/*/spec.md` and `openspec/changes/journey-chapter-scrubber/specs/*/spec.md`, add proper `### Requirement: ...` / `#### Scenario:` blocks, then re-run `npx openspec archive <name> -y --skip-specs`).

---

## Payload — candidate issues to file

All four candidates below are deduped against: open PRs, `openspec/changes/` (active + freshly archived), `CLAUDE.md`'s Pending Items table (avatar upload, project videos, Cal.com link), and the two already-tracked pending items named directly in specs (SHA-14 Cal.com booking, SHA-13 emoji scroll-morph — **do not** re-file either of these, they're already tracked). **Still search Linear by the terms given per candidate before filing** — this session could not.

### Candidate 1 — spec-drift

**Title:** `🔄 Voice Agent spec is stale vs. what's actually shipped`

**In short:** Voice-agent spec outdated

**Problem:** `openspec/specs/voice-agent/spec.md` still describes the original single-response design — ElevenLabs as the (only) TTS provider, agent model `llama-3.1-8b-instant`, no mention of the tour/spotlight system.

**Solution:** Rewrite the capability spec to match what's actually live: multi-segment tours with `focus`/`cite`, Sarvam Bulbul as primary TTS (ElevenLabs backup, browser fallback), the real Groq model, citation-driven spotlighting, and conversation memory.

**Why:** `openspec/project.md` tells any agent picking up a voice-agent issue to read this ONE file, not the whole tree — right now that agent would build against a description of a system that no longer exists (wrong model name, wrong TTS order, missing the entire tour/spotlight/memory layer).

**What it looks like:** An updated `voice-agent/spec.md` whose Technology Stack table and pipeline description match `CLAUDE.md`'s "Voice Agent Pipeline" and "Voice Agent Spotlighting" sections.

**Suggested priority:** Medium — documentation-only, but real risk of a future agent building against a wrong model/provider.

**Dedupe search terms:** "voice agent spec", "voice-agent spec.md", "spec drift voice"

**Evidence for first comment:** `openspec/specs/voice-agent/spec.md` lines 37–48 (Technology Stack table: `ElevenLabs` listed as the synthesis provider, agent model given as `llama-3.1-8b-instant`) vs. `app/api/agent/route.ts:149` (`model: "openai/gpt-oss-20b"`) and `CLAUDE.md`'s "Voice Agent Pipeline" / "Voice Agent Spotlighting" sections (Sarvam Bulbul primary TTS, segments/focus/cite, `runTour()`, `PageSpotlight`, conversation memory — none of which appear in spec.md at all).

---

### Candidate 2 — market-feature

**Title:** `🎯 JD-matched tour mode`

**In short:** Tailor the tour to a job description

**Problem:** Every visitor gets the same generic voice tour regardless of which specific PM role they're evaluating Sharad for, even though the whole site is framed as a living demo for an active job search.

**Solution:** Let a visitor paste or say a short job description into the command bar; the agent picks the 2–3 most relevant eras/facts for that role and closes with a one-line fit summary — reusing the existing multi-segment tour mechanic already built for "compare X and Y" questions.

**Why:** Directly serves the site's own stated positioning (`openspec/project.md`: "a living product demo for an active PM job search") and is a differentiator no static portfolio can match.

**What it looks like:** Visitor says "I'm hiring for a growth PM role" → the agent runs a short 2–3 stop tour hitting the most relevant metrics/projects, ending with a plain-language fit line.

**Suggested priority:** Low — speculative, larger scope than a typical feature.

**Dedupe search terms:** "JD match", "job description tour", "tailored tour"

---

### Candidate 3 — market-feature

**Title:** `🔗 Shareable tour recap link`

**In short:** Let visitors forward a tour recap

**Problem:** A recruiter who has a good voice conversation with the agent has no way to hand what they learned to a colleague except retelling it from memory — the conversation itself disappears when they close the tab.

**Solution:** After a tour finishes, offer a short "share this" link encoding the transcript and the facts it cited (no login, no backend account) that a colleague can open to see the same recap.

**Why:** Turns a single-visitor voice session into something that spreads inside a hiring team — extends the "living product demo" idea past one visit, at low build cost since the transcript and cited facts already exist client-side.

**What it looks like:** A "Share this conversation" button appears once a tour ends; opening the resulting link replays the same Q&A as text (not audio) with the same spotlighted facts.

**Suggested priority:** Low — speculative.

**Dedupe search terms:** "share tour", "share conversation", "recap link"

---

### Candidate 4 — housekeeping (optional, not from an idea-generation role — flag only)

**Title:** `🧹 Two OpenSpec change proposals have malformed delta specs and can't be archived`

**In short:** Fix broken delta specs

**Problem:** `mobile-qa-pass` and `journey-chapter-scrubber` are both fully implemented and task-complete, but their spec deltas have no parsed `### Requirement:` blocks, so `openspec archive` refuses them — they'll sit un-archived forever until someone edits the delta files.

**Solution:** Add proper `### Requirement:` / `#### Scenario:` blocks to each change's `specs/*/spec.md`, then archive normally.

**Why:** Keeps `openspec/changes/` from accumulating dead-but-unarchivable folders that future spec-drift runs re-check every time for no reason.

**What it looks like:** N/A — not a visual/UI issue, no screenshot needed.

**Suggested priority:** Low.

**Dedupe search terms:** "openspec archive", "delta spec validation"

---

## Instructions for receiving agent

1. **Issue Cap pre-flight first** (`agents/shared/issue-cap.md`): count Resume Website's active pipeline issues using Linear Project ID `b01a99ac-46a3-4b00-9139-31e00fae781d` (from `projects.md`), not the display name. If ≥5, stop — do not file any candidate below this cycle (spec-drift's own housekeeping in this run is already done and doesn't count against the cap).
2. If under cap, search Linear for each candidate's dedupe terms above. Skip anything already tracked.
3. File remaining candidates 1–3 as Backlog + `spec-needed`, assignee Sharad Rohra, title exactly as given (leading emoji), description in Issue Brief format as drafted above (Candidates already follow the five-field template from `agents/shared/issue-brief.md` — copy directly). Candidate 4 is optional/lower-stakes; file it too if it's useful, or just fix the two spec files directly instead of filing.
4. Attach a real Playwright screenshot per `agents/shared/visual-self-qa.md` for Candidates 1–3 (mandatory for every issue any idea-generation role creates) via `prepare_attachment_upload` → PUT → `create_attachment_from_upload` — never base64.
5. Post a first comment on each created issue with execution detail per `agents/shared/issue-brief.md` rule 9 — the "Evidence for first comment" text under Candidate 1 is ready to paste; for 2 and 3, note that these are speculative market-feature ideas checked against `openspec/project.md` + `openspec/specs/` and the open-PR/pending-items list, with no equivalent already proposed as of 2026-09-14.
6. Run spec-drift step 10 (stale-issue sweep) for Resume Website — this session could not list or read comments on existing issues at all, so it has never run this cycle.
7. Append a ledger line to `data/sweep-runs.jsonl` once filing is complete, e.g.:
   ```json
   {"at":"<ISO8601-when-you-file>","project":"Resume Website","filed":{"bugs":0,"features":<N filed>},"clean":false}
   ```
   (I did not append one myself yet since the actual filed count isn't known until you run this — see note in my own session's ledger entry, appended separately, which records `filed: 0` for this run since nothing was actually filed here.)
8. Run `node scripts/generate-routine-log.mjs` (needs `LINEAR_API_KEY`) to refresh the dashboard — also blocked in this session, same missing key as the preview-branch-cleanup handover.
9. Delete this handover file once candidates are filed (or explicitly rejected) and the stale-issue sweep has run — until then it's the source of truth for this cycle's Resume Website findings.
