# Handover: Feature Prioritization Wedge — Signal Inventory (Q1)

**For:** Sharad (decision needed) / next agent once Q1–Q3 are resolved
**From:** Claude, feature-prioritization-wedge session
**Status:** Inventory complete. Build is still blocked — worse than the spec assumed.

This follows the spec's own instruction: *"Don't build ingestion yet. Start with Q1 — inventory what signal actually exists and in what form."* Findings below.

---

## Finding 1 — "TRD" is not reachable by any connected tool

The spec's Inputs section says: *"Backlog: Linear, TRD team — pull via `Linear:list_issues` / `Linear:list_projects`, filtered to TRD."*

There is no TRD team or project in the connected Linear workspace. I checked directly:

- `list_teams` → one team only: **Sharad Rohra** (key `SHA`).
- `list_projects` → five projects only: Resume Website, PM OS, AI Landscape, Application Agent, UserCon. No TRD.

Cross-checking Drive and Usercon resolved what "TRD" actually is: **Amadeus TRD, Bangalore** — Sharad's real employer team (see `TRD_ProductJam_ArjunaFramework.pptx` in Drive, and the Usercon "About Me" note: *"Role: Product Manager @ Amadeus (travel tech)"*).

**This means the backlog this spec wants to rank lives inside Amadeus's own systems — not in this AI-Workspace stack at all.** AI-Workspace is Sharad's personal PM-OS (Linear/Notion/Slack/Drive under his personal Google account); it has no connector to Amadeus's internal tools (Jira, Confluence, whatever TRD actually uses), and realistically never will, for confidentiality reasons. `Linear:list_issues filtered to TRD` as written in the spec is not executable — there is nothing to filter to.

## Finding 2 — No customer/usage signal exists in any connected source, for TRD or otherwise

Searched every connected source for TRD-related signal — support tickets, interview notes, usage dashboards, strategy docs:

| Source | Searched for | Result |
|---|---|---|
| Linear | "TRD", "flight" | 0 relevant hits |
| Notion | "TRD backlog", "Amadeus TRD strategy OKR", "flight content aggregator" | 0 relevant hits |
| Slack (all channels) | "TRD", "Amadeus TRD", "flight content aggregator" | 1 hit — a job-application fit-assessment message that only *mentions* "your TRD work at Amadeus," no substance |
| Google Drive | "TRD", "flight content aggregator" | 1 hit — the Product Jam slide deck (an internal AI-agents presentation, not backlog/signal data) |
| Gmail | "content aggregator", "shutdown" | 0 relevant hits |
| Granola | — | Not set up (account not created) |
| Usercon (personal context layer) | career life area | Confirms career facts (B2B→B2C transition, satisfaction 6/10) and the origin of this exact idea, but holds no TRD backlog or signal data |

**Conclusion on the spec's own Q1 hypothesis — confirmed, and it's the binding constraint:** *"the real bottleneck is that there's no structured signal to ingest yet."* That's not just true for usage/customer signal — it's also true for the backlog itself. There is currently **zero agent-accessible data** for this wedge to run against. Every input (backlog issues, support tickets, interview notes, or "what stakeholders said in meetings") would have to be manually typed or pasted in by Sharad from wherever it actually lives at Amadeus.

## Finding 3 — Q2 (flight-content-aggregator shutdown) can't be answered from here

No trace of a "flight-content-aggregator" project, decision doc, or shutdown rationale in Notion, Slack, Drive, Gmail, or Usercon. If Sharad wants to use it as a labeled validation example, he'll need to supply the inputs available at decision time and the actual call made directly — nothing to reconstruct it from is on file.

## Finding 4 — Q3 (single-run vs. repeatable) is moot until Q1/Q2 land

Given Finding 2, there's no automated ingestion to make repeatable yet regardless of the answer — every run starts from a manual data drop. Recommend deciding this only after a first single run proves the synthesis step is worth repeating.

---

## What this changes about the suggested build path

The spec frames this as a choice between "ranking problem" and "signal-structuring problem." Given Findings 1–2, it's neither yet — it's a **data access problem**: nothing about TRD (backlog or signal) is machine-readable from any tool this agent can reach. The realistic v0 is:

1. Sharad manually exports/pastes the TRD backlog (issue titles + one-liners is enough) and whatever signal actually exists — even if that's just "what stakeholders said in meetings," written down — into a plain-text or Markdown drop.
2. The agent ranks off that pasted input in one script/session run, per the spec's original scope (JSON/Markdown table, rationale citing the pasted evidence).
3. No live Linear/API ingestion against TRD is buildable in this workspace — drop that from scope rather than block on it.

## Questions for Sharad before build starts

1. Confirm: TRD = your Amadeus team in Bangalore, not a workspace this agent can otherwise reach — correct?
2. What can you actually hand over in an hour: backlog item titles/descriptions (copy-paste export is fine), plus whatever signal exists — ticket notes, interview notes, or just your own recollection of stakeholder asks?
3. Do you want to supply the flight-content-aggregator shutdown inputs/decision yourself as a validation case, or drop Q2 from v0?
4. Given Finding 2, are you still good with a single manual-input run for v0 (recommended), or is there an export you'd rather script against?
