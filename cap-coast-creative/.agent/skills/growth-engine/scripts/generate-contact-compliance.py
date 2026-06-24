#!/usr/bin/env python3
import os
from common import clean, p, read_csv, rel, today, write_csv

FIELDS = ["date", "business", "channel", "contact_basis", "sender_id", "opt_out", "outreach_approval", "compliance_status", "next_action", "notes"]

prospects = read_csv(p("prospects.csv"))
drafts = {row.get("business"): row for row in read_csv(p("outreach_drafts.csv"))}

rows = []
for prospect in prospects:
    business = clean(prospect.get("business"))
    contact_basis = clean(prospect.get("contact_basis"), "none documented")
    opt_out = clean(prospect.get("opt_out"), "No")
    draft = drafts.get(business, {})
    has_basis = contact_basis.casefold() not in {"", "-", "none documented"}
    has_opt_out = opt_out.casefold() in {"yes", "included"} or clean(draft.get("opt_out"), "").casefold() == "included"
    sender_id = "Cap Coast Creative / Daniel"
    approved = "not-approved"
    status = "blocked"
    next_action = "Document lawful contact basis, opt-out wording, sender ID, and Daniel outreach approval."
    if has_basis and has_opt_out:
        status = "needs-outreach-approval"
        next_action = "Daniel must approve exact channel, copy, and recipient before any send."
    rows.append({
        "date": today(),
        "business": business,
        "channel": clean(draft.get("channel"), "not selected"),
        "contact_basis": contact_basis,
        "sender_id": sender_id,
        "opt_out": "included" if has_opt_out else "missing",
        "outreach_approval": approved,
        "compliance_status": status,
        "next_action": next_action,
        "notes": "Compliance review only; no outreach sent.",
    })

write_csv(p("contact_compliance.csv"), rows, FIELDS)

os.makedirs(p("contact_compliance"), exist_ok=True)
path = p("contact_compliance", f"{today()}.md")
with open(path, "w", encoding="utf-8") as handle:
    handle.write("# Contact Compliance Review\n\n")
    handle.write(f"- Date: {today()}\n")
    handle.write(f"- Prospects reviewed: {len(rows)}\n")
    handle.write("- Safety: no outreach sent or scheduled.\n\n")
    if rows:
        for row in rows:
            handle.write(f"- {row['business']}: {row['compliance_status']} / {row['next_action']}\n")
    else:
        handle.write("No contact compliance rows yet because there are no approved prospects.\n")

print(rel(path))
