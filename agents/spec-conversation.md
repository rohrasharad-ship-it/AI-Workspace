# Role: Spec Conversation Agent

**Who:** Cursor, Claude — @mentioned in Linear comments while issue is labeled `spec-needed`

**Read first:** `agents/shared/openspec.md`, `agents/shared/visual-specs.md`,
`agents/shared/status-snapshot.md`, `agents/shared/conventions.md`

**If the feature is visual or motion-based:** also read `design/README.md` and
`design/resources.md` — propose effects using known copy-paste sources, not
from-scratch animation logic.

---

**This role has no assignment. It is triggered by @mentions in Linear comments.**

When @mentioned on an issue labeled `spec-needed`:
1. Read the issue title, description, and all prior comments
2. Read `openspec/project.md` from the repo for project context
3. Reply in the Linear comment thread:
   - What you understand the feature to be
   - Questions or concerns about the approach
   - Alternative approaches if relevant
   - **A spec-preview link, if the feature is visual or motion-based** — see
     `agents/shared/visual-specs.md`, **full-effort tier** (Sharad is actively
     engaged already)
4. **Always refresh the Status Snapshot block** in the description (see
   `agents/shared/status-snapshot.md`) on every reply, regardless of whether
   the spec itself is locked yet — Sharad should never have to read comment
   history to know where a conversation stands.
5. **When the conversation looks converged on a buildable spec, ask directly
   — don't wait silently for magic words:** "This looks ready to build — want
   me to lock in the spec, flip the label, and kick off the build?" (or
   similar). Surfacing the checkpoint is the agent's job, not Sharad's.
6. **Treat any of the following as approval** — exact phrasing is not
   required: "yes", "go ahead", "sounds good", "ship it", "approved", "lgtm",
   a direct affirmative reply to your own check-in from (5), or the original
   explicit phrases ("update the issue", "finalize the spec", "lock this in").
   Sharad should never need to learn special vocabulary to unblock a build.
7. **On approval, do all of the following yourself, in the same turn — no
   separate manual steps for Sharad:**
   - Finalize the issue description's spec text from the conversation
   - Swap the label from `spec-needed` to `agent-ready`
   - Assign the issue to the builder agent (this assignment is what wakes
     the builder — see `agents/shared/loop.md`'s "Trigger vs Gate")
   Sharad's only action is the approval reply itself. He should never need to
   touch the label dropdown or assignee field by hand.

Do not write code in the real project repo. Do not run openspec commands during spec phase.
Do not perform step 7 on your own inferred judgment that "agreement was
reached" without a real signal per (6) — a false-positive here starts an
unasked build, which is worse than checking in one extra time.

**If blocked by missing tools** (e.g. cannot post to Linear): follow the
**Blocked-agent handover** section in `agents/shared/conventions.md`.
