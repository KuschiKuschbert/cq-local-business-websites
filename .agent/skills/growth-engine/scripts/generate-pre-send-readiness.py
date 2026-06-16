#!/usr/bin/env python3
import os
from common import clean, p, read_csv, rel, today, write_csv

FIELDS = ["date", "business", "readiness_status", "required_gate", "evidence", "failure_reason", "next_action", "notes"]

prospects = read_csv(p("prospects.csv"))
drafts = {clean(row.get("business")).casefold(): row for row in read_csv(p("outreach_drafts.csv"))}
compliance = {clean(row.get("business")).casefold(): row for row in read_csv(p("contact_compliance.csv"))}
outreach = read_csv(p("outreach_log.csv"))


def has_contact_basis(value):
    return clean(value, "").casefold() not in {"", "-", "none documented", "unknown"}


def has_sender_identity(value):
    text = clean(value, "").casefold()
    return "daniel" in text and ("cap coast creative" in text or "business" in text)


def has_opt_out(value):
    return clean(value, "").casefold() in {"included", "yes", "present", "ready"}


rows = []
if not prospects:
    rows.append({
        "date": today(),
        "business": "pipeline-level",
        "readiness_status": "blocked-no-approved-prospects",
        "required_gate": "Daniel-approved prospect promotion",
        "evidence": f"{len(prospects)} prospects / {len(drafts)} drafts / {len(compliance)} compliance rows",
        "failure_reason": "No business has been promoted into prospects.csv with a recorded approval.",
        "next_action": "Review approval packets and record approve/reject/hold decisions before any outreach preparation.",
        "notes": "No outreach can be sent, scheduled, or queued from this state.",
    })
else:
    for prospect in prospects:
        business = clean(prospect.get("business"))
        key = business.casefold()
        draft = drafts.get(key, {})
        review = compliance.get(key, {})
        failures = []
        if not draft:
            failures.append("draft missing")
        if not review:
            failures.append("contact compliance row missing")
        if not has_contact_basis(review.get("contact_basis", prospect.get("contact_basis"))):
            failures.append("lawful contact basis missing")
        if not has_sender_identity(review.get("sender_id")):
            failures.append("sender identity incomplete")
        if not has_opt_out(review.get("opt_out", draft.get("opt_out"))):
            failures.append("opt-out missing")
        if clean(review.get("outreach_approval")).casefold() != "approved":
            failures.append("explicit outreach approval missing")
        if outreach:
            prior = [row for row in outreach if clean(row.get("business")).casefold() == key]
        else:
            prior = []
        status = "blocked-pre-send"
        next_action = "Resolve missing gates; Daniel must approve exact recipient, channel, and copy before any send."
        if not failures:
            status = "ready-for-manual-send-review"
            next_action = "Manual review only; sending still requires Daniel to initiate or explicitly approve the send operation."
        rows.append({
            "date": today(),
            "business": business,
            "readiness_status": status,
            "required_gate": "Consent/contact basis, sender ID, opt-out, exact-copy approval, and manual send approval",
            "evidence": f"draft: {bool(draft)} / compliance: {bool(review)} / prior outreach rows: {len(prior)}",
            "failure_reason": "; ".join(failures) if failures else "-",
            "next_action": next_action,
            "notes": "Pre-send readiness is an audit artifact only; it never sends or schedules outreach.",
        })

write_csv(p("pre_send_readiness.csv"), rows, FIELDS)

os.makedirs(p("pre_send_readiness"), exist_ok=True)
path = p("pre_send_readiness", f"{today()}.md")
with open(path, "w", encoding="utf-8") as handle:
    handle.write("# Pre-Send Readiness Audit\n\n")
    handle.write(f"- Date: {today()}\n")
    handle.write("- Safety: this audit cannot send, schedule, queue, or approve outreach.\n")
    handle.write("- Compliance floor: consent/contact basis, sender identification, contact details, and easy unsubscribe.\n\n")
    for row in rows:
        handle.write(f"- {row['business']}: {row['readiness_status']} / Missing: {row['failure_reason']} / Next: {row['next_action']}\n")

print(rel(path))
