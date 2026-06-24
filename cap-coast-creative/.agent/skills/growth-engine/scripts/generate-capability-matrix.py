#!/usr/bin/env python3
import os
from common import p, read_csv, rel, today, write_csv

FIELDS = ["date", "capability", "status", "evidence", "remaining_gap", "safety_gate", "notes"]

data = {
    "source_plan": read_csv(p("source_plan.csv")),
    "research_controller": read_csv(p("research_controller.csv")),
    "automation_status": read_csv(p("automation_status.csv")),
    "intake": read_csv(p("prospect_intake.csv")),
    "verification": read_csv(p("intake_verification.csv")),
    "approvals": read_csv(p("approval_queue.csv")),
    "approval_decisions": read_csv(p("approval_decisions.csv")),
    "prospects": read_csv(p("prospects.csv")),
    "concepts": read_csv(p("private_concepts.csv")),
    "priority": read_csv(p("priority_board.csv")),
    "strategy": read_csv(p("offer_strategy.csv")),
    "github_plan": read_csv(p("github_execution_plan.csv")),
    "weekly": read_csv(p("weekly_plan.csv")),
    "scorecard": read_csv(p("improvement_scorecard.csv")),
    "delivery": read_csv(p("delivery_readiness.csv")),
    "compliance": read_csv(p("contact_compliance.csv")),
    "outreach": read_csv(p("outreach_log.csv")),
    "safety_invariants": read_csv(p("safety_invariants.csv")),
}

ready_count = sum(1 for row in data["verification"] if row.get("readiness") == "promotion-review-ready")

rows = [
    {
        "capability": "Regional business discovery",
        "status": "ready",
        "evidence": f"{len(data['source_plan'])} source lanes / {len(data['research_controller'])} ranked lanes / {len(data['automation_status'])} automation checks",
        "remaining_gap": "Run more research passes and add only sourced candidates.",
        "safety_gate": "Discovery is not contact.",
        "notes": "Covers Kawana, Rockhampton, Yeppoon, Emu Park, and Capricorn Coast.",
    },
    {
        "capability": "Social-first prospect intake",
        "status": "ready",
        "evidence": f"{len(data['intake'])} staged candidates / {ready_count} evidence-ready",
        "remaining_gap": "Verify remaining research-more candidates.",
        "safety_gate": "Staged intake is not promotion.",
        "notes": "Requires public source URL and business-owned social evidence.",
    },
    {
        "capability": "Website design concept engine",
        "status": "ready",
        "evidence": f"{len(data['concepts'])} private concept pages",
        "remaining_gap": "Concepts stay internal until approved.",
        "safety_gate": "Do not publish or send private concepts.",
        "notes": "Generated for promotion-review-ready candidates.",
    },
    {
        "capability": "Prioritization and offer strategy",
        "status": "ready",
        "evidence": f"{len(data['priority'])} ranked items / {len(data['strategy'])} offer strategies",
        "remaining_gap": "Use top-ranked approvals first.",
        "safety_gate": "Ranking and strategy are not approval.",
        "notes": "Includes price tier, CTA, trust hook, and next best action.",
    },
    {
        "capability": "Approval control",
        "status": "gated",
        "evidence": f"{len(data['approvals'])} approvals / {len(data['approval_decisions'])} recorded decisions / {len(data['prospects'])} approved prospects",
        "remaining_gap": "Daniel must record approve/reject/hold decisions before promotion.",
        "safety_gate": "Recorded approval required before promotion.",
        "notes": "Promotion script now enforces decision ledger.",
    },
    {
        "capability": "GitHub work orchestration",
        "status": "gated",
        "evidence": f"{len(data['github_plan'])} local issue commands prepared",
        "remaining_gap": "Remote issue creation requires explicit approval.",
        "safety_gate": "No remote GitHub writes without approval.",
        "notes": "Commands are local plan artifacts only.",
    },
    {
        "capability": "Cold outreach drafting",
        "status": "gated",
        "evidence": f"{len(data['prospects'])} approved prospects / {len(data['compliance'])} contact checks / {len(data['outreach'])} outreach events",
        "remaining_gap": "Needs promoted prospect, contact basis, opt-out, sender ID, and outreach approval.",
        "safety_gate": "No email, SMS, DM, forms, social posts, or calls without approval.",
        "notes": "Draft generators stay empty until eligible prospects exist.",
    },
    {
        "capability": "Client delivery operations",
        "status": "gated",
        "evidence": f"{len(data['delivery'])} delivery readiness plans",
        "remaining_gap": "Needs promoted prospect before delivery plan activation.",
        "safety_gate": "No publishing, hosting, billing, or proposal sending without approval.",
        "notes": "Delivery stages and gates are defined.",
    },
    {
        "capability": "CEO operating rhythm",
        "status": "ready",
        "evidence": f"{len(data['weekly'])} weekly plan items",
        "remaining_gap": "Continue running CEO loop and reviews.",
        "safety_gate": "Operating plans do not approve actions.",
        "notes": "Monday-Friday cadence is generated.",
    },
    {
        "capability": "Self-improvement and risk control",
        "status": "ready",
        "evidence": f"{len(data['scorecard'])} scorecard checks / {len(data['safety_invariants'])} safety invariant checks",
        "remaining_gap": "Use repeated outcomes before changing durable lessons.",
        "safety_gate": "Diagnostics do not approve actions.",
        "notes": "Scorecard identifies approval bottleneck as current weak point.",
    },
]

for row in rows:
    row["date"] = today()

write_csv(p("capability_matrix.csv"), rows, FIELDS)

os.makedirs(p("capability_matrices"), exist_ok=True)
path = p("capability_matrices", f"{today()}.md")
with open(path, "w", encoding="utf-8") as handle:
    handle.write("# Cap Coast Creative Capability Matrix\n\n")
    handle.write(f"- Date: {today()}\n")
    handle.write("- Purpose: verify progress against the full business-engine objective.\n\n")
    for row in rows:
        handle.write(f"- {row['capability']}: {row['status']} / {row['evidence']} / Gap: {row['remaining_gap']}\n")

print(rel(path))
