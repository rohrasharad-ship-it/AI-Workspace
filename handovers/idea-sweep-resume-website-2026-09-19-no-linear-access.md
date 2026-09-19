# Handover: idea-sweep (Resume Website) — research done, nothing filed, no Linear access this session

**For:** Any agent with Linear MCP access (or a valid `LINEAR_API_KEY`)
**From:** Claude Code idea-sweep session, Resume Website, 2026-09-19
**Blocked by:** This session has no Linear MCP tools at all (not just no push access — the
`Linear` MCP server is listed as "requires authentication before its tools can be used," and
this is a non-interactive scheduled run, so the OAuth flow can't be completed here). No
`LINEAR_API_KEY` env var either. So the Issue Cap pre-flight, Linear dedupe search, issue
creation, comments, and the spec-drift stale-issue sweep (step 10) could not run at all —
this is a harder blocker than the long-standing `LINEAR_API_KEY`-for-scripts issue tracked in
`handovers/preview-branch-cleanup-linear-api-key.md` (that one still had Linear MCP for
reading/creating, just not git push for branch deletion).

Also hit, separately: this session's outbound HTTPS is blocked by organization policy for
**all** external domains (confirmed via `curl -sSI https://www.google.com` and
`https://meet-sharad.vercel.app` both returning a 403 CONNECT rejection from the proxy, not a
site-specific block) — see the agent-proxy status output referenced below. That means the
mandatory live-site screenshots (Visual Self-QA, `agents/shared/visual-self-qa.md`) could not
be captured this run either. Per that module's "Network-policy fallback" section, this is
recorded here rather than skipped silently or faked.

**Action:** Check the Issue Cap for Resume Website (Linear Project ID
`b01a99ac-46a3-4b00-9139-31e00fae781d`, see `agents/shared/issue-cap.md`), then — if under
cap — create the two market-feature issues below (search Linear for duplicates first; I could
not). Everything needed to file them directly is in this doc; no further research should be
required.

---

## What did run this session (no Linear needed)

1. **openspec archive housekeeping (spec-drift step 12)** — ran
   `scripts/archive-merged-openspec-changes.sh --sweep` against the `resume-website` checkout
   (not AI-Workspace's own openspec — the script is generic and operates on whatever repo's
   `openspec/changes/` is in the working directory when invoked; running it inside
   AI-Workspace as spec-drift.md step 12 literally instructs would only ever touch
   AI-Workspace's own changes, which is very likely not the intent for a per-project routine —
   flagging this as a possible doc bug in `agents/spec-drift.md` step 12, not fixing it myself).
   Result: `warmer-chatbot-avatar`, `save-contact-vcard`, and `suggested-prompt-chips` archived
   (all three were fully merged, complete, and already reflected in the live `openspec/specs/`
   capability files). `journey-chapter-scrubber` and `mobile-qa-pass` are also complete but
   **fail `openspec`'s own delta validation** (malformed `## ADDED/MODIFIED Requirements`
   sections — no parseable `### Requirement:` blocks) even with `--skip-specs`, so they were
   left in place rather than force-archived with `--no-validate`. Someone with time to fix the
   delta headers in those two change folders (or willing to accept `--no-validate`) can finish
   the sweep; not urgent, it's pure bookkeeping. Committed and pushed to
   `resume-website@claude/trusting-ramanujan-gl2ig4` (commit `ab36232`).
   - **Note on `suggested-prompt-chips`:** its tasks.md says complete (6/6, shipped in PR #30),
     but the feature was **later fully reverted** in PR #38 ("weren't earning their spot in the
     UI") along with its openspec section. Archiving it is still correct — `openspec archive`
     is a record that the *proposal's implementation phase* finished, not a live-status
     claim — but worth knowing before anyone re-proposes tappable prompt chips as a "new" idea;
     it was tried and explicitly rejected on product grounds, not left half-done.
2. **spec-drift gap analysis (steps 1–4, read-only)** — read `openspec/project.md`, all 7
   `openspec/specs/*/spec.md` files, and cross-checked against the live codebase (Hero.tsx has
   Download/LinkedIn/GitHub all present; Contact.tsx has email/LinkedIn/vCard/WhatsApp all
   present; `app/opengraph-image.tsx` exists). **No new gap found** — the only two
   pending/unbuilt items mentioned anywhere in the specs (emoji scroll-morph animation,
   design-system spec.md; Cal.com booking button, contact/spec.md) are already explicitly
   tracked as SHA-13 and SHA-14 respectively and correctly say so in the spec text. Per
   `agents/spec-drift.md` step 9 ("if nothing meaningful is found, create nothing"), **no gap
   issues to file.**
3. **bug-error (steps 1–2)** — `mcp__Vercel__get_runtime_errors` for the Resume Website
   project (`prj_P1V3fzfZ1QwZcVvUNHzdq1DQRtGt`, team `team_P5vgMhFNfh2d4fCe2YkRLjey`), 7-day
   window: **no runtime errors found.** Raw runtime-log lines aren't retained that far back on
   this plan (1h/1d retention message), but the pre-aggregated error-cluster table the role
   file calls for is clean. **No bug issues to file.**
4. **market-feature (steps 1–3)** — read `openspec/project.md` vision/non-negotiables/out-of-
   scope, all capability specs, git history of every `openspec/changes/*` (including archived)
   to avoid re-proposing something already tried, and did one light web search for portfolio-
   differentiation ideas (nothing there suggested anything not already covered by this site's
   existing case-study-modal structure). Landed on **2 genuinely new ideas**, not filler — see
   below. Did not force a 3rd to hit the cap.

## What could NOT run (Linear access required)

- Issue Cap pre-flight for Resume Website — **do this first**, see Action above.
- Linear dedupe search for the two ideas below.
- Creating the two issues, or anything from spec-drift/bug-error even though both came back
  clean (nothing to file either way, so this doesn't change).
- spec-drift step 10 (stale-issue sweep / "may already be done" comments on open Backlog
  issues) — entirely skipped, not attempted.
- Attaching the mockups/screenshots to Linear via `prepare_attachment_upload`.

## What could NOT run (network policy — all outbound HTTPS blocked, not just Linear)

- Live screenshot of the current homepage / Currently section for market-feature step 7 —
  `curl -sSI https://meet-sharad.vercel.app/` and even `https://www.google.com` both got a 403
  CONNECT rejection from this session's egress proxy (`curl -sS
  http://127.0.0.1:39053/__agentproxy/status` shows `recentRelayFailures` for both hosts,
  `kind: connect_rejected`, `"gateway answered 403 to CONNECT (policy denial or upstream
  failure)"`). This is a blanket policy block for this session, not a site-specific issue — GitHub
  and Vercel *MCP* tool calls still worked fine (they don't go through this proxy path), only
  raw outbound HTTPS (curl, Playwright) is affected.
- Per `agents/shared/visual-self-qa.md`'s documented fallback: no fabricated/placeholder
  screenshot was attached, nothing was skipped silently. The receiving agent (or Sharad,
  directly on the live URL) should do the real Visual Self-QA screenshot + attach step when
  creating these issues, if their own session has working network access.
- Pushing the two mockups below to a `preview/<issue-id>-v1` branch (visual-specs.md's normal
  mechanism) — skipped for a different reason: there's no real issue ID yet since nothing was
  created in Linear. The mockup HTML is included as plain files instead (see Payload below);
  push each to `preview/<real-issue-id>-v1` once the issue exists, following
  `agents/shared/visual-specs.md` exactly (branch name, delete old iterations, link the file
  path not the bare deployment URL).

---

## Payload — 2 market-feature issues to create

Both are genuinely new (not in any `openspec/changes/` — active or archived — and not close to
`suggested-prompt-chips`, the one prior market-feature-style idea I found in git history, which
was a tap-to-ask affordance, not a data/positioning feature). **Search Linear for these terms
before filing** — I could not: "shipped", "build activity", "commit strip", "audience toggle",
"hiring for", "PM vs builder".

### Issue A

| Field | Value |
|---|---|
| Project | Resume Website |
| Status | Backlog |
| Label | `spec-needed` |
| Assignee | Sharad Rohra |
| Priority | Low (speculative) |
| Title | `📈 [Feature] "Shipped this week" build-activity strip` |

**Description (Issue Brief):**
```markdown
**In short:** Show real build activity

**Problem:** The "Building" card in Currently just links out to Usercon — visitors have to take "actively shipping" on faith, with no evidence on the page itself.

**Solution:** A small strip near Currently listing the site's own most recent real commits as plain-language "shipped" lines with a days-ago timestamp, generated at build time from git history — no backend, no live API, no new dependency.

**Why:** "AI Systems Builder who ships fast" is the whole pitch of this page — a page that already calls itself a living product demo should be able to prove that claim with its own real commit cadence instead of just stating it.

**What it looks like:** A slim horizontal strip of 3–4 short chips like "Shipped: Journey chapter scrubber · 3 days ago," reading left to right, sitting under or beside the existing Currently section. Mockup: `handovers/idea-sweep-resume-website-2026-09-19/shipped-strip-mockup.html` in AI-Workspace (attach a real screenshot once pushed to a preview branch under this issue's ID).
```

**First-comment execution detail (post after creating):**
```markdown
Checked `openspec/project.md` (Capabilities table) and all 7 capability specs — nothing like
this exists or is proposed anywhere in current or archived `openspec/changes/`. Checked git
log for "build log", "activity strip", "shipped" — no prior attempt. Closest prior
market-feature-style idea in history is `suggested-prompt-chips` (SHA-65, PR #30), which was a
tap-to-ask UI affordance later reverted (PR #38) for being low-value — unrelated concept to
this one (proof-of-work strip, not a chat shortcut), so not a repeat of a rejected idea.

Implementation sketch (not binding, spec-needed only): a small build-time script reads
`git log --oneline -n 5` (or similar) against `main`, formats each subject line + relative
timestamp, and either writes a static JSON the Currently section imports, or runs via a
Next.js build-time data fetch — no runtime API route needed, so no new attack surface and no
new env var.

Mockup (static frame, not built): `handovers/idea-sweep-resume-website-2026-09-19/shipped-strip-mockup.html`
in AI-Workspace, `claude/vibrant-faraday-gl2ig4` branch (or wherever it lands on main). Push it
to `preview/<this-issue-id>-v1` per `agents/shared/visual-specs.md` to get a linkable Vercel
preview, then swap this note for the real link.

Live-screenshot step (market-feature step 7, homepage/Currently context) was not completed —
this session's outbound HTTPS was blocked by organization policy for all external domains, not
specific to this site. Deferred per the network-policy fallback in
`agents/shared/visual-self-qa.md`.
```

### Issue B

| Field | Value |
|---|---|
| Project | Resume Website |
| Status | Backlog |
| Label | `spec-needed` |
| Assignee | Sharad Rohra |
| Priority | Low (speculative) |
| Title | `🎯 [Feature] Audience toggle — Product vs Builder emphasis` |

**Description (Issue Brief):**
```markdown
**In short:** Let visitors pick their lens

**Problem:** The subtitle pitches Sharad as both "Product Manager" and "AI Systems Builder," but every visitor sees the exact same ordering and emphasis regardless of which one they actually came for.

**Solution:** A small 2–3 option pill toggle near the hero subtitle ("Product" / "Builder" / "Both") that reorders which Journey metrics lead and nudges the voice agent's opening line to match — same content, no new page or route.

**Why:** A B2B PM hiring manager and a technical AI-builder recruiter are looking for different proof points in the same story — letting them self-select surfaces the right one first instead of making everyone scroll past the other audience's framing.

**What it looks like:** Two or three small pill buttons under the hero cycling text; selecting one subtly reorders Journey metrics/labels and changes the voice agent's first line, with a soft transition, no reload. Mockup: `handovers/idea-sweep-resume-website-2026-09-19/audience-toggle-mockup.html` in AI-Workspace (attach a real screenshot once pushed to a preview branch under this issue's ID).
```

**First-comment execution detail (post after creating):**
```markdown
Checked `openspec/project.md` and `openspec/specs/hero/spec.md` — no existing or proposed
audience segmentation anywhere. Checked git log for "audience", "toggle", "persona" — no prior
attempt. Respects the Non-Negotiables in `openspec/project.md` (single long-scroll, no new
page/route) and doesn't touch Out of Scope items (no auth, no form).

Implementation sketch (not binding, spec-needed only): client-side state only (no backend) —
a selected mode reorders `lib/content/eras.ts` metric emphasis client-side and passes a short
mode hint into the existing `/api/agent` system-prompt construction so the voice agent's first
line reflects it; falls back to current default ("Both"/neutral) if untouched, so nothing
breaks for a visitor who never interacts with the toggle.

Mockup (static frame, not built): `handovers/idea-sweep-resume-website-2026-09-19/audience-toggle-mockup.html`
in AI-Workspace. Push to `preview/<this-issue-id>-v1` per `agents/shared/visual-specs.md`.

Live-screenshot step not completed this session — see Issue A's comment, same network-policy
blocker, same fallback applied.
```

---

## Instructions for receiving agent

1. Read `agents/shared/issue-cap.md` and check Resume Website's Issue Cap first (Linear
   Project ID `b01a99ac-46a3-4b00-9139-31e00fae781d`). If at/over cap (5), stop — do not file
   either issue this cycle, and don't run spec-drift/bug-error again either (both already came
   back clean this run, see above — no need to repeat that research).
2. If under cap: search Linear for the dedupe terms listed above. If genuinely not tracked,
   create both issues exactly as specified (fields, Issue Brief description, first comment).
3. For each: push its mockup HTML (already written, listed above) to
   `preview/<real-issue-id>-v1` per `agents/shared/visual-specs.md`, get the live preview
   link, and edit it into the issue description's "What it looks like" line and the first
   comment (replacing the raw file path).
4. Take the mandatory live screenshot (`agents/shared/visual-self-qa.md`) of the current
   homepage/Currently section for context and attach it via the signed-upload flow — this
   session couldn't reach the live site at all (network policy), so this step is still fully
   outstanding, not just the Linear-attach part.
5. Do **not** re-run the spec-drift/bug-error research — both are recorded clean above for
   this cycle. Do **not** re-attempt `journey-chapter-scrubber`/`mobile-qa-pass` archiving
   unless you're also going to fix their delta headers or accept `--no-validate` — that's a
   separate, low-priority loose end, not part of this handover's Action.
6. Delete this handover file and the `idea-sweep-resume-website-2026-09-19/` mockup directory
   once both issues are created and their mockups are properly re-hosted on preview branches —
   until then, this is the source of truth for both drafts.

## Sweep ledger entry (already appended to `data/sweep-runs.jsonl`)

```json
{"at":"2026-09-19T23:50:00Z","project":"Resume Website","filed":{"bugs":0,"features":0},"clean":false,"blocked":"no-linear-mcp-access","note":"2 market-feature drafts + spec-drift/bug-error both clean, all pending Linear filing — see handovers/idea-sweep-resume-website-2026-09-19-no-linear-access.md"}
```

`generate-routine-log.mjs` was not run (also needs `LINEAR_API_KEY`, same long-standing gap as
`handovers/preview-branch-cleanup-linear-api-key.md`) — not repeating that investigation here,
it's already fully documented there.
