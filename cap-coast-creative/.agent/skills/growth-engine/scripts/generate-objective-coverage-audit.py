#!/usr/bin/env python3
import os
from common import p, read_csv, rel, today, write_csv

FIELDS = ["date", "objective_requirement", "status", "evidence_path", "evidence_summary", "remaining_gap", "safety_gate", "notes"]

source_plan = read_csv(p("source_plan.csv"))
source_quality = read_csv(p("source_quality_map.csv"))
research_controller = read_csv(p("research_controller.csv"))
automation_status = read_csv(p("automation_status.csv"))
action_permissions = read_csv(p("action_permissions.csv"))
intake = read_csv(p("prospect_intake.csv"))
verification = read_csv(p("intake_verification.csv"))
approvals = read_csv(p("approval_queue.csv"))
approval_packets = read_csv(p("approval_packets.csv"))
prospects = read_csv(p("prospects.csv"))
concepts = read_csv(p("private_concepts.csv"))
drafts = read_csv(p("outreach_drafts.csv"))
compliance = read_csv(p("contact_compliance.csv"))
outreach = read_csv(p("outreach_log.csv"))
weekly = read_csv(p("weekly_plan.csv"))
operating = read_csv(p("operating_review.csv"))
scorecard = read_csv(p("improvement_scorecard.csv"))
safety_invariants = read_csv(p("safety_invariants.csv"))
github_plan = read_csv(p("github_execution_plan.csv"))
revenue_forecast = read_csv(p("revenue_forecast.csv"))
priority = read_csv(p("priority_board.csv"))
strategy = read_csv(p("offer_strategy.csv"))

ready_count = sum(1 for row in verification if row.get("readiness") == "promotion-review-ready")
active_research_automations = [
    row for row in automation_status
    if row.get("status", "").lower() == "active"
    and ("no outreach" in row.get("safety_gate", "").lower() or "research-only" in row.get("safety_gate", "").lower())
]

rows = [
    {
        "objective_requirement": "Autonomous supervised CEO operating engine",
        "status": "ready" if weekly and operating and action_permissions else "not-yet",
        "evidence_path": ".agent/memory/working/operating_review.csv",
        "evidence_summary": f"{len(weekly)} weekly plan items / {len(operating)} operating checks / {len(action_permissions)} permission checks",
        "remaining_gap": "Keep the loop supervised for approvals, publishing, GitHub writes, and outreach sends.",
        "safety_gate": "Operating automation may plan and report only.",
        "notes": "The engine can run a local CEO loop, but authority stays gated.",
    },
    {
        "objective_requirement": "Website design business workflow",
        "status": "ready" if concepts and priority and strategy else "not-yet",
        "evidence_path": ".agent/memory/working/private_concepts.csv",
        "evidence_summary": f"{len(concepts)} private concepts / {len(priority)} ranked candidates / {len(strategy)} offer strategies",
        "remaining_gap": "Approved prospects are needed before client-facing delivery, proposal, or publishing.",
        "safety_gate": "Private concepts are not publish or send approval.",
        "notes": "Concepts, pricing, CTA, and priority logic are present.",
    },
    {
        "objective_requirement": "Cold outreach pipeline",
        "status": "gated" if not prospects else "ready",
        "evidence_path": ".agent/memory/working/outreach_drafts.csv",
        "evidence_summary": f"{len(prospects)} approved prospects / {len(drafts)} drafts / {len(compliance)} compliance checks / {len(outreach)} outreach events",
        "remaining_gap": "Needs approved prospects, contact basis, opt-out, sender identity, and explicit send approval.",
        "safety_gate": "No email, SMS, DM, form, social post, or call without explicit approval.",
        "notes": "The pipeline exists, but it is intentionally blocked right now.",
    },
    {
        "objective_requirement": "Safety guidelines and action control",
        "status": "ready" if action_permissions and safety_invariants else "not-yet",
        "evidence_path": ".agent/memory/working/action_permissions.csv",
        "evidence_summary": f"{len(action_permissions)} action permission rows / {len(safety_invariants)} invariant checks",
        "remaining_gap": "Treat any failed invariant as a hard stop before autonomous work continues.",
        "safety_gate": "Safety reports do not approve blocked actions.",
        "notes": "Allowed and blocked actions are explicit.",
    },
    {
        "objective_requirement": "Self-improvement and self-regulation",
        "status": "ready" if scorecard and safety_invariants else "not-yet",
        "evidence_path": ".agent/memory/working/improvement_scorecard.csv",
        "evidence_summary": f"{len(scorecard)} scorecard rows / {len(safety_invariants)} invariant checks",
        "remaining_gap": "Convert repeated validated lessons into durable memory only after review.",
        "safety_gate": "Diagnostics are not permission to change external state.",
        "notes": "The system audits bottlenecks and process health.",
    },
    {
        "objective_requirement": "Constant regional prospect research",
        "status": "ready" if source_plan and research_controller and active_research_automations else "gated",
        "evidence_path": ".agent/memory/working/research_controller.csv",
        "evidence_summary": f"{len(source_plan)} source lanes / {len(research_controller)} ranked lanes / {len(active_research_automations)} active research-only automations",
        "remaining_gap": "Continue research-only passes and log failed lanes before broadening.",
        "safety_gate": "Research automation may capture sourced intake only; no contact.",
        "notes": "Daily scanning is configured as research-only.",
    },
    {
        "objective_requirement": "Social-first lead sourcing",
        "status": "ready" if intake and source_quality else "not-yet",
        "evidence_path": ".agent/memory/working/source_quality_map.csv",
        "evidence_summary": f"{len(intake)} staged candidates / {ready_count} promotion-review-ready / {len(source_quality)} source routes",
        "remaining_gap": "Verify remaining candidates with business-owned social evidence and public source URLs.",
        "safety_gate": "Staged intake is not prospect promotion.",
        "notes": "Capture is biased toward public social proof plus website-gap evidence.",
    },
    {
        "objective_requirement": "Region coverage for Kawana, Capricorn Coast, Rockhampton, Yeppoon, and Emu Park",
        "status": "ready" if len({row.get("region") for row in source_plan if row.get("region")}) >= 5 else "not-yet",
        "evidence_path": ".agent/memory/working/source_plan.csv",
        "evidence_summary": f"{len({row.get('region') for row in source_plan if row.get('region')})} regions covered / {len(source_plan)} source lanes",
        "remaining_gap": "Keep balancing research attempts across regions with lower verified intake.",
        "safety_gate": "Coverage planning is not outreach approval.",
        "notes": "Source lanes include the requested regional footprint.",
    },
    {
        "objective_requirement": "Tracking, plans, and decision records",
        "status": "ready" if approvals and approval_packets and revenue_forecast else "not-yet",
        "evidence_path": ".agent/memory/working/approval_packets.csv",
        "evidence_summary": f"{len(approvals)} approval rows / {len(approval_packets)} packets / {len(revenue_forecast)} forecast stages",
        "remaining_gap": "Daniel must record decisions before promotion or outreach work can proceed.",
        "safety_gate": "Tracking does not imply approval.",
        "notes": "Approval packets, priority board, and forecasts make the pipeline reviewable.",
    },
    {
        "objective_requirement": "GitHub-integrated work orchestration",
        "status": "gated" if github_plan else "not-yet",
        "evidence_path": ".agent/memory/working/github_execution_plan.csv",
        "evidence_summary": f"{len(github_plan)} local GitHub execution plan rows",
        "remaining_gap": "Remote issue creation needs explicit approval for the exact workflow.",
        "safety_gate": "No remote GitHub writes without approval.",
        "notes": "Local issue drafts and command plan exist, but have not been executed.",
    },
    {
        "objective_requirement": "Revenue and business management",
        "status": "ready" if revenue_forecast and strategy else "not-yet",
        "evidence_path": ".agent/memory/working/revenue_forecast.csv",
        "evidence_summary": f"{len(revenue_forecast)} forecast stages / {len(strategy)} offer strategies",
        "remaining_gap": "Actual revenue depends on approved outreach, client agreement, and delivery.",
        "safety_gate": "Forecast is not invoice, charge, or client promise approval.",
        "notes": "Monthly-fee strategy is trackable without making claims externally.",
    },
]

for row in rows:
    row["date"] = today()

write_csv(p("objective_coverage_audit.csv"), rows, FIELDS)

os.makedirs(p("objective_coverage_audits"), exist_ok=True)
path = p("objective_coverage_audits", f"{today()}.md")
with open(path, "w", encoding="utf-8") as handle:
    handle.write("# Cap Coast Creative Objective Coverage Audit\n\n")
    handle.write(f"- Date: {today()}\n")
    handle.write("- Purpose: map the current engine against Daniel's original autonomous business-engine objective.\n\n")
    for row in rows:
        handle.write(f"- {row['objective_requirement']}: {row['status']} / {row['evidence_summary']} / Gap: {row['remaining_gap']}\n")

print(rel(path))
