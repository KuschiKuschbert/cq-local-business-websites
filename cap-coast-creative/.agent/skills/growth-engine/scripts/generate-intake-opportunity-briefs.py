#!/usr/bin/env python3
import os
from common import clean, p, read_csv, rel, slug, today, write_csv

FIELDS = ["date", "business", "region", "niche", "readiness", "brief_path", "primary_opportunity", "safe_next_step", "notes"]
verify = {clean(row.get("business"), "").casefold(): row for row in read_csv(p("intake_verification.csv"))}
rows = []
os.makedirs(p("intake_opportunity_briefs"), exist_ok=True)
for row in read_csv(p("prospect_intake.csv")):
    business = clean(row.get("business"), "")
    gate = verify.get(business.casefold(), {})
    if gate.get("readiness") != "promotion-review-ready":
        continue
    path = p("intake_opportunity_briefs", f"{slug(business)}.md")
    opportunity = "Turn Facebook/directory attention into a simple owned information and enquiry page."
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(f"# Private Opportunity Brief: {business}\n\n")
        handle.write("- Status: internal planning only\n")
        handle.write(f"- Region: {clean(row.get('region'))}\n- Niche: {clean(row.get('niche'))}\n")
        handle.write(f"- Socials: {clean(row.get('socials'))}\n- Sources: {clean(row.get('source_urls'))}\n\n")
        handle.write(f"## Primary Opportunity\n\n{opportunity}\n\n")
        handle.write("Promotion is not outreach approval. Do not imply endorsement.\n")
    rows.append({"date": today(), "business": business, "region": clean(row.get("region")), "niche": clean(row.get("niche")), "readiness": gate.get("readiness"), "brief_path": rel(path), "primary_opportunity": opportunity, "safe_next_step": "Daniel promotion review; no outreach approval implied", "notes": "Private concept planning only; not client-approved."})
write_csv(p("intake_opportunity_briefs.csv"), rows, FIELDS)
print("\n".join(row["brief_path"] for row in rows) if rows else "No evidence-ready intake rows for opportunity brief generation.")
