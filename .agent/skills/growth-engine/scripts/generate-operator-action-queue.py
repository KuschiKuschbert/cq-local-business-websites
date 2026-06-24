#!/usr/bin/env python3
import os
from common import clean, p, read_csv, rel, today, write_csv

FIELDS = [
    "date",
    "rank",
    "action_id",
    "category",
    "action",
    "owner",
    "status",
    "evidence",
    "safe_command_or_next_step",
    "blocked_until",
    "safety_gate",
    "source_path",
    "notes",
]


def add(rows, action_id, category, action, owner, status, evidence, next_step, blocked_until, safety_gate, source_path, notes):
    rows.append({
        "date": today(),
        "rank": "0",
        "action_id": action_id,
        "category": category,
        "action": action,
        "owner": owner,
        "status": status,
        "evidence": evidence,
        "safe_command_or_next_step": next_step,
        "blocked_until": blocked_until,
        "safety_gate": safety_gate,
        "source_path": source_path,
        "notes": notes,
    })


permissions = {clean(row.get("action")).casefold(): row for row in read_csv(p("action_permissions.csv"))}
approval_packets = read_csv(p("approval_packets.csv"))
approval_inbox = {clean(row.get("business")).casefold(): row for row in read_csv(p("approval_decision_inbox.csv"))}
research_experiments = read_csv(p("research_experiments.csv"))
source_pivots = read_csv(p("source_pivot_plan.csv"))
research_suppression = read_csv(p("research_suppression_list.csv"))
github_readiness = read_csv(p("github_readiness_audit.csv"))
pre_send = read_csv(p("pre_send_readiness.csv"))
weekly = read_csv(p("weekly_plan.csv"))
prospects = read_csv(p("prospects.csv"))

rows = []

research_permission = permissions.get("run safe prospect research", {})
if clean(research_permission.get("status")) == "allowed":
    experiment = next(
        (
            row
            for row in research_experiments
            if clean(row.get("status")) == "ready-to-test"
        ),
        research_experiments[0] if research_experiments else {},
    )
    add(
        rows,
        "research-next-experiment",
        "research",
        "Run the highest-ranked research experiment and log the result.",
        "Codex",
        "allowed-now",
        clean(experiment.get("query"), clean(research_permission.get("evidence"))),
        "Research public sources only; capture only strong public evidence or log a failed attempt.",
        "-",
        clean(research_permission.get("safety_gate")),
        ".agent/memory/working/research_experiments.csv",
        "No contact, login, form submission, DM, call, or social interaction.",
    )

for index, pivot in enumerate(source_pivots[:3], start=1):
    pivot_status = clean(pivot.get("status"))
    is_ready = pivot_status == "ready-for-pivot-research"
    add(
        rows,
        f"source-pivot-{index}",
        "research",
        f"Run source-family pivot research for {clean(pivot.get('business'))}.",
        "Codex",
        "allowed-now" if is_ready else "planned",
        clean(pivot.get("pivot_reason")),
        clean(pivot.get("primary_query")),
        "-" if is_ready else "A new public source family or stronger source appears.",
        clean(pivot.get("safe_next_action")),
        ".agent/memory/working/source_pivot_plan.csv",
        f"Pivot status: {pivot_status}. Pivot research is not capture, promotion, outreach, publishing, or approval.",
    )

for index, suppression in enumerate(research_suppression[:3], start=1):
    add(
        rows,
        f"research-suppression-{index}",
        "research",
        f"Avoid repeated weak search for {clean(suppression.get('business'))}.",
        "Codex",
        "planned",
        f"{clean(suppression.get('failed_attempts'))} failed attempts",
        clean(suppression.get("safe_next_action")),
        "A new source family or stronger public source appears.",
        clean(suppression.get("safety_gate")),
        ".agent/memory/working/research_suppression_list.csv",
        f"Replacement source family: {clean(suppression.get('replacement_source_family'))}. Suppression is not capture, promotion, outreach, publishing, or approval.",
    )

for packet in approval_packets:
    rank = clean(packet.get("rank"), "999")
    inbox = approval_inbox.get(clean(packet.get("business")).casefold(), {})
    add(
        rows,
        f"approval-{rank}-{clean(packet.get('business')).casefold().replace(' ', '-')}",
        "approval",
        f"Review promotion packet for {clean(packet.get('business'))}.",
        "Daniel",
        "needs-daniel-decision",
        clean(packet.get("evidence_path")),
        clean(inbox.get("approve_command"), clean(packet.get("decision_command"))),
        "Daniel records approve, reject, or hold.",
        "Promotion approval required; promotion is not outreach approval.",
        clean(inbox.get("packet_path"), clean(packet.get("packet_path"))),
        f"Reject: {clean(inbox.get('reject_command'), 'available in approval decision inbox')} / Hold: {clean(inbox.get('hold_command'), 'available in approval decision inbox')}. {clean(packet.get('still_blocked'))}",
    )

if github_readiness:
    add(
        rows,
        "github-local-review",
        "github",
        "Review local GitHub issue readiness.",
        "Daniel",
        "blocked-external-write",
        f"{len(github_readiness)} local readiness rows",
        "Review local issue drafts only.",
        "Daniel explicitly approves remote GitHub issue creation.",
        "No remote GitHub writes without exact approval.",
        ".agent/memory/working/github_readiness_audit.csv",
        "Local drafts are ready for review but not for remote execution.",
    )

if pre_send:
    add(
        rows,
        "outreach-pre-send-gate",
        "outreach",
        "Keep outreach blocked until approved prospects and compliance evidence exist.",
        "Daniel",
        "blocked",
        clean(pre_send[0].get("failure_reason"), f"{len(prospects)} approved prospects"),
        clean(pre_send[0].get("next_action"), "Review approval packets first."),
        "Approved prospect, compliant draft, sender ID, opt-out, contact basis, and exact send approval.",
        "No email, SMS, DM, forms, social posts, calls, or scheduling without approval.",
        ".agent/memory/working/pre_send_readiness.csv",
        "This gate remains blocked even if copy exists.",
    )

for day in weekly[:2]:
    add(
        rows,
        f"weekly-{clean(day.get('day')).casefold()}",
        "operations",
        f"{clean(day.get('day'))}: {clean(day.get('focus'))}",
        "Codex",
        "planned",
        clean(day.get("inputs")),
        clean(day.get("outputs")),
        "-",
        clean(day.get("safety_gate")),
        ".agent/memory/working/weekly_plan.csv",
        clean(day.get("done_definition")),
    )

status_weight = {
    "allowed-now": 0,
    "needs-daniel-decision": 1,
    "planned": 2,
    "blocked-external-write": 3,
    "blocked": 4,
}
rows.sort(key=lambda row: (status_weight.get(row["status"], 9), row["category"], row["action"]))
for index, row in enumerate(rows, start=1):
    row["rank"] = str(index)

write_csv(p("operator_action_queue.csv"), rows, FIELDS)

os.makedirs(p("operator_action_queue"), exist_ok=True)
path = p("operator_action_queue", f"{today()}.md")
with open(path, "w", encoding="utf-8") as handle:
    handle.write("# Operator Action Queue\n\n")
    handle.write(f"- Date: {today()}\n")
    handle.write("- Purpose: one ranked queue of safe next actions, Daniel decisions, and blocked external actions.\n")
    handle.write("- Safety: this queue cannot approve outreach, promotion, remote GitHub writes, publishing, billing, or client-facing claims.\n\n")
    for row in rows:
        handle.write(f"## {row['rank']}. {row['action']}\n\n")
        handle.write(f"- Status: {row['status']}\n")
        handle.write(f"- Owner: {row['owner']}\n")
        handle.write(f"- Evidence: {row['evidence']}\n")
        handle.write(f"- Next step: {row['safe_command_or_next_step']}\n")
        handle.write(f"- Blocked until: {row['blocked_until']}\n")
        handle.write(f"- Gate: {row['safety_gate']}\n")
        handle.write(f"- Source: {row['source_path']}\n\n")

print(rel(path))
