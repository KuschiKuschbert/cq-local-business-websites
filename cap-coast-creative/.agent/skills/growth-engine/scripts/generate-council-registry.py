#!/usr/bin/env python3
import os
from common import p, rel, today, write_csv

FIELDS = ["date", "council", "task_area", "trigger", "roles", "decision_standard", "output_artifact", "safety_gate", "notes"]

rows = [
    {
        "council": "Prospect Research Council",
        "task_area": "prospecting",
        "trigger": "New source lane, failed source route, or candidate capture decision.",
        "roles": "Local scout; Skeptic; Evidence clerk; Niche specialist; Safety controller",
        "decision_standard": "Capture only when public business-owned social/profile evidence, region fit, and website-gap evidence are present.",
        "output_artifact": ".agent/memory/working/research_experiments.csv",
        "safety_gate": "Research-only; no account login, contact, forms, DMs, calls, or social interaction.",
        "notes": "Use after weak broad searches to force better source-route tests.",
    },
    {
        "council": "Web Design Council",
        "task_area": "website-design",
        "trigger": "Private concept, mockup brief, CTA, content structure, or visual direction decision.",
        "roles": "Conversion designer; Local customer advocate; Brand critic; Mobile performance lead; Skeptic",
        "decision_standard": "Pick the design move that makes the business clearer, more trustworthy, faster on mobile, and easier to contact.",
        "output_artifact": ".agent/memory/working/private_concepts.csv",
        "safety_gate": "Private concept only; do not publish or imply client approval.",
        "notes": "Avoid pretty-but-vague concepts that do not improve trust or enquiry flow.",
    },
    {
        "council": "Offer Pricing Council",
        "task_area": "offer-pricing",
        "trigger": "Tier, price, guarantee, scope, CTA, or package decision.",
        "roles": "Value strategist; Scope controller; Buyer advocate; Margin keeper; Skeptic",
        "decision_standard": "Choose the smallest offer that is easy to understand, profitable to deliver, and credible for the niche.",
        "output_artifact": ".agent/memory/working/offer_strategy.csv",
        "safety_gate": "Offer strategy is not a client promise, invoice, or proposal approval.",
        "notes": "Keep the $0 upfront monthly model consistent unless Daniel changes strategy.",
    },
    {
        "council": "Outreach Review Council",
        "task_area": "outreach",
        "trigger": "Drafting, channel choice, follow-up, compliance, or send-readiness decision.",
        "roles": "Compliance guard; Buyer empathy lead; Copy critic; Deliverability skeptic; Daniel proxy",
        "decision_standard": "Approve only drafts with contact basis, sender ID, opt-out, exact-copy approval, and non-pushy relevance.",
        "output_artifact": ".agent/memory/working/pre_send_readiness.csv",
        "safety_gate": "No send, schedule, DM, form submission, call, social post, or follow-up without explicit Daniel approval.",
        "notes": "Promotion approval never counts as outreach approval.",
    },
    {
        "council": "Delivery Ops Council",
        "task_area": "delivery",
        "trigger": "Client delivery plan, domain, hosting, proposal, handover, or fulfilment sequence decision.",
        "roles": "Project manager; Quality controller; Scope guard; Client advocate; Automation builder",
        "decision_standard": "Proceed only when the next action is reversible, scoped, approved, and has a clear done definition.",
        "output_artifact": ".agent/memory/working/delivery_readiness.csv",
        "safety_gate": "No hosting, DNS, publishing, billing, or client-facing promises without explicit approval.",
        "notes": "Design for the worst normal day: low context, many small clients, and tight follow-up windows.",
    },
    {
        "council": "GitHub Work Council",
        "task_area": "github",
        "trigger": "Issue draft, branch, PR, remote issue creation, or work orchestration decision.",
        "roles": "Repo operator; Safety controller; Issue triager; Automation skeptic; Builder",
        "decision_standard": "Keep remote writes blocked unless the exact command and target have been approved.",
        "output_artifact": ".agent/memory/working/github_readiness_audit.csv",
        "safety_gate": "No remote GitHub writes without explicit approval.",
        "notes": "Local plans may be generated and audited without touching GitHub.",
    },
    {
        "council": "Titan CEO Council",
        "task_area": "strategy",
        "trigger": "Major prioritization, business model, growth bet, risk tradeoff, or resource allocation decision.",
        "roles": "Operator; Investor; Customer advocate; Brand strategist; Skeptic; Builder",
        "decision_standard": "Choose one path: do it, do not do it, test smaller, defer, or reframe.",
        "output_artifact": ".agent/memory/working/council_debates.csv",
        "safety_gate": "Strategy recommendations do not approve external actions.",
        "notes": "Use when the system is tempted to add complexity before the base engine is reliable.",
    },
]

for row in rows:
    row["date"] = today()

write_csv(p("council_registry.csv"), rows, FIELDS)

os.makedirs(p("councils"), exist_ok=True)
path = p("councils", f"registry-{today()}.md")
with open(path, "w", encoding="utf-8") as handle:
    handle.write("# Council Registry\n\n")
    handle.write(f"- Date: {today()}\n")
    handle.write("- Purpose: route business-engine decisions to the right debate council before action.\n\n")
    for row in rows:
        handle.write(f"- {row['council']} ({row['task_area']}): {row['trigger']} / Gate: {row['safety_gate']}\n")

print(rel(path))
