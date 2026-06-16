#!/usr/bin/env python3
import os
from common import clean, p, read_csv, rel, slug, today, write_csv

FIELDS = ["date", "business", "region", "niche", "tier", "monthly_fee", "status", "proposal_path", "approval_status", "next_action", "notes"]

strategies = {row.get("business"): row for row in read_csv(p("offer_strategy.csv"))}
prospects = read_csv(p("prospects.csv"))
out_dir = p("proposals")
os.makedirs(out_dir, exist_ok=True)

rows = []
for prospect in prospects:
    status = clean(prospect.get("status"), "").lower()
    if status not in {"meeting", "proposal-needed", "proposal-draft", "qualified", "briefed", "mockup-ready"}:
        continue
    business = clean(prospect.get("business"))
    strategy = strategies.get(business, {})
    monthly_fee = clean(strategy.get("monthly_fee"), clean(prospect.get("tier")))
    tier = clean(strategy.get("tier"), "local-growth")
    path = os.path.join(out_dir, f"{slug(business)}.md")
    body = f"""# Proposal Draft: {business}

Status: internal draft only, not sent, not approved.

## Offer

- $0 upfront website build
- Flat monthly fee: {monthly_fee}
- Tier: {tier}
- Region: {clean(prospect.get("region"))}
- Niche: {clean(prospect.get("niche"))}

## Scope

- Premium single-site web presence using vanilla HTML, CSS, and JavaScript
- Mobile-first design with Outfit/Inter typography
- Clear conversion path: {clean(strategy.get("primary_cta"), "Make an enquiry")}
- Trust hook: {clean(strategy.get("trust_hook"), clean(prospect.get("hook")))}
- Basic local SEO structure and performance-minded page build

## Safety

This proposal must be reviewed by Daniel before sending. It does not change billing, domains, hosting, or client obligations.
"""
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(body)
    rows.append({
        "date": today(),
        "business": business,
        "region": clean(prospect.get("region")),
        "niche": clean(prospect.get("niche")),
        "tier": tier,
        "monthly_fee": monthly_fee,
        "status": "internal-draft",
        "proposal_path": rel(path),
        "approval_status": "needs-daniel-review",
        "next_action": "Review only; do not send or invoice.",
        "notes": "Generated locally from approved prospect and offer strategy.",
    })

write_csv(p("proposals.csv"), rows, FIELDS)
print(f"Generated {len(rows)} proposal records." if rows else "No eligible prospect rows for proposal generation.")
