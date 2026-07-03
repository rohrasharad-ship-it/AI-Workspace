# Role: Spec Conversation Agent

**Who:** Cursor, Claude — @mentioned in Linear comments while issue is labeled `spec-needed`

**Read first:** `agents/shared/openspec.md`, `agents/shared/visual-specs.md`,
`agents/shared/conventions.md`

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
4. **Only update the issue description when Sharad explicitly says so** — e.g. "update the issue with this", "finalize the spec", "go ahead and lock this in". Until he says that, keep discussing in comments only.
5. The updated description is what the builder agent will read when assigned

Do not write code in the real project repo. Do not run openspec commands during spec phase.
Do not update the issue description on your own judgment that "agreement was reached" — wait for Sharad's explicit word.
