## Context

The v8 layout: horizontal pipeline KPIs (pending, today, bugs, features), two stacked bar charts (features and bugs, each segmented by project with consistent colors and project names inside segments), then project cards from `projects.md` with numeric bug/feature counts and per-sweep filed/open numbers only. No red/blue ratio bars, no bottom "Recent Runs" feed.

Data sources:
1. **Linear** — pending pipeline issues per project (Backlog/Todo/In Progress/In Review); classify bugs (title starts with 🐛) vs features (everything else)
2. **Sweep ledger** — `data/sweep-runs.jsonl`, one JSON line per project per sweep, appended by idea-sweep orchestrator (includes zero-finding "clean" runs)
3. **Issue creation dates** — fallback to infer filed counts when ledger entry missing

## Goals / Non-Goals

**Goals:**
- Static page on sandbox, no server runtime
- Regenerate JSON via script with `LINEAR_API_KEY`
- Match v8 visual layout (stacked project bars + numbers-only cards)

**Non-Goals:**
- Real-time Linear polling in the browser (no API keys client-side)
- Per-role columns (spec-drift / bug-error / market) — bugs vs features only
- Slack parsing as data source

## Decisions

### 1. JSON file + static HTML

`routine-log.html` fetches `/data/routine-log.json` and renders. Vercel serves static files from repo root. Regenerate on schedule or after sweeps.

### 2. Sweep ledger format (JSONL)

```json
{"at":"2026-07-21T09:00:00Z","project":"Usercon","filed":{"bugs":0,"features":0},"clean":true}
```

### 3. Bug vs feature classification

- Bug: issue title starts with `🐛`
- Feature: all other pipeline issues

### 4. Per-run "still open"

For each sweep date, count issues created that day (per project) still in pipeline states.

## Risks / Trade-offs

- **[Ledger not backfilled]** → Historical clean sweeps only appear after idea-sweep starts logging; script can infer filing days from Linear until ledger grows
- **[Classification heuristic]** → Emoji-based bug detection is imperfect but matches how bug-error files issues
