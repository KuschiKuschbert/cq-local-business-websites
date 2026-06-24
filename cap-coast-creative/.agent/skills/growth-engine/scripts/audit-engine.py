#!/usr/bin/env python3
import csv
import os
import re
import stat
import sys
from common import ROOT

REQUIRED = [
    ".agent/protocols/outreach-safety.md",
    ".agent/memory/working/PROSPECT_PIPELINE.md",
    ".agent/memory/working/CLIENT_DELIVERY.md",
    ".agent/memory/working/RETROSPECTIVE_SYSTEM.md",
    ".agent/memory/working/AUTOMATIONS.md",
    ".agent/memory/working/automation_status.csv",
    ".agent/memory/working/action_permissions.csv",
    ".agent/memory/working/prospect_intake.csv",
    ".agent/memory/working/intake_review.csv",
    ".agent/memory/working/intake_verification.csv",
    ".agent/memory/working/research_queue.csv",
    ".agent/memory/working/research_controller.csv",
    ".agent/memory/working/regional_coverage_heatmap.csv",
    ".agent/memory/working/source_plan.csv",
    ".agent/memory/working/source_quality_map.csv",
    ".agent/memory/working/research_experiments.csv",
    ".agent/memory/working/source_pivot_plan.csv",
    ".agent/memory/working/research_suppression_list.csv",
    ".agent/memory/working/council_registry.csv",
    ".agent/memory/working/council_debates.csv",
    ".agent/memory/working/council_quality_audit.csv",
    ".agent/memory/working/council_ceo_brief.csv",
    ".agent/memory/working/council_decision_gates.csv",
    ".agent/memory/working/weekly_plan.csv",
    ".agent/memory/working/improvement_scorecard.csv",
    ".agent/memory/working/learning_queue.csv",
    ".agent/memory/working/operator_action_queue.csv",
    ".agent/memory/working/research_attempts.csv",
    ".agent/memory/working/intake_opportunity_briefs.csv",
    ".agent/memory/working/private_concepts.csv",
    ".agent/memory/working/github_issue_drafts.csv",
    ".agent/memory/working/github_execution_plan.csv",
    ".agent/memory/working/github_readiness_audit.csv",
    ".agent/memory/working/operating_review.csv",
    ".agent/memory/working/priority_board.csv",
    ".agent/memory/working/offer_strategy.csv",
    ".agent/memory/working/outreach_drafts.csv",
    ".agent/memory/working/outreach_playbook_library.csv",
    ".agent/memory/working/delivery_readiness.csv",
    ".agent/memory/working/contact_compliance.csv",
    ".agent/memory/working/pre_send_readiness.csv",
    ".agent/memory/working/capability_matrix.csv",
    ".agent/memory/working/safety_invariants.csv",
    ".agent/memory/working/decision_log.csv",
    ".agent/memory/working/risk_register.csv",
    ".agent/memory/working/approval_queue.csv",
    ".agent/memory/working/approval_decisions.csv",
    ".agent/memory/working/approval_decision_summary.csv",
    ".agent/memory/working/approval_decision_inbox.csv",
    ".agent/memory/working/decision_cockpit.csv",
    ".agent/memory/working/post_approval_workflow.csv",
    ".agent/memory/working/approval_packets.csv",
    ".agent/memory/working/revenue_forecast.csv",
    ".agent/memory/working/objective_coverage_audit.csv",
    ".agent/memory/working/prospects.csv",
    ".agent/memory/working/dashboard/index.html",
    ".agent/commands/growth-ceo-loop.md",
    ".agent/commands/approval-queue.md",
    ".agent/commands/record-approval-decision.md",
    ".agent/commands/approval-decision-summary.md",
    ".agent/commands/approval-decision-inbox.md",
    ".agent/commands/decision-cockpit.md",
    ".agent/commands/post-approval-workflow.md",
    ".agent/commands/approval-packets.md",
    ".agent/commands/revenue-forecast.md",
    ".agent/commands/objective-coverage-audit.md",
    ".agent/commands/private-concepts.md",
    ".agent/commands/github-issue-drafts.md",
    ".agent/commands/github-execution-plan.md",
    ".agent/commands/github-readiness-audit.md",
    ".agent/commands/operating-review.md",
    ".agent/commands/priority-board.md",
    ".agent/commands/offer-strategy.md",
    ".agent/commands/outreach-draft-packs.md",
    ".agent/commands/outreach-playbook-library.md",
    ".agent/commands/delivery-readiness.md",
    ".agent/commands/contact-compliance.md",
    ".agent/commands/pre-send-readiness.md",
    ".agent/commands/capability-matrix.md",
    ".agent/commands/safety-invariants.md",
    ".agent/commands/research-queue.md",
    ".agent/commands/research-controller.md",
    ".agent/commands/regional-coverage-heatmap.md",
    ".agent/commands/log-research-attempt.md",
    ".agent/commands/capture-intake-candidate.md",
    ".agent/commands/automation-status.md",
    ".agent/commands/action-permissions.md",
    ".agent/commands/source-plan.md",
    ".agent/commands/source-quality-map.md",
    ".agent/commands/research-experiments.md",
    ".agent/commands/source-pivot-plan.md",
    ".agent/commands/research-suppression-list.md",
    ".agent/commands/council-registry.md",
    ".agent/commands/council-debates.md",
    ".agent/commands/council-quality-audit.md",
    ".agent/commands/council-ceo-brief.md",
    ".agent/commands/council-decision-gates.md",
    ".agent/commands/weekly-plan.md",
    ".agent/commands/improvement-scorecard.md",
    ".agent/commands/learning-queue.md",
    ".agent/commands/operator-action-queue.md",
    ".agent/commands/promote-intake.md",
    ".github/ISSUE_TEMPLATE/outreach-approval.md",
]

SCRIPTS = [
    ".agent/skills/growth-engine/scripts/assert-state.sh",
    ".agent/skills/growth-engine/scripts/run-pipeline.py",
    ".agent/skills/growth-engine/scripts/review-intake.py",
    ".agent/skills/growth-engine/scripts/verify-intake-evidence.py",
    ".agent/skills/growth-engine/scripts/generate-research-queue.py",
    ".agent/skills/growth-engine/scripts/generate-research-controller.py",
    ".agent/skills/growth-engine/scripts/generate-regional-coverage-heatmap.py",
    ".agent/skills/growth-engine/scripts/log-research-attempt.py",
    ".agent/skills/growth-engine/scripts/capture-intake-candidate.py",
    ".agent/skills/growth-engine/scripts/generate-automation-status.py",
    ".agent/skills/growth-engine/scripts/generate-action-permissions.py",
    ".agent/skills/growth-engine/scripts/generate-source-plan.py",
    ".agent/skills/growth-engine/scripts/generate-source-quality-map.py",
    ".agent/skills/growth-engine/scripts/generate-research-experiments.py",
    ".agent/skills/growth-engine/scripts/generate-source-pivot-plan.py",
    ".agent/skills/growth-engine/scripts/generate-research-suppression-list.py",
    ".agent/skills/growth-engine/scripts/generate-council-registry.py",
    ".agent/skills/growth-engine/scripts/generate-council-debates.py",
    ".agent/skills/growth-engine/scripts/generate-council-quality-audit.py",
    ".agent/skills/growth-engine/scripts/generate-council-ceo-brief.py",
    ".agent/skills/growth-engine/scripts/generate-council-decision-gates.py",
    ".agent/skills/growth-engine/scripts/generate-intake-opportunity-briefs.py",
    ".agent/skills/growth-engine/scripts/generate-private-concepts.py",
    ".agent/skills/growth-engine/scripts/generate-approval-queue.py",
    ".agent/skills/growth-engine/scripts/record-approval-decision.py",
    ".agent/skills/growth-engine/scripts/generate-approval-decision-summary.py",
    ".agent/skills/growth-engine/scripts/generate-approval-decision-inbox.py",
    ".agent/skills/growth-engine/scripts/generate-decision-cockpit.py",
    ".agent/skills/growth-engine/scripts/generate-post-approval-workflow.py",
    ".agent/skills/growth-engine/scripts/generate-approval-packets.py",
    ".agent/skills/growth-engine/scripts/generate-revenue-forecast.py",
    ".agent/skills/growth-engine/scripts/generate-objective-coverage-audit.py",
    ".agent/skills/growth-engine/scripts/generate-offer-strategy.py",
    ".agent/skills/growth-engine/scripts/generate-priority-board.py",
    ".agent/skills/growth-engine/scripts/generate-github-issue-drafts.py",
    ".agent/skills/growth-engine/scripts/generate-github-execution-plan.py",
    ".agent/skills/growth-engine/scripts/generate-github-readiness-audit.py",
    ".agent/skills/growth-engine/scripts/generate-operating-review.py",
    ".agent/skills/growth-engine/scripts/generate-weekly-plan.py",
    ".agent/skills/growth-engine/scripts/generate-improvement-scorecard.py",
    ".agent/skills/growth-engine/scripts/generate-learning-queue.py",
    ".agent/skills/growth-engine/scripts/generate-operator-action-queue.py",
    ".agent/skills/growth-engine/scripts/generate-delivery-readiness.py",
    ".agent/skills/growth-engine/scripts/generate-outreach-playbook-library.py",
    ".agent/skills/growth-engine/scripts/generate-contact-compliance.py",
    ".agent/skills/growth-engine/scripts/generate-pre-send-readiness.py",
    ".agent/skills/growth-engine/scripts/generate-capability-matrix.py",
    ".agent/skills/growth-engine/scripts/validate-safety-invariants.py",
    ".agent/skills/growth-engine/scripts/promote-intake.py",
    ".agent/skills/growth-engine/scripts/generate-dashboard.py",
    ".agent/skills/growth-engine/scripts/run-ceo-loop.py",
    ".agent/skills/growth-engine/scripts/audit-engine.py",
]

SCHEMAS = {
    ".agent/memory/working/prospect_intake.csv": ["business","region","niche","socials","website","source_urls","observed_social_signal","observed_website_gap","proposed_hook","notes"],
    ".agent/memory/working/intake_review.csv": ["date","business","region","niche","score","recommendation","missing_evidence","next_action","notes"],
    ".agent/memory/working/intake_verification.csv": ["date","business","social_status","website_status","source_status","readiness","next_action","notes"],
    ".agent/memory/working/intake_opportunity_briefs.csv": ["date","business","region","niche","readiness","brief_path","primary_opportunity","safe_next_step","notes"],
    ".agent/memory/working/approval_queue.csv": ["date","approval_type","business","priority","source_path","requested_decision","safe_command","blocked_until_approved","notes"],
    ".agent/memory/working/approval_decisions.csv": ["date","business","approval_type","decision","decided_by","evidence_path","follow_up_action","notes"],
    ".agent/memory/working/approval_decision_summary.csv": ["date","status","business","approval_type","decision","evidence_path","next_action","notes"],
    ".agent/memory/working/approval_decision_inbox.csv": ["date","rank","business","approval_type","recommended_decision","approve_command","reject_command","hold_command","approve_effect","reject_effect","hold_effect","evidence_path","packet_path","safety_gate","notes"],
    ".agent/memory/working/decision_cockpit.csv": ["date","rank","business","decision_type","recommended_decision","evidence_path","approval_packet","private_concept","github_issue_draft","github_status","approve_command","reject_command","hold_command","after_approve","still_blocked","safety_gate","notes"],
    ".agent/memory/working/post_approval_workflow.csv": ["date","rank","business","trigger_decision","step_order","step","owner","safe_command_or_action","expected_artifact","blocked_until","safety_gate","notes"],
    ".agent/memory/working/approval_packets.csv": ["date","business","rank","approval_type","recommended_decision","evidence_path","decision_command","after_approve","still_blocked","packet_path","notes"],
    ".agent/memory/working/revenue_forecast.csv": ["date","stage","count","weighted_probability","gross_monthly_fee","weighted_mrr","next_action","safety_gate","notes"],
    ".agent/memory/working/objective_coverage_audit.csv": ["date","objective_requirement","status","evidence_path","evidence_summary","remaining_gap","safety_gate","notes"],
    ".agent/memory/working/private_concepts.csv": ["date","business","region","niche","concept_path","readiness","primary_cta","notes"],
    ".agent/memory/working/github_issue_drafts.csv": ["date","business","approval_type","issue_title","labels","draft_path","safe_next_step","notes"],
    ".agent/memory/working/github_execution_plan.csv": ["date","business","issue_title","labels","draft_path","command_path","approval_status","safe_next_action","notes"],
    ".agent/memory/working/github_readiness_audit.csv": ["date","business","readiness_status","approval_packet","issue_draft","execution_plan","command_status","failure_reason","next_action","notes"],
    ".agent/memory/working/operating_review.csv": ["date","area","status","next_action","owner","safety_gate","evidence_path","notes"],
    ".agent/memory/working/priority_board.csv": ["date","rank","business","region","niche","priority_score","status","next_best_action","evidence_path","notes"],
    ".agent/memory/working/offer_strategy.csv": ["date","business","niche","tier","monthly_fee","offer_angle","trust_hook","primary_cta","outreach_angle","notes"],
    ".agent/memory/working/outreach_drafts.csv": ["date","business","channel","draft_path","approval_status","contact_basis","opt_out","next_action","notes"],
    ".agent/memory/working/outreach_playbook_library.csv": ["date","playbook_id","niche","channel","recipient_type","opening_principle","observation_type","safe_message_template","follow_up_template","opt_out","required_personalization","blocked_until","safety_gate","notes"],
    ".agent/memory/working/delivery_readiness.csv": ["date","business","stage","readiness","plan_path","next_action","safety_gate","notes"],
    ".agent/memory/working/contact_compliance.csv": ["date","business","channel","contact_basis","sender_id","opt_out","outreach_approval","compliance_status","next_action","notes"],
    ".agent/memory/working/pre_send_readiness.csv": ["date","business","readiness_status","required_gate","evidence","failure_reason","next_action","notes"],
    ".agent/memory/working/capability_matrix.csv": ["date","capability","status","evidence","remaining_gap","safety_gate","notes"],
    ".agent/memory/working/safety_invariants.csv": ["date","invariant","status","evidence","required_action","notes"],
    ".agent/memory/working/decision_log.csv": ["date","decision","area","approved_by","evidence_path","notes"],
    ".agent/memory/working/risk_register.csv": ["date","risk","severity","control","status","notes"],
    ".agent/memory/working/research_queue.csv": ["date","business","region","niche","missing_evidence","search_query","source_hint","next_action","notes"],
    ".agent/memory/working/research_controller.csv": ["date","rank","region","niche","lane_status","attempts_logged","intake_matches","priority_score","recommended_query","next_action","safety_gate","notes"],
    ".agent/memory/working/regional_coverage_heatmap.csv": ["date","rank","region","niche","coverage_status","intake_count","evidence_ready_count","attempts_logged","suppressed_patterns","priority_score","recommended_query","safe_next_action","safety_gate","notes"],
    ".agent/memory/working/automation_status.csv": ["date","automation_id","name","kind","status","schedule","workspace","safety_gate","notes"],
    ".agent/memory/working/action_permissions.csv": ["date","action","status","evidence","allowed_next_step","blocked_until","safety_gate","notes"],
    ".agent/memory/working/source_plan.csv": ["date","region","niche","query","evidence_required","safe_next_action","status","notes"],
    ".agent/memory/working/source_quality_map.csv": ["date","region","niche","source_family","query","quality_score","use_when","evidence_to_capture","failure_pattern","safe_next_action","notes"],
    ".agent/memory/working/research_experiments.csv": ["date","rank","region","niche","experiment_type","query","hypothesis","prior_failure_signal","success_criteria","safe_next_action","status","notes"],
    ".agent/memory/working/source_pivot_plan.csv": ["date","business","region","niche","pivot_reason","primary_source_family","primary_query","secondary_source_family","secondary_query","evidence_required","safe_next_action","status","notes"],
    ".agent/memory/working/research_suppression_list.csv": ["date","business","failed_attempts","suppressed_query_pattern","suppression_reason","replacement_source_family","safe_next_action","status","safety_gate","notes"],
    ".agent/memory/working/council_registry.csv": ["date","council","task_area","trigger","roles","decision_standard","output_artifact","safety_gate","notes"],
    ".agent/memory/working/council_debates.csv": ["date","decision_id","council","task_area","decision","best_case","hard_pushback","council_split","verdict","next_test","evidence_path","safety_gate","status","notes"],
    ".agent/memory/working/council_quality_audit.csv": ["date","decision_id","council","quality_status","score","missing_elements","argument_test","evidence_path","safety_gate","next_action","notes"],
    ".agent/memory/working/council_ceo_brief.csv": ["date","brief_id","priority","decision_id","council","task_area","boardroom_read","strongest_argument","strongest_objection","uncomfortable_truth","allowed_next_move","blocked_actions","daniel_decision_needed","evidence_path","status","notes"],
    ".agent/memory/working/council_decision_gates.csv": ["date","action","council","decision_id","council_verdict","action_status","gate_status","evidence","required_before_action","safety_gate","notes"],
    ".agent/memory/working/weekly_plan.csv": ["week_start","day","focus","inputs","outputs","safety_gate","done_definition","notes"],
    ".agent/memory/working/improvement_scorecard.csv": ["date","area","score","status","evidence","improvement_action","owner","notes"],
    ".agent/memory/working/learning_queue.csv": ["date","learning_id","source","area","proposal","evidence","target_artifact","approval_required","status","safety_gate","notes"],
    ".agent/memory/working/operator_action_queue.csv": ["date","rank","action_id","category","action","owner","status","evidence","safe_command_or_next_step","blocked_until","safety_gate","source_path","notes"],
    ".agent/memory/working/research_attempts.csv": ["date","business","query","source_checked","result","next_action","notes"],
}

errors = []
for rel in REQUIRED + SCRIPTS:
    if not os.path.exists(os.path.join(ROOT, rel)):
        errors.append(f"Missing required file: {rel}")
for rel, expected in SCHEMAS.items():
    with open(os.path.join(ROOT, rel), newline="", encoding="utf-8") as handle:
        header = next(csv.reader(handle), [])
    if header != expected:
        errors.append(f"CSV schema mismatch in {rel}")
for rel in SCRIPTS:
    full = os.path.join(ROOT, rel)
    if rel.endswith(".py"):
        with open(full, encoding="utf-8") as handle:
            first = handle.readline()
            rest = handle.read()
            if "python3" not in first:
                errors.append(f"Python script missing python3 shebang: {rel}")
            if re.search(r"20[0-9]{2}-[0-9]{2}-[0-9]{2}", rest):
                errors.append(f"Python script contains hard-coded date: {rel}")
    if rel.endswith(".sh") and not (os.stat(full).st_mode & stat.S_IXUSR):
        errors.append(f"Shell script is not executable: {rel}")
text = ""
for rel in [".agent/protocols/outreach-safety.md", ".agent/protocols/permissions.md"]:
    with open(os.path.join(ROOT, rel), encoding="utf-8") as handle:
        text += handle.read().lower()
for phrase in ["daniel", "do not send", "opt-out", "harvested"]:
    if phrase not in text:
        errors.append(f"Missing safety concept: {phrase}")
print("\nCap Coast Creative Engine Audit")
print("==============================")
if errors:
    print("Status: FAIL\n")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)
print("Status: PASS")
print("- Required files present")
print("- CSV schemas match")
print("- Scripts are shaped correctly")
print("- Safety concepts present")
