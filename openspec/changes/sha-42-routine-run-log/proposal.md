## Why

Idea sweeps file issues and post Slack summaries, but there is no single place to verify routine health or see pending bugs vs features across projects. Sharad currently scrolls Slack to answer "did sweeps run?" and "what's still open?"

## What Changes

- Add `routine-log.html` on the PM OS sandbox — pipeline KPI strip + per-project cards (v7 spec layout; no global Recent Runs feed)
- Add `data/routine-log.json` generated from Linear + a lightweight sweep run ledger
- Add `scripts/generate-routine-log.mjs` to refresh JSON (Linear API key via env; runnable in CI or locally)
- Link the dashboard from `index.html`
- Extend `routines/idea-sweep.md` output step to append clean/findings runs to `data/sweep-runs.jsonl`

## Capabilities

### New Capabilities

- `routine-run-log`: Sandbox dashboard for idea-sweep pipeline health and per-project sweep history

### Modified Capabilities

- `visual-qa`: Sandbox homepage links to routine run log page

## Impact

- `routine-log.html`, `data/routine-log.json`, `data/sweep-runs.jsonl`, `scripts/generate-routine-log.mjs`
- `index.html` — nav link to routine log
- `routines/idea-sweep.md` — append sweep run records after each run
- `openspec/specs/visual-qa/spec.md` — routine log page requirement
