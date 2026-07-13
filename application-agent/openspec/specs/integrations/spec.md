# Integrations — Slack capture & queue (SHA-49)

## Capture contract

Every ingestion path normalizes to:

```json
{
  "source": "gmail | slack | bookmarklet",
  "url": "https://careers.example.com/jobs/...",
  "title": "optional",
  "captured_at": "ISO-8601",
  "slack_channel_id": "optional",
  "slack_thread_ts": "optional"
}
```

## Phase 1 — Slack (shipped in this change)

### `/capture <url>`
- Runs in `#application-agent`
- Auto-starts prep pipeline (no confirmation step)
- Creates one thread per application (slash-command response is thread root)
- Dedupes on normalized URL

### `/queue`
- Ephemeral dashboard of active applications
- Status icons: Prepping, Ready, In progress, Skipped

### Thread commands
- `status` / `queue` — single-app or full queue
- `done` / `skip` — update tracker

### Fill companion (Ready gate)
When prep completes, thread receives:
1. Job link
2. Cover letter (code block)
3. Resume PDF note (generation pipeline attaches real PDF later)
4. Field-by-field paste guide
5. Buttons: I'm on it / Skip / Submitted

## Phase 2 — Bookmarklet (deferred)
Same capture handler; POST from bookmarklet with shared token auth.

## Gmail
Existing primary ingestion path; uses same capture contract and thread model.
