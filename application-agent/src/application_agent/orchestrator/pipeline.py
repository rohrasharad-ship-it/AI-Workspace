from __future__ import annotations

from application_agent.generation.fill_plan import build_fill_companion
from application_agent.models import Application, ApplicationStatus
from application_agent.tracker import TrackerStore


class PrepPipeline:
    """Cloud prep stub — tailor → draft → fill-plan. Real generation plugs in later."""

    def __init__(self, tracker: TrackerStore) -> None:
        self.tracker = tracker

    def start(self, application: Application) -> Application:
        application.status = ApplicationStatus.PREPPING
        return self.tracker.upsert(application)

    def complete(self, application: Application) -> Application:
        application.fill_companion = build_fill_companion(application)
        application.status = ApplicationStatus.READY
        return self.tracker.upsert(application)

    def run_sync(self, application: Application) -> Application:
        """Synchronous prep for tests and local dev without a job queue."""
        application = self.start(application)
        return self.complete(application)


def capture_and_start(
    tracker: TrackerStore,
    pipeline: PrepPipeline,
    lead,
) -> tuple[Application, bool, bool]:
    """Capture lead, auto-start prep if newly created or still captured."""
    app, created = tracker.capture(lead)
    restarted = False
    if created or app.status == ApplicationStatus.CAPTURED:
        pipeline.run_sync(app)
        restarted = True
        app = tracker.get(app.id) or app
    return app, created, restarted
