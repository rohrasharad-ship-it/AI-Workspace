# Handover: idea-sweep routine for Usercon could not run — Linear MCP entirely unavailable this session

**For:** Any agent whose session has working Linear MCP access
**From:** Claude Code cloud session, idea-sweep routine run for Usercon, 2026-09-21
**Blocked by:** Linear MCP is not connected in this session at all (the harness reports it as "requires authentication before its tools can be used" and no `mcp__Linear__*` tool exists in the tool list) — not the narrower missing-`LINEAR_API_KEY`-secret issue already tracked in `handovers/preview-branch-cleanup-linear-api-key.md`. This is a full loss of every Linear operation: `list_issues`, `search_issues`, `create_issue`, comment, attach.
**Action:** Re-run the `idea-sweep` routine for Usercon (`routines/idea-sweep.md`) from a session with Linear MCP access, starting at the Issue Cap pre-flight. Everything below this line is the research idea-sweep would otherwise have spent tokens re-deriving — reuse it rather than re-reading the repo from scratch.

**Issue:** N/A — this run was triggered by the scheduled `idea-sweep` routine, not by a specific Linear issue.

---

## Payload

### What this session could and could not do

Read-only GitHub MCP access and Vercel MCP access both worked fine. Only Linear was unavailable, which blocks every idea-generation step that matters:

- **Issue Cap pre-flight** (`agents/shared/issue-cap.md`) — could not run. Cap status for Usercon (Linear Project ID `47ebefac-a4f4-4bdd-a382-4506f7e79b6b`) is **unknown** this cycle.
- **spec-drift steps 1–9** (gap-filing) — research below is done, but step 4 (dedupe search against Linear) could not run, so nothing was filed.
- **spec-drift steps 10–11** (stale-issue sweep, preview-branch housekeeping) — could not run; both need Linear issue lookups.
- **spec-drift step 12** (OpenSpec archive housekeeping, AI-Workspace) — ran. `openspec/changes/` in AI-Workspace has no active (non-archived) folders — clean, 0 archived. No blocker here.
- **bug-error** — Vercel side is clean and confirmed (see below), but step 3 (Linear dedupe) and step 4 (create) could not run even if a bug had been found.
- **market-feature** — same shape: research could be done, filing could not.

### Signal worth flagging before anyone files new issues for Usercon

Usercon's `openspec/changes/` directory currently has **24 active (unarchived) change proposals**, most named `sha-<number>-<slug>` (e.g. `sha-204-mobile-tab-nav`, `sha-211-context-node-detail-screen`, `sha-243-context-item-version-history`). That naming convention matches existing Linear issue keys elsewhere in this workspace (per `handovers/preview-branch-cleanup-linear-api-key.md`, `SHA-*` is the issue-key prefix used workspace-wide). This strongly suggests most of what a naive spec-vs-code gap scan would surface for Usercon is **already tracked** — running spec-drift steps 1–9 blind (without the dedupe search) would very likely create duplicates. Whoever picks this up should run the Issue Cap check and a full `list_issues` dedupe pass first; given 24 in-flight change proposals, Usercon may already be at or near the 5-issue active-pipeline cap by itself, independent of anything this session would have proposed.

Full list of active change folders found: `portable-context-packet-export`, `sha-139-detail-missing-fields`, `sha-143-agent-contribution-breakdown`, `sha-179-empty-lifeareas-you`, `sha-180-habit-context-type`, `sha-181-bulk-add-context`, `sha-182-archived-context-purge`, `sha-183-sensitivity-visibility-level`, `sha-184-multi-user-isolation`, `sha-186-login`, `sha-203-stitch-visual-design`, `sha-204-mobile-tab-nav`, `sha-207-context-receipt-panel`, `sha-211-context-node-detail-screen`, `sha-212-you-identity-card`, `sha-213-grouped-settings-screen`, `sha-214-simplified-menu-overlay`, `sha-216-mcp-setup-tutorial-ui`, `sha-220-contextual-manual-rule-input`, `sha-231-restore-archived-context`, `sha-243-context-item-version-history`, `sha-74-pending-review-actions`, `sha-75-context-card-metadata`.

### Vercel / bug-error research (done, reusable)

- Usercon **does** have a live Vercel project despite `projects.md` listing its prod URL as `TBD`: project `usercon` (`prj_MAkmwIEkHssO8BH1DfYLbPTNNKxU`), domains `usercon.vercel.app` / `usercon-rohrasharad-5924s-projects.vercel.app` / `usercon-git-main-rohrasharad-5924s-projects.vercel.app`. Latest deployment `dpl_86SwsmwY3NxfcurDz65GZEM3wbSM` is `READY`/production. No password or SSO protection enabled, so it should be reachable for Playwright visual self-QA in a future run.
- **Fixed `projects.md` in this same commit**: Usercon's Vercel Prod column now reads `usercon.vercel.app` instead of `TBD`, so future bug-error runs don't have to rediscover this.
- `get_runtime_errors` for the Usercon project returned **no runtime errors** in the default lookback window — the prod site is clean as of this run. If bug-error re-runs and still finds nothing, that's consistent, not a regression.

### OpenSpec / spec-drift research (partial — dedupe not done)

- Read `openspec/project.md` in full (Usercon = "user-owned context layer for AI agents"; explicit non-negotiables and Out-of-Scope list are in the file, worth re-reading before proposing anything).
- Read all 8 top-level capability specs under `openspec/specs/`: `context-graph`, `context-review`, `agent-api`, `context-usage-insights`, `context-receipt`, `drive-storage`, `mcp-oauth`, `settings-screen`. A ninth capability, `mobile-shell`, is referenced from `project.md` but its spec currently lives under an active change folder (`openspec/changes/sha-204-mobile-tab-nav/specs/mobile-shell/spec.md`), not yet promoted to `openspec/specs/` — that's expected for an in-flight change, not itself a gap to file.
- Did not attempt to enumerate spec-vs-code gaps beyond this, since without a Linear dedupe pass any candidate would risk duplicating one of the 24 in-flight changes above.

## Instructions for receiving agent

1. Confirm Linear MCP is actually working in your session (a real `list_issues` call, not just tool presence).
2. Run the Issue Cap pre-flight for Usercon (`agents/shared/issue-cap.md`) using Linear Project ID `47ebefac-a4f4-4bdd-a382-4506f7e79b6b` — **not** the display name.
3. If at/over cap: run spec-drift steps 10–11 only (stale-issue sweep + preview-branch housekeeping), skip steps 1–9 and skip bug-error/market-feature, per `routines/idea-sweep.md` pre-flight.
4. If under cap: run spec-drift steps 1–9 (dedupe first against the 24 change folders listed above before proposing anything), then bug-error (Vercel is clean per above — a fresh check is still fine, cheap), then market-feature.
5. Append the sweep ledger line to `data/sweep-runs.jsonl` per `routines/idea-sweep.md` once real filing happens (this session did not append one, since nothing was filed and no cap status is known — appending a `"clean": true` line would be inaccurate when the actual reason was "blocked," not "checked and clean").
6. Delete this handover file once a real idea-sweep run for Usercon completes end-to-end (or once Linear MCP access is confirmed working in a follow-up session, whichever comes first) — until then, it's the record of why this cycle produced no issues.
