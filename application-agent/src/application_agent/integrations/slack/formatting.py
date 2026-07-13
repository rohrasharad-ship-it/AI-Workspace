from __future__ import annotations

from application_agent.models import Application, ApplicationStatus, relative_age


STATUS_ICONS = {
    ApplicationStatus.CAPTURED: "📥",
    ApplicationStatus.PREPPING: "🟡",
    ApplicationStatus.READY: "✅",
    ApplicationStatus.IN_PROGRESS: "👀",
    ApplicationStatus.SKIPPED: "⏸",
    ApplicationStatus.SUBMITTED: "✔️",
}


def format_queue(apps: list[Application]) -> str:
    if not apps:
        return "No active applications. Capture one with `/capture <url>`."

    lines = [f"*Your applications ({len(apps)} active)*", ""]
    for app in apps:
        icon = STATUS_ICONS.get(app.status, "•")
        label = _status_label(app)
        age = relative_age(app.lead.captured_at)
        detail = ""
        if app.status == ApplicationStatus.READY and app.fill_companion:
            flagged = app.fill_companion.flagged_count()
            if flagged:
                detail = f" — {flagged} field{'s' if flagged != 1 else ''} need you"
            else:
                detail = " — all drafted"
        thread = ""
        if app.lead.slack_thread_ts:
            thread = " → open thread in channel"
        lines.append(f"{icon} *{label}*  {app.display_name()}  _({age})_{detail}{thread}")
    return "\n".join(lines)


def _status_label(app: Application) -> str:
    mapping = {
        ApplicationStatus.CAPTURED: "Captured",
        ApplicationStatus.PREPPING: "Prepping",
        ApplicationStatus.READY: "Ready",
        ApplicationStatus.IN_PROGRESS: "In progress",
        ApplicationStatus.SKIPPED: "Skipped",
        ApplicationStatus.SUBMITTED: "Submitted",
    }
    return mapping.get(app.status, app.status.value)


def format_capture_ack(app: Application, created: bool, restarted: bool) -> str:
    if not created and not restarted:
        return (
            f"Already tracking *{app.display_name()}* (status: `{app.status.value}`).\n"
            f"Open the existing thread to continue."
        )
    return (
        f"Captured — prep pipeline started for *{app.display_name()}*.\n"
        f"I'll post the fill companion here when ready (~2 min)."
    )


def format_fill_companion(app: Application) -> str:
    fc = app.fill_companion
    if not fc:
        return "Fill companion not ready yet."

    lines = [
        f"*Ready for you — {app.display_name()}*",
        f"<{app.lead.url}|Open job posting>",
        "",
        "*Cover letter*",
        f"```{fc.cover_letter}```",
        "",
        f"_{fc.resume_note}_",
        "",
        "*Paste guide*",
    ]
    for field in fc.fields:
        if field.needs_human:
            lines.append(f"⚠️ *Needs you:* `{field.label}`")
            lines.append("_No confident draft — add your own answer or ask me to regenerate._")
        else:
            lines.append(f"*Field:* `{field.label}`")
            lines.append(f"```{field.value}```")
        lines.append("")
    lines.append("When done: reply `done` or use the buttons below.")
    return "\n".join(lines).strip()


def format_status_line(app: Application) -> str:
    return f"*{app.display_name()}* — `{app.status.value}` (updated {relative_age(app.updated_at)})"
