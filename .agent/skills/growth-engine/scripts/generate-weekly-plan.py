#!/usr/bin/env python3
import os
from datetime import date, timedelta
from common import p, read_csv, rel, today, write_csv

FIELDS = ["week_start", "day", "focus", "inputs", "outputs", "safety_gate", "done_definition", "notes"]

week_start = date.today() - timedelta(days=date.today().weekday())
source_plan = read_csv(p("source_plan.csv"))
research = read_csv(p("research_queue.csv"))
approvals = read_csv(p("approval_queue.csv"))
priority = read_csv(p("priority_board.csv"))
concepts = read_csv(p("private_concepts.csv"))
drafts = read_csv(p("outreach_drafts.csv"))
prospects = read_csv(p("prospects.csv"))

rows = [
    {
        "day": "Monday",
        "focus": "Discovery lanes and evidence gathering",
        "inputs": f"{len(source_plan)} source lanes / {len(research)} research tasks",
        "outputs": "Research attempts logged; only sourced candidates added to intake.",
        "safety_gate": "Research only; no contact or account interaction.",
        "done_definition": "Every checked lane has a source note or remains queued.",
        "notes": "Prioritize active lanes before covered-but-refresh lanes.",
    },
    {
        "day": "Tuesday",
        "focus": "Intake verification and priority review",
        "inputs": f"{len(priority)} priority items",
        "outputs": "Updated priority board and promotion candidates.",
        "safety_gate": "Ranking is not approval.",
        "done_definition": "Top candidates have evidence paths and next best action.",
        "notes": "Keep weak candidates in research-more.",
    },
    {
        "day": "Wednesday",
        "focus": "Private concepts and offer strategy",
        "inputs": f"{len(concepts)} private concepts",
        "outputs": "Concepts and strategy reviewed for top promotion candidates.",
        "safety_gate": "Do not publish or send concepts.",
        "done_definition": "Top candidate has a clear CTA, trust hook, and monthly fee.",
        "notes": "Use $0 upfront flat monthly positioning.",
    },
    {
        "day": "Thursday",
        "focus": "Approval review and GitHub planning",
        "inputs": f"{len(approvals)} approvals / {len(prospects)} approved prospects",
        "outputs": "Daniel decisions recorded; approved work can become tracked issues.",
        "safety_gate": "No promotion or remote GitHub issue creation without explicit approval.",
        "done_definition": "Each approval item is approved, rejected, or left pending with a reason.",
        "notes": "Promotion is still not outreach approval.",
    },
    {
        "day": "Friday",
        "focus": "Draft review, delivery planning, and retrospective",
        "inputs": f"{len(drafts)} outreach drafts",
        "outputs": "Drafts/proposals reviewed only for approved prospects; weekly retrospective updated.",
        "safety_gate": "Drafting is not sending.",
        "done_definition": "No unsent draft lacks opt-out wording or contact-basis notes.",
        "notes": "Do not send email, SMS, DM, forms, social posts, or calls without approval.",
    },
]

for row in rows:
    row["week_start"] = week_start.isoformat()

write_csv(p("weekly_plan.csv"), rows, FIELDS)

os.makedirs(p("weekly_plans"), exist_ok=True)
path = p("weekly_plans", f"{week_start.isoformat()}.md")
with open(path, "w", encoding="utf-8") as handle:
    handle.write("# Cap Coast Creative Weekly Execution Plan\n\n")
    handle.write(f"- Generated: {today()}\n")
    handle.write(f"- Week start: {week_start.isoformat()}\n")
    handle.write("- Safety: planning only. Approval gates remain active.\n\n")
    for row in rows:
        handle.write(f"## {row['day']}: {row['focus']}\n\n")
        handle.write(f"- Inputs: {row['inputs']}\n")
        handle.write(f"- Outputs: {row['outputs']}\n")
        handle.write(f"- Safety gate: {row['safety_gate']}\n")
        handle.write(f"- Done: {row['done_definition']}\n")
        handle.write(f"- Notes: {row['notes']}\n\n")

print(rel(path))
