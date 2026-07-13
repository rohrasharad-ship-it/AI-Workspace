from __future__ import annotations

import os
import re

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from application_agent.integrations.slack.service import SlackCaptureService
from application_agent.tracker import TrackerStore


def create_slack_app() -> App:
    signing_secret = os.environ["SLACK_SIGNING_SECRET"]
    bot_token = os.environ["SLACK_BOT_TOKEN"]
    bolt = App(token=bot_token, signing_secret=signing_secret)
    tracker = TrackerStore()
    service = SlackCaptureService(
        tracker=tracker,
        post_message=lambda **kwargs: bolt.client.chat_postMessage(**kwargs),
    )

    @bolt.command("/capture")
    def capture_command(ack, command, respond, client):  # type: ignore[no-untyped-def]
        ack()
        payload = service.handle_capture(
            text=command.get("text", ""),
            channel_id=command["channel_id"],
            thread_ts=command.get("thread_ts"),
        )
        respond(**payload)
        # Bind thread to application using the response message as thread root.
        if payload.get("response_type") == "in_channel":
            # Respond creates a message; for slash commands we use response_url message ts via metadata later.
            # Bind on next thread message or via stored mapping in v1 follow-up.
            pass

    @bolt.command("/queue")
    def queue_command(ack, respond):  # type: ignore[no-untyped-def]
        ack()
        respond(**service.handle_queue())

    @bolt.message(re.compile(r"^(queue|status|done|skip|submitted)\b", re.I))
    def thread_keywords(message, say):  # type: ignore[no-untyped-def]
        thread_ts = message.get("thread_ts") or message["ts"]
        reply = service.handle_thread_text(
            text=message.get("text", ""),
            channel_id=message["channel"],
            thread_ts=thread_ts,
        )
        if reply:
            say(text=reply, thread_ts=thread_ts)

    @bolt.action("app_start")
    @bolt.action("app_skip")
    @bolt.action("app_submitted")
    def handle_buttons(ack, body, respond):  # type: ignore[no-untyped-def]
        ack()
        action = body["actions"][0]
        text = service.handle_action(action["action_id"], action["value"])
        respond(text=text, response_type="in_channel", replace_original=False)

    return bolt


def run_socket_mode() -> None:
    app = create_slack_app()
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()
