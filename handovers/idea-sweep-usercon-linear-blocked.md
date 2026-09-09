# Handover: idea-sweep routine for Usercon blocked — no Linear MCP access

**For:** Any agent/session with Linear MCP access (create + search issues,
comment, attach files) against the **UserCon** Linear project
**From:** `idea-sweep` routine (orchestrating session), triggered for Usercon,
2026-09-09
**Blocked by:** No Linear MCP server/tools available in this session (listed
as "requires authentication before its tools can be used"), and no
`LINEAR_API_KEY` in the environment either (checked — empty). This blocks
every Linear-dependent step of the routine: the Issue Cap pre-flight count,
the dedupe search, issue creation, first-comment posting, the stale-issue
sweep, and the preview-branch cleanup script (`scripts/cleanup-preview-branches.sh`
also needs `LINEAR_API_KEY`, which is likewise absent).
**Action:** Run the Issue Cap pre-flight for Usercon (Linear Project ID
`47ebefac-a4f4-4bdd-a382-4506f7e79b6b`, per `projects.md`), then file the
candidate issues below (spec-drift + market-feature) if under cap, following
`agents/shared/issue-cap.md` and `agents/shared/issue-brief.md` exactly.
**Issue:** N/A — this is a routine run (`idea-sweep` for Usercon), not tied to
a single pre-existing Linear issue.

---

## What this session *could* do (completed)

Bug-error was **not run**: `projects.md` lists Usercon's Vercel Prod URL as
`TBD`, so there is no production target to read runtime logs/errors from.
This is a separate, pre-existing gap independent of the Linear blocker — see
"Also worth doing" below.

Spec-drift (steps 1–3) and market-feature (steps 1–3) were run read-only
against `rohrasharad-ship-it/Usercon` (openspec/specs, the actual Next.js
codebase under `src/`, and PRD.md/STRATEGY.md for vision). Findings below are
fully drafted in Issue Brief format and ready to file — nothing further needs
research, only Linear execution.

Steps that were **not** attempted because they need Linear regardless of the
above: the Issue Cap count itself (step 0 of every role), the Linear dedupe
search (step 4 of every role), issue creation, first-comment posting, the
stale-issue sweep (spec-drift step 10), and preview-branch/openspec-archive
housekeeping (spec-drift steps 11–12, which need `LINEAR_API_KEY` to run the
scripts even though they live in this repo).

## Payload — candidate issues, ready to file

**Do the Issue Cap check first** (`agents/shared/issue-cap.md`, project ID
`47ebefac-a4f4-4bdd-a382-4506f7e79b6b`). If Usercon is at/over 5 active
pipeline issues, do not file any of the below — skip to "Housekeeping still
needed" instead. If under cap, search Linear for each item's `dedupe_terms`
before filing (some of these may already be tracked; that search could not be
done this session).

Cap allows **5 total for spec-drift** and **3 total for market-feature** —
the 4 spec-drift candidates below are all under that cap already; pick from
the 3 market-feature candidates as space allows if spec-drift issues plus
existing backlog would otherwise push over the 5-active cap. Every issue:
status `Backlog`, label `spec-needed`, assignee Sharad Rohra, per
`agents/shared/conventions.md`.

### Spec-drift candidates (4)

---
**Title:** `🧟 Remove dead legacy prototype from repo root`
**In short:** stale root-level prototype
**Problem:** The repo root still contains a full static prototype (`app.js`,
`index.html`, `styles.css`, `service-worker.js`, `manifest.webmanifest`) left
over from before the Next.js migration.
**Solution:** Remove the root-level prototype files (or move them to a
clearly-labeled `legacy/`/`reference/` folder) now that the Next.js app under
`src/` is the production surface.
**Why:** The dead prototype uses product language that's explicitly banned
(`"Memory"`, a `"General"` life area) per `openspec/project.md`'s
Non-Negotiables, and the `check-product-language.mjs` guardrail only scans
`src/`, so this violation is permanently invisible to CI.
**What it looks like:** A repo root with one clear app, not two competing
implementations with different terminology.
**Priority:** Medium
**First-comment execution detail:** Confirmed by reading `app.js` (root,
hardcoded `CARDS` array, hash routes `#memory`/`#card`/`#profile`) and
`index.html` (root) against `scripts/check-product-language.mjs` (`roots =
["src"]`, blocks `Memory`, `General`, `Domain`, `Node`), and against
`openspec/project.md` Non-Negotiables. `SYSTEM_DESIGN.md` treats the static
prototype as an inert visual reference, but nothing enforces that it stays
inert. Dedupe search terms: `legacy prototype`, `app.js cleanup`, `product
language`, `dead code`, `root cleanup`.

---
**Title:** `📦 Sync context-review spec with shipped context packet export`
**In short:** spec lags shipped code
**Problem:** The portable context packet export feature (copy visible/collection
context as a plain-text packet) is fully built and its own OpenSpec change
has every task checked off, but it was never merged into
`openspec/specs/context-review/spec.md`.
**Solution:** Archive the `portable-context-packet-export` change into the
`context-review` spec so the spec reflects what's actually shipped.
**Why:** `openspec/project.md` states specs are the source of truth for what
exists — right now anyone reading only `openspec/specs/` would not know this
feature exists.
**What it looks like:** `openspec/specs/context-review/spec.md` gains a
section describing the packet export, matching the working "Copy visible
packet" button already in the product.
**Priority:** Medium
**First-comment execution detail:** `openspec/changes/portable-context-packet-export/tasks.md`
shows all task groups checked off. `src/lib/context-packet.ts`
(`formatPortableContextPacket`, `filterPortableContextItems`) and
`src/components/context-workspace.tsx` implement it per the change's own
proposal. Current `openspec/specs/context-review/spec.md` has no mention of
packets/export. Dedupe search terms: `context packet export`, `openspec
archive`, `spec sync`, `context-review spec`.

---
**Title:** `🔓 Document or restrict agent self-approval of pending context`
**In short:** agent self-approval bypass
**Problem:** `approve_context` and `reject_context` are live, callable MCP
tools, but they're missing from `openspec/specs/agent-api/spec.md`'s own
Required Tools list, and the product's stated intent frames approve/reject as
human actions — the whole point of `approval_required` mode is a human
review gate.
**Solution:** Either explicitly document and scope agent-callable
approve/reject in the agent-api spec (e.g. restrict to a different agent than
the writer), or remove agent access to these tools so `approval_required`
can't be self-approved by the same or a colluding agent.
**Why:** This is a review-integrity gap in the core "user reviews context"
pillar of the PRD — an undocumented tool lets a connected agent skip the
human review gate entirely and silently.
**What it looks like:** An MCP client can no longer make an item active
without a human ever seeing it in the review queue — either the tools are
gone for agents, or the spec explicitly says why it's safe.
**Priority:** High
**First-comment execution detail:** `openspec/specs/agent-api/spec.md` §
"Required Tools/Endpoints" lists `add_context, bulk_add_context, list_context,
search_context, read_context, update_context, archive_context,
list_stale_pending, list_life_areas, get_profile_context` — no
approve/reject. `src/lib/context-tools.ts` defines `approve_context`/
`reject_context` (POST `/api/context/[id]/approve` and `/reject`) and
`src/lib/mcp-tool-runtime.ts` executes them with no source-agent restriction.
`DECISIONS.md` frames approve/reject as human actions. Dedupe search terms:
`approve_context`, `reject_context`, `review gate`, `MCP tool surface`,
`self-approval`.

---
**Title:** `🗂 Archive sha-204-mobile-tab-nav so mobile-shell has a real spec file`
**In short:** capability spec misfiled
**Problem:** `openspec/project.md`'s Capabilities list points `mobile-shell`
at a spec file still inside an un-archived change folder
(`openspec/changes/sha-204-mobile-tab-nav/specs/mobile-shell/spec.md`)
instead of `openspec/specs/mobile-shell/spec.md` like the other 8 tracked
capabilities.
**Solution:** Archive `sha-204-mobile-tab-nav` so `openspec/specs/mobile-shell/spec.md`
exists alongside the rest.
**Why:** The canonical specs directory is incomplete relative to what the
project's own index claims is a tracked capability, even though the feature
is shipped and in production.
**What it looks like:** `ls openspec/specs/` shows all 9 capability folders
the project index promises, not 8.
**Priority:** Low
**First-comment execution detail:** `openspec/project.md` Capabilities
section cites the change-folder path directly; `openspec/specs/` has no
`mobile-shell` directory. Shipped code confirms the feature is live:
`src/components/mobile-tab-nav.tsx`, `src/app/(shell)/review/page.tsx`,
`src/components/settings-mobile-header.tsx`,
`src/components/app-menu-overlay.tsx`. Dedupe search terms: `mobile-shell`,
`openspec archive`, `sha-204`, `capability index`.

### Market-feature candidates (3 — cap is 3 for this role; use judgment on how
many fit under the overall 5-active-issue project cap alongside spec-drift)

---
**Title:** `📊 Decision-Gate Digest — narrate cross-vertical reuse`
**In short:** narrative cross-vertical proof
**Problem:** Sharad's own 2-week decision-gate self-test (`STRATEGY.md`)
requires him to *name* concrete cross-vertical reuse events, but today that
evidence sits only as raw log entries in a "Cross-vertical hits" panel he has
to read and interpret himself.
**Solution:** Auto-generate a periodic plain-language digest (e.g. "Your
travel-booking task pulled in your 'sleeps early' preference from Health on
Tuesday") from the existing cross-vertical activity log.
**Why:** It turns Usercon's own success metric into a self-serving feature —
the one proof point a single-vertical agent's memory could never produce on
its own.
**What it looks like:** A "This week, Usercon helped elsewhere" card on the
home surface, written in sentences, not a log table.
**Priority:** Medium
**First-comment execution detail:** Net-new — not in `openspec/specs/`.
Builds on the existing `crossVertical` field already logged per
`openspec/specs/context-receipt/spec.md` and
`src/components/cross-vertical-hits-panel.tsx` (currently a raw list).
Dedupe search terms: `cross-vertical digest`, `decision gate`, `activity
narrative`, `weekly summary`.

---
**Title:** `🌐 Agent Reuse / Portability Score`
**In short:** cross-agent reuse metric
**Problem:** Nothing today measures the actual thesis variable from
`STRATEGY.md` — how many *distinct* agents read the same horizontal fact —
only per-item single-agent read counts exist.
**Solution:** Surface a per-item and per-life-area "read by N distinct
agents" score alongside the existing usage-insight counts.
**Why:** It's a direct instrument of Usercon's stated differentiation
(neutrality × plurality across competing agents), which no single-vendor
memory product can replicate.
**What it looks like:** A small badge like "Read by 2 agents (Claude, Codex)"
next to a preference, distinct from the existing per-agent read count.
**Priority:** Medium
**First-comment execution detail:** Net-new. Extends
`openspec/specs/context-usage-insights/spec.md`'s existing per-agent read
counts (`src/lib/usage-insights.ts`) with a distinct-agent aggregation not
currently computed. Dedupe search terms: `portability score`, `cross-agent
reuse`, `neutrality metric`, `usage insights`.

---
**Title:** `🕰 Context Freshness Signal on Reads`
**In short:** machine-readable staleness metadata
**Problem:** When an agent reads a context item, it gets `updatedAt` but no
signal about whether the fact is still likely trustworthy versus long
unconfirmed.
**Solution:** Attach a computed freshness/confidence indicator to read
responses (`read_context`, `search_context`, `list_context`), derived purely
from existing timestamp and review-state metadata.
**Why:** Makes the read surface smarter without violating Usercon's
zero-maintenance design constraint (from the Notion Life OS failure analysis
in `STRATEGY.md`) — the signal is computed, never hand-maintained.
**What it looks like:** A `freshness: "confirmed_recently" | "aging" |
"stale"` field returned with each item, so a receiving agent can decide
whether to double-check before relying on it.
**Priority:** Low
**First-comment execution detail:** Net-new. Would extend the read path in
`openspec/specs/agent-api/spec.md` / `src/lib/mcp-tool-runtime.ts`; no
freshness/confidence field exists today in `src/lib/context-schema.ts` /
`SYSTEM_DESIGN.md`. Dedupe search terms: `freshness signal`, `confidence
score`, `staleness`, `read metadata`.

## Also worth doing (separate from the Linear blocker)

- **Usercon's Vercel Prod URL is `TBD` in `projects.md`.** The app is
  actually deployed at `usercon.vercel.app` per `HANDOFF.md`/`NEXT.md` in the
  Usercon repo. Update the `projects.md` row so future `bug-error` runs have
  a real target instead of skipping every cycle.
- **Housekeeping still needed regardless of the cap outcome:** the
  stale-issue sweep (spec-drift step 10) and preview-branch/openspec-archive
  cleanup (steps 11–12) all need Linear/`LINEAR_API_KEY` and were not run
  this cycle — worth doing on the same pass that files the issues above.
- **Sweep ledger:** once this handover is acted on, append the resulting
  counts to `data/sweep-runs.jsonl` for Usercon (this session could not,
  since it filed nothing) and run
  `node scripts/generate-routine-log.mjs` to refresh the dashboard.

## Instructions for receiving agent

1. Run the Issue Cap pre-flight for Usercon (project ID
   `47ebefac-a4f4-4bdd-a382-4506f7e79b6b`) per `agents/shared/issue-cap.md`.
2. If at/over cap: file nothing from this handover. Still run the stale-issue
   sweep and preview-branch/openspec-archive housekeeping (they shrink the
   backlog rather than add to it). Skip to step 6.
3. If under cap: for each candidate above, search Linear using its
   `dedupe_terms` first — skip anything already tracked. File the rest as
   Backlog + `spec-needed`, assignee Sharad Rohra, using the Issue Brief text
   given (it's already in the right format — copy directly). Attach a real
   Playwright screenshot per `agents/shared/visual-self-qa.md` and, where the
   candidate has a UI component, a minimal-effort visual preview per
   `agents/shared/visual-specs.md`, then post the first comment with the
   "First-comment execution detail" text given above for that candidate.
4. Update the `projects.md` Vercel Prod field for Usercon to
   `usercon.vercel.app` (see "Also worth doing").
5. Append a line to `data/sweep-runs.jsonl`:
   `{"at":"<ISO8601>","project":"Usercon","filed":{"bugs":0,"features":N},"clean":false}`
   where N = spec-drift + market-feature issues actually filed (features =
   spec-drift + market combined per the routine's own convention; bugs stays
   0 since bug-error did not run — no prod URL was configured at trigger
   time). Then run `node scripts/generate-routine-log.mjs`.
6. Delete this handover file once the above is complete and tracked in
   Linear/git — until then it is the source of truth for this cycle's
   Usercon idea-sweep.
