#!/usr/bin/env python3
import os
from common import clean, p, read_csv, rel, slug, today, write_csv

FIELDS = ["date", "business", "stage", "readiness", "plan_path", "next_action", "safety_gate", "notes"]

prospects = read_csv(p("prospects.csv"))
strategy = {row.get("business"): row for row in read_csv(p("offer_strategy.csv"))}
concepts = {row.get("business"): row for row in read_csv(p("private_concepts.csv"))}
out_dir = p("delivery_readiness")
os.makedirs(out_dir, exist_ok=True)

rows = []
for prospect in prospects:
    business = clean(prospect.get("business"))
    status = clean(prospect.get("status"), "qualified")
    if status.lower() not in {"qualified", "briefed", "mockup-needed", "mockup-ready", "meeting", "proposal-needed", "won"}:
        continue
    plan_path = os.path.join(out_dir, f"{slug(business)}.md")
    item = strategy.get(business, {})
    concept = concepts.get(business, {})
    body = f"""# Delivery Readiness Plan: {business}

Status: internal delivery plan only.

## Inputs

- Region: {clean(prospect.get("region"))}
- Niche: {clean(prospect.get("niche"))}
- Tier: {clean(item.get("tier"), clean(prospect.get("tier")))}
- Monthly fee: {clean(item.get("monthly_fee"), clean(prospect.get("tier")))}
- Primary CTA: {clean(item.get("primary_cta"), "Make an enquiry")}
- Trust hook: {clean(item.get("trust_hook"), clean(prospect.get("hook")))}
- Private concept: {clean(concept.get("concept_path"), "none yet")}

## Delivery Stages

1. Confirm brief evidence and source URLs.
2. Build or refine private mockup.
3. Run mobile, accessibility, copy, and claim QA.
4. Prepare owner demo notes.
5. Draft proposal after Daniel review.
6. Onboard only after client agreement.
7. Publish only after domain, hosting, content, and billing approvals.

## Safety Gates

- Do not publish concepts.
- Do not claim client approval.
- Do not change domains, hosting, billing, or invoices.
- Do not send proposals or outreach without explicit approval.
"""
    with open(plan_path, "w", encoding="utf-8") as handle:
        handle.write(body)
    rows.append({
        "date": today(),
        "business": business,
        "stage": status,
        "readiness": "delivery-plan-ready",
        "plan_path": rel(plan_path),
        "next_action": "Review mockup brief and QA checklist before any client-facing step.",
        "safety_gate": "Internal plan only; client-facing delivery requires approval.",
        "notes": "Generated from approved prospect data.",
    })

write_csv(p("delivery_readiness.csv"), rows, FIELDS)

report = os.path.join(out_dir, f"{today()}.md")
with open(report, "w", encoding="utf-8") as handle:
    handle.write("# Delivery Readiness\n\n")
    handle.write(f"- Date: {today()}\n")
    handle.write(f"- Approved/active prospects with delivery plans: {len(rows)}\n")
    handle.write("- Safety: no publishing, billing, hosting, or client-facing action performed.\n\n")
    if rows:
        for row in rows:
            handle.write(f"- {row['business']}: {row['readiness']} / {row['plan_path']}\n")
    else:
        handle.write("No active delivery plans yet because there are no approved prospects.\n")

print(rel(report))
