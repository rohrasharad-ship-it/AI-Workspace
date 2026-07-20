# Role: Builder Agent

**Who:** Cursor (primary), Claude, Codex
**Triggered by:** Assigned to a Linear issue

**Read first:** `agents/shared/loop.md`, `agents/shared/openspec.md`,
`agents/shared/visual-self-qa.md`, `agents/shared/status-snapshot.md`,
`agents/shared/conventions.md`

**If the issue touches UI, layout, or animation:** also read `design/README.md`
(and `design/workflow.md` when implementing).

---

**FIRST ACTION ON ANY ASSIGNMENT — check the label, never the status:**
Status will already say "In Progress" by the time you read this — that is
Linear's automatic behavior on assignment, not a signal that the spec is ready.
Ignore it. Check labels instead.

**If the issue is labeled `spec-needed` (not `agent-ready`):**
Do not build. Post this comment on the Linear issue and stop:

```
⚠️ Spec not confirmed.

This issue is still labeled spec-needed — the spec hasn't been approved yet.
I can't start building.

Please review and refine the spec with me in the comments below, then:
1. Swap the label from spec-needed to agent-ready
2. Re-assign me (or just comment to ping me again)

I'll start the moment I see the agent-ready label.
```

**If the issue is labeled `agent-ready`:**
1. **Cleanup:** delete any leftover `preview/<issue-id>-*` branch from the spec
   phase (`git push origin --delete preview/<issue-id>-vN`). These are scratch
   demos from the spec-conversation role and must not survive into the build.
2. Read the full Linear issue: the finalized description is the spec, comments are context
3. Ensure OpenSpec is installed: `npm install --save-dev @fission-ai/openspec@latest`
4. Run `npx openspec propose "<issue title>"` (base it on the finalized description)
5. Run `npx openspec apply` — implement
6. **Test proportionally — not a full suite for every change, but never skip
   the build check:**
   - **Always** run the project's build command (e.g. `npm run build`). If it
     fails, fix it before proceeding. This alone catches the worst failure
     mode (site doesn't compile) and costs seconds, not tokens — never skip it.
   - **If** an existing test suite is present in the repo (e.g. `test:qa`) —
     run it **only when the change plausibly touches shared or critical
     surface**: navigation, layout, design-system-level styling, or anything
     used across multiple capabilities. A copy tweak or a single isolated
     component doesn't need the full suite run against it.
   - **Never require a project to have a test suite.** If none exists, the
     build check alone is the gate — do not create a test suite as a
     side-effect of a task, and do not block on its absence.
   - If tests are run and fail, fix them or, if you genuinely cannot, stop and
     flag Sharad on the Linear issue rather than opening a PR with known-failing tests.
7. Open a PR using `.github/pull_request_template.md` — preview per
   `agents/shared/status-snapshot.md` (Vercel URL for UI; `N/A (infra-only —
   verify on GitHub)` for AI-Workspace infra/docs)
8. **Move issue to `In Review` immediately — do this now, not after anything
   below, and as literally the next tool call after the PR is created (before
   drafting the Slack message, before polling Vercel, before anything else).**
   This must never depend on Vercel, screenshots, or anything else succeeding.
   A PR existing is enough to justify this status. If everything after this
   step fails or the session ends unexpectedly, the status change has already
   happened. Also refresh the Status Snapshot block (Phase: In Review, PR
   link) in the same action — see `agents/shared/status-snapshot.md`.
   **This step has been observed being skipped in practice** — do not treat it
   as optional or something to get to eventually; treat it as blocking every
   later step in this list. (See also the native-automation backup in
   `agents/shared/conventions.md`'s Cursor Rules section, which does not
   depend on the agent remembering this at all.)
9. **Get the preview URL as soon as it's knowable — do not wait for the
   build to finish** (for AI-Workspace infra/docs, skip polling and use
   `N/A` immediately):
   - Vercel assigns the preview URL the moment the deployment is *created*,
     not when the build succeeds. Poll the PR's checks / the Vercel bot's PR
     comment every ~10-15 seconds, up to about 2 minutes total, and grab the
     real public `*.vercel.app` URL (not a Vercel dashboard/inspector link
     that requires login) as soon as it appears — even while the check still
     shows pending/building.
   - **Post the Slack message below as soon as you have that URL.** Note "still
     building, give it a minute" in the message if the check hasn't reached
     success yet. Do not hold the message back waiting for full completion.
   - **If you truly cannot get a real preview URL after ~2 minutes of
     polling, do not go silent.** Post to Slack and comment on the Linear
     issue anyway: "PR opened, preview link pending — check directly: [PR URL]."
     Silence is the failure mode to avoid; a slightly late or missing preview
     link is recoverable, no notification at all is not.
   - **Preflight check before claiming "preview ready" — do a quick HEAD
     request on the URL and check where it lands.** If it redirects to
     `vercel.com/sso-api` or any Vercel login page, the deployment is real but
     access-gated (Vercel's "Deployment Protection" setting) — this already
     happened once (see SHA-25) and silently produced a link Sharad couldn't
     actually open. Do not claim the preview is ready in that case; instead
     say so plainly: "Preview exists but appears access-gated — check Vercel
     Deployment Protection settings on this project." Protection should be
     off on both current projects as of July 2026, but this check costs
     nothing and catches it immediately if it's ever re-enabled (e.g. by a
     new project defaulting to it again).
   - **Repo-specific preview expectations** (see `agents/shared/status-snapshot.md`
     for the full table Sharad sees):
     - **Product repos** (resume-website, etc.): branch Vercel URL = real app
       preview. Put it in the status snapshot and PR body.
     - **AI-Workspace infra/docs** (no UI): set snapshot `Preview: N/A` and
       tell Sharad to verify on GitHub — Linear's Preview button will still
       open the sandbox placeholder homepage, which is not the deliverable.
     - Never use a production domain as the preview URL.
10. Once the build actually finishes (not just the URL existing), do **Visual
    Self-QA — mandatory** (see `agents/shared/visual-self-qa.md` for the exact
    mechanism) **unless this is AI-Workspace infra/docs with no UI** — then
    skip screenshots and verify on GitHub instead. Otherwise: screenshot the
    changed area on the real preview URL, desktop and mobile, actually look at
    both, attach both screenshots to the Linear issue.
    - If something looks wrong, fix it, push to the same branch, and post a
      follow-up comment on the Linear issue: "Found and fixed [X] during
      self-QA — preview refreshed at the same URL." Do not re-post to Slack
      for this; the issue comment is enough.
11. **Stop.** This session ends here for every PR, regardless of size — a
    typo fix and a new page both wait the same way. Sharad's `@<agent>
    approved` comment re-wakes an agent to finish the merge (see
    `agents/reviewer.md`). Nothing merges or auto-completes without that
    explicit comment.

**Slack post (every PR, no exceptions — send as soon as the preview URL is known,
or immediately with `N/A` for AI-Workspace infra/docs):**
```
🔍 Ready for your review
Feature: [issue title]
Preview: [Vercel preview URL, or "N/A — verify on GitHub" for infra/docs] ← tap this (note if still building)
What changed: [2 sentences]
Checks: ✅ build passing, tests passing
Approve: comment "@<agent> approved" on [Linear issue URL]
```

**Never:**
- Write any code on an issue labeled `spec-needed` — check the label every time, regardless of status
- Add or remove the `agent-ready` label yourself — only Sharad does that
- Open a PR without first confirming the build succeeds and existing tests pass
- Merge any PR without Sharad's explicit "approved" comment — there is no
  size-based exception, no auto-merge, ever
- Move any issue to `Done` yourself — that only happens as a direct result of
  Sharad's approval (see `agents/reviewer.md`)
- Push directly to main
- Change code without updating the spec first
- Leave a `preview/*` branch alive once you start building
