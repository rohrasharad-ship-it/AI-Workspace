# Project: Application Agent

## What This Is
A personal, human-in-the-loop career co-pilot that removes manual grind from job
applications — pre-fills and pauses for human review, never auto-submits.

## Tech Stack
- Framework: Python 3.11+
- Integrations: Slack (slack-bolt), Gmail (planned)
- Storage: JSON tracker (local / cloud volume)
- Hosting: Cloud prep + laptop control (TBD)

## Non-Negotiables
- Human-in-the-loop: never auto-submit job applications
- Slack is the two-way control channel
- Fill companion in Slack for v1 (no browser automation for form fill)
- Quality over volume

## Out of Scope
- Mass auto-apply bots
- LinkedIn scraping / automation
- Browser CDP fill-plan playback (deprecated for v1)

## Capabilities
| Capability | Spec file |
|------------|-----------|
| orchestrator | `openspec/specs/orchestrator/spec.md` |
| tracker | `openspec/specs/tracker/spec.md` |
| integrations | `openspec/specs/integrations/spec.md` |
| generation | `openspec/specs/generation/spec.md` |
