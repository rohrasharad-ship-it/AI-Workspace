# Project: PM OS (AI-Workspace)

## What This Is
The central instruction hub for Sharad's AI-first product development loop — agent roles, routines, conventions, and integrations that every project repo points to via a thin `AGENTS.md` pointer.

## Tech Stack
- Format: Markdown instruction files (no application runtime)
- Spec layer: OpenSpec (`@fission-ai/openspec`)
- Integrations: Linear (issues), Slack (notifications), Vercel (spec-preview sandbox)
- Hosting: `ai-workspace-blond.vercel.app` — static spec-preview sandbox only, not a product deployment
- Language: N/A (documentation repo)

## Non-Negotiables
- This repo is the **only** place full agent process instructions live — project repos get thin pointers, never full copies
- Every product repo MUST have its own `openspec/` with per-capability specs; this repo now follows the same rule
- Assignment wakes an agent; the `agent-ready` label is the gate — status is never the gate
- `spec-needed` = discuss only, no code; `agent-ready` = build
- Every PR waits for Sharad's explicit "@agent approved" before merge — no auto-merge
- Spec update before code change — always
- Idea-generation roles create `spec-needed` issues only — never `agent-ready`
- New issues: assignee Sharad Rohra, title starts with one emoji, Issue Brief description format
- Visual Self-QA is mandatory for builder and idea-generation roles when applicable

## Out of Scope
- Shipping product features for Resume Website, AI Landscape, or other product repos (those live in their own repos)
- Storing secrets or API keys in this repo (must stay public for agent fetch)
- Auto-merging PRs or moving issues to Done without Sharad's approval
- The "Capture agent" Slack/voice-note → Linear issue feeder (not yet built)
- Duplicating the full ruleset into Cursor Settings or per-project repos

## Capabilities

| Capability | Spec file | What it covers |
|---|---|---|
| Agent dispatch | `openspec/specs/agent-dispatch/spec.md` | `AGENTS.md` router, hub model, role dispatch table |
| Build loop | `openspec/specs/build-loop/spec.md` | Builder and reviewer roles, trigger vs gate, PR → approval → merge flow |
| Spec conversation | `openspec/specs/spec-conversation/spec.md` | Spec-phase discussion on `spec-needed` issues |
| Idea generation | `openspec/specs/idea-generation/spec.md` | Spec-drift, bug-error, and market-feature roles |
| Routines | `openspec/specs/routines/spec.md` | Named routine bundles (`idea-sweep`, orchestration model) |
| Shared conventions | `openspec/specs/shared-conventions/spec.md` | Issue Brief, issue cap, status snapshot, always-apply rules |
| Integrations | `openspec/specs/integrations/spec.md` | Project registry (`projects.md`), Linear → Slack notifications |
| Visual QA | `openspec/specs/visual-qa/spec.md` | Visual specs (previews), visual self-QA (screenshots), preview sandbox |
| Design reference | `openspec/specs/design-reference/spec.md` | UI animation catalog, snippets, copy-paste workflow |
