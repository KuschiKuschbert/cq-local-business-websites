#!/usr/bin/env python3
import os
from common import p, read_csv, rel

intake = read_csv(p("prospect_intake.csv"))
verification = read_csv(p("intake_verification.csv"))
briefs = read_csv(p("intake_opportunity_briefs.csv"))
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
proposals = read_csv(p("proposals.csv"))
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
os.makedirs(p("dashboard"), exist_ok=True)
path = p("dashboard", "index.html")
with open(path, "w", encoding="utf-8") as handle:
    handle.write("<!doctype html><html><head><meta charset='utf-8'><title>Cap Coast Creative Growth Dashboard</title>")
    handle.write("<style>@import url('https://fonts.googleapis.com/css2?family=Inter:wght@500;700;800&family=Outfit:wght@600;800&display=swap');body{font-family:Inter,Arial,sans-serif;background:#101418;color:#edf3f1;padding:24px}h1,h2{font-family:Outfit,Inter,sans-serif;letter-spacing:0}section{border:1px solid #314047;border-radius:8px;padding:16px;margin:12px 0}td,th{padding:8px;border-bottom:1px solid #314047;text-align:left}</style></head><body>")
    handle.write("<h1>Cap Coast Creative Growth Dashboard</h1>")
    handle.write(f"<section><h2>Snapshot</h2><p>Intake: {len(intake)} | Evidence ready: {sum(1 for r in verification if r.get('readiness') == 'promotion-review-ready')} | Source lanes: {len(source_plan)} | Research lanes ranked: {len(research_controller)} | Regional heatmap: {len(regional_heatmap)} | Source routes: {len(source_quality)} | Research experiments: {len(research_experiments)} | Source pivots: {len(source_pivots)} | Research suppressions: {len(research_suppression)} | Council routes: {len(council_registry)} | Council debates: {len(council_debates)} | Council quality: {len(council_quality)} | Council CEO brief: {len(council_brief)} | Council gates: {len(council_decision_gates)} | Automation checks: {len(automation_status)} | Permission checks: {len(action_permissions)} | Weekly plan: {len(weekly_plan)} | Scorecard: {len(scorecard)} | Learning queue: {len(learning_queue)} | Operator queue: {len(operator_queue)} | Objective checks: {len(objective_coverage)} | Capability checks: {len(capabilities)} | Safety checks: {len(safety_invariants)} | Research tasks: {len(research)} | Attempts logged: {len(attempts)} | Opportunity briefs: {len(briefs)} | Private concepts: {len(concepts)} | Pending approvals: {len(approvals)} | Approval decisions: {len(approval_decisions)} | Approval inbox: {len(approval_inbox)} | Decision cockpit: {len(decision_cockpit)} | Post-approval steps: {len(post_approval)} | Approval packets: {len(approval_packets)} | Revenue stages: {len(revenue_forecast)} | GitHub issue drafts: {len(issue_drafts)} | GitHub plan: {len(github_plan)} | GitHub readiness: {len(github_readiness)} | Operating items: {len(operating)} | Priority items: {len(priority)} | Offer strategies: {len(strategy)} | Outreach playbooks: {len(playbooks)} | Outreach drafts: {len(drafts)} | Delivery plans: {len(delivery)} | Contact checks: {len(compliance)} | Pre-send checks: {len(pre_send)} | Proposals: {len(proposals)} | Prospects: {len(prospects)}</p></section>")
    handle.write("<section><h2>Safety Invariants</h2><table><tr><th>Invariant</th><th>Status</th><th>Evidence</th><th>Action</th></tr>")
    for row in safety_invariants:
        handle.write(f"<tr><td>{row.get('invariant')}</td><td>{row.get('status')}</td><td>{row.get('evidence')}</td><td>{row.get('required_action')}</td></tr>")
    handle.write("</table></section>")
    handle.write("<section><h2>Operator Action Queue</h2><table><tr><th>Rank</th><th>Status</th><th>Owner</th><th>Action</th><th>Gate</th></tr>")
    for row in operator_queue:
        handle.write(f"<tr><td>{row.get('rank')}</td><td>{row.get('status')}</td><td>{row.get('owner')}</td><td>{row.get('action')}</td><td>{row.get('safety_gate')}</td></tr>")
    handle.write("</table></section>")
    handle.write("<section><h2>Source Quality Map</h2><table><tr><th>Region</th><th>Niche</th><th>Source</th><th>Score</th><th>Query</th></tr>")
    for row in source_quality[:10]:
        handle.write(f"<tr><td>{row.get('region')}</td><td>{row.get('niche')}</td><td>{row.get('source_family')}</td><td>{row.get('quality_score')}</td><td>{row.get('query')}</td></tr>")
    handle.write("</table></section>")
    handle.write("<section><h2>Revenue Forecast</h2><table><tr><th>Stage</th><th>Count</th><th>Gross</th><th>Weighted</th><th>Next Action</th></tr>")
    for row in revenue_forecast:
        handle.write(f"<tr><td>{row.get('stage')}</td><td>{row.get('count')}</td><td>{row.get('gross_monthly_fee')}</td><td>{row.get('weighted_mrr')}</td><td>{row.get('next_action')}</td></tr>")
    handle.write("</table></section>")
    handle.write("<section><h2>Approval Packets</h2><table><tr><th>Rank</th><th>Business</th><th>Decision</th><th>Packet</th></tr>")
    for row in approval_packets:
        handle.write(f"<tr><td>{row.get('rank')}</td><td>{row.get('business')}</td><td>{row.get('recommended_decision')}</td><td>{row.get('packet_path')}</td></tr>")
    handle.write("</table></section>")
    handle.write("<section><h2>Approval Decision Inbox</h2><table><tr><th>Rank</th><th>Business</th><th>Recommended</th><th>Gate</th></tr>")
    for row in approval_inbox:
        handle.write(f"<tr><td>{row.get('rank')}</td><td>{row.get('business')}</td><td>{row.get('recommended_decision')}</td><td>{row.get('safety_gate')}</td></tr>")
    handle.write("</table></section>")
    handle.write("<section><h2>Decision Cockpit</h2><table><tr><th>Rank</th><th>Business</th><th>Evidence</th><th>Concept</th><th>GitHub</th><th>Gate</th></tr>")
    for row in decision_cockpit:
        handle.write(f"<tr><td>{row.get('rank')}</td><td>{row.get('business')}</td><td>{row.get('evidence_path')}</td><td>{row.get('private_concept')}</td><td>{row.get('github_status')}</td><td>{row.get('safety_gate')}</td></tr>")
    handle.write("</table></section>")
    handle.write("<section><h2>Post-Approval Workflow</h2><table><tr><th>Rank</th><th>Business</th><th>Step</th><th>Owner</th><th>Blocked Until</th><th>Gate</th></tr>")
    for row in post_approval[:20]:
        handle.write(f"<tr><td>{row.get('rank')}</td><td>{row.get('business')}</td><td>{row.get('step_order')}. {row.get('step')}</td><td>{row.get('owner')}</td><td>{row.get('blocked_until')}</td><td>{row.get('safety_gate')}</td></tr>")
    handle.write("</table></section>")
    handle.write("<section><h2>Action Permissions</h2><table><tr><th>Action</th><th>Status</th><th>Gate</th><th>Blocked Until</th></tr>")
    for row in action_permissions:
        handle.write(f"<tr><td>{row.get('action')}</td><td>{row.get('status')}</td><td>{row.get('safety_gate')}</td><td>{row.get('blocked_until')}</td></tr>")
    handle.write("</table></section>")
    handle.write("<section><h2>Objective Coverage</h2><table><tr><th>Requirement</th><th>Status</th><th>Evidence</th><th>Gap</th></tr>")
    for row in objective_coverage:
        handle.write(f"<tr><td>{row.get('objective_requirement')}</td><td>{row.get('status')}</td><td>{row.get('evidence_summary')}</td><td>{row.get('remaining_gap')}</td></tr>")
    handle.write("</table></section>")
    handle.write("<section><h2>Automation Status</h2><table><tr><th>ID</th><th>Status</th><th>Schedule</th><th>Gate</th></tr>")
    for row in automation_status:
        handle.write(f"<tr><td>{row.get('automation_id')}</td><td>{row.get('status')}</td><td>{row.get('schedule')}</td><td>{row.get('safety_gate')}</td></tr>")
    handle.write("</table></section>")
    handle.write("<section><h2>Research Controller</h2><table><tr><th>Rank</th><th>Region</th><th>Niche</th><th>Status</th><th>Score</th><th>Query</th></tr>")
    for row in research_controller[:10]:
        handle.write(f"<tr><td>{row.get('rank')}</td><td>{row.get('region')}</td><td>{row.get('niche')}</td><td>{row.get('lane_status')}</td><td>{row.get('priority_score')}</td><td>{row.get('recommended_query')}</td></tr>")
    handle.write("</table></section>")
    handle.write("<section><h2>Regional Coverage Heatmap</h2><table><tr><th>Rank</th><th>Region</th><th>Niche</th><th>Status</th><th>Ready</th><th>Attempts</th><th>Action</th></tr>")
    for row in regional_heatmap[:12]:
        handle.write(f"<tr><td>{row.get('rank')}</td><td>{row.get('region')}</td><td>{row.get('niche')}</td><td>{row.get('coverage_status')}</td><td>{row.get('evidence_ready_count')}</td><td>{row.get('attempts_logged')}</td><td>{row.get('safe_next_action')}</td></tr>")
    handle.write("</table></section>")
    handle.write("<section><h2>Research Experiments</h2><table><tr><th>Rank</th><th>Region</th><th>Niche</th><th>Type</th><th>Query</th></tr>")
    for row in research_experiments[:10]:
        handle.write(f"<tr><td>{row.get('rank')}</td><td>{row.get('region')}</td><td>{row.get('niche')}</td><td>{row.get('experiment_type')}</td><td>{row.get('query')}</td></tr>")
    handle.write("</table></section>")
    handle.write("<section><h2>Source Pivot Plan</h2><table><tr><th>Business</th><th>Reason</th><th>Primary Query</th><th>Secondary Query</th><th>Status</th></tr>")
    for row in source_pivots:
        handle.write(f"<tr><td>{row.get('business')}</td><td>{row.get('pivot_reason')}</td><td>{row.get('primary_query')}</td><td>{row.get('secondary_query')}</td><td>{row.get('status')}</td></tr>")
    handle.write("</table></section>")
    handle.write("<section><h2>Research Suppression List</h2><table><tr><th>Business</th><th>Failures</th><th>Suppressed Pattern</th><th>Replacement</th><th>Gate</th></tr>")
    for row in research_suppression:
        handle.write(f"<tr><td>{row.get('business')}</td><td>{row.get('failed_attempts')}</td><td>{row.get('suppressed_query_pattern')}</td><td>{row.get('replacement_source_family')}</td><td>{row.get('safety_gate')}</td></tr>")
    handle.write("</table></section>")
    handle.write("<section><h2>Council Debates</h2><table><tr><th>Council</th><th>Decision</th><th>Verdict</th><th>Next Test</th></tr>")
    for row in council_debates:
        handle.write(f"<tr><td>{row.get('council')}</td><td>{row.get('decision_id')}</td><td>{row.get('verdict')}</td><td>{row.get('next_test')}</td></tr>")
    handle.write("</table></section>")
    handle.write("<section><h2>Council Quality</h2><table><tr><th>Decision</th><th>Council</th><th>Status</th><th>Missing</th></tr>")
    for row in council_quality:
        handle.write(f"<tr><td>{row.get('decision_id')}</td><td>{row.get('council')}</td><td>{row.get('quality_status')}</td><td>{row.get('missing_elements')}</td></tr>")
    handle.write("</table></section>")
    handle.write("<section><h2>Council CEO Brief</h2><table><tr><th>Priority</th><th>Council</th><th>Allowed Move</th><th>Blocked</th><th>Daniel Decision</th></tr>")
    for row in council_brief:
        handle.write(f"<tr><td>{row.get('priority')}</td><td>{row.get('council')}</td><td>{row.get('allowed_next_move')}</td><td>{row.get('blocked_actions')}</td><td>{row.get('daniel_decision_needed')}</td></tr>")
    handle.write("</table></section>")
    handle.write("<section><h2>Council Decision Gates</h2><table><tr><th>Action</th><th>Council</th><th>Verdict</th><th>Gate</th></tr>")
    for row in council_decision_gates:
        handle.write(f"<tr><td>{row.get('action')}</td><td>{row.get('council')}</td><td>{row.get('council_verdict')}</td><td>{row.get('gate_status')}</td></tr>")
    handle.write("</table></section>")
    handle.write("<section><h2>Capability Matrix</h2><table><tr><th>Capability</th><th>Status</th><th>Evidence</th><th>Gap</th></tr>")
    for row in capabilities:
        handle.write(f"<tr><td>{row.get('capability')}</td><td>{row.get('status')}</td><td>{row.get('evidence')}</td><td>{row.get('remaining_gap')}</td></tr>")
    handle.write("</table></section>")
    handle.write("<section><h2>Improvement Scorecard</h2><table><tr><th>Area</th><th>Score</th><th>Status</th><th>Action</th></tr>")
    for row in scorecard:
        handle.write(f"<tr><td>{row.get('area')}</td><td>{row.get('score')}</td><td>{row.get('status')}</td><td>{row.get('improvement_action')}</td></tr>")
    handle.write("</table></section>")
    handle.write("<section><h2>Learning Queue</h2><table><tr><th>ID</th><th>Area</th><th>Status</th><th>Proposal</th></tr>")
    for row in learning_queue:
        handle.write(f"<tr><td>{row.get('learning_id')}</td><td>{row.get('area')}</td><td>{row.get('status')}</td><td>{row.get('proposal')}</td></tr>")
    handle.write("</table></section>")
    handle.write("<section><h2>Weekly Plan</h2><table><tr><th>Day</th><th>Focus</th><th>Inputs</th><th>Gate</th></tr>")
    for row in weekly_plan:
        handle.write(f"<tr><td>{row.get('day')}</td><td>{row.get('focus')}</td><td>{row.get('inputs')}</td><td>{row.get('safety_gate')}</td></tr>")
    handle.write("</table></section>")
    handle.write("<section><h2>Source Plan</h2><table><tr><th>Region</th><th>Niche</th><th>Query</th><th>Status</th></tr>")
    for row in source_plan[:10]:
        handle.write(f"<tr><td>{row.get('region')}</td><td>{row.get('niche')}</td><td>{row.get('query')}</td><td>{row.get('status')}</td></tr>")
    handle.write("</table></section>")
    handle.write("<section><h2>Priority Board</h2><table><tr><th>Rank</th><th>Business</th><th>Score</th><th>Status</th><th>Next Action</th></tr>")
    for row in priority[:8]:
        handle.write(f"<tr><td>{row.get('rank')}</td><td>{row.get('business')}</td><td>{row.get('priority_score')}</td><td>{row.get('status')}</td><td>{row.get('next_best_action')}</td></tr>")
    handle.write("</table></section>")
    handle.write("<section><h2>Offer Strategy</h2><table><tr><th>Business</th><th>Fee</th><th>CTA</th><th>Trust Hook</th></tr>")
    for row in strategy[:8]:
        handle.write(f"<tr><td>{row.get('business')}</td><td>{row.get('monthly_fee')}</td><td>{row.get('primary_cta')}</td><td>{row.get('trust_hook')}</td></tr>")
    handle.write("</table></section>")
    handle.write("<section><h2>Outreach Playbook Library</h2><table><tr><th>Playbook</th><th>Niche</th><th>Channel</th><th>Gate</th></tr>")
    for row in playbooks:
        handle.write(f"<tr><td>{row.get('playbook_id')}</td><td>{row.get('niche')}</td><td>{row.get('channel')}</td><td>{row.get('safety_gate')}</td></tr>")
    handle.write("</table></section>")
    handle.write("<section><h2>Operating Review</h2><table><tr><th>Area</th><th>Status</th><th>Next Action</th><th>Gate</th></tr>")
    for row in operating:
        handle.write(f"<tr><td>{row.get('area')}</td><td>{row.get('status')}</td><td>{row.get('next_action')}</td><td>{row.get('safety_gate')}</td></tr>")
    handle.write("</table></section>")
    handle.write("<section><h2>Research Queue</h2><table><tr><th>Business</th><th>Missing</th><th>Query</th></tr>")
    for row in research:
        handle.write(f"<tr><td>{row.get('business')}</td><td>{row.get('missing_evidence')}</td><td>{row.get('search_query')}</td></tr>")
    handle.write("</table></section>")
    handle.write("<section><h2>Private Concepts</h2><table><tr><th>Business</th><th>Path</th><th>CTA</th></tr>")
    for row in concepts:
        handle.write(f"<tr><td>{row.get('business')}</td><td>{row.get('concept_path')}</td><td>{row.get('primary_cta')}</td></tr>")
    handle.write("</table></section>")
    handle.write("<section><h2>Delivery Readiness</h2><table><tr><th>Business</th><th>Stage</th><th>Readiness</th><th>Gate</th></tr>")
    for row in delivery:
        handle.write(f"<tr><td>{row.get('business')}</td><td>{row.get('stage')}</td><td>{row.get('readiness')}</td><td>{row.get('safety_gate')}</td></tr>")
    handle.write("</table></section>")
    handle.write("<section><h2>Contact Compliance</h2><table><tr><th>Business</th><th>Status</th><th>Basis</th><th>Next Action</th></tr>")
    for row in compliance:
        handle.write(f"<tr><td>{row.get('business')}</td><td>{row.get('compliance_status')}</td><td>{row.get('contact_basis')}</td><td>{row.get('next_action')}</td></tr>")
    handle.write("</table></section>")
    handle.write("<section><h2>Pre-Send Readiness</h2><table><tr><th>Business</th><th>Status</th><th>Missing</th><th>Next Action</th></tr>")
    for row in pre_send:
        handle.write(f"<tr><td>{row.get('business')}</td><td>{row.get('readiness_status')}</td><td>{row.get('failure_reason')}</td><td>{row.get('next_action')}</td></tr>")
    handle.write("</table></section>")
    handle.write("<section><h2>Approval Queue</h2><table><tr><th>Type</th><th>Business</th><th>Decision</th></tr>")
    for row in approvals:
        handle.write(f"<tr><td>{row.get('approval_type')}</td><td>{row.get('business')}</td><td>{row.get('requested_decision')}</td></tr>")
    handle.write("</table></section>")
    handle.write("<section><h2>Approval Decisions</h2><table><tr><th>Business</th><th>Decision</th><th>Next Action</th></tr>")
    for row in approval_decisions:
        handle.write(f"<tr><td>{row.get('business')}</td><td>{row.get('decision')}</td><td>{row.get('next_action')}</td></tr>")
    handle.write("</table></section>")
    handle.write("<section><h2>GitHub Issue Drafts</h2><table><tr><th>Business</th><th>Title</th><th>Path</th></tr>")
    for row in issue_drafts:
        handle.write(f"<tr><td>{row.get('business')}</td><td>{row.get('issue_title')}</td><td>{row.get('draft_path')}</td></tr>")
    handle.write("</table></section>")
    handle.write("<section><h2>GitHub Execution Plan</h2><table><tr><th>Business</th><th>Status</th><th>Command Artifact</th></tr>")
    for row in github_plan:
        handle.write(f"<tr><td>{row.get('business')}</td><td>{row.get('approval_status')}</td><td>{row.get('command_path')}</td></tr>")
    handle.write("</table></section>")
    handle.write("<section><h2>GitHub Readiness</h2><table><tr><th>Business</th><th>Status</th><th>Command</th><th>Missing</th></tr>")
    for row in github_readiness:
        handle.write(f"<tr><td>{row.get('business')}</td><td>{row.get('readiness_status')}</td><td>{row.get('command_status')}</td><td>{row.get('failure_reason')}</td></tr>")
    handle.write("</table></section><p>Research and planning only. Outbound contact needs approval.</p></body></html>")
print(rel(path))
