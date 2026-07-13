from __future__ import annotations

from application_agent.models import Application, FillCompanion, FillField


def build_fill_companion(application: Application) -> FillCompanion:
    company = application.company or "the company"
    role = application.role or "this role"
    cover = (
        f"Dear {company} hiring team,\n\n"
        f"I'm excited to apply for {role}. My background aligns with the posting "
        f"and I'd welcome a conversation about how I can contribute.\n\n"
        f"Best,\nSharad"
    )
    fields = [
        FillField(
            label="Why this company?",
            value=f"I'm drawn to {company}'s mission and the scope of {role}.",
        ),
        FillField(
            label="Salary expectation",
            value="$180–200k (per disclosure policy)",
        ),
        FillField(
            label="Work authorization",
            value="Authorized to work in the US; no sponsorship needed.",
        ),
        FillField(
            label="Describe a relevant accomplishment",
            value="",
            needs_human=True,
        ),
    ]
    return FillCompanion(cover_letter=cover, fields=fields)
