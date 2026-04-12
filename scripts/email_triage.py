"""
email_triage.py -- Deterministic email classification helpers.

Provides pre-classification of emails by keyword matching.
The LLM layer applies judgment for final triage decisions.

NOTE: Actual email fetching uses Gmail MCP tools.
This module handles classification logic and report formatting.
"""

from datetime import datetime
from dataclasses import dataclass


@dataclass
class TriagedEmail:
    message_id: str
    subject: str
    sender: str
    date: str
    snippet: str
    classification: str = ""  # act_now, act_today, track, drop
    reason: str = ""
    action_needed: str = ""
    is_receipt: bool = False
    is_travel: bool = False
    is_newsletter: bool = False


RECEIPT_KEYWORDS = ["receipt", "invoice", "order confirmation", "payment", "transaction", "billing"]
TRAVEL_KEYWORDS = ["booking confirmation", "itinerary", "flight", "hotel", "reservation", "boarding pass"]
NEWSLETTER_KEYWORDS = ["unsubscribe", "view in browser", "email preferences", "newsletter", "digest"]


def pre_classify(subject: str, snippet: str) -> dict:
    text = f"{subject} {snippet}".lower()
    return {
        "is_receipt": any(k in text for k in RECEIPT_KEYWORDS),
        "is_travel": any(k in text for k in TRAVEL_KEYWORDS),
        "is_newsletter": any(k in text for k in NEWSLETTER_KEYWORDS),
    }


def format_triage_report(emails: list[TriagedEmail]) -> str:
    sections = {"act_now": [], "act_today": [], "track": [], "auto": []}

    for e in emails:
        if e.is_receipt or e.is_travel:
            label = "Receipt" if e.is_receipt else "Travel"
            sections["auto"].append(f"  - {label}: {e.subject}")
        elif e.classification == "act_now":
            sections["act_now"].append(f"  - **{e.sender}**: {e.subject}\n    Action: {e.action_needed}")
        elif e.classification == "act_today":
            sections["act_today"].append(f"  - {e.sender}: {e.subject}\n    Action: {e.action_needed}")
        elif e.classification == "track":
            sections["track"].append(f"  - {e.sender}: {e.subject}")

    report = f"**Email Triage -- {datetime.now().strftime('%H:%M')}**\n\n"
    if sections["act_now"]:
        report += "**Needs Attention Now**\n" + "\n".join(sections["act_now"]) + "\n\n"
    if sections["act_today"]:
        report += "**Act Today**\n" + "\n".join(sections["act_today"]) + "\n\n"
    if sections["track"]:
        report += "**Tracking**\n" + "\n".join(sections["track"]) + "\n\n"
    if sections["auto"]:
        report += "**Auto-Processed**\n" + "\n".join(sections["auto"]) + "\n\n"

    dropped = len(emails) - sum(len(v) for v in sections.values())
    if dropped > 0:
        report += f"_{dropped} emails filtered as noise._\n"
    return report
