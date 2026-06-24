#!/usr/bin/env python3
import os
from common import clean, p, read_csv, rel, today, write_csv

FIELDS = ["date", "area", "status", "next_action", "owner", "safety_gate", "evidence_path", "notes"]
DECISION_FIELDS = ["date", "decision", "area", "approved_by", "evidence_path", "notes"]
RISK_FIELDS = ["date", "risk", "severity", "control", "status", "notes"]


def ensure_csv(path, fields):
    if not os.path.exists(path):
        write_csv(path, [], fields)


ensure_csv(p("decision_log.csv"), DECISION_FIELDS)
ensure_csv(p("risk_register.csv"), RISK_FIELDS)

intake = read_csv(p("prospect_intake.csv"))
verification = read_csv(p("intake_verification.csv"))
research = read_csv(p("research_queue.csv"))
research_controller = read_csv(p("research_controller.csv"))
automation_status = read_csv(p("automation_status.csv"))
action_permissions = read_csv(p("action_permissions.csv"))
council_decision_gates = read_csv(p("council_decision_gates.csv"))
source_plan = read_csv(p("source_plan.csv"))
source_quality = read_csv(p("source_quality_map.csv"))
research_experiments = read_csv(p("research_experiments.csv"))
regional_heatmap = read_csv(p("regional_coverage_heatmap.csv"))
source_pivots = read_csv(p("source_pivot_plan.csv"))
research_suppression = read_csv(p("research_suppression_list.csv"))
council_registry = read_csv(p("council_registry.csv"))
council_debates = read_csv(p("council_debates.csv"))
council_quality = read_csv(p("council_quality_audit.csv"))
council_brief = read_csv(p("council_ceo_brief.csv"))
approvals = read_csv(p("approval_queue.csv"))
approval_decisions = read_csv(p("approval_decision_summary.csv"))
approval_inbox = read_csv(p("approval_decision_inbox.csv"))
decision_cockpit = read_csv(p("decision_cockpit.csv"))
post_approval = read_csv(p("post_approval_workflow.csv"))
approval_packets = read_csv(p("approval_packets.csv"))
revenue_forecast = read_csv(p("revenue_forecast.csv"))
objective_coverage = read_csv(p("objective_coverage_audit.csv"))
concepts = read_csv(p("private_concepts.csv"))
issue_drafts = read_csv(p("github_issue_drafts.csv"))
github_plan = read_csv(p("github_execution_plan.csv"))
github_readiness = read_csv(p("github_readiness_audit.csv"))
prospects = read_csv(p("prospects.csv"))
outreach = read_csv(p("outreach_log.csv"))
priority = read_csv(p("priority_board.csv"))
strategy = read_csv(p("offer_strategy.csv"))
drafts = read_csv(p("outreach_drafts.csv"))
playbooks = read_csv(p("outreach_playbook_library.csv"))
delivery = read_csv(p("delivery_readiness.csv"))
compliance = read_csv(p("contact_compliance.csv"))
pre_send = read_csv(p("pre_send_readiness.csv"))
scorecard = read_csv(p("improvement_scorecard.csv"))
learning_queue = read_csv(p("learning_queue.csv"))
operator_queue = read_csv(p("operator_action_queue.csv"))
capabilities = read_csv(p("capability_matrix.csv"))
safety_invariants = read_csv(p("safety_invariants.csv"))

ready = [row for row in verification if row.get("readiness") == "promotion-review-ready"]
rows = []

rows.append({
    "date": today(),
    "area": "Prospect intake",
    "status": f"{len(intake)} staged / {len(ready)} evidence-ready",
    "next_action": "Review pending promotion approvals before any prospect work starts.",
    "owner": "Daniel",
    "safety_gate": "Promotion approval required",
    "evidence_path": ".agent/memory/working/approval_queue.csv",
    "notes": "Promotion is not outreach approval.",
})
rows.append({
    "date": today(),
    "area": "Objective coverage",
    "status": f"{len(objective_coverage)} original-objective checks",
    "next_action": "Use gated items as the honest remaining path to full supervised business operation.",
    "owner": "Codex",
    "safety_gate": "Objective audit does not approve blocked actions",
    "evidence_path": ".agent/memory/working/objective_coverage_audit.csv",
    "notes": "Maps autonomous CEO engine, outreach, design, tracking, GitHub, region coverage, and revenue management.",
})
rows.append({
    "date": today(),
    "area": "Safety invariants",
    "status": f"{len(safety_invariants)} logical safety checks",
    "next_action": "Treat any failed invariant as a hard stop before outreach or promotion work.",
    "owner": "Codex",
    "safety_gate": "Invariant failures block the CEO loop",
    "evidence_path": ".agent/memory/working/safety_invariants.csv",
    "notes": "Cross-file consistency and approval enforcement checks.",
})
rows.append({
    "date": today(),
    "area": "Capability matrix",
    "status": f"{len(capabilities)} objective coverage checks",
    "next_action": "Use gated items as the remaining path to full autonomous business operation.",
    "owner": "Codex",
    "safety_gate": "Readiness audit does not approve actions",
    "evidence_path": ".agent/memory/working/capability_matrix.csv",
    "notes": "Maps current engine state to the original objective.",
})
rows.append({
    "date": today(),
    "area": "Contact compliance",
    "status": f"{len(compliance)} contact-basis checks",
    "next_action": "Require contact basis, sender ID, opt-out, and explicit outreach approval before any send.",
    "owner": "Daniel",
    "safety_gate": "Compliance review is not outreach approval",
    "evidence_path": ".agent/memory/working/contact_compliance.csv",
    "notes": "Commercial electronic messages require a lawful basis, identification, and opt-out.",
})
rows.append({
    "date": today(),
    "area": "Pre-send readiness",
    "status": f"{len(pre_send)} send-readiness audit rows",
    "next_action": "Treat any blocked-pre-send or blocked-no-approved-prospects status as a hard stop for outreach.",
    "owner": "Daniel",
    "safety_gate": "Pre-send readiness does not send or approve outreach",
    "evidence_path": ".agent/memory/working/pre_send_readiness.csv",
    "notes": "Checks consent/contact basis, sender ID, opt-out, exact-copy approval, and manual send gate.",
})
rows.append({
    "date": today(),
    "area": "Delivery readiness",
    "status": f"{len(delivery)} internal delivery plans",
    "next_action": "Generate delivery plans after prospect promotion, then keep all client-facing steps gated.",
    "owner": "Codex",
    "safety_gate": "No publish, hosting, billing, or proposal send without approval",
    "evidence_path": ".agent/memory/working/delivery_readiness.csv",
    "notes": "Delivery plans are internal project scaffolds only.",
})
rows.append({
    "date": today(),
    "area": "Approval decisions",
    "status": f"{len(approval_decisions)} decision summary items / {len(approval_packets)} approval packets",
    "next_action": "Use approval packets to record approve, reject, or hold before promotion work proceeds.",
    "owner": "Daniel",
    "safety_gate": "Decision recording is not outreach approval",
    "evidence_path": ".agent/memory/working/approval_decision_summary.csv",
    "notes": "Approve decisions still require separate promotion execution.",
})
rows.append({
    "date": today(),
    "area": "Approval decision inbox",
    "status": f"{len(approval_inbox)} approve/reject/hold decision rows",
    "next_action": "Use the inbox to record approve, reject, or hold without confusing promotion with outreach.",
    "owner": "Daniel",
    "safety_gate": "Decision recording does not approve outreach, publishing, GitHub writes, billing, or client-facing actions",
    "evidence_path": ".agent/memory/working/approval_decision_inbox.csv",
    "notes": "Gives Daniel all decision choices for each promotion packet.",
})
rows.append({
    "date": today(),
    "area": "Decision cockpit",
    "status": f"{len(decision_cockpit)} consolidated decision rows",
    "next_action": "Review cockpit rows when deciding approve, reject, or hold for promotion packets.",
    "owner": "Daniel",
    "safety_gate": "Cockpit is advisory and only records local decisions",
    "evidence_path": ".agent/memory/working/decision_cockpit.csv",
    "notes": "Combines evidence, private concepts, GitHub local drafts, and blocked follow-ons in one place.",
})
rows.append({
    "date": today(),
    "area": "Post-approval workflow",
    "status": f"{len(post_approval)} gated workflow steps",
    "next_action": "Use this map after a promotion approval is recorded, then stop again at outreach and remote-write gates.",
    "owner": "Codex",
    "safety_gate": "Workflow map is advisory and cannot execute external actions",
    "evidence_path": ".agent/memory/working/post_approval_workflow.csv",
    "notes": "Turns approval decisions into a safe regeneration sequence.",
})
rows.append({
    "date": today(),
    "area": "Self-improvement",
    "status": f"{len(scorecard)} scorecard checks",
    "next_action": "Review watch and needs-work items before changing process or memory.",
    "owner": "Codex",
    "safety_gate": "Diagnostics do not approve actions",
    "evidence_path": ".agent/memory/working/improvement_scorecard.csv",
    "notes": "Use evidence before updating durable lessons.",
})
rows.append({
    "date": today(),
    "area": "Learning queue",
    "status": f"{len(learning_queue)} gated learning proposals",
    "next_action": "Review proposal items before changing durable memory, protocols, or operating manual.",
    "owner": "Daniel",
    "safety_gate": "Learning proposals do not edit memory or approve actions",
    "evidence_path": ".agent/memory/working/learning_queue.csv",
    "notes": "Turns repeated evidence and council verdicts into reviewable self-improvement proposals.",
})
rows.append({
    "date": today(),
    "area": "Operator action queue",
    "status": f"{len(operator_queue)} ranked actions",
    "next_action": "Work allowed-now research items and keep Daniel/external actions gated.",
    "owner": "Codex",
    "safety_gate": "Queue is advisory and cannot approve promotion, outreach, remote writes, publishing, or billing",
    "evidence_path": ".agent/memory/working/operator_action_queue.csv",
    "notes": "Unifies research, approvals, GitHub, outreach, and weekly operations into one action surface.",
})
rows.append({
    "date": today(),
    "area": "Source plan",
    "status": f"{len(source_plan)} regional search lanes",
    "next_action": "Run research-only checks from source_plan.csv before adding new intake rows.",
    "owner": "Codex",
    "safety_gate": "Discovery is not contact",
    "evidence_path": ".agent/memory/working/source_plan.csv",
    "notes": "Covers Kawana, Rockhampton, Yeppoon, Emu Park, and Capricorn Coast.",
})
rows.append({
    "date": today(),
    "area": "Source quality map",
    "status": f"{len(source_quality)} targeted source routes",
    "next_action": "Use high-quality source routes before broad web searches when a lane has prior failures.",
    "owner": "Codex",
    "safety_gate": "Source routing is research-only and does not approve capture or outreach",
    "evidence_path": ".agent/memory/working/source_quality_map.csv",
    "notes": "Designed to reduce repeated locality-page search failures.",
})
rows.append({
    "date": today(),
    "area": "Outreach drafts",
    "status": f"{len(drafts)} unsent draft packs",
    "next_action": "Create drafts only for promoted prospects, then require separate send approval.",
    "owner": "Codex",
    "safety_gate": "Drafting is not sending",
    "evidence_path": ".agent/memory/working/outreach_drafts.csv",
    "notes": "Every draft must include opt-out wording and documented contact basis.",
})
rows.append({
    "date": today(),
    "area": "Outreach playbook library",
    "status": f"{len(playbooks)} generic playbook templates",
    "next_action": "Use playbooks only as council-reviewed starting points after prospect approval and exact outreach approval.",
    "owner": "Codex",
    "safety_gate": "Templates are not approved copy and cannot be sent",
    "evidence_path": ".agent/memory/working/outreach_playbook_library.csv",
    "notes": "Every playbook must keep placeholders, opt-out wording, contact-basis requirements, and manual send gates.",
})
rows.append({
    "date": today(),
    "area": "Offer strategy",
    "status": f"{len(strategy)} candidate offer angles prepared",
    "next_action": "Use the strategy matrix when creating mockup briefs, outreach drafts, and proposals after approval.",
    "owner": "Codex",
    "safety_gate": "Strategy is not outreach approval",
    "evidence_path": ".agent/memory/working/offer_strategy.csv",
    "notes": "Keeps pricing, trust hooks, and CTAs consistent with the business model.",
})
rows.append({
    "date": today(),
    "area": "Revenue forecast",
    "status": f"{len(revenue_forecast)} forecast stages",
    "next_action": "Use forecast stages to prioritize approval decisions and avoid mistaking pipeline value for booked revenue.",
    "owner": "Codex",
    "safety_gate": "Forecast is not invoice, charge, or client promise approval",
    "evidence_path": ".agent/memory/working/revenue_forecast.csv",
    "notes": "Weighted MRR is planning math only.",
})
rows.append({
    "date": today(),
    "area": "Priority board",
    "status": f"{len(priority)} ranked candidates",
    "next_action": "Review the top ranked item first, then decide whether to approve promotion.",
    "owner": "Daniel",
    "safety_gate": "Ranking is not approval",
    "evidence_path": ".agent/memory/working/priority_board.csv",
    "notes": "Priority score combines evidence strength, niche fit, website opportunity, and concept readiness.",
})
rows.append({
    "date": today(),
    "area": "Research queue",
    "status": f"{len(research)} candidates need more evidence",
    "next_action": "Continue research-only verification for social profiles and owned website gaps.",
    "owner": "Codex",
    "safety_gate": "Research-only; no account login, contact, forms, DMs, or calls",
    "evidence_path": ".agent/memory/working/research_queue.csv",
    "notes": "Log each source checked in research_attempts.csv.",
})
rows.append({
    "date": today(),
    "area": "Research controller",
    "status": f"{len(research_controller)} ranked source lanes",
    "next_action": "Work the highest-ranked safe lane, then log the result before adding any intake evidence.",
    "owner": "Codex",
    "safety_gate": "Research-only; no account login, contact, forms, DMs, calls, or social interaction",
    "evidence_path": ".agent/memory/working/research_controller.csv",
    "notes": "Turns the source plan into a daily research priority order.",
})
rows.append({
    "date": today(),
    "area": "Regional coverage heatmap",
    "status": f"{len(regional_heatmap)} region/niche lanes scored",
    "next_action": "Use top under-covered lanes for research-only sourcing before repeating saturated searches.",
    "owner": "Codex",
    "safety_gate": "Heatmap is research-only and cannot approve capture or outreach",
    "evidence_path": ".agent/memory/working/regional_coverage_heatmap.csv",
    "notes": "Balances Kawana, Capricorn Coast, Rockhampton, Yeppoon, and Emu Park.",
})
rows.append({
    "date": today(),
    "area": "Research experiments",
    "status": f"{len(research_experiments)} safe experiment routes",
    "next_action": "Run the top experiment as research-only, then capture strong evidence or log a failed attempt.",
    "owner": "Codex",
    "safety_gate": "Experiments are research-only and do not approve contact or capture weak evidence",
    "evidence_path": ".agent/memory/working/research_experiments.csv",
    "notes": "Converts failed broad searches into deliberate source-route tests.",
})
rows.append({
    "date": today(),
    "area": "Source pivot plan",
    "status": f"{len(source_pivots)} candidates need alternate source-family research",
    "next_action": "Use pivot queries when named social searches have failed repeatedly.",
    "owner": "Codex",
    "safety_gate": "Pivot research is research-only and cannot approve capture, promotion, or outreach",
    "evidence_path": ".agent/memory/working/source_pivot_plan.csv",
    "notes": "Prevents repeated failed social searches by shifting to directories, official sources, or tourism/council sources.",
})
rows.append({
    "date": today(),
    "area": "Research suppression list",
    "status": f"{len(research_suppression)} repeated failed query patterns suppressed",
    "next_action": "Use suppression rows to avoid repeating weak public searches until a stronger source family appears.",
    "owner": "Codex",
    "safety_gate": "Suppression is advisory research memory only and cannot approve capture or outreach",
    "evidence_path": ".agent/memory/working/research_suppression_list.csv",
    "notes": "This is the self-regulating layer for failed source patterns.",
})
rows.append({
    "date": today(),
    "area": "Council debates",
    "status": f"{len(council_debates)} active debate records / {len(council_registry)} council routes",
    "next_action": "Use council verdicts as advisory decision pressure before any gated action.",
    "owner": "Codex",
    "safety_gate": "Council verdicts do not approve gated external actions",
    "evidence_path": ".agent/memory/working/council_debates.csv",
    "notes": "Every debate includes best case, hard pushback, split, verdict, and next test.",
})
rows.append({
    "date": today(),
    "area": "Council quality",
    "status": f"{len(council_quality)} debate quality checks",
    "next_action": "Regenerate council debates if any quality_status is needs-rework.",
    "owner": "Codex",
    "safety_gate": "Council quality does not approve gated actions",
    "evidence_path": ".agent/memory/working/council_quality_audit.csv",
    "notes": "Checks for real disagreement, verdict, next test, evidence, and safety gate.",
})
rows.append({
    "date": today(),
    "area": "Council CEO brief",
    "status": f"{len(council_brief)} ranked boardroom guidance items",
    "next_action": "Use the brief to choose the next supervised move while keeping blocked actions blocked.",
    "owner": "Codex",
    "safety_gate": "CEO brief is advisory and cannot approve gated actions",
    "evidence_path": ".agent/memory/working/council_ceo_brief.csv",
    "notes": "Summarizes council arguments, objections, uncomfortable truths, allowed moves, and Daniel decisions needed.",
})
rows.append({
    "date": today(),
    "area": "Council decision gates",
    "status": f"{len(council_decision_gates)} action-to-council gates",
    "next_action": "Check gate_status before using any council verdict to justify an action.",
    "owner": "Codex",
    "safety_gate": "Council gates do not replace Daniel approval or action permissions",
    "evidence_path": ".agent/memory/working/council_decision_gates.csv",
    "notes": "Prevents a council recommendation from being mistaken for permission.",
})
rows.append({
    "date": today(),
    "area": "Automation status",
    "status": f"{len(automation_status)} automation configs checked",
    "next_action": "Keep prospect scanning active, research-only, and tied to log/capture gates.",
    "owner": "Codex",
    "safety_gate": "Automation may research and stage only; no outreach or promotion",
    "evidence_path": ".agent/memory/working/automation_status.csv",
    "notes": "Verifies actual Codex automation config rather than a static note.",
})
rows.append({
    "date": today(),
    "area": "Action permissions",
    "status": f"{len(action_permissions)} allowed/blocked action checks",
    "next_action": "Use blocked_until fields before taking any promotion, outreach, GitHub, or publishing step.",
    "owner": "Codex",
    "safety_gate": "Permission map is advisory but binding for autonomous actions",
    "evidence_path": ".agent/memory/working/action_permissions.csv",
    "notes": "Turns safety gates into operational action states.",
})
rows.append({
    "date": today(),
    "area": "Private concepts",
    "status": f"{len(concepts)} internal concept pages generated",
    "next_action": "Use concepts only for internal review until a prospect and outreach approval exist.",
    "owner": "Codex",
    "safety_gate": "Do not publish or send concepts",
    "evidence_path": ".agent/memory/working/private_concepts.csv",
    "notes": "Concepts are planning assets, not client-facing promises.",
})
rows.append({
    "date": today(),
    "area": "GitHub workflow",
    "status": f"{len(issue_drafts)} local issue drafts prepared",
    "next_action": "Create GitHub issues only after Daniel approves the exact issue creation workflow.",
    "owner": "Daniel",
    "safety_gate": "No remote issue creation without explicit approval",
    "evidence_path": ".agent/memory/working/github_issue_drafts.csv",
    "notes": "Drafts are local Markdown only.",
})
rows.append({
    "date": today(),
    "area": "GitHub readiness",
    "status": f"{len(github_readiness)} local readiness checks",
    "next_action": "Fix any local mismatch before asking Daniel to approve remote issue creation.",
    "owner": "Codex",
    "safety_gate": "Readiness does not approve remote GitHub writes",
    "evidence_path": ".agent/memory/working/github_readiness_audit.csv",
    "notes": "Checks packet, issue draft, execution plan, command artifact, title/label match, and lock status.",
})
rows.append({
    "date": today(),
    "area": "GitHub execution plan",
    "status": f"{len(github_plan)} local issue creation commands prepared",
    "next_action": "Execute only after Daniel approves exact remote issue creation.",
    "owner": "Daniel",
    "safety_gate": "No remote GitHub writes without approval",
    "evidence_path": ".agent/memory/working/github_execution_plan.csv",
    "notes": "The generated command file is a plan, not permission to run it.",
})
rows.append({
    "date": today(),
    "area": "Outreach",
    "status": f"{len(outreach)} logged outreach events / {len(prospects)} approved prospects",
    "next_action": "Keep outreach disabled until prospects are promoted and outreach drafts are separately approved.",
    "owner": "Daniel",
    "safety_gate": "Explicit outreach approval required",
    "evidence_path": ".agent/memory/working/outreach_log.csv",
    "notes": "No email, SMS, DM, form submission, social post, or call.",
})

write_csv(p("operating_review.csv"), rows, FIELDS)

risk_rows = [
    {
        "date": today(),
        "risk": "Accidental unsupervised outreach",
        "severity": "high",
        "control": "Outreach safety protocol, empty outreach log unless approved, approval queue separation",
        "status": "controlled",
        "notes": "Promotion and outreach are separate gates.",
    },
    {
        "date": today(),
        "risk": "Weak or stale prospect evidence",
        "severity": "medium",
        "control": "Verification CSV, research queue, source notes, promotion-review-ready status",
        "status": "controlled",
        "notes": "Research-more candidates stay out of prospects.csv.",
    },
    {
        "date": today(),
        "risk": "Overpromising delivery scope",
        "severity": "medium",
        "control": "Proposal/admin trackers and monthly tier memory",
        "status": "monitor",
        "notes": "Keep offers to the approved flat monthly website design model.",
    },
]
write_csv(p("risk_register.csv"), risk_rows, RISK_FIELDS)

os.makedirs(p("operating_reviews"), exist_ok=True)
path = p("operating_reviews", f"{today()}.md")
with open(path, "w", encoding="utf-8") as handle:
    handle.write("# Cap Coast Creative Operating Review\n\n")
    handle.write(f"- Date: {today()}\n")
    handle.write(f"- Intake candidates: {len(intake)}\n")
    handle.write(f"- Evidence-ready candidates: {len(ready)}\n")
    handle.write(f"- Pending approvals: {len(approvals)}\n")
    handle.write(f"- Approval decision items: {len(approval_decisions)}\n")
    handle.write(f"- Approval decision inbox items: {len(approval_inbox)}\n")
    handle.write(f"- Decision cockpit items: {len(decision_cockpit)}\n")
    handle.write(f"- Post-approval workflow items: {len(post_approval)}\n")
    handle.write(f"- Approval packets: {len(approval_packets)}\n")
    handle.write(f"- GitHub execution plan items: {len(github_plan)}\n")
    handle.write(f"- GitHub readiness items: {len(github_readiness)}\n")
    handle.write(f"- Delivery readiness items: {len(delivery)}\n")
    handle.write(f"- Contact compliance items: {len(compliance)}\n")
    handle.write(f"- Pre-send readiness items: {len(pre_send)}\n")
    handle.write(f"- Source plan lanes: {len(source_plan)}\n")
    handle.write(f"- Source quality routes: {len(source_quality)}\n")
    handle.write(f"- Research experiment items: {len(research_experiments)}\n")
    handle.write(f"- Source pivot items: {len(source_pivots)}\n")
    handle.write(f"- Research suppression items: {len(research_suppression)}\n")
    handle.write(f"- Council route items: {len(council_registry)}\n")
    handle.write(f"- Council debate items: {len(council_debates)}\n")
    handle.write(f"- Council quality items: {len(council_quality)}\n")
    handle.write(f"- Council CEO brief items: {len(council_brief)}\n")
    handle.write(f"- Council decision gate items: {len(council_decision_gates)}\n")
    handle.write(f"- Research controller lanes: {len(research_controller)}\n")
    handle.write(f"- Regional coverage heatmap lanes: {len(regional_heatmap)}\n")
    handle.write(f"- Automation status items: {len(automation_status)}\n")
    handle.write(f"- Action permission items: {len(action_permissions)}\n")
    handle.write(f"- Improvement scorecard items: {len(scorecard)}\n")
    handle.write(f"- Learning queue items: {len(learning_queue)}\n")
    handle.write(f"- Operator action queue items: {len(operator_queue)}\n")
    handle.write(f"- Capability matrix items: {len(capabilities)}\n")
    handle.write(f"- Safety invariant checks: {len(safety_invariants)}\n")
    handle.write(f"- Priority board items: {len(priority)}\n")
    handle.write(f"- Offer strategy items: {len(strategy)}\n")
    handle.write(f"- Outreach playbook items: {len(playbooks)}\n")
    handle.write(f"- Revenue forecast stages: {len(revenue_forecast)}\n")
    handle.write(f"- Objective coverage checks: {len(objective_coverage)}\n")
    handle.write(f"- Approved prospects: {len(prospects)}\n")
    handle.write(f"- Outreach events: {len(outreach)}\n\n")
    handle.write("## Control Board\n\n")
    for row in rows:
        handle.write(f"- {row['area']}: {row['status']} / {row['next_action']} / Gate: {row['safety_gate']}\n")
    handle.write("\n## Risks\n\n")
    for row in risk_rows:
        handle.write(f"- {row['severity']} / {row['risk']}: {row['control']} ({row['status']})\n")

print(rel(path))
