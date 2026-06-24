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
    "social_signal",
    "website_gap",
    "proposed_opportunity",
    "evidence_grade",
    "review_focus",
    "evidence_path",
    "packet_path",
    "safety_gate",
    "notes",
]

priority = {clean(row.get("business")).casefold(): row for row in read_csv(p("priority_board.csv"))}
packets = {clean(row.get("business")).casefold(): row for row in read_csv(p("approval_packets.csv"))}
intake = {clean(row.get("business")).casefold(): row for row in read_csv(p("prospect_intake.csv"))}
rows = []


def evidence_grade(row):
    website = clean(row.get("website"), "")
    socials = clean(row.get("socials"), "")
    gap = clean(row.get("observed_website_gap"), "")
    if socials and not website:
        return "A - verified social with missing owned website"
    if socials and website and gap:
        return "B - verified social with website improvement opportunity"
    if socials:
        return "C - verified social; review website gap manually"
    return "D - evidence needs review before promotion"


def review_focus(row):
    website = clean(row.get("website"), "")
    if website:
        return "Decide whether the observed website gap is commercially strong enough for prospect promotion."
    return "Decide whether the missing owned website is enough to justify prospect promotion."


for item in read_csv(p("approval_queue.csv")):
    business = clean(item.get("business"))
    key = business.casefold()
    rank = clean(priority.get(key, {}).get("rank"), "999")
    packet_path = clean(packets.get(key, {}).get("packet_path"), f".agent/memory/working/approval_packets/{slug(business)}.md")
    intake_row = intake.get(key, {})
    base = f'python3 .agent/skills/growth-engine/scripts/record-approval-decision.py --business "{business}" --decided-by "Daniel"'
    rows.append({
        "date": today(),
        "rank": rank,
        "business": business,
        "approval_type": clean(item.get("approval_type")),
        "recommended_decision": "approve only if Daniel accepts evidence for prospect promotion; otherwise hold or reject",
        "approve_command": f'{base} --decision approve --notes "Approved for prospect promotion only."',
        "reject_command": f'{base} --decision reject --notes "Rejected for prospect promotion."',
        "hold_command": f'{base} --decision hold --notes "Hold for more evidence before promotion."',
        "approve_effect": clean(item.get("safe_command")),
        "reject_effect": "Leaves the candidate out of prospects.csv unless new evidence changes the decision.",
        "hold_effect": "Keeps the item pending and routes it back to evidence review.",
        "social_signal": clean(intake_row.get("observed_social_signal")),
        "website_gap": clean(intake_row.get("observed_website_gap")),
        "proposed_opportunity": clean(intake_row.get("proposed_hook")),
        "evidence_grade": evidence_grade(intake_row),
        "review_focus": review_focus(intake_row),
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
        handle.write(f"- Social signal: {row['social_signal']}\n")
        handle.write(f"- Website gap: {row['website_gap']}\n")
        handle.write(f"- Proposed opportunity: {row['proposed_opportunity']}\n")
        handle.write(f"- Evidence grade: {row['evidence_grade']}\n")
        handle.write(f"- Review focus: {row['review_focus']}\n")
        handle.write(f"- Evidence: {row['evidence_path']}\n")
        handle.write(f"- Packet: {row['packet_path']}\n")
        handle.write(f"- Approve: `{row['approve_command']}`\n")
        handle.write(f"- Reject: `{row['reject_command']}`\n")
        handle.write(f"- Hold: `{row['hold_command']}`\n")
        handle.write(f"- Gate: {row['safety_gate']}\n\n")

print(rel(path))
