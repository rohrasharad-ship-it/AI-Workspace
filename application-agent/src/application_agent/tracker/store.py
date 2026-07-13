from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

from application_agent.models import (
    ACTIVE_STATUSES,
    Application,
    ApplicationStatus,
    CaptureLead,
)


class TrackerStore:
    """Merge-safe JSON tracker — canonical application state."""

    def __init__(self, data_dir: str | Path | None = None) -> None:
        base = data_dir or os.environ.get("APPLICATION_AGENT_DATA_DIR", "./data")
        self.path = Path(base) / "applications.json"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._write([])

    def _read(self) -> list[Application]:
        raw = json.loads(self.path.read_text(encoding="utf-8"))
        return [Application.from_dict(item) for item in raw]

    def _write(self, apps: list[Application]) -> None:
        payload = [app.to_dict() for app in apps]
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        tmp.replace(self.path)

    def find_by_url(self, url: str) -> Application | None:
        normalized = CaptureLead(source="slack", url=url).normalized_url()
        for app in self._read():
            if app.lead.normalized_url() == normalized:
                return app
        return None

    def get(self, app_id: str) -> Application | None:
        for app in self._read():
            if app.id == app_id:
                return app
        return None

    def list_active(self) -> list[Application]:
        apps = [a for a in self._read() if a.status in ACTIVE_STATUSES]
        return sorted(apps, key=lambda a: a.lead.captured_at)

    def list_all(self) -> list[Application]:
        return sorted(self._read(), key=lambda a: a.lead.captured_at, reverse=True)

    def upsert(self, application: Application) -> Application:
        apps = self._read()
        application.updated_at = datetime.now(timezone.utc)
        for idx, existing in enumerate(apps):
            if existing.id == application.id:
                apps[idx] = application
                self._write(apps)
                return application
        apps.append(application)
        self._write(apps)
        return application

    def capture(self, lead: CaptureLead) -> tuple[Application, bool]:
        """Returns (application, created). Dedupes on normalized URL."""
        existing = self.find_by_url(lead.url)
        if existing:
            if lead.slack_thread_ts and not existing.lead.slack_thread_ts:
                existing.lead.slack_thread_ts = lead.slack_thread_ts
                existing.lead.slack_channel_id = lead.slack_channel_id
                self.upsert(existing)
            return existing, False
        app = Application.new_from_lead(lead)
        self.upsert(app)
        return app, True

    def set_status(self, app_id: str, status: ApplicationStatus) -> Application | None:
        app = self.get(app_id)
        if not app:
            return None
        app.status = status
        return self.upsert(app)
