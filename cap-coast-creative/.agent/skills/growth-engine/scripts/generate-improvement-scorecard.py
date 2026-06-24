#!/usr/bin/env python3
import os
from common import p, read_csv, rel, today, write_csv

FIELDS = ["date", "area", "score", "status", "evidence", "improvement_action", "owner", "notes"]

intake = read_csv(p("prospect_intake.csv"))
verification = read_csv(p("intake_verification.csv"))
approvals = read_csv(p("approval_queue.csv"))
approval_decisions = read_csv(p("approval_decisions.csv"))
prospects = read_csv(p("prospects.csv"))
source_plan = read_csv(p("source_plan.csv"))
research_controller = read_csv(p("research_controller.csv"))
source_quality = read_csv(p("source_quality_map.csv"))
research = read_csv(p("research_queue.csv"))
attempts = read_csv(p("research_attempts.csv"))
concepts = read_csv(p("private_concepts.csv"))
strategy = read_csv(p("offer_strategy.csv"))
drafts = read_csv(p("outreach_drafts.csv"))
compliance = read_csv(p("contact_compliance.csv"))
risks = read_csv(p("risk_register.csv"))

ready = [row for row in verification if row.get("readiness") == "promotion-review-ready"]
active_source_lanes = [row for row in source_plan if row.get("status") == "active"]
controlled_risks = [row for row in risks if row.get("status") in {"controlled", "monitor"}]


def status(score):
    if score >= 85:
        return "strong"
    if score >= 65:
        return "watch"
    return "needs-work"


rows = []
checks = [
    {
        "area": "Pipeline evidence",
        "score": min(100, 55 + len(ready) * 10),
        "evidence": f"{len(ready)} promotion-ready / {len(intake)} intake candidates",
        "improvement_action": "Convert research-more candidates only after verified social and website-gap evidence is found.",
        "owner": "Codex",
    },
    {
        "area": "Research coverage",
        "score": min(100, 45 + len(active_source_lanes) * 2 + len(attempts) * 3 + (10 if research_controller else 0) + (10 if source_quality else 0)),
        "evidence": f"{len(source_plan)} source lanes / {len(research_controller)} ranked / {len(source_quality)} source routes / {len(active_source_lanes)} active / {len(attempts)} attempts logged",
        "improvement_action": "Let the weekday automation work high-quality source routes before broad search, then log every source checked.",
        "owner": "Codex",
    },
    {
        "area": "Approval bottleneck",
        "score": 90 if not approvals else max(45, 90 - len(approvals) * 8 + len(approval_decisions) * 5),
        "evidence": f"{len(approvals)} pending approvals / {len(approval_decisions)} decisions / {len(prospects)} approved prospects",
        "improvement_action": "Review top ranked approval items and record approve/reject/hold decisions before promotion.",
        "owner": "Daniel",
    },
    {
        "area": "Offer readiness",
        "score": min(100, 50 + len(strategy) * 4 + len(concepts) * 3),
        "evidence": f"{len(strategy)} offer strategies / {len(concepts)} private concepts",
        "improvement_action": "Keep strategy, CTA, price tier, and trust hooks aligned for priority candidates.",
        "owner": "Codex",
    },
    {
        "area": "Outreach safety",
        "score": 100 if not drafts and not prospects else 85,
        "evidence": f"{len(drafts)} draft packs / {len(compliance)} contact checks / {len(prospects)} approved prospects",
        "improvement_action": "Keep drafts unsent until contact basis, sender ID, opt-out, and explicit outreach approval exist.",
        "owner": "Daniel",
    },
    {
        "area": "Risk control",
        "score": min(100, 50 + len(controlled_risks) * 15),
        "evidence": f"{len(controlled_risks)} controlled or monitored risks / {len(risks)} total risks",
        "improvement_action": "Promote repeated failures into experiments before changing durable lessons.",
        "owner": "Codex",
    },
]

for check in checks:
    score = check["score"]
    rows.append({
        "date": today(),
        "area": check["area"],
        "score": str(score),
        "status": status(score),
        "evidence": check["evidence"],
        "improvement_action": check["improvement_action"],
        "owner": check["owner"],
        "notes": "Self-improvement item; does not approve outreach or change durable memory.",
    })

write_csv(p("improvement_scorecard.csv"), rows, FIELDS)

os.makedirs(p("improvement_scorecards"), exist_ok=True)
path = p("improvement_scorecards", f"{today()}.md")
with open(path, "w", encoding="utf-8") as handle:
    handle.write("# Cap Coast Creative Improvement Scorecard\n\n")
    handle.write(f"- Date: {today()}\n")
    handle.write("- Safety: scorecard is diagnostic only.\n\n")
    for row in rows:
        handle.write(f"- {row['area']}: {row['score']} / {row['status']} / {row['improvement_action']} / Evidence: {row['evidence']}\n")

print(rel(path))
