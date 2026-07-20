## Context

The AI-Workspace Vercel project (`prj_iDnY3CHqZIZaId6RTJINJZjZnsMB`) was assigned the production alias `ai-workspace-blond.vercel.app` when created. The shorter `ai-workspace.vercel.app` hostname belongs to a different, unrelated deployment (a generic React app).

## Decision

Use `ai-workspace-blond.vercel.app` as the canonical production sandbox URL everywhere in the registry and specs. Do not attempt to claim `ai-workspace.vercel.app` — it is not under our control.

## Verification

Confirmed via Vercel MCP `get_project` (domains list) and HTTP GET:
- `https://ai-workspace-blond.vercel.app` → 200, "PM OS — Spec Preview Sandbox"
- `https://ai-workspace.vercel.app` → 200, unrelated "React App"
