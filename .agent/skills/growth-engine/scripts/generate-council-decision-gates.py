#!/usr/bin/env python3
import os
from common import clean, p, read_csv, rel, today, write_csv

FIELDS = ["date", "action", "council", "decision_id", "council_verdict", "action_status", "gate_status", "evidence", "required_before_action", "safety_gate", "notes"]

ACTION_TO_DECISION = {
    "Run safe prospect research": ("Prospect Research Council", "research-next-lane"),
    "Capture sourced intake candidate": ("Prospect Research Council", "research-next-lane"),
    "Promote candidate to prospect": ("Titan CEO Council", "approval-bottleneck"),
    "Create remote GitHub issues": ("GitHub Work Council", "github-remote-issues"),
    "Generate outreach drafts": ("Outreach Review Council", "outreach-readiness"),
    "Send or schedule outreach": ("Outreach Review Council", "outreach-readiness"),
    "Publish concepts or start delivery": ("Web Design Council", "concept-publication"),
}

debates = {clean(row.get("decision_id")): row for row in read_csv(p("council_debates.csv"))}
rows = []
for action in read_csv(p("action_permissions.csv")):
    action_name = clean(action.get("action"))
    council, decision_id = ACTION_TO_DECISION.get(action_name, ("Titan CEO Council", "approval-bottleneck"))
    debate = debates.get(decision_id, {})
    action_status = clean(action.get("status"))
    gate_status = "blocked-by-action-permission" if action_status.startswith("blocked") else "allowed-with-council-constraints"
    if not debate:
        gate_status = "blocked-missing-council-debate"
    if clean(debate.get("status")).startswith("blocked"):
        gate_status = "blocked-by-council-verdict"
    if action_name == "Capture sourced intake candidate" and action_status == "allowed":
        gate_status = "allowed-only-with-strong-public-evidence"
    rows.append({
        "date": today(),
        "action": action_name,
        "council": council,
        "decision_id": decision_id,
        "council_verdict": clean(debate.get("verdict"), "missing"),
        "action_status": action_status,
        "gate_status": gate_status,
        "evidence": clean(action.get("evidence")),
        "required_before_action": clean(action.get("blocked_until"), clean(debate.get("next_test"), "-")),
        "safety_gate": clean(action.get("safety_gate"), clean(debate.get("safety_gate"))),
        "notes": "Council verdict is advisory unless action permissions and Daniel approval gates also allow the action.",
    })

write_csv(p("council_decision_gates.csv"), rows, FIELDS)

os.makedirs(p("councils"), exist_ok=True)
path = p("councils", f"decision-gates-{today()}.md")
with open(path, "w", encoding="utf-8") as handle:
    handle.write("# Council Decision Gates\n\n")
    handle.write(f"- Date: {today()}\n")
    handle.write("- Purpose: bind action permissions to the council verdict that governs each action.\n\n")
    for row in rows:
        handle.write(f"- {row['action']}: {row['gate_status']} / {row['council']} / Verdict: {row['council_verdict']}\n")

print(rel(path))
