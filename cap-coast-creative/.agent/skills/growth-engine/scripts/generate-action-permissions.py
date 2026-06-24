#!/usr/bin/env python3
import os
from common import p, read_csv, rel, today, write_csv

FIELDS = ["date", "action", "status", "evidence", "allowed_next_step", "blocked_until", "safety_gate", "notes"]

intake = read_csv(p("prospect_intake.csv"))
verification = read_csv(p("intake_verification.csv"))
approval_queue = read_csv(p("approval_queue.csv"))
approval_decisions = read_csv(p("approval_decisions.csv"))
prospects = read_csv(p("prospects.csv"))
outreach_drafts = read_csv(p("outreach_drafts.csv"))
contact_compliance = read_csv(p("contact_compliance.csv"))
delivery = read_csv(p("delivery_readiness.csv"))
github_plan = read_csv(p("github_execution_plan.csv"))
automation_status = read_csv(p("automation_status.csv"))
research_controller = read_csv(p("research_controller.csv"))
outreach_log = read_csv(p("outreach_log.csv"))

ready_count = sum(1 for row in verification if row.get("readiness") == "promotion-review-ready")
approved_decisions = [
    row for row in approval_decisions
    if row.get("decision") == "approve" and row.get("approval_type") == "promotion"
]
active_scan = any(
    row.get("automation_id") == "cap-coast-prospect-scan"
    and row.get("status", "").lower() == "active"
    and "research-only" in row.get("safety_gate", "").lower()
    for row in automation_status
)
remote_github_approved = any(row.get("approval_status") == "approved-to-run" for row in github_plan)
send_ready = bool(prospects and outreach_drafts and contact_compliance)

rows = [
    {
        "action": "Run safe prospect research",
        "status": "allowed" if research_controller and active_scan else "needs-setup",
        "evidence": f"{len(research_controller)} ranked lanes / prospect scan active: {active_scan}",
        "allowed_next_step": "Work the top research_controller.csv lane and log checked sources.",
        "blocked_until": "-" if research_controller and active_scan else "Research controller and active safe scan automation exist.",
        "safety_gate": "Public research only; no contact or account interaction.",
        "notes": "This is the only autonomous external-info action currently allowed.",
    },
    {
        "action": "Capture sourced intake candidate",
        "status": "allowed",
        "evidence": f"{len(intake)} staged rows / capture command requires public social and source URL",
        "allowed_next_step": "Use capture-intake-candidate.py only for public, business-owned evidence.",
        "blocked_until": "-",
        "safety_gate": "Capture is not promotion and not outreach.",
        "notes": "Weak or directory-only evidence must be logged as a research attempt instead.",
    },
    {
        "action": "Promote candidate to prospect",
        "status": "blocked" if not approved_decisions else "approval-recorded",
        "evidence": f"{ready_count} evidence-ready / {len(approved_decisions)} recorded approve decisions / {len(prospects)} prospects",
        "allowed_next_step": "Run promote-intake.py only for businesses with a recorded approve decision.",
        "blocked_until": "Daniel records an approve decision in approval_decisions.csv.",
        "safety_gate": "Human approval required before promotion.",
        "notes": "Promotion still does not approve outreach.",
    },
    {
        "action": "Create remote GitHub issues",
        "status": "blocked" if not remote_github_approved else "approval-recorded",
        "evidence": f"{len(github_plan)} local issue plans / remote approval: {remote_github_approved}",
        "allowed_next_step": "Execute create-issues.sh only after exact remote GitHub approval.",
        "blocked_until": "Daniel approves remote GitHub issue creation.",
        "safety_gate": "No remote GitHub writes without explicit approval.",
        "notes": "Local drafts and commands remain planning artifacts.",
    },
    {
        "action": "Generate outreach drafts",
        "status": "blocked" if not prospects else "allowed-after-compliance",
        "evidence": f"{len(prospects)} prospects / {len(outreach_drafts)} draft packs",
        "allowed_next_step": "Generate drafts only for approved prospects, then review compliance.",
        "blocked_until": "At least one prospect exists from approved promotion.",
        "safety_gate": "Drafting is not sending.",
        "notes": "Drafts must include opt-out wording and contact basis notes.",
    },
    {
        "action": "Send or schedule outreach",
        "status": "blocked",
        "evidence": f"send-ready prerequisites present: {send_ready} / outreach events: {len(outreach_log)}",
        "allowed_next_step": "None. Ask Daniel for exact send approval after compliance review.",
        "blocked_until": "Promoted prospect, compliant draft, sender ID, opt-out, contact basis, and explicit send approval.",
        "safety_gate": "No email, SMS, DM, forms, social posts, calls, or scheduling without approval.",
        "notes": "This remains blocked even if drafts exist.",
    },
    {
        "action": "Publish concepts or start delivery",
        "status": "blocked" if not delivery else "internal-only",
        "evidence": f"{len(delivery)} delivery plans / {len(prospects)} approved prospects",
        "allowed_next_step": "Keep concepts internal until client-facing approval exists.",
        "blocked_until": "Approved prospect and explicit approval for publication or delivery step.",
        "safety_gate": "No hosting, domains, billing, publishing, or client-facing promises without approval.",
        "notes": "Private concepts are planning assets.",
    },
]

for row in rows:
    row["date"] = today()

write_csv(p("action_permissions.csv"), rows, FIELDS)

os.makedirs(p("action_permissions"), exist_ok=True)
path = p("action_permissions", f"{today()}.md")
with open(path, "w", encoding="utf-8") as handle:
    handle.write("# Action Permissions\n\n")
    handle.write(f"- Date: {today()}\n")
    handle.write("- Purpose: current allowed/blocked actions for the business engine.\n\n")
    for row in rows:
        handle.write(f"- {row['action']}: {row['status']} / Gate: {row['safety_gate']} / Evidence: {row['evidence']}\n")

print(rel(path))
