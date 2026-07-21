# Shared Module: The Loop

Referenced by: `agents/builder.md`

## Core Concept: Trigger vs Gate

Two different things, often confused:

- **Trigger** = what *wakes* an agent. Assigning an issue to an agent, or
  @mentioning it in a comment, starts a fresh agent session. This is the only
  way an agent starts working — nothing else wakes it (a plain comment with no
  @mention wakes no one; a status change wakes no one).
- **Gate** = what the woken agent *checks before proceeding*. This is the
  `agent-ready` label. The agent wakes on assignment, then reads the label to
  decide whether to build or refuse.

So the build flow is always: **assignment wakes the agent → the agent checks the
label → builds if `agent-ready`, refuses if `spec-needed`.**

### Why the label, not the status

Linear automatically flips an issue's status to "In Progress" the instant you
assign it to an agent — core to Linear's native agent-assignment feature, not
configurable. By the time an agent's session starts, status has already left
Backlog whether or not the spec is ready. So **status can never be the gate.**

- `spec-needed` — spec not yet approved. Agent refuses to build.
- `agent-ready` — spec approved by Sharad. Agent may build.

Status is cosmetic — it reflects Linear's automation, not a signal agents act on.

## The Loop

```
SPEC PHASE (issue labeled spec-needed — no agent assignment yet)
  Sharad @mentions an agent in a Linear comment: "@cursor what do you think about..."
  Agent replies in comments, refines the spec
  Back-and-forth until Sharad is satisfied
  Agent updates the issue DESCRIPTION only when Sharad explicitly says so
  No code. No branches. No assignment.

BUILD TRIGGER
  Sharad swaps the label from spec-needed to agent-ready, then assigns to an agent
  (assignment wakes the agent; the agent-ready label is what tells it to proceed)

BUILD PHASE
  Agent's first action: check the label, not the status
  If spec-needed → refuse (see agents/builder.md) and stop
  If agent-ready → proceed:
    Clean up any leftover preview/<issue-id>-* branch from the spec phase
    Read full issue: finalized description = spec, comments = context
    Run OpenSpec, implement
    Run the build and the existing test suite — do not open a PR if either fails
    Open PR
    Move issue to In Review IMMEDIATELY — never gated on Vercel or anything else
    Poll for the real Vercel preview URL (not just build success) — up to ~2 min
    Slack as soon as the URL is known: "🔍 [feature] ready. Preview: [URL]. Approve with '@<agent> approved' on [Linear link]"
    (If no URL after ~2 min, post anyway with the PR link — never go silent)
    Once the build finishes, do Visual Self-QA against the real preview; fix and note any issue found
    STOP. The session ends here — nothing watches for approval automatically.
    (No auto-merge, no size-based exception. Every PR waits, always.)

APPROVAL (every PR — no exceptions for size or type)
  Sharad taps the preview URL on his phone, reviews visually
  Either:
    Feedback → comments on the Linear issue (spec change first, then code — see agents/reviewer.md)
    Approved → comments "@<agent> approved" (the @mention re-wakes the agent)
  On approval, the re-woken agent: merges → openspec archive → moves to Done → Slack "🚀 live"
```
