# Shared Module: The Issue Description — Spec Text vs. Status Snapshot

Referenced by: `agents/builder.md`, `agents/spec-conversation.md`

Every issue description has two parts, updated under different rules — this
is what lets Sharad get a full picture from the description alone, without
digging through comment history, while still keeping the spec itself from
being rewritten mid-conversation on a whim:

1. **Spec text** — the finalized feature description. Only changes on
   approval (see `agents/spec-conversation.md`). This is what the builder
   reads as "the spec."
2. **Status Snapshot** — a short block pinned at the very top of the
   description, refreshed by whichever agent/role last touched the issue, on
   *every* meaningful turn (spec reply, PR opened, self-QA fix found,
   approval, merge) — not gated on the spec being locked.

```
--- STATUS ---
Phase: <Spec discussion | Building | In Review | Done>
Last update: <date> — <one sentence of what just happened>
PR: <link, or "none yet">
Preview: <link, or "none yet">
--- END STATUS ---
```

Keep it to those four lines — this is a dashboard, not a log. Comments remain
the full history; this block is only ever overwritten with the current
snapshot, never appended to.
