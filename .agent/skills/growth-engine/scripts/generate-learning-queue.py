#!/usr/bin/env python3
import os
from common import clean, p, read_csv, rel, today, write_csv

FIELDS = ["date", "learning_id", "source", "area", "proposal", "evidence", "target_artifact", "approval_required", "status", "safety_gate", "notes"]

scorecard = read_csv(p("improvement_scorecard.csv"))
attempts = read_csv(p("research_attempts.csv"))
experiments = read_csv(p("research_experiments.csv"))
council_debates = read_csv(p("council_debates.csv"))
approvals = read_csv(p("approval_queue.csv"))
prospects = read_csv(p("prospects.csv"))

failed_attempts = [row for row in attempts if clean(row.get("result")).startswith("no_")]
rows = []

if failed_attempts and experiments:
    rows.append({
        "date": today(),
        "learning_id": "research-route-discipline",
        "source": "research_attempts + research_experiments",
        "area": "prospecting",
        "proposal": "Prefer source-route experiments before broad regional search when prior attempts returned locality/background pages.",
        "evidence": f"{len(failed_attempts)} failed/no-social attempts / {len(experiments)} experiment routes",
        "target_artifact": ".agent/memory/semantic/LESSONS.md",
        "approval_required": "Daniel review before durable memory update",
        "status": "proposal-review",
        "safety_gate": "Learning proposal only; does not change memory or capture prospects.",
        "notes": "Useful if repeated failed routes keep producing locality pages.",
    })

needs_work = [row for row in scorecard if clean(row.get("status")) == "needs-work"]
for item in needs_work:
    rows.append({
        "date": today(),
        "learning_id": f"scorecard-{clean(item.get('area')).lower().replace(' ', '-')}",
        "source": "improvement_scorecard",
        "area": clean(item.get("area")),
        "proposal": clean(item.get("improvement_action")),
        "evidence": clean(item.get("evidence")),
        "target_artifact": ".agent/memory/working/OPERATOR_MANUAL.md",
        "approval_required": "Daniel review before changing operating rules",
        "status": "proposal-review",
        "safety_gate": "Scorecard learning does not approve blocked actions.",
        "notes": "Keep as an operational learning until repeated evidence justifies durable memory.",
    })

for debate in council_debates:
    if clean(debate.get("verdict")) in {"do-not-automate-promotion", "keep-local-only", "keep-private", "defer-until-prospect-approved"}:
        rows.append({
            "date": today(),
            "learning_id": f"council-{clean(debate.get('decision_id'))}",
            "source": "council_debates",
            "area": clean(debate.get("task_area")),
            "proposal": f"Preserve council verdict: {clean(debate.get('verdict'))}.",
            "evidence": clean(debate.get("hard_pushback")),
            "target_artifact": ".agent/protocols/permissions.md",
            "approval_required": "Daniel review before protocol changes",
            "status": "proposal-review",
            "safety_gate": "Council learning is advisory; does not approve external actions.",
            "notes": clean(debate.get("notes")),
        })

if approvals and not prospects:
    rows.append({
        "date": today(),
        "learning_id": "approval-bottleneck-review",
        "source": "approval_queue + prospects",
        "area": "approval-control",
        "proposal": "Add a weekly human review ritual for pending approval packets before expecting outreach or delivery progress.",
        "evidence": f"{len(approvals)} pending approvals / {len(prospects)} approved prospects",
        "target_artifact": ".agent/memory/working/OPERATOR_MANUAL.md",
        "approval_required": "Daniel review before operating manual update",
        "status": "proposal-review",
        "safety_gate": "Approval ritual proposal does not approve any candidate.",
        "notes": "This protects momentum without weakening approval gates.",
    })

write_csv(p("learning_queue.csv"), rows, FIELDS)

os.makedirs(p("learning_queue"), exist_ok=True)
path = p("learning_queue", f"{today()}.md")
with open(path, "w", encoding="utf-8") as handle:
    handle.write("# Learning Queue\n\n")
    handle.write(f"- Date: {today()}\n")
    handle.write("- Purpose: propose self-improvement changes without silently rewriting rules or memory.\n\n")
    for row in rows:
        handle.write(f"- {row['learning_id']}: {row['status']} / {row['proposal']} / Gate: {row['safety_gate']}\n")

print(rel(path))
