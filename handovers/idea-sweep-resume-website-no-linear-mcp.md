# Handover: idea-sweep routine for Resume Website blocked — no Linear MCP tool in this session

**For:** Any agent/session with working Linear MCP access
**From:** idea-sweep routine run (Claude Code cloud session), Resume Website, 2026-09-24
**Blocked by:** No Linear MCP tools available in this session at all — this is not the already-documented `LINEAR_API_KEY` shell-script blocker (see `handovers/preview-branch-cleanup-linear-api-key.md`). The Linear MCP server itself was never connected: `ToolSearch` for Linear tools returns nothing, and the session's own tooling explicitly reports Linear requires an OAuth flow this non-interactive session cannot run.
**Action:** Finish the idea-sweep routine's Linear-dependent steps for Resume Website using the investigative work already done below, once Linear MCP access is available.
**Issue:** N/A — this handover covers the idea-sweep routine run itself, not a single tracked issue.

---

## What I could NOT do (all require Linear MCP)

- Issue Cap pre-flight count for Resume Website (Linear Project ID `b01a99ac-46a3-4b00-9139-31e00fae781d`)
- Search the Resume Website Linear project for existing/duplicate issues
- Create any Backlog issues
- Comment on issues (spec-drift step 10, stale-issue sweep)
- Attach screenshots via `prepare_attachment_upload` → PUT → `create_attachment_from_upload`

## What I COULD do without Linear, and did

### bug-error role (steps 1-2)

Read Vercel production runtime errors for the resume-website project
(`prj_P1V3fzfZ1QwZcVvUNHzdq1DQRtGt`, team `team_P5vgMhFNfh2d4fCe2YkRLjey`) for the
last 24h via `get_runtime_errors`. **Result: zero runtime errors in the window.**
If Linear becomes available soon, re-check the last 24h fresh rather than trusting
this stale window — but as of this run, bug-error would have filed nothing.

### spec-drift role (steps 1-3)

Read `openspec/project.md` and all 7 capability spec files (hero, journey, about,
contact, voice-agent, design-system, site-meta) against the current codebase as
documented in the repo's `CLAUDE.md`. Findings:

1. **`openspec/specs/voice-agent/spec.md` is significantly stale** relative to
   the actual shipped implementation:
   - Spec says the agent model is `llama-3.1-8b-instant`; `CLAUDE.md` says
     `openai/gpt-oss-20b`.
   - Spec says TTS is ElevenLabs only (`/api/tts`); `CLAUDE.md` documents Sarvam
     Bulbul as the primary provider, ElevenLabs as backup, browser
     `speechSynthesis` as last resort.
   - Spec has no mention of the segment/"tour" response format
     (`{segments: [{say, focus, cite}]}`), `scrollToFocus`/`waitForScrollSettle`,
     `PageSpotlight` citation highlighting, conversation memory
     (`historyRef`/`sanitizeHistory`), or the ⌘K/Ctrl+K shortcut — all live per
     `CLAUDE.md`.
   - Spec describes a large illustrated SVG face avatar (120×138px, South Asian
     illustrated face, lip-sync via `AnalyserNode`, eye blink) fixed above the
     command bar; `CLAUDE.md` instead describes a simple 56px photo circle
     avatar (`/public/photo/avatar.jpeg`). Unclear whether the SVG face was
     actually replaced or the spec was just never written for the photo
     version — worth confirming with Sharad before filing anything, since this
     might be the *spec* that's simply wrong/pre-dates a pivot, not a code gap.
   - **Recommendation:** this may be better handled as a direct `openspec`
     spec-sync rewrite of that one capability file than a Backlog Linear issue.
     If a Linear-enabled agent judges otherwise, a candidate issue: `📝 [Docs]
     Voice Agent spec is out of date vs. shipped implementation` (Backlog,
     `spec-needed`, Low/Medium priority — "Why: future agents reading this spec
     get a wrong picture of how the voice agent actually works").
   - **Search Resume Website Linear first** before filing anything — the spec
     tree already cross-references SHA-11, SHA-13, SHA-14 for other known-pending
     items, so this project clearly already tracks drift like this when known;
     it's plausible this is too.

2. **No other meaningful spec-vs-code gaps found.** The three items explicitly
   marked "Pending" across the spec tree (Cal.com/Calendly button in
   `contact/spec.md`, emoji scroll-morph in `design-system/spec.md`, and the
   project demo videos for Impact Analytics/DTU implied by the Journey
   media-box fallback) are all already tied to existing Linear issue IDs
   (SHA-14, SHA-13) or are content Sharad needs to supply himself — **do not
   re-file any of these as new issues.**

Steps 10-12 (stale-issue sweep, preview-branch housekeeping, openspec archive
housekeeping) were **not attempted**: step 10 needs to read/comment on Linear
issues; steps 11-12 need a checkout of AI-Workspace plus `LINEAR_API_KEY`, which
is the separate, already-documented blocker in
`handovers/preview-branch-cleanup-linear-api-key.md`. Net effect this cycle:
nobody ran 10-12 either way.

### market-feature role

**Not attempted.** Every market-feature issue is mandatory-visual (a real
screenshot of the current homepage plus a mockup pushed to a `preview/*`
branch) and still needs a Linear dedupe search before proposing — not worth
speculatively drafting ideas here only to have them re-derived by whoever
actually has Linear access. Whoever picks this up should run market-feature's
steps 1-9 fresh.

## Sweep ledger

**Deliberately did not append to `data/sweep-runs.jsonl`.** The ledger's
`"clean": true` is supposed to mean "all three roles ran and found nothing" —
that isn't what happened: two of three roles never reached their
Linear-dependent steps, and the one gap that was found (voice-agent spec
drift) was never checked against Linear since search wasn't possible. Writing
`clean: true` would misrepresent this run on the dashboard. Whoever completes
this handover should append the real ledger line once the Issue Cap check,
dedupe search, and any filing actually happen.

## Instructions for receiving agent

1. Confirm Linear MCP access actually works (e.g. a `list_issues` call) before
   starting.
2. Do the Issue Cap pre-flight for Resume Website (`agents/shared/issue-cap.md`,
   Linear Project ID `b01a99ac-46a3-4b00-9139-31e00fae781d`).
3. If under cap: re-run bug-error steps 1-2 fresh (don't trust this handover's
   Vercel window if much time has passed) — it filed nothing as of this run.
4. Search Linear for the voice-agent spec-drift finding above; if not already
   tracked and worth a Linear issue rather than a direct spec-sync edit, file it
   per spec-drift steps 4-9.
5. Run market-feature steps 1-9 fresh (not attempted this run).
6. Run spec-drift steps 10-12 — note the `LINEAR_API_KEY` blocker in
   `handovers/preview-branch-cleanup-linear-api-key.md` may still apply to 11-12.
7. Append the real `data/sweep-runs.jsonl` line once actual counts are known,
   then run `node scripts/generate-routine-log.mjs`.
8. Delete this handover file once the above is complete.
