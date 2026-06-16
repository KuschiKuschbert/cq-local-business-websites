#!/usr/bin/env python3
import os
from common import ROOT, clean, p, read_csv, rel, today, write_csv

FIELDS = ["date", "business", "readiness_status", "approval_packet", "issue_draft", "execution_plan", "command_status", "failure_reason", "next_action", "notes"]

packets = {clean(row.get("business")).casefold(): row for row in read_csv(p("approval_packets.csv"))}
drafts = {clean(row.get("business")).casefold(): row for row in read_csv(p("github_issue_drafts.csv"))}
plans = {clean(row.get("business")).casefold(): row for row in read_csv(p("github_execution_plan.csv"))}
businesses = sorted(set(packets) | set(drafts) | set(plans))

rows = []
for key in businesses:
    packet = packets.get(key, {})
    draft = drafts.get(key, {})
    plan = plans.get(key, {})
    business = clean(packet.get("business"), clean(draft.get("business"), clean(plan.get("business"), key)))
    failures = []
    draft_path = clean(draft.get("draft_path"), "")
    command_path = clean(plan.get("command_path"), "")
    if not packet:
        failures.append("approval packet missing")
    if not draft:
        failures.append("issue draft missing")
    if not plan:
        failures.append("execution plan row missing")
    if draft and not os.path.exists(os.path.join(ROOT, draft_path)):
        failures.append("issue draft file missing")
    if plan and not os.path.exists(os.path.join(ROOT, command_path)):
        failures.append("command artifact missing")
    if draft and plan and clean(draft.get("issue_title")) != clean(plan.get("issue_title")):
        failures.append("issue title mismatch")
    if draft and plan and clean(draft.get("labels")) != clean(plan.get("labels")):
        failures.append("label mismatch")
    if plan and clean(plan.get("approval_status")) != "not-approved-not-run":
        failures.append("execution plan is not locked")
    status = "ready-local-only" if not failures else "blocked-local-plan-mismatch"
    rows.append({
        "date": today(),
        "business": business,
        "readiness_status": status,
        "approval_packet": clean(packet.get("packet_path"), "-"),
        "issue_draft": draft_path or "-",
        "execution_plan": command_path or "-",
        "command_status": clean(plan.get("approval_status"), "missing"),
        "failure_reason": "; ".join(failures) if failures else "-",
        "next_action": "Daniel may review local issue draft; remote creation still needs explicit approval." if not failures else "Regenerate GitHub issue drafts and execution plan before review.",
        "notes": "Readiness audit only; no GitHub command executed.",
    })

if not rows:
    rows.append({
        "date": today(),
        "business": "pipeline-level",
        "readiness_status": "no-pending-approval-issues",
        "approval_packet": "-",
        "issue_draft": "-",
        "execution_plan": "-",
        "command_status": "not-applicable",
        "failure_reason": "-",
        "next_action": "Generate approval packets before preparing GitHub issue drafts.",
        "notes": "Readiness audit only; no GitHub command executed.",
    })

write_csv(p("github_readiness_audit.csv"), rows, FIELDS)

os.makedirs(p("github_readiness_audits"), exist_ok=True)
path = p("github_readiness_audits", f"{today()}.md")
with open(path, "w", encoding="utf-8") as handle:
    handle.write("# GitHub Readiness Audit\n\n")
    handle.write(f"- Date: {today()}\n")
    handle.write("- Safety: local consistency check only; no GitHub command executed.\n\n")
    for row in rows:
        handle.write(f"- {row['business']}: {row['readiness_status']} / Command: {row['command_status']} / Missing: {row['failure_reason']}\n")

print(rel(path))
