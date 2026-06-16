#!/usr/bin/env python3
import os
from common import clean, p, read_csv, rel, today, write_csv

FIELDS = ["date", "status", "business", "approval_type", "decision", "evidence_path", "next_action", "notes"]
DECISION_FIELDS = ["date", "business", "approval_type", "decision", "decided_by", "evidence_path", "follow_up_action", "notes"]

if not os.path.exists(p("approval_decisions.csv")):
    write_csv(p("approval_decisions.csv"), [], DECISION_FIELDS)
decisions = {
    (clean(row.get("business")).casefold(), clean(row.get("approval_type")).casefold()): row
    for row in read_csv(p("approval_decisions.csv"))
}
rows = []
for item in read_csv(p("approval_queue.csv")):
    key = (clean(item.get("business")).casefold(), clean(item.get("approval_type")).casefold())
    decision = decisions.get(key)
    if decision:
        decision_value = clean(decision.get("decision"))
        next_action = clean(decision.get("follow_up_action"))
        status = f"decision-{decision_value}"
        notes = clean(decision.get("notes"))
    else:
        decision_value = "pending"
        next_action = "Daniel review required."
        status = "pending"
        notes = "No decision recorded yet."
    rows.append({
        "date": today(),
        "status": status,
        "business": clean(item.get("business")),
        "approval_type": clean(item.get("approval_type")),
        "decision": decision_value,
        "evidence_path": clean(item.get("source_path")),
        "next_action": next_action,
        "notes": notes,
    })

write_csv(p("approval_decision_summary.csv"), rows, FIELDS)

os.makedirs(p("approval_decision_summaries"), exist_ok=True)
path = p("approval_decision_summaries", f"{today()}.md")
with open(path, "w", encoding="utf-8") as handle:
    handle.write("# Approval Decision Summary\n\n")
    handle.write(f"- Date: {today()}\n")
    handle.write(f"- Items: {len(rows)}\n")
    handle.write("- Safety: approval decisions do not send outreach.\n\n")
    for row in rows:
        handle.write(f"- {row['business']}: {row['decision']} / {row['next_action']}\n")

print(rel(path))
