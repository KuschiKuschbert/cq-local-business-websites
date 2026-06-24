#!/usr/bin/env python3
import os
from common import p, rel, today, write_csv

FIELDS = ["date", "automation_id", "name", "kind", "status", "schedule", "workspace", "safety_gate", "notes"]
AUTOMATION_DIR = os.path.expanduser("~/.codex/automations")
TARGETS = ["cap-coast-prospect-scan", "monitor-cq-outreach-replies"]


def read_automation(automation_id):
    path = os.path.join(AUTOMATION_DIR, automation_id, "automation.toml")
    if not os.path.exists(path):
        return None
    data = {}
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = [part.strip() for part in line.split("=", 1)]
            if value.startswith("[") and value.endswith("]"):
                data[key] = [
                    item.strip().strip('"')
                    for item in value[1:-1].split(",")
                    if item.strip()
                ]
            else:
                data[key] = value.strip('"')
    return data


rows = []
for automation_id in TARGETS:
    item = read_automation(automation_id)
    if not item:
        rows.append({
            "date": today(),
            "automation_id": automation_id,
            "name": automation_id,
            "kind": "missing",
            "status": "missing",
            "schedule": "-",
            "workspace": "-",
            "safety_gate": "Missing automation cannot run.",
            "notes": "Create or restore the automation before relying on recurring behavior.",
        })
        continue
    prompt = item.get("prompt", "").lower()
    if automation_id == "cap-coast-prospect-scan":
        gated = all(phrase in prompt for phrase in ["do not send", "capture-intake-candidate", "log-research-attempt"])
        gate_text = "Research-only with capture/log gates."
    else:
        gated = all(phrase in prompt for phrase in ["do not send", "report", "do not"])
        gate_text = "Report-only; no send/contact actions."
    rows.append({
        "date": today(),
        "automation_id": automation_id,
        "name": item.get("name", automation_id),
        "kind": item.get("kind", "-"),
        "status": item.get("status", "-"),
        "schedule": item.get("rrule", "-"),
        "workspace": "; ".join(item.get("cwds", [])) if item.get("cwds") else item.get("target_thread_id", "-"),
        "safety_gate": gate_text if gated else "Review prompt safety language before relying on automation.",
        "notes": "Reads actual Codex automation config; does not create, update, or run automations.",
    })

write_csv(p("automation_status.csv"), rows, FIELDS)

os.makedirs(p("automation_status"), exist_ok=True)
path = p("automation_status", f"{today()}.md")
with open(path, "w", encoding="utf-8") as handle:
    handle.write("# Automation Status\n\n")
    handle.write(f"- Date: {today()}\n")
    handle.write("- Safety: status report only; does not run automation.\n\n")
    for row in rows:
        handle.write(f"- {row['automation_id']}: {row['status']} / {row['schedule']} / Gate: {row['safety_gate']}\n")

print(rel(path))
