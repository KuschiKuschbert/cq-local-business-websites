#!/usr/bin/env python3
import os
from common import clean, p, rel, read_csv, slug, today, write_csv

FIELDS = [
    "date",
    "rank",
    "business",
    "decision_type",
    "recommended_decision",
    "evidence_path",
    "approval_packet",
    "private_concept",
    "github_issue_draft",
    "github_status",
    "social_signal",
    "website_gap",
    "proposed_opportunity",
    "evidence_grade",
    "review_focus",
    "approve_command",
    "reject_command",
    "hold_command",
    "after_approve",
    "still_blocked",
    "safety_gate",
    "notes",
]

inbox = read_csv(p("approval_decision_inbox.csv"))
packets = {clean(row.get("business")).casefold(): row for row in read_csv(p("approval_packets.csv"))}
concepts = {clean(row.get("business")).casefold(): row for row in read_csv(p("private_concepts.csv"))}
github = {clean(row.get("business")).casefold(): row for row in read_csv(p("github_readiness_audit.csv"))}
intake = {clean(row.get("business")).casefold(): row for row in read_csv(p("prospect_intake.csv"))}

rows = []
for item in inbox:
    business = clean(item.get("business"))
    key = business.casefold()
    packet = packets.get(key, {})
    concept = concepts.get(key, {})
    github_row = github.get(key, {})
    intake_row = intake.get(key, {})
    rows.append({
        "date": today(),
        "rank": clean(item.get("rank"), "999"),
        "business": business,
        "decision_type": clean(item.get("approval_type")),
        "recommended_decision": clean(item.get("recommended_decision")),
        "evidence_path": clean(item.get("evidence_path")),
        "approval_packet": clean(item.get("packet_path"), clean(packet.get("packet_path"))),
        "private_concept": clean(concept.get("concept_path"), f".agent/memory/working/private_concepts/{slug(business)}/index.html"),
        "github_issue_draft": clean(github_row.get("issue_draft"), "-"),
        "github_status": clean(github_row.get("readiness_status"), "not-generated"),
        "social_signal": clean(item.get("social_signal"), clean(intake_row.get("observed_social_signal"))),
        "website_gap": clean(item.get("website_gap"), clean(intake_row.get("observed_website_gap"))),
        "proposed_opportunity": clean(item.get("proposed_opportunity"), clean(intake_row.get("proposed_hook"))),
        "evidence_grade": clean(item.get("evidence_grade")),
        "review_focus": clean(item.get("review_focus")),
        "approve_command": clean(item.get("approve_command")),
        "reject_command": clean(item.get("reject_command")),
        "hold_command": clean(item.get("hold_command")),
        "after_approve": clean(item.get("approve_effect"), clean(packet.get("after_approve"))),
        "still_blocked": clean(packet.get("still_blocked"), "Outreach send, remote GitHub writes, publishing, hosting, billing, and client-facing promises."),
        "safety_gate": "Decision cockpit is advisory; it does not approve promotion, outreach, publishing, remote GitHub writes, billing, or client-facing action.",
        "notes": "Use this cockpit to review evidence and record a local approve/reject/hold decision only.",
    })

rows.sort(key=lambda row: int(row["rank"]) if row["rank"].isdigit() else 999)
write_csv(p("decision_cockpit.csv"), rows, FIELDS)

os.makedirs(p("decision_cockpit"), exist_ok=True)
path = p("decision_cockpit", f"{today()}.md")
with open(path, "w", encoding="utf-8") as handle:
    handle.write("# Decision Cockpit\n\n")
    handle.write(f"- Date: {today()}\n")
    handle.write("- Purpose: one review surface for pending promotion decisions, evidence, concepts, GitHub local drafts, and follow-on gates.\n")
    handle.write("- Safety: advisory only. Recording a decision is not promotion, outreach, publishing, remote GitHub write, billing, or client-facing approval.\n\n")
    if not rows:
        handle.write("No pending decision rows.\n")
    for row in rows:
        handle.write(f"## #{row['rank']} {row['business']}\n\n")
        handle.write(f"- Recommended decision: {row['recommended_decision']}\n")
        handle.write(f"- Social signal: {row['social_signal']}\n")
        handle.write(f"- Website gap: {row['website_gap']}\n")
        handle.write(f"- Proposed opportunity: {row['proposed_opportunity']}\n")
        handle.write(f"- Evidence grade: {row['evidence_grade']}\n")
        handle.write(f"- Review focus: {row['review_focus']}\n")
        handle.write(f"- Evidence: {row['evidence_path']}\n")
        handle.write(f"- Approval packet: {row['approval_packet']}\n")
        handle.write(f"- Private concept: {row['private_concept']}\n")
        handle.write(f"- GitHub draft: {row['github_issue_draft']} ({row['github_status']})\n")
        handle.write(f"- Approve decision record: `{row['approve_command']}`\n")
        handle.write(f"- Reject decision record: `{row['reject_command']}`\n")
        handle.write(f"- Hold decision record: `{row['hold_command']}`\n")
        handle.write(f"- After approve: {row['after_approve']}\n")
        handle.write(f"- Still blocked: {row['still_blocked']}\n")
        handle.write(f"- Gate: {row['safety_gate']}\n\n")

print(rel(path))
