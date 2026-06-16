#!/usr/bin/env python3
import os
import sys
from common import clean, p, read_csv, rel, today, write_csv

FIELDS = ["date", "invariant", "status", "evidence", "required_action", "notes"]

intake = read_csv(p("prospect_intake.csv"))
decisions = read_csv(p("approval_decisions.csv"))
prospects = read_csv(p("prospects.csv"))
outreach = read_csv(p("outreach_log.csv"))
drafts = read_csv(p("outreach_drafts.csv"))
playbooks = read_csv(p("outreach_playbook_library.csv"))
compliance = read_csv(p("contact_compliance.csv"))
delivery = read_csv(p("delivery_readiness.csv"))
pre_send = read_csv(p("pre_send_readiness.csv"))
approval_inbox = read_csv(p("approval_decision_inbox.csv"))
decision_cockpit = read_csv(p("decision_cockpit.csv"))
post_approval = read_csv(p("post_approval_workflow.csv"))
github_plan = read_csv(p("github_execution_plan.csv"))
github_readiness = read_csv(p("github_readiness_audit.csv"))
council_decision_gates = read_csv(p("council_decision_gates.csv"))
council_quality = read_csv(p("council_quality_audit.csv"))
council_brief = read_csv(p("council_ceo_brief.csv"))
regional_heatmap = read_csv(p("regional_coverage_heatmap.csv"))
source_pivots = read_csv(p("source_pivot_plan.csv"))
research_suppression = read_csv(p("research_suppression_list.csv"))
operator_queue = read_csv(p("operator_action_queue.csv"))
learning_queue = read_csv(p("learning_queue.csv"))
promotion_log = read_csv(p("promotion_log.csv"))

approved = {
    clean(row.get("business")).casefold()
    for row in decisions
    if row.get("approval_type") == "promotion" and row.get("decision") == "approve"
}
prospect_names = {clean(row.get("business")).casefold() for row in prospects}
intake_names = {clean(row.get("business")).casefold() for row in intake}

checks = []

noncanonical_approvals = sorted(
    f"{clean(row.get('business'))}:{clean(row.get('approval_type'))}"
    for row in decisions
    if clean(row.get("approval_type")).casefold() != "promotion"
)
checks.append({
    "invariant": "Approval decisions use canonical promotion type",
    "status": "pass" if not noncanonical_approvals else "fail",
    "evidence": f"{len(decisions)} approval decision rows",
    "required_action": "Normalize approval_type values before promotion or permission checks.",
    "notes": ", ".join(noncanonical_approvals) if noncanonical_approvals else "Approval decision types are canonical.",
})

unapproved_prospects = sorted(name for name in prospect_names if name not in approved)
checks.append({
    "invariant": "Prospects require recorded approval",
    "status": "pass" if not unapproved_prospects else "fail",
    "evidence": f"{len(prospects)} prospects / {len(approved)} recorded promotion approvals",
    "required_action": "Remove or investigate prospects without matching approval decision.",
    "notes": ", ".join(unapproved_prospects) if unapproved_prospects else "All prospect rows are approval-backed or there are no prospects.",
})

unknown_prospects = sorted(name for name in prospect_names if name not in intake_names)
checks.append({
    "invariant": "Prospects must originate from staged intake",
    "status": "pass" if not unknown_prospects else "fail",
    "evidence": f"{len(prospects)} prospects / {len(intake)} intake rows",
    "required_action": "Investigate any prospect not present in staged intake.",
    "notes": ", ".join(unknown_prospects) if unknown_prospects else "Prospect origin invariant holds.",
})

unsafe_outreach = [
    row for row in outreach
    if clean(row.get("status")).casefold() not in {"draft", "planned", "approved-but-unsent"}
    and not clean(row.get("approved_by"), "")
]
checks.append({
    "invariant": "Outreach requires explicit approval",
    "status": "pass" if not unsafe_outreach else "fail",
    "evidence": f"{len(outreach)} outreach log rows",
    "required_action": "Do not send; add approval evidence or correct the log.",
    "notes": "No sent outreach rows without approval." if not unsafe_outreach else "Unsafe outreach rows detected.",
})

bad_github_plan = [row for row in github_plan if clean(row.get("approval_status")) != "not-approved-not-run"]
checks.append({
    "invariant": "GitHub plan must not be runnable by default",
    "status": "pass" if not bad_github_plan else "fail",
    "evidence": f"{len(github_plan)} GitHub execution plan rows",
    "required_action": "Reset GitHub plan rows to not-approved-not-run unless explicit execution approval exists.",
    "notes": "All GitHub commands remain local plans." if not bad_github_plan else "GitHub execution rows have unsafe status.",
})

bad_github_readiness = [
    row for row in github_readiness
    if clean(row.get("command_status")) not in {"not-approved-not-run", "not-applicable"}
]
checks.append({
    "invariant": "GitHub readiness audit must stay local-only",
    "status": "pass" if not bad_github_readiness else "fail",
    "evidence": f"{len(github_readiness)} GitHub readiness rows",
    "required_action": "Reset readiness and execution plan rows unless Daniel explicitly approved remote issue creation.",
    "notes": "GitHub readiness rows are local-only." if not bad_github_readiness else "GitHub readiness contains an executable status.",
})

bad_council_gates = [
    row for row in council_decision_gates
    if clean(row.get("gate_status")) in {"allowed-with-council-constraints", "allowed-only-with-strong-public-evidence"}
    and clean(row.get("action")) not in {"Run safe prospect research", "Capture sourced intake candidate"}
]
checks.append({
    "invariant": "Council gates cannot unlock external actions",
    "status": "pass" if not bad_council_gates else "fail",
    "evidence": f"{len(council_decision_gates)} council decision gate rows",
    "required_action": "Reset any council gate that appears to allow promotion, outreach, GitHub writes, publishing, delivery, or billing.",
    "notes": "Council gates only allow research/capture under existing evidence rules." if not bad_council_gates else "Unsafe council gate allowance detected.",
})

bad_council_quality = [row for row in council_quality if clean(row.get("quality_status")) != "pass"]
checks.append({
    "invariant": "Council debates must pass quality audit",
    "status": "pass" if not bad_council_quality else "fail",
    "evidence": f"{len(council_quality)} council quality rows",
    "required_action": "Regenerate council debates before using them to influence action gates.",
    "notes": "Council debates pass quality audit." if not bad_council_quality else "Council debate quality issues detected.",
})

unsafe_brief_phrases = (
    "send outreach now",
    "schedule outreach now",
    "publish now",
    "create remote github issue now",
    "charge now",
    "invoice now",
    "client-facing action approved",
    "approval not required",
)
unsafe_council_brief = []
for row in council_brief:
    decision_text = clean(row.get("daniel_decision_needed"), "").casefold()
    allowed_text = clean(row.get("allowed_next_move"), "").casefold()
    notes_text = clean(row.get("notes"), "").casefold()
    if decision_text in {"", "-", "none", "not needed", "no approval needed"}:
        unsafe_council_brief.append(row)
        continue
    if any(phrase in allowed_text for phrase in unsafe_brief_phrases):
        unsafe_council_brief.append(row)
        continue
    if "advisory" not in notes_text or "cannot approve" not in notes_text:
        unsafe_council_brief.append(row)
checks.append({
    "invariant": "Council CEO brief cannot approve gated actions",
    "status": "pass" if not unsafe_council_brief else "fail",
    "evidence": f"{len(council_brief)} council CEO brief rows",
    "required_action": "Regenerate the council CEO brief so it reports allowed moves, blocked actions, and Daniel decisions without granting approval.",
    "notes": "CEO brief remains advisory only." if not unsafe_council_brief else "Unsafe council brief approval language detected.",
})

unsafe_source_pivots = [
    row for row in source_pivots
    if "research only" not in clean(row.get("safe_next_action"), "").casefold()
    or any(
        phrase in " ".join([
            row.get("safe_next_action", ""),
            row.get("notes", ""),
            row.get("status", ""),
        ]).casefold()
        for phrase in ["approve promotion", "send outreach now", "publish now", "invoice now", "charge now", "run remote github"]
    )
]
checks.append({
    "invariant": "Source pivot plan stays research-only",
    "status": "pass" if not unsafe_source_pivots else "fail",
    "evidence": f"{len(source_pivots)} source pivot rows",
    "required_action": "Regenerate source pivot plan so pivot queries cannot imply capture, promotion, outreach, GitHub, publishing, billing, or client-facing approval.",
    "notes": "Source pivots are research-only." if not unsafe_source_pivots else "Unsafe source pivot language detected.",
})

unsafe_regional_heatmap = [
    row for row in regional_heatmap
    if any(
        phrase in " ".join([
            row.get("safe_next_action", ""),
            row.get("safety_gate", ""),
            row.get("notes", ""),
        ]).casefold()
        for phrase in ["approve promotion", "send outreach now", "publish now", "invoice now", "charge now", "run remote github"]
    )
    or "research-only" not in clean(row.get("safety_gate"), "").casefold()
]
checks.append({
    "invariant": "Regional coverage heatmap stays research-only",
    "status": "pass" if not unsafe_regional_heatmap else "fail",
    "evidence": f"{len(regional_heatmap)} regional coverage rows",
    "required_action": "Regenerate heatmap so it only recommends safe public research and cannot approve capture, promotion, outreach, publishing, billing, or remote GitHub writes.",
    "notes": "Regional heatmap only prioritizes research lanes." if not unsafe_regional_heatmap else "Unsafe regional heatmap language detected.",
})

unsafe_research_suppression = [
    row for row in research_suppression
    if any(
        phrase in " ".join([
            row.get("safe_next_action", ""),
            row.get("safety_gate", ""),
            row.get("notes", ""),
            row.get("status", ""),
        ]).casefold()
        for phrase in ["approve promotion", "send outreach now", "publish now", "invoice now", "charge now", "run remote github"]
    )
    or "advisory" not in clean(row.get("safety_gate"), "").casefold()
]
checks.append({
    "invariant": "Research suppression list stays advisory and research-only",
    "status": "pass" if not unsafe_research_suppression else "fail",
    "evidence": f"{len(research_suppression)} suppressed repeat-search rows",
    "required_action": "Regenerate suppression rows so they only steer public research and cannot approve capture, promotion, outreach, publishing, billing, or remote GitHub writes.",
    "notes": "Suppression rows only steer future research." if not unsafe_research_suppression else "Unsafe research suppression language detected.",
})

unsafe_operator_queue = [
    row for row in operator_queue
    if clean(row.get("status")) == "allowed-now"
    and clean(row.get("category")) not in {"research", "operations"}
]
checks.append({
    "invariant": "Operator queue cannot allow gated external actions",
    "status": "pass" if not unsafe_operator_queue else "fail",
    "evidence": f"{len(operator_queue)} operator queue rows",
    "required_action": "Regenerate operator queue so promotion, outreach, remote GitHub writes, publishing, billing, and client-facing actions are never allowed-now.",
    "notes": "Operator queue only allows research/local planning now." if not unsafe_operator_queue else "Unsafe allowed-now operator queue row detected.",
})

unsafe_approval_inbox = [
    row for row in approval_inbox
    if not clean(row.get("approve_command"), "").startswith("python3 .agent/skills/growth-engine/scripts/record-approval-decision.py")
    or not clean(row.get("reject_command"), "").startswith("python3 .agent/skills/growth-engine/scripts/record-approval-decision.py")
    or not clean(row.get("hold_command"), "").startswith("python3 .agent/skills/growth-engine/scripts/record-approval-decision.py")
    or not all(
        term in clean(row.get("safety_gate"), "").casefold()
        for term in ["not", "outreach", "publishing", "remote github", "billing", "client-facing"]
    )
]
checks.append({
    "invariant": "Approval decision inbox offers safe approve reject hold choices",
    "status": "pass" if not unsafe_approval_inbox else "fail",
    "evidence": f"{len(approval_inbox)} approval decision inbox rows",
    "required_action": "Regenerate approval decision inbox so every row has approve/reject/hold local decision commands and a clear non-outreach safety gate.",
    "notes": "Approval inbox decisions remain local and separate from outreach." if not unsafe_approval_inbox else "Unsafe approval inbox row detected.",
})

unsafe_decision_cockpit = [
    row for row in decision_cockpit
    if not all(
        clean(row.get(command), "").startswith("python3 .agent/skills/growth-engine/scripts/record-approval-decision.py")
        for command in ["approve_command", "reject_command", "hold_command"]
    )
    or "advisory" not in clean(row.get("safety_gate"), "").casefold()
    or any(
        phrase in " ".join([
            row.get("safety_gate", ""),
            row.get("notes", ""),
        ]).casefold()
        for phrase in ["send outreach now", "publish now", "invoice now", "charge now", "run remote github"]
    )
]
checks.append({
    "invariant": "Decision cockpit stays advisory and local",
    "status": "pass" if not unsafe_decision_cockpit else "fail",
    "evidence": f"{len(decision_cockpit)} cockpit decision rows",
    "required_action": "Regenerate decision cockpit so it only exposes local approve/reject/hold decision recording and does not approve promotion, outreach, publishing, billing, or remote GitHub writes.",
    "notes": "Decision cockpit is a review surface, not permission." if not unsafe_decision_cockpit else "Unsafe cockpit row detected.",
})

unsafe_post_approval = [
    row for row in post_approval
    if any(
        phrase in " ".join([
            row.get("safe_command_or_action", ""),
            row.get("safety_gate", ""),
            row.get("notes", ""),
        ]).casefold()
        for phrase in ["send outreach now", "publish now", "invoice now", "charge now", "run remote github"]
    )
    or (
        clean(row.get("step_order")) == "2"
        and "promote-intake.py" not in clean(row.get("safe_command_or_action"), "")
    )
    or (
        clean(row.get("step_order")) == "2"
        and "approval" not in clean(row.get("blocked_until"), "").casefold()
    )
]
checks.append({
    "invariant": "Post-approval workflow stays gated and local",
    "status": "pass" if not unsafe_post_approval else "fail",
    "evidence": f"{len(post_approval)} workflow rows",
    "required_action": "Regenerate post-approval workflow so it maps local steps only, keeps external actions blocked, and requires recorded approval before promotion.",
    "notes": "Post-approval workflow is an advisory sequence only." if not unsafe_post_approval else "Unsafe post-approval workflow row detected.",
})

unsafe_learning = [
    row for row in learning_queue
    if clean(row.get("approval_required")).casefold() in {"", "-", "none", "not required"}
    or clean(row.get("status")).casefold() not in {"proposal-review", "rejected", "approved-for-manual-update"}
]
checks.append({
    "invariant": "Learning queue cannot mutate rules without review",
    "status": "pass" if not unsafe_learning else "fail",
    "evidence": f"{len(learning_queue)} learning proposal rows",
    "required_action": "Restore proposal-review status and explicit Daniel review requirement before any memory/protocol update.",
    "notes": "Learning queue items are review-gated." if not unsafe_learning else "Unsafe learning queue item detected.",
})

orphaned_drafts = sorted(clean(row.get("business")) for row in drafts if clean(row.get("business")).casefold() not in prospect_names)
checks.append({
    "invariant": "Outreach drafts require approved prospects",
    "status": "pass" if not orphaned_drafts else "fail",
    "evidence": f"{len(drafts)} draft rows / {len(prospects)} prospects",
    "required_action": "Delete or regenerate orphaned draft rows.",
    "notes": ", ".join(orphaned_drafts) if orphaned_drafts else "Draft/prospect relationship holds.",
})

unsafe_playbooks = []
for row in playbooks:
    text = " ".join([
        clean(row.get("safe_message_template"), ""),
        clean(row.get("follow_up_template"), ""),
        clean(row.get("required_personalization"), ""),
        clean(row.get("blocked_until"), ""),
        clean(row.get("safety_gate"), ""),
    ]).casefold()
    template = clean(row.get("safe_message_template"), "")
    if "[" not in template or "]" not in template:
        unsafe_playbooks.append(row)
        continue
    if any(
        phrase in text
        for phrase in [
            "send now",
            "schedule now",
            "approval not required",
            "contact basis not required",
        ]
    ):
        unsafe_playbooks.append(row)
        continue
    if not all(
        term in text
        for term in [
            "approved prospect",
            "contact basis",
            "opt-out",
            "sender identity",
            "exact daniel approval",
            "manual send",
        ]
    ):
        unsafe_playbooks.append(row)
checks.append({
    "invariant": "Outreach playbook library stays generic and gated",
    "status": "pass" if not unsafe_playbooks else "fail",
    "evidence": f"{len(playbooks)} generic playbook rows",
    "required_action": "Regenerate playbooks so every row uses placeholders and requires prospect approval, contact basis, opt-out, sender identity, exact Daniel approval, and manual send.",
    "notes": "Playbooks are generic templates, not approved copy." if not unsafe_playbooks else "Unsafe playbook row detected.",
})

orphaned_compliance = sorted(clean(row.get("business")) for row in compliance if clean(row.get("business")).casefold() not in prospect_names)
checks.append({
    "invariant": "Contact compliance rows require approved prospects",
    "status": "pass" if not orphaned_compliance else "fail",
    "evidence": f"{len(compliance)} contact compliance rows / {len(prospects)} prospects",
    "required_action": "Regenerate compliance after prospect tracker is corrected.",
    "notes": ", ".join(orphaned_compliance) if orphaned_compliance else "Compliance/prospect relationship holds.",
})

orphaned_delivery = sorted(clean(row.get("business")) for row in delivery if clean(row.get("business")).casefold() not in prospect_names)
checks.append({
    "invariant": "Delivery plans require approved prospects",
    "status": "pass" if not orphaned_delivery else "fail",
    "evidence": f"{len(delivery)} delivery rows / {len(prospects)} prospects",
    "required_action": "Regenerate delivery readiness after prospect tracker is corrected.",
    "notes": ", ".join(orphaned_delivery) if orphaned_delivery else "Delivery/prospect relationship holds.",
})

unsafe_pre_send = [
    row for row in pre_send
    if clean(row.get("business")).casefold() != "pipeline-level"
    and clean(row.get("business")).casefold() not in prospect_names
]
checks.append({
    "invariant": "Pre-send readiness rows require approved prospects",
    "status": "pass" if not unsafe_pre_send else "fail",
    "evidence": f"{len(pre_send)} pre-send rows / {len(prospects)} prospects",
    "required_action": "Regenerate pre-send readiness after correcting prospect, draft, and compliance trackers.",
    "notes": ", ".join(clean(row.get("business")) for row in unsafe_pre_send) if unsafe_pre_send else "Pre-send readiness rows are prospect-backed or pipeline-level only.",
})

promotion_without_decision = sorted(
    clean(row.get("business")) for row in promotion_log
    if clean(row.get("business")).casefold() not in approved
)
checks.append({
    "invariant": "Promotion log requires recorded approval",
    "status": "pass" if not promotion_without_decision else "fail",
    "evidence": f"{len(promotion_log)} promotion log rows / {len(approved)} recorded approvals",
    "required_action": "Investigate promotion log rows without matching approval decisions.",
    "notes": ", ".join(promotion_without_decision) if promotion_without_decision else "Promotion log invariant holds.",
})

for row in checks:
    row["date"] = today()
write_csv(p("safety_invariants.csv"), checks, FIELDS)

os.makedirs(p("safety_invariants"), exist_ok=True)
path = p("safety_invariants", f"{today()}.md")
with open(path, "w", encoding="utf-8") as handle:
    handle.write("# Safety Invariant Report\n\n")
    handle.write(f"- Date: {today()}\n")
    handle.write(f"- Checks: {len(checks)}\n\n")
    for row in checks:
        handle.write(f"- {row['invariant']}: {row['status']} / {row['evidence']} / {row['notes']}\n")

failed = [row for row in checks if row["status"] == "fail"]
print(rel(path))
if failed:
    for row in failed:
        print(f"FAIL: {row['invariant']} - {row['notes']}")
    sys.exit(1)
