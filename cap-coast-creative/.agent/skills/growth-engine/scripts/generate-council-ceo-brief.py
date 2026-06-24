#!/usr/bin/env python3
import os
from common import clean, p, read_csv, rel, today, write_csv

FIELDS = [
    "date",
    "brief_id",
    "priority",
    "decision_id",
    "council",
    "task_area",
    "boardroom_read",
    "strongest_argument",
    "strongest_objection",
    "uncomfortable_truth",
    "allowed_next_move",
    "blocked_actions",
    "daniel_decision_needed",
    "evidence_path",
    "status",
    "notes",
]

ACTION_LABELS = {
    "research-next-lane": "Run a research-only source-route test and log the result.",
    "approval-bottleneck": "Review approval packets and record approve, reject, or hold.",
    "outreach-readiness": "Wait for approved prospects, then regenerate drafts and pre-send checks.",
    "github-remote-issues": "Keep GitHub issue work local until remote write approval exists.",
    "concept-publication": "Keep concepts private and use them only for internal review.",
    "offer-model": "Keep the flat monthly model, but protect scope and claims.",
}

BLOCKED_ACTIONS = {
    "research-next-lane": "Contacting, following, liking, messaging, scraping behind login, or capturing weak evidence.",
    "approval-bottleneck": "Automatic promotion, outreach approval, proposal sending, or treating a council verdict as consent.",
    "outreach-readiness": "Email, SMS, DM, contact form, call, social post, scheduling, or follow-up.",
    "github-remote-issues": "Creating, editing, or pushing remote GitHub issues without exact approval.",
    "concept-publication": "Publishing, sending, or implying endorsement of private concept sites.",
    "offer-model": "Invoices, charges, signed proposal claims, revenue guarantees, or booked-revenue assumptions.",
}

DECISION_NEEDED = {
    "research-next-lane": "No Daniel decision needed for safe public research; Daniel approval needed before promotion or outreach.",
    "approval-bottleneck": "Daniel must decide approve, reject, or hold for each promotion packet.",
    "outreach-readiness": "Daniel must approve the prospect, exact copy, channel, contact basis, sender ID, and opt-out before send.",
    "github-remote-issues": "Daniel must explicitly approve any remote GitHub write.",
    "concept-publication": "Daniel must approve any client-facing publication, send, demo, hosting, or claim.",
    "offer-model": "Daniel must approve proposal sending, client promises, invoices, or charges.",
}

UNCOMFORTABLE_TRUTHS = {
    "research-next-lane": "The engine needs better source discipline more than it needs more broad searching.",
    "approval-bottleneck": "The approval bottleneck is intentional; removing it would make the engine less trustworthy.",
    "outreach-readiness": "Generic outreach readiness is false readiness if the prospect and contact basis are not approved.",
    "github-remote-issues": "A polished local command is still an external action when it touches GitHub remotely.",
    "concept-publication": "A pretty mockup can become reputational risk if the business did not ask to see it.",
    "offer-model": "Low upfront friction only works if scope, support load, and trust are controlled.",
}

STATUS_PRIORITY = {
    "blocked-awaiting-daniel-decision": 1,
    "blocked-pre-send": 2,
    "ready-for-research-only-test": 3,
    "ready-local-only": 4,
    "internal-only": 5,
    "advisory": 6,
}


def row_priority(debate):
    status = clean(debate.get("status"), "")
    return STATUS_PRIORITY.get(status, 9)


debates = sorted(read_csv(p("council_debates.csv")), key=row_priority)
quality = {clean(row.get("decision_id")): row for row in read_csv(p("council_quality_audit.csv"))}
gates = read_csv(p("council_decision_gates.csv"))
gate_map = {}
for gate in gates:
    gate_map.setdefault(clean(gate.get("decision_id")), []).append(gate)

rows = []
for index, debate in enumerate(debates, start=1):
    decision_id = clean(debate.get("decision_id"))
    quality_row = quality.get(decision_id, {})
    related_gates = gate_map.get(decision_id, [])
    blocked = [clean(gate.get("action")) for gate in related_gates if "blocked" in clean(gate.get("gate_status"), "")]
    allowed = [clean(gate.get("action")) for gate in related_gates if "allowed" in clean(gate.get("gate_status"), "")]
    quality_status = clean(quality_row.get("quality_status"), "missing-quality")
    boardroom_read = (
        f"{clean(debate.get('verdict'))}: {clean(debate.get('next_test'))} "
        f"Quality status: {quality_status}. "
        f"Allowed gates: {', '.join(allowed) if allowed else 'none'}."
    )
    rows.append({
        "date": today(),
        "brief_id": f"council-brief-{index}",
        "priority": str(index),
        "decision_id": decision_id,
        "council": clean(debate.get("council")),
        "task_area": clean(debate.get("task_area")),
        "boardroom_read": boardroom_read,
        "strongest_argument": clean(debate.get("best_case")),
        "strongest_objection": clean(debate.get("hard_pushback")),
        "uncomfortable_truth": UNCOMFORTABLE_TRUTHS.get(decision_id, "Use the council verdict as pressure, not permission."),
        "allowed_next_move": ACTION_LABELS.get(decision_id, clean(debate.get("next_test"))),
        "blocked_actions": BLOCKED_ACTIONS.get(decision_id, ", ".join(blocked) if blocked else "No external action is approved by this brief."),
        "daniel_decision_needed": DECISION_NEEDED.get(decision_id, "Daniel approval is required before any gated external action."),
        "evidence_path": clean(debate.get("evidence_path")),
        "status": "ready" if quality_status == "pass" else "needs-rework",
        "notes": "CEO council brief is advisory; it cannot approve promotion, outreach, remote GitHub writes, publishing, billing, or client-facing claims.",
    })

write_csv(p("council_ceo_brief.csv"), rows, FIELDS)

os.makedirs(p("councils"), exist_ok=True)
path = p("councils", f"ceo-brief-{today()}.md")
with open(path, "w", encoding="utf-8") as handle:
    handle.write("# Council CEO Brief\n\n")
    handle.write(f"- Date: {today()}\n")
    handle.write("- Purpose: turn council arguments into supervised CEO guidance without approving gated actions.\n")
    handle.write("- Safety: no outreach, promotion, publishing, remote GitHub write, billing, or client-facing action is approved here.\n\n")
    for row in rows:
        handle.write(f"## {row['priority']}. {row['council']} - {row['decision_id']}\n\n")
        handle.write(f"- Boardroom read: {row['boardroom_read']}\n")
        handle.write(f"- Strongest argument: {row['strongest_argument']}\n")
        handle.write(f"- Strongest objection: {row['strongest_objection']}\n")
        handle.write(f"- Uncomfortable truth: {row['uncomfortable_truth']}\n")
        handle.write(f"- Allowed next move: {row['allowed_next_move']}\n")
        handle.write(f"- Blocked actions: {row['blocked_actions']}\n")
        handle.write(f"- Daniel decision needed: {row['daniel_decision_needed']}\n")
        handle.write(f"- Evidence: {row['evidence_path']}\n\n")

print(rel(path))
