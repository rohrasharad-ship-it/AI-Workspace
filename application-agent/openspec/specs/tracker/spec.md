# Tracker

## Storage
JSON file at `{APPLICATION_AGENT_DATA_DIR}/applications.json` with atomic write.

## Status lifecycle
`captured` → `prepping` → `ready` → `in_progress` → `submitted` | `skipped`

## Dedup
Normalized URL (scheme + host + path, trailing slash stripped). Re-capture
updates Slack thread binding if missing; does not re-run prep unless status is
still `captured`.

## Active set
`captured`, `prepping`, `ready`, `in_progress` appear in `/queue`.
