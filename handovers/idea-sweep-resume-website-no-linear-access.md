# Handover: idea-sweep routine for Resume Website could not file/check anything — no Linear access in this session

**For:** Any agent/session with working Linear MCP access (or Sharad, to authorize the Linear connector for scheduled sessions)
**From:** idea-sweep routine run (Claude Code scheduled session), 2026-09-06
**Blocked by:** No Linear MCP tools were available in this session at all (the Linear connector needs interactive OAuth authorization, which a non-interactive scheduled session cannot perform), and no `LINEAR_API_KEY` env var was set either. This is a stricter blocker than the one in `handovers/preview-branch-cleanup-linear-api-key.md` (that one only blocks the housekeeping *script*, which needs an API key; this one blocks the Linear MCP tools directly — there was no Linear tool of any kind to call).
**Action:** Authorize the Linear connector for this account (claude.ai → Settings → Connectors → Linear) so scheduled/automated `idea-sweep` sessions can use Linear MCP tools, then re-run `idea-sweep` for Resume Website from scratch — nothing below was filed, so there's no partial state to reconcile.

## What this blocked, specifically

Per `routines/idea-sweep.md` and `agents/shared/issue-cap.md`, every step that matters requires Linear:
- The Issue Cap pre-flight (`list_issues` filtered by Resume Website's Linear Project ID `b01a99ac-46a3-4b00-9139-31e00fae781d`) — **could not run**, so it's unknown whether Resume Website is at/over the 5-issue active-pipeline cap.
- spec-drift steps 1–9 (gap-filing) — blocked on the cap check above and on Linear dedup search.
- bug-error steps 3–4 (dedup search + issue creation) — blocked, see below for what *was* checked.
- market-feature steps 4–5 (dedup search + issue creation) — blocked.
- spec-drift step 10 (stale-issue sweep / comment on possibly-resolved Backlog issues) — blocked, needs to read/comment on Linear issues.

Because the cap status is unknown, **do not assume Resume Website has headroom** — check the cap first thing on the next run before filing anything.

## What this session *could* still check (no Linear needed) — use this as a head start, don't re-derive it

**Vercel runtime errors (bug-error step 1):** `get_runtime_errors` on project `prj_P1V3fzfZ1QwZcVvUNHzdq1DQRtGt` (team `team_P5vgMhFNfh2d4fCe2YkRLjey`), last 7 days — **zero runtime errors**. Bug-error would likely have filed nothing this cycle even with Linear access, but re-check on the actual run day rather than trusting this as still current.

**Already in-flight OpenSpec changes in `resume-website/openspec/changes/`** (as of this run) — spec-drift and market-feature should **not** re-propose anything overlapping these, they're presumably already tracked as Linear issues:
| Change folder | What it's about |
|---|---|
| `fix-mobile-voice-audio` | iOS/Android TTS audio silent — `MediaElementSource`/`AudioContext` suspend bug |
| `journey-chapter-scrubber` | Journey section needs a way to jump straight to an era instead of scrolling through all four |
| `mobile-qa-pass` (SHA-12) | General mobile layout/voice-agent QA pass — overflow, sticker overlap, scroll issues |
| `save-contact-vcard` | One-tap vCard download in Contact section |
| `social-share-preview` | Missing `og:image`/`og:url` — link previews look unfinished when shared |
| `suggested-prompt-chips` | Tappable suggestion chips so visitors know what to ask the voice agent |
| `warmer-chatbot-avatar` | Voice-agent avatar reads as stern — expression/presence fix, not animation mechanics |

That's 7 of the areas a fresh spec-drift/market-feature pass would most likely land on already spoken for. A dedup search in Linear should confirm each has a live issue before either role proposes something that overlaps.

**Known pending items already documented in `resume-website/CLAUDE.md`** (also likely already tracked, verify in Linear): avatar headshot upload, Impact Analytics/DTU project demo videos, Cal.com/Calendly link for Contact.

## Instructions for receiving agent

1. Confirm Linear MCP tools actually work (a simple `list_issues` call against `b01a99ac-46a3-4b00-9139-31e00fae781d`).
2. Run the Issue Cap pre-flight for Resume Website per `agents/shared/issue-cap.md`. If at/over cap, stop (spec-drift can still do steps 10–11 only).
3. If under cap, run spec-drift → bug-error → market-feature per `routines/idea-sweep.md`, using the table above to skip anything already covered by an active OpenSpec change or a `CLAUDE.md` pending item that's already tracked — search Linear to confirm each before skipping or filing.
4. Re-check Vercel runtime errors fresh rather than trusting the "zero errors" result above if more than a day or two has passed.
5. Append the real sweep-ledger line to `data/sweep-runs.jsonl` once issues are actually filed (or confirmed clean) — the line this session appended for 2026-09-06 records zero filed because nothing *could* be filed, not because nothing was found; don't treat it as a "clean" run.
6. Delete this handover once a Linear-enabled run has completed the Resume Website sweep.
