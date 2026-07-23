# Role: Review & Merge (on approval)

**Who:** Cursor, Claude — whichever agent Sharad @mentions
**Triggered by:** Sharad commenting on the Linear issue while any PR is open

**Read first:** `agents/shared/openspec.md`, `agents/shared/conventions.md`

---

There is no always-on autonomous reviewer, and no auto-merge path — every PR,
regardless of size, waits for Sharad. The open PR simply sits until he
comments. His comment is one of two kinds:

**A. Feedback ("make the button red", "the animation is too fast"):**
1. Every piece of feedback = spec amendment first
2. Run `npx openspec propose "adjustment: [what Sharad said]"`, update `openspec/project.md`
3. Then update the code
4. Push to the **same branch** — PR and Vercel preview auto-refresh
5. Comment on the Linear issue: "Updated — preview refreshed at the same URL"
6. Stop. Wait for the next comment (more feedback, or approval).

**B. Approval ("@<agent> approved", "@<agent> lgtm"):**
1. Confirm checks are green (Vercel build + any CI). If red, say so and stop.
2. Merge the PR
3. Run `npx openspec archive`
4. Move the Linear issue to `Done`
5. Slack: "🚀 [feature] is live. [prod URL]"

**If blocked by missing tools** (e.g. cannot merge because of token scope):
follow the **Blocked-agent handover** section in
`agents/shared/conventions.md`.

**Spillover — gaps noticed while building or reviewing:**
If you notice a gap out of scope for the current issue (missing error state, no
empty state, accessibility, mobile handling), don't block. File a new Linear
issue (`Backlog`, `spec-needed`, title + Issue Brief description — see
`agents/shared/conventions.md` and `agents/shared/issue-brief.md`) and note it in a
comment: "Noticed [gap] — filed SHA-XX separately. Not blocking this." Post
execution detail (spec refs, areas checked) in the first comment on the new
issue, same as idea-generation roles.

**Never:**
- Merge with failing checks
- Merge any PR without an explicit "approved" comment from Sharad — no exceptions for size or type
- Show Sharad code — only preview URLs
- Change code without updating the spec first
