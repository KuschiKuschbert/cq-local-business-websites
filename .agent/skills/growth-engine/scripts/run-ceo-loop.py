#!/usr/bin/env python3
import os
import subprocess
import sys
from common import p, read_csv, rel, today

STEPS = [
    "review-intake.py",
    "verify-intake-evidence.py",
    "generate-source-plan.py",
    "generate-research-controller.py",
    "generate-regional-coverage-heatmap.py",
    "generate-source-quality-map.py",
    "generate-research-experiments.py",
    "generate-source-pivot-plan.py",
    "generate-research-suppression-list.py",
    "generate-council-registry.py",
    "generate-automation-status.py",
    "generate-research-queue.py",
    "generate-intake-opportunity-briefs.py",
    "generate-private-concepts.py",
    "generate-approval-queue.py",
    "generate-offer-strategy.py",
    "generate-priority-board.py",
    "generate-approval-packets.py",
    "generate-revenue-forecast.py",
    "generate-github-issue-drafts.py",
    "generate-github-execution-plan.py",
    "generate-github-readiness-audit.py",
    "generate-council-debates.py",
    "generate-council-quality-audit.py",
    "generate-council-ceo-brief.py",
    "generate-approval-decision-summary.py",
    "generate-approval-decision-inbox.py",
    "generate-decision-cockpit.py",
    "generate-post-approval-workflow.py",
    "generate-weekly-plan.py",
    "generate-improvement-scorecard.py",
    "generate-learning-queue.py",
    "generate-operator-action-queue.py",
    "run-pipeline.py",
    "generate-mockup-briefs.py",
    "generate-delivery-readiness.py",
    "generate-outreach-playbook-library.py",
    "generate-outreach-drafts.py",
    "generate-contact-compliance.py",
    "generate-pre-send-readiness.py",
    "generate-proposals.py",
    "generate-action-permissions.py",
    "generate-council-decision-gates.py",
    "validate-safety-invariants.py",
    "generate-capability-matrix.py",
    "generate-objective-coverage-audit.py",
    "generate-operating-review.py",
    "generate-retrospective.py --append-kpi",
    "generate-dashboard.py",
    "audit-engine.py",
]

base = os.path.dirname(__file__)
results = []
for step in STEPS:
    parts = step.split()
    cmd = [sys.executable, os.path.join(base, parts[0])] + parts[1:]
    done = subprocess.run(cmd, cwd=os.path.abspath(os.path.join(base, "../../../..")), text=True, capture_output=True)
    results.append((step, done.returncode, (done.stdout or done.stderr).strip()))

os.makedirs(p("ceo_reports"), exist_ok=True)
path = p("ceo_reports", f"{today()}.md")
intake = read_csv(p("prospect_intake.csv"))
verify = read_csv(p("intake_verification.csv"))
approvals = read_csv(p("approval_queue.csv"))
approval_decisions = read_csv(p("approval_decision_summary.csv"))
approval_inbox = read_csv(p("approval_decision_inbox.csv"))
decision_cockpit = read_csv(p("decision_cockpit.csv"))
post_approval = read_csv(p("post_approval_workflow.csv"))
approval_packets = read_csv(p("approval_packets.csv"))
revenue_forecast = read_csv(p("revenue_forecast.csv"))
objective_coverage = read_csv(p("objective_coverage_audit.csv"))
prospects = read_csv(p("prospects.csv"))
concepts = read_csv(p("private_concepts.csv"))
issue_drafts = read_csv(p("github_issue_drafts.csv"))
github_plan = read_csv(p("github_execution_plan.csv"))
github_readiness = read_csv(p("github_readiness_audit.csv"))
operating = read_csv(p("operating_review.csv"))
priority = read_csv(p("priority_board.csv"))
strategy = read_csv(p("offer_strategy.csv"))
drafts = read_csv(p("outreach_drafts.csv"))
playbooks = read_csv(p("outreach_playbook_library.csv"))
delivery = read_csv(p("delivery_readiness.csv"))
compliance = read_csv(p("contact_compliance.csv"))
pre_send = read_csv(p("pre_send_readiness.csv"))
source_plan = read_csv(p("source_plan.csv"))
research_controller = read_csv(p("research_controller.csv"))
regional_heatmap = read_csv(p("regional_coverage_heatmap.csv"))
source_quality = read_csv(p("source_quality_map.csv"))
research_experiments = read_csv(p("research_experiments.csv"))
source_pivots = read_csv(p("source_pivot_plan.csv"))
research_suppression = read_csv(p("research_suppression_list.csv"))
council_registry = read_csv(p("council_registry.csv"))
council_debates = read_csv(p("council_debates.csv"))
council_quality = read_csv(p("council_quality_audit.csv"))
council_brief = read_csv(p("council_ceo_brief.csv"))
automation_status = read_csv(p("automation_status.csv"))
action_permissions = read_csv(p("action_permissions.csv"))
council_decision_gates = read_csv(p("council_decision_gates.csv"))
weekly_plan = read_csv(p("weekly_plan.csv"))
scorecard = read_csv(p("improvement_scorecard.csv"))
learning_queue = read_csv(p("learning_queue.csv"))
operator_queue = read_csv(p("operator_action_queue.csv"))
capabilities = read_csv(p("capability_matrix.csv"))
safety_invariants = read_csv(p("safety_invariants.csv"))
research = read_csv(p("research_queue.csv"))
attempts = read_csv(p("research_attempts.csv"))
with open(path, "w", encoding="utf-8") as handle:
    handle.write("# Cap Coast Creative CEO Loop\n\n")
    handle.write(f"- Status: {'FAIL' if any(code for _, code, _ in results) else 'PASS'}\n")
    handle.write("- Safety: no outreach sent; local reports and tracker files only.\n\n")
    handle.write("## Operating Snapshot\n\n")
    handle.write(f"- Intake candidates: {len(intake)}\n")
    handle.write(f"- Evidence-ready candidates: {sum(1 for row in verify if row.get('readiness') == 'promotion-review-ready')}\n")
    handle.write(f"- Pending approvals: {len(approvals)}\n")
    handle.write(f"- Approval decision items: {len(approval_decisions)}\n")
    handle.write(f"- Approval decision inbox items: {len(approval_inbox)}\n")
    handle.write(f"- Decision cockpit items: {len(decision_cockpit)}\n")
    handle.write(f"- Post-approval workflow items: {len(post_approval)}\n")
    handle.write(f"- Approval packets: {len(approval_packets)}\n")
    handle.write(f"- Revenue forecast stages: {len(revenue_forecast)}\n")
    handle.write(f"- Objective coverage checks: {len(objective_coverage)}\n")
    handle.write(f"- GitHub issue drafts: {len(issue_drafts)}\n")
    handle.write(f"- GitHub execution plan items: {len(github_plan)}\n")
    handle.write(f"- GitHub readiness audit items: {len(github_readiness)}\n")
    handle.write(f"- Operating review items: {len(operating)}\n")
    handle.write(f"- Priority board items: {len(priority)}\n")
    handle.write(f"- Offer strategy items: {len(strategy)}\n")
    handle.write(f"- Outreach draft packs: {len(drafts)}\n")
    handle.write(f"- Outreach playbooks: {len(playbooks)}\n")
    handle.write(f"- Delivery readiness items: {len(delivery)}\n")
    handle.write(f"- Contact compliance items: {len(compliance)}\n")
    handle.write(f"- Pre-send readiness items: {len(pre_send)}\n")
    handle.write(f"- Source plan lanes: {len(source_plan)}\n")
    handle.write(f"- Research controller lanes: {len(research_controller)}\n")
    handle.write(f"- Regional heatmap lanes: {len(regional_heatmap)}\n")
    handle.write(f"- Source quality routes: {len(source_quality)}\n")
    handle.write(f"- Research experiments: {len(research_experiments)}\n")
    handle.write(f"- Source pivot items: {len(source_pivots)}\n")
    handle.write(f"- Research suppression items: {len(research_suppression)}\n")
    handle.write(f"- Council routes: {len(council_registry)}\n")
    handle.write(f"- Council debates: {len(council_debates)}\n")
    handle.write(f"- Council quality checks: {len(council_quality)}\n")
    handle.write(f"- Council CEO brief items: {len(council_brief)}\n")
    handle.write(f"- Automation status items: {len(automation_status)}\n")
    handle.write(f"- Action permission items: {len(action_permissions)}\n")
    handle.write(f"- Council decision gates: {len(council_decision_gates)}\n")
    handle.write(f"- Weekly plan items: {len(weekly_plan)}\n")
    handle.write(f"- Improvement scorecard items: {len(scorecard)}\n")
    handle.write(f"- Learning queue items: {len(learning_queue)}\n")
    handle.write(f"- Operator action queue items: {len(operator_queue)}\n")
    handle.write(f"- Capability matrix items: {len(capabilities)}\n")
    handle.write(f"- Safety invariant checks: {len(safety_invariants)}\n")
    handle.write(f"- Private concepts: {len(concepts)}\n")
    handle.write(f"- Research tasks: {len(research)}\n")
    handle.write(f"- Research attempts logged: {len(attempts)}\n")
    handle.write(f"- Approved prospects: {len(prospects)}\n\n")
    handle.write("## Step Results\n\n")
    for step, code, output in results:
        handle.write(f"- {step}: {'PASS' if code == 0 else 'FAIL'} - {output}\n")
    handle.write("\n## Safety Gate\n\nPromotion is not outreach approval. Outreach needs separate explicit approval.\n")
print(rel(path))
raise SystemExit(1 if any(code for _, code, _ in results) else 0)
