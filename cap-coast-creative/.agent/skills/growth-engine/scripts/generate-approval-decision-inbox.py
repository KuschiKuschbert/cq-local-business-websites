#!/usr/bin/env python3
import os
from common import clean, p, read_csv, rel, slug, today, write_csv

FIELDS = [
    "date",
    "rank",
    "business",
    "approval_type",
    "recommended_decision",
    "approve_command",
    "reject_command",
    "hold_command",
    "approve_effect",
    "reject_effect",
    "hold_effect",
    "evidence_path",
    "packet_path",
    "safety_gate",
    "notes",
]

priority = {clean(row.get("business")).casefold(): row for row in read_csv(p("priority_board.csv"))}
packets = {clean(row.get("business")).casefold(): row for row in read_csv(p("approval_packets.csv"))}
decisions = {
    (clean(row.get("business")).casefold(), clean(row.get("approval_type")).casefold()): row
    for row in read_csv(p("approval_decisions.csv"))
}
rows = []

for item in read_csv(p("approval_queue.csv")):
    business = clean(item.get("business"))
    key = business.casefold()
    approval_type = clean(item.get("approval_type"))
    if decisions.get((key, approval_type.casefold())):
        continue
    rank = clean(priority.get(key, {}).get("rank"), "999")
    packet_path = clean(packets.get(key, {}).get("packet_path"), f".agent/memory/working/approval_packets/{slug(business)}.md")
    base = f'python3 .agent/skills/growth-engine/scripts/record-approval-decision.py --business "{business}" --decided-by "Daniel"'
    rows.append({
        "date": today(),
        "rank": rank,
        "business": business,
        "approval_type": approval_type,
        "recommended_decision": "approve only if Daniel accepts evidence for prospect promotion; otherwise hold or reject",
        "approve_command": f'{base} --decision approve --notes "Approved for prospect promotion only."',
        "reject_command": f'{base} --decision reject --notes "Rejected for prospect promotion."',
        "hold_command": f'{base} --decision hold --notes "Hold for more evidence before promotion."',
        "approve_effect": clean(item.get("safe_command")),
        "reject_effect": "Leaves the candidate out of prospects.csv unless new evidence changes the decision.",
        "hold_effect": "Keeps the item pending and routes it back to evidence review.",
        "evidence_path": clean(item.get("source_path")),
        "packet_path": packet_path,
        "safety_gate": "Decision recording is not promotion, outreach, publishing, remote GitHub write, billing, or client-facing approval.",
        "notes": "Approve/reject/hold are local decision records only. Promotion and outreach remain separate gates.",
    })

rows.sort(key=lambda row: int(row["rank"]) if row["rank"].isdigit() else 999)
write_csv(p("approval_decision_inbox.csv"), rows, FIELDS)

os.makedirs(p("approval_decision_inbox"), exist_ok=True)
path = p("approval_decision_inbox", f"{today()}.md")
with open(path, "w", encoding="utf-8") as handle:
    handle.write("# Approval Decision Inbox\n\n")
    handle.write(f"- Date: {today()}\n")
    handle.write("- Purpose: expose approve, reject, and hold choices for each promotion packet.\n")
    handle.write("- Safety: decision recording does not approve outreach, publishing, remote GitHub writes, billing, or client-facing actions.\n\n")
    for row in rows:
        handle.write(f"## #{row['rank']} {row['business']}\n\n")
        handle.write(f"- Evidence: {row['evidence_path']}\n")
        handle.write(f"- Packet: {row['packet_path']}\n")
        handle.write(f"- Approve: `{row['approve_command']}`\n")
        handle.write(f"- Reject: `{row['reject_command']}`\n")
        handle.write(f"- Hold: `{row['hold_command']}`\n")
        handle.write(f"- Gate: {row['safety_gate']}\n\n")

print(rel(path))
