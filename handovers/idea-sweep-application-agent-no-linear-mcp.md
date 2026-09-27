# Handover: idea-sweep routine blocked — no Linear MCP access (Application Agent)

**For:** Any agent/session with Linear MCP access authorized
**From:** Scheduled `idea-sweep` routine run, Claude (Sonnet 5) cloud session, 2026-09-27
**Blocked by:** Linear MCP server requires OAuth authorization; this session runs
non-interactively (fired by a schedule, no human present) and cannot complete
the OAuth flow. Every Linear tool was reported unavailable for the whole run.
**Action:** Re-run the `idea-sweep` routine for **Application Agent** from a
session where Linear MCP is already authorized (or authorize it, then re-fire
this schedule), following `routines/idea-sweep.md` exactly.
**Issue:** none — this handover is routine-driven, not issue-driven; there is
no Linear issue to link since nothing could be read from or written to Linear.

---

## Payload

The trigger was:

```
Run the "idea-sweep" routine for Application Agent.
Follow rohrasharad-ship-it/AI-Workspace/routines/idea-sweep.md exactly.
```

Project row from `projects.md`:

| Project | Repo | Linear Project | Linear Project ID | Vercel Prod |
|---|---|---|---|---|
| Application Agent | rohrasharad-ship-it/Application-Agent | Application Agent | `7dc5202c-a586-4bed-b2d3-fba10f2dd913` | TBD |

### What blocked every step

All three roles (`spec-drift`, `bug-error`, `market-feature`) — and the
routine's own Issue Cap pre-flight — depend on Linear MCP tools
(`list_issues`, `create_issue`/`save_issue`, comment creation, attachment
upload to an issue). This session's tool list showed Linear as an MCP server
still requiring authorization, with an explicit note that a non-interactive
session cannot run the OAuth flow. No Linear tool call was attempted against
real data as a result — there was nothing to query.

Concretely, this session could not:

1. Run the **Issue Cap pre-flight** (`agents/shared/issue-cap.md`) — cannot
   `list_issues` filtered by Linear Project ID `7dc5202c-a586-4bed-b2d3-fba10f2dd913`
   to count active-pipeline issues.
2. Run **spec-drift** steps 4–5 (dedupe search + file gaps) or steps 10–11
   (stale-issue sweep needs to read/post Linear comments).
3. Run **bug-error** steps 3–4 (dedupe + file) — separately, this role is also
   not fully actionable regardless of Linear: `projects.md` lists Application
   Agent's Vercel Prod as **TBD**, so there is no deployed prod URL/Vercel
   project to pull runtime logs from yet. Worth flagging to Sharad independent
   of the Linear gap.
4. Run **market-feature** steps 4–5 (dedupe + file).

Non-Linear groundwork that *was* available this session (repo read via GitHub
MCP) was intentionally **not** used to pre-draft candidate issues: without
being able to search Linear first, any drafted issue could not be checked
against what's already tracked, which is a hard requirement in
`routines/README.md` ("Search Linear first — skip anything already tracked").
Drafting un-deduped candidates risked a receiving agent filing duplicates
rather than saving it work.

### What was NOT logged

The `data/sweep-runs.jsonl` ledger was **not** appended for this run. Every
existing line in that file records a routine that actually executed against
Linear (either filing something or genuinely confirming a clean backlog).
This run confirmed nothing — it never reached Linear — so a `"clean":true`
line would misrepresent it as a completed sweep and would also inflate the
`sweeps30d` counter that `scripts/generate-routine-log.mjs` computes for the
dashboard. Log the real run (with real filed counts) once this handover's
receiving agent actually executes the routine.

---

## Instructions for receiving agent

1. Confirm Linear MCP is authorized in your session (tool list shows real
   Linear tools, not an auth-required placeholder).
2. Run `routines/idea-sweep.md` for **Application Agent** from step 1 —
   Issue Cap pre-flight, then spec-drift → bug-error → market-feature, in
   order, per the routine file. Nothing from this handover substitutes for
   any of those steps; no partial work was done to build on.
3. For **bug-error** specifically: check whether `projects.md`'s Vercel Prod
   value for Application Agent is still `TBD`. If the project has no
   deployment yet, bug-error has no logs to read this cycle — that's expected,
   not a new blocker; note it in your own run output and skip filing for that
   role rather than treating it as another handover.
4. Append the real `data/sweep-runs.jsonl` line for this run once it
   completes (filed counts or `"clean":true`, per `routines/idea-sweep.md`
   Output section), and run `node scripts/generate-routine-log.mjs` if
   `LINEAR_API_KEY` is available.
5. Delete this handover file once a real idea-sweep run for Application Agent
   has completed and is reflected in the ledger — until then it's the record
   of why the 2026-09-27 scheduled firing produced no Linear activity.

**Do not** treat the absence of new issues from this run as a "clean" signal
about the Application Agent backlog — it means the check never ran.
