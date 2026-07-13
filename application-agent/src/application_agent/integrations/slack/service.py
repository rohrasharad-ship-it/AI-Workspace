from __future__ import annotations

from typing import Any, Callable

from application_agent.integrations.slack.formatting import (
    format_capture_ack,
    format_fill_companion,
    format_queue,
    format_status_line,
)
from application_agent.models import ApplicationStatus, CaptureLead, parse_capture_url
from application_agent.orchestrator import PrepPipeline, capture_and_start
from application_agent.tracker import TrackerStore


class SlackCaptureService:
    """Slash commands and thread actions for capture + queue."""

    def __init__(
        self,
        tracker: TrackerStore | None = None,
        pipeline: PrepPipeline | None = None,
        post_message: Callable[..., Any] | None = None,
    ) -> None:
        self.tracker = tracker or TrackerStore()
        self.pipeline = pipeline or PrepPipeline(self.tracker)
        self.post_message = post_message

    def handle_capture(
        self,
        text: str,
        channel_id: str,
        thread_ts: str | None = None,
    ) -> dict[str, Any]:
        url = parse_capture_url(text)
        if not url:
            return {
                "response_type": "ephemeral",
                "text": "Usage: `/capture https://careers.example.com/jobs/...`",
            }

        lead = CaptureLead(
            source="slack",
            url=url,
            slack_channel_id=channel_id,
            slack_thread_ts=thread_ts,
        )
        app, created, restarted = capture_and_start(self.tracker, self.pipeline, lead)

        ack = format_capture_ack(app, created, restarted)
        blocks: list[dict] = [
            {"type": "section", "text": {"type": "mrkdwn", "text": ack}},
        ]

        if app.status == ApplicationStatus.READY and app.fill_companion:
            blocks.append(
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": format_fill_companion(app),
                    },
                }
            )
        blocks.extend(_action_blocks(app.id))

        return {
            "response_type": "in_channel",
            "text": ack,
            "blocks": blocks,
        }

    def handle_queue(self) -> dict[str, Any]:
        apps = self.tracker.list_active()
        return {
            "response_type": "ephemeral",
            "text": format_queue(apps),
        }

    def handle_thread_text(
        self,
        text: str,
        channel_id: str,
        thread_ts: str,
    ) -> str | None:
        lowered = text.strip().lower()
        app = self._find_by_thread(channel_id, thread_ts)
        if not app:
            return None

        if lowered in {"queue", "status"}:
            if lowered == "queue":
                return format_queue(self.tracker.list_active())
            return format_status_line(app)

        if lowered in {"done", "submitted"}:
            self.tracker.set_status(app.id, ApplicationStatus.SUBMITTED)
            return f"Marked *{app.display_name()}* as submitted. Nice work."

        if lowered == "skip":
            self.tracker.set_status(app.id, ApplicationStatus.SKIPPED)
            return f"Skipped *{app.display_name()}*."

        return None

    def handle_action(self, action_id: str, app_id: str) -> str:
        if action_id == "app_start":
            app = self.tracker.set_status(app_id, ApplicationStatus.IN_PROGRESS)
            if not app:
                return "Application not found."
            return f"You're on *{app.display_name()}*. Open the job link and use the paste guide above."

        if action_id == "app_skip":
            app = self.tracker.set_status(app_id, ApplicationStatus.SKIPPED)
            if not app:
                return "Application not found."
            return f"Skipped *{app.display_name()}*."

        if action_id == "app_submitted":
            app = self.tracker.set_status(app_id, ApplicationStatus.SUBMITTED)
            if not app:
                return "Application not found."
            return f"Logged *{app.display_name()}* as submitted."

        return "Unknown action."

    def bind_thread(self, channel_id: str, message_ts: str, app_id: str) -> None:
        app = self.tracker.get(app_id)
        if not app:
            return
        app.lead.slack_channel_id = channel_id
        app.lead.slack_thread_ts = message_ts
        self.tracker.upsert(app)
        if app.status == ApplicationStatus.READY:
            self._post_fill_companion(app)

    def _post_fill_companion(self, app) -> None:
        if not self.post_message or not app.lead.slack_channel_id:
            return
        thread = app.lead.slack_thread_ts
        self.post_message(
            channel=app.lead.slack_channel_id,
            thread_ts=thread,
            text=format_fill_companion(app),
            blocks=[
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": format_fill_companion(app)},
                },
                *_action_blocks(app.id),
            ],
        )

    def _find_by_thread(self, channel_id: str, thread_ts: str):
        for app in self.tracker.list_all():
            if (
                app.lead.slack_channel_id == channel_id
                and app.lead.slack_thread_ts == thread_ts
            ):
                return app
        return None


def _action_blocks(app_id: str) -> list[dict[str, Any]]:
    return [
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "I'm on it"},
                    "action_id": "app_start",
                    "value": app_id,
                },
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Skip"},
                    "action_id": "app_skip",
                    "value": app_id,
                    "style": "danger",
                },
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Submitted"},
                    "action_id": "app_submitted",
                    "value": app_id,
                    "style": "primary",
                },
            ],
        }
    ]
