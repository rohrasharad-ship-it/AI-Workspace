# Application Agent

Personal, human-in-the-loop career co-pilot. Slack is the control surface; the
orchestrator prepares applications and pauses for your review before anything
is submitted.

> **Repo note:** This tree lives under `AI-Workspace/application-agent/` until
> `rohrasharad-ship-it/Application-Agent` is accessible to the build agent.
> Copy to the Application-Agent repo root when that remote is linked.

## SHA-49: Slack capture + queue

- `/capture <url>` — hand off a job posting URL; prep starts automatically
- `/queue` — see all in-flight applications and what needs you
- One Slack thread per application with a fill companion when ready

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Run tests
pytest

# Start Slack listener (requires env vars)
export SLACK_BOT_TOKEN=xoxb-...
export SLACK_SIGNING_SECRET=...
application-agent slack
```

## Environment

| Variable | Purpose |
|----------|---------|
| `SLACK_BOT_TOKEN` | Bot token for posting and slash commands |
| `SLACK_SIGNING_SECRET` | Verify Slack request signatures |
| `APPLICATION_AGENT_DATA_DIR` | Tracker JSON store (default: `./data`) |
