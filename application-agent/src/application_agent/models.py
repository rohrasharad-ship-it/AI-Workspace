from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from urllib.parse import urlparse
import re
import uuid


class ApplicationStatus(str, Enum):
    CAPTURED = "captured"
    PREPPING = "prepping"
    READY = "ready"
    IN_PROGRESS = "in_progress"
    SUBMITTED = "submitted"
    SKIPPED = "skipped"


ACTIVE_STATUSES = {
    ApplicationStatus.CAPTURED,
    ApplicationStatus.PREPPING,
    ApplicationStatus.READY,
    ApplicationStatus.IN_PROGRESS,
}


@dataclass
class CaptureLead:
    """Normalized capture object — every ingestion path produces this."""

    source: str
    url: str
    title: str | None = None
    captured_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    slack_channel_id: str | None = None
    slack_thread_ts: str | None = None

    def normalized_url(self) -> str:
        parsed = urlparse(self.url.strip())
        scheme = parsed.scheme or "https"
        netloc = parsed.netloc.lower()
        path = parsed.path.rstrip("/") or "/"
        return f"{scheme}://{netloc}{path}"


@dataclass
class FillField:
    label: str
    value: str
    needs_human: bool = False


@dataclass
class FillCompanion:
    cover_letter: str
    fields: list[FillField]
    resume_note: str = "Tailored resume PDF attached (stub in v1 — generation pipeline TBD)."

    def flagged_count(self) -> int:
        return sum(1 for f in self.fields if f.needs_human)


@dataclass
class Application:
    id: str
    lead: CaptureLead
    status: ApplicationStatus = ApplicationStatus.CAPTURED
    company: str = ""
    role: str = ""
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    fill_companion: FillCompanion | None = None

    @staticmethod
    def new_from_lead(lead: CaptureLead) -> Application:
        company, role = infer_company_role(lead.url, lead.title)
        return Application(
            id=str(uuid.uuid4()),
            lead=lead,
            company=company,
            role=role,
        )

    def display_name(self) -> str:
        if self.company and self.role:
            return f"{self.company} — {self.role}"
        if self.role:
            return self.role
        return self.lead.normalized_url()

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "status": self.status.value,
            "source": self.lead.source,
            "url": self.lead.url,
            "normalized_url": self.lead.normalized_url(),
            "title": self.lead.title,
            "captured_at": self.lead.captured_at.isoformat(),
            "slack_channel_id": self.lead.slack_channel_id,
            "slack_thread_ts": self.lead.slack_thread_ts,
            "company": self.company,
            "role": self.role,
            "updated_at": self.updated_at.isoformat(),
            "fill_companion": (
                {
                    "cover_letter": self.fill_companion.cover_letter,
                    "resume_note": self.fill_companion.resume_note,
                    "fields": [
                        {
                            "label": f.label,
                            "value": f.value,
                            "needs_human": f.needs_human,
                        }
                        for f in self.fill_companion.fields
                    ],
                }
                if self.fill_companion
                else None
            ),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Application:
        lead = CaptureLead(
            source=data["source"],
            url=data["url"],
            title=data.get("title"),
            captured_at=datetime.fromisoformat(data["captured_at"]),
            slack_channel_id=data.get("slack_channel_id"),
            slack_thread_ts=data.get("slack_thread_ts"),
        )
        fill_raw = data.get("fill_companion")
        fill_companion = None
        if fill_raw:
            fill_companion = FillCompanion(
                cover_letter=fill_raw["cover_letter"],
                resume_note=fill_raw.get("resume_note", ""),
                fields=[
                    FillField(
                        label=f["label"],
                        value=f["value"],
                        needs_human=f.get("needs_human", False),
                    )
                    for f in fill_raw.get("fields", [])
                ],
            )
        app = cls(
            id=data["id"],
            lead=lead,
            status=ApplicationStatus(data["status"]),
            company=data.get("company", ""),
            role=data.get("role", ""),
            updated_at=datetime.fromisoformat(data["updated_at"]),
            fill_companion=fill_companion,
        )
        return app


def infer_company_role(url: str, title: str | None) -> tuple[str, str]:
    if title:
        parts = re.split(r"\s+[—–-]\s+|\s+at\s+", title, maxsplit=1)
        if len(parts) == 2:
            return parts[1].strip(), parts[0].strip()
        return "", title.strip()

    host = urlparse(url).netloc.lower().removeprefix("www.")
    company = host.split(".")[0].replace("-", " ").title() if host else ""
    return company, "Role TBD"


def parse_capture_url(text: str) -> str | None:
    match = re.search(r"https?://\S+", text)
    if not match:
        return None
    return match.group(0).rstrip(">)")


def relative_age(dt: datetime, now: datetime | None = None) -> str:
    now = now or datetime.now(timezone.utc)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    seconds = int((now - dt).total_seconds())
    if seconds < 60:
        return "just now"
    minutes = seconds // 60
    if minutes < 60:
        return f"{minutes}m ago"
    hours = minutes // 60
    if hours < 48:
        return f"{hours}h ago"
    days = hours // 24
    return f"{days}d ago"
