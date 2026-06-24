#!/usr/bin/env python3
import os
from common import clean, p, read_csv, rel, today, write_csv

FIELDS = ["date", "decision_id", "council", "task_area", "decision", "best_case", "hard_pushback", "council_split", "verdict", "next_test", "evidence_path", "safety_gate", "status", "notes"]

research_experiments = read_csv(p("research_experiments.csv"))
approvals = read_csv(p("approval_queue.csv"))
approval_packets = read_csv(p("approval_packets.csv"))
prospects = read_csv(p("prospects.csv"))
pre_send = read_csv(p("pre_send_readiness.csv"))
github_readiness = read_csv(p("github_readiness_audit.csv"))
concepts = read_csv(p("private_concepts.csv"))
strategy = read_csv(p("offer_strategy.csv"))
revenue = read_csv(p("revenue_forecast.csv"))

rows = []

top_experiment = research_experiments[0] if research_experiments else {}
research_next_test = "Run the top research_experiments.csv route, then capture strong evidence or log the failed attempt."
if top_experiment:
    research_next_test = (
        f"Run research-only query {clean(top_experiment.get('query'))}; capture only if public business-owned social/profile, "
        "region fit, and website-gap evidence are all present; otherwise log the failed attempt."
    )
rows.append({
    "decision_id": "research-next-lane",
    "council": "Prospect Research Council",
    "task_area": "prospecting",
    "decision": "Should the engine keep using broad regional searches or switch to a narrower source-route experiment?",
    "best_case": "Broad search is fast and can surface unknown businesses without hand-curated directories.",
    "hard_pushback": "Broad search has repeatedly returned locality pages; repeating it burns time and creates false confidence.",
    "council_split": "Local scout wants wider coverage; Evidence clerk demands business-owned proof; Skeptic says failed patterns must change; Safety controller allows only public research.",
    "verdict": "test-smaller-source-route",
    "next_test": research_next_test,
    "evidence_path": ".agent/memory/working/research_experiments.csv",
    "safety_gate": "Research-only; no contact, login, scraping behind login, forms, DMs, calls, or social interaction.",
    "status": "ready-for-research-only-test",
    "notes": "Council chooses a smaller source-route test before more broad search.",
})

rows.append({
    "decision_id": "approval-bottleneck",
    "council": "Titan CEO Council",
    "task_area": "strategy",
    "decision": "Should the engine promote evidence-ready candidates automatically to unlock outreach work?",
    "best_case": "Promotion would unlock drafts, delivery planning, and pipeline learning faster.",
    "hard_pushback": "Automatic promotion would collapse Daniel approval into automation and weaken the central safety control.",
    "council_split": "Operator wants momentum; Investor wants conversion data; Customer advocate wants relevance; Skeptic says trust is lost if the system outruns consent; Builder recommends preserving the gate.",
    "verdict": "do-not-automate-promotion",
    "next_test": f"Review {len(approval_packets)} approval packets and record approve, reject, or hold decisions.",
    "evidence_path": ".agent/memory/working/approval_packets.csv",
    "safety_gate": "Daniel approval required before promotion; promotion is still not outreach approval.",
    "status": "blocked-awaiting-daniel-decision",
    "notes": "The uncomfortable truth: approval is the bottleneck by design, not a bug.",
})

rows.append({
    "decision_id": "outreach-readiness",
    "council": "Outreach Review Council",
    "task_area": "outreach",
    "decision": "Should outreach drafts or sends be prepared before approved prospects exist?",
    "best_case": "Drafting early could make the engine feel ready and shorten turnaround after promotion.",
    "hard_pushback": "Drafting against unapproved businesses risks weak relevance, compliance gaps, and accidental send pressure.",
    "council_split": "Copy critic wants practice reps; Compliance guard blocks without basis; Buyer empathy lead warns against generic outreach; Daniel proxy requires exact approval.",
    "verdict": "defer-until-prospect-approved",
    "next_test": clean(pre_send[0].get("next_action"), "Keep pre-send readiness blocked until approved prospects exist.") if pre_send else "Generate pre-send readiness after promotion.",
    "evidence_path": ".agent/memory/working/pre_send_readiness.csv",
    "safety_gate": "No email, SMS, DM, form, social post, call, scheduling, or follow-up without explicit Daniel approval.",
    "status": "blocked-pre-send",
    "notes": "Pre-send readiness remains the hard red light.",
})

rows.append({
    "decision_id": "github-remote-issues",
    "council": "GitHub Work Council",
    "task_area": "github",
    "decision": "Should local GitHub issue drafts be created remotely now?",
    "best_case": "Remote issues would make review and tracking easier in GitHub.",
    "hard_pushback": "Remote issue creation is an external write and should not happen just because local artifacts are ready.",
    "council_split": "Issue triager likes the structure; Safety controller blocks remote writes; Automation skeptic says local readiness is enough; Builder keeps the command file locked.",
    "verdict": "keep-local-only",
    "next_test": f"Review {len(github_readiness)} local readiness rows; ask for exact approval only if Daniel wants remote issues.",
    "evidence_path": ".agent/memory/working/github_readiness_audit.csv",
    "safety_gate": "No remote GitHub writes without explicit approval.",
    "status": "ready-local-only",
    "notes": "Local readiness does not equal permission to execute gh commands.",
})

rows.append({
    "decision_id": "concept-publication",
    "council": "Web Design Council",
    "task_area": "website-design",
    "decision": "Should private website concepts be published or shown externally before prospect/outreach approval?",
    "best_case": "A visible concept can make the offer tangible and speed up buyer understanding.",
    "hard_pushback": "Publishing or sending unsolicited concepts can imply endorsement and create reputational risk.",
    "council_split": "Conversion designer wants tangible proof; Brand critic wants restraint; Customer advocate wants permission; Skeptic says this sounds premium to the maker, not necessarily to the buyer.",
    "verdict": "keep-private",
    "next_test": f"Use {len(concepts)} private concepts only for internal review until promotion and outreach approval exist.",
    "evidence_path": ".agent/memory/working/private_concepts.csv",
    "safety_gate": "Do not publish, send, or imply approval of private concepts.",
    "status": "internal-only",
    "notes": "Concepts are sales preparation assets, not client-facing claims.",
})

rows.append({
    "decision_id": "offer-model",
    "council": "Offer Pricing Council",
    "task_area": "offer-pricing",
    "decision": "Should the engine keep the flat monthly offer model for current local niches?",
    "best_case": "$0 upfront lowers friction for small local businesses and keeps offers easy to understand.",
    "hard_pushback": "A low-friction offer can attract low-commitment buyers if trust, scope, and cancellation terms are unclear.",
    "council_split": "Value strategist likes clarity; Scope controller demands strict deliverables; Buyer advocate wants no surprise fees; Margin keeper watches support load.",
    "verdict": "keep-model-with-scope-control",
    "next_test": f"Use {len(strategy)} offer strategy rows and {len(revenue)} forecast stages without treating forecast as booked revenue.",
    "evidence_path": ".agent/memory/working/offer_strategy.csv",
    "safety_gate": "Offer strategy is not invoice, proposal send, or client promise approval.",
    "status": "advisory",
    "notes": "The price is not the problem; trust, clarity, and follow-up are the constraint.",
})

for row in rows:
    row["date"] = today()

write_csv(p("council_debates.csv"), rows, FIELDS)

os.makedirs(p("councils"), exist_ok=True)
path = p("councils", f"debates-{today()}.md")
with open(path, "w", encoding="utf-8") as handle:
    handle.write("# Council Debates\n\n")
    handle.write(f"- Date: {today()}\n")
    handle.write("- Purpose: force useful disagreement before business-engine decisions.\n\n")
    for row in rows:
        handle.write(f"## {row['council']}: {row['decision_id']}\n\n")
        handle.write(f"- Decision: {row['decision']}\n")
        handle.write(f"- Best case: {row['best_case']}\n")
        handle.write(f"- Hard pushback: {row['hard_pushback']}\n")
        handle.write(f"- Split: {row['council_split']}\n")
        handle.write(f"- Verdict: {row['verdict']}\n")
        handle.write(f"- Next test: {row['next_test']}\n")
        handle.write(f"- Gate: {row['safety_gate']}\n\n")

print(rel(path))
