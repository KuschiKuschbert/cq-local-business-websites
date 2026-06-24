#!/usr/bin/env python3
import os
from common import clean, p, read_csv, rel, today, write_csv

FIELDS = ["date", "approval_type", "business", "priority", "source_path", "requested_decision", "safe_command", "blocked_until_approved", "notes"]
approved = {
    clean(row.get("business")).casefold()
    for row in read_csv(p("approval_decisions.csv"))
    if clean(row.get("approval_type")).casefold() == "promotion"
    and clean(row.get("decision")).casefold() == "approve"
}
promoted = {
    clean(row.get("business")).casefold()
    for row in read_csv(p("prospects.csv"))
}
rows = []
for row in read_csv(p("intake_opportunity_briefs.csv")):
    business = clean(row.get("business"), "")
    if not business:
        continue
    if business.casefold() in approved or business.casefold() in promoted:
        continue
    rows.append({
        "date": today(),
        "approval_type": "promotion",
        "business": business,
        "priority": "high",
        "source_path": clean(row.get("brief_path")),
        "requested_decision": "Approve or reject moving this staged candidate into prospects.csv.",
        "safe_command": f'python3 .agent/skills/growth-engine/scripts/promote-intake.py --business "{business}" --approved-by "Daniel"',
        "blocked_until_approved": "prospect promotion, mockup brief generation, outreach drafting",
        "notes": "Promotion is not outreach approval.",
    })
write_csv(p("approval_queue.csv"), rows, FIELDS)
os.makedirs(p("approval_reports"), exist_ok=True)
report = p("approval_reports", f"{today()}.md")
with open(report, "w", encoding="utf-8") as handle:
    handle.write("# Approval Queue\n\n")
    handle.write(f"- Pending items: {len(rows)}\n\n")
    for row in rows:
        handle.write(f"- {row['approval_type']} / {row['business']} / {row['safe_command']}\n")
print(rel(report))
