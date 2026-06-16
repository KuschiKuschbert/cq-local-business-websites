#!/usr/bin/env python3
import os
from common import clean, p, read_csv, rel, slug, today, write_csv

FIELDS = [
    "date",
    "business",
    "rank",
    "approval_type",
    "recommended_decision",
    "evidence_path",
    "decision_command",
    "after_approve",
    "still_blocked",
    "packet_path",
    "notes",
]

priority = {clean(row.get("business")).casefold(): row for row in read_csv(p("priority_board.csv"))}
strategy = {clean(row.get("business")).casefold(): row for row in read_csv(p("offer_strategy.csv"))}
permissions = {clean(row.get("action")).casefold(): row for row in read_csv(p("action_permissions.csv"))}
rows = []
os.makedirs(p("approval_packets"), exist_ok=True)

for item in read_csv(p("approval_queue.csv")):
    business = clean(item.get("business"))
    key = business.casefold()
    priority_row = priority.get(key, {})
    strategy_row = strategy.get(key, {})
    decision_command = (
        f'python3 .agent/skills/growth-engine/scripts/record-approval-decision.py '
        f'--business "{business}" --decision approve --decided-by "Daniel" --notes "Approved for prospect promotion only."'
    )
    packet_path = p("approval_packets", f"{slug(business)}.md")
    after_approve = clean(item.get("safe_command"))
    still_blocked = "Outreach send, remote GitHub writes, publishing, hosting, billing, and client-facing promises."
    with open(packet_path, "w", encoding="utf-8") as handle:
        handle.write(f"# Approval Packet: {business}\n\n")
        handle.write(f"- Date: {today()}\n")
        handle.write(f"- Approval type: {clean(item.get('approval_type'))}\n")
        handle.write(f"- Priority rank: {clean(priority_row.get('rank'))}\n")
        handle.write(f"- Priority score: {clean(priority_row.get('priority_score'))}\n")
        handle.write(f"- Evidence: {clean(item.get('source_path'))}\n")
        handle.write(f"- Offer tier: {clean(strategy_row.get('tier'))} / {clean(strategy_row.get('monthly_fee'))}\n")
        handle.write(f"- Trust hook: {clean(strategy_row.get('trust_hook'))}\n")
        handle.write(f"- Primary CTA: {clean(strategy_row.get('primary_cta'))}\n\n")
        handle.write("## Decision\n\n")
        handle.write("- Recommended decision: approve for prospect promotion only if Daniel accepts the evidence packet.\n")
        handle.write(f"- Record approval: `{decision_command}`\n")
        handle.write(f"- After approval, promotion command: `{after_approve}`\n\n")
        handle.write("## Still Blocked\n\n")
        handle.write(f"- {still_blocked}\n")
        handle.write("- Promotion does not approve outreach.\n")
        handle.write("- Outreach requires separate compliance and send approval.\n\n")
        handle.write("## Current Permission Context\n\n")
        for action in ["Promote candidate to prospect", "Create remote GitHub issues", "Send or schedule outreach"]:
            row = permissions.get(action.casefold(), {})
            handle.write(f"- {action}: {clean(row.get('status'))} / {clean(row.get('blocked_until'))}\n")
    rows.append({
        "date": today(),
        "business": business,
        "rank": clean(priority_row.get("rank")),
        "approval_type": clean(item.get("approval_type")),
        "recommended_decision": "approve-for-prospect-promotion-only",
        "evidence_path": clean(item.get("source_path")),
        "decision_command": decision_command,
        "after_approve": after_approve,
        "still_blocked": still_blocked,
        "packet_path": rel(packet_path),
        "notes": "Decision packet only; no outreach, promotion, GitHub write, or publish action performed.",
    })

write_csv(p("approval_packets.csv"), rows, FIELDS)

index_path = p("approval_packets", f"{today()}.md")
with open(index_path, "w", encoding="utf-8") as handle:
    handle.write("# Approval Packets\n\n")
    handle.write(f"- Date: {today()}\n")
    handle.write(f"- Pending packet count: {len(rows)}\n")
    handle.write("- Safety: packets support human review only.\n\n")
    for row in rows:
        handle.write(f"- #{row['rank']} {row['business']}: {row['packet_path']}\n")

print(rel(index_path))
