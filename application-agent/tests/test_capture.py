from pathlib import Path

import pytest

from application_agent.models import ApplicationStatus, CaptureLead, parse_capture_url
from application_agent.orchestrator import PrepPipeline, capture_and_start
from application_agent.tracker import TrackerStore
from application_agent.integrations.slack.service import SlackCaptureService
from application_agent.integrations.slack.formatting import format_queue


@pytest.fixture
def tracker(tmp_path: Path) -> TrackerStore:
    return TrackerStore(tmp_path)


def test_parse_capture_url():
    assert parse_capture_url("/capture https://careers.stripe.com/jobs/123") == (
        "https://careers.stripe.com/jobs/123"
    )
    assert parse_capture_url("no url") is None


def test_tracker_dedupes_url(tracker: TrackerStore):
    lead = CaptureLead(source="slack", url="https://Example.com/jobs/foo/")
    app1, created1 = tracker.capture(lead)
    app2, created2 = tracker.capture(
        CaptureLead(source="slack", url="https://example.com/jobs/foo")
    )
    assert created1 is True
    assert created2 is False
    assert app1.id == app2.id


def test_pipeline_marks_ready(tracker: TrackerStore):
    lead = CaptureLead(source="slack", url="https://acme.com/jobs/1")
    app, _ = tracker.capture(lead)
    pipeline = PrepPipeline(tracker)
    done = pipeline.run_sync(app)
    assert done.status == ApplicationStatus.READY
    assert done.fill_companion is not None
    assert done.fill_companion.flagged_count() >= 1


def test_capture_and_start_auto_prep(tracker: TrackerStore):
    pipeline = PrepPipeline(tracker)
    lead = CaptureLead(source="slack", url="https://meta.com/jobs/9")
    app, created, restarted = capture_and_start(tracker, pipeline, lead)
    assert created is True
    assert restarted is True
    assert app.status == ApplicationStatus.READY


def test_slack_capture_command(tracker: TrackerStore):
    service = SlackCaptureService(tracker=tracker)
    payload = service.handle_capture(
        text="https://careers.example.com/jobs/staff-ml-engineer",
        channel_id="C123",
    )
    assert "Captured" in payload["text"]
    assert payload["response_type"] == "in_channel"
    assert any(b.get("type") == "actions" for b in payload.get("blocks", []))


def test_queue_lists_active(tracker: TrackerStore):
    pipeline = PrepPipeline(tracker)
    capture_and_start(
        tracker,
        pipeline,
        CaptureLead(source="slack", url="https://a.com/1"),
    )
    service = SlackCaptureService(tracker=tracker)
    payload = service.handle_queue()
    assert "Your applications" in payload["text"]
    assert "a.com" in payload["text"].lower() or "A" in payload["text"]


def test_thread_done_updates_status(tracker: TrackerStore):
    pipeline = PrepPipeline(tracker)
    app, _, _ = capture_and_start(
        tracker,
        pipeline,
        CaptureLead(
            source="slack",
            url="https://b.com/2",
            slack_channel_id="C1",
            slack_thread_ts="111.222",
        ),
    )
    service = SlackCaptureService(tracker=tracker)
    reply = service.handle_thread_text("done", "C1", "111.222")
    assert reply is not None
    assert "submitted" in reply.lower()
    updated = tracker.get(app.id)
    assert updated is not None
    assert updated.status == ApplicationStatus.SUBMITTED


def test_format_queue_empty():
    assert "No active" in format_queue([])
