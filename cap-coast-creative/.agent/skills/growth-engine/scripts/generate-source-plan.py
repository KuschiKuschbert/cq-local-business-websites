#!/usr/bin/env python3
import os
from common import p, read_csv, rel, today, write_csv

FIELDS = ["date", "region", "niche", "query", "evidence_required", "safe_next_action", "status", "notes"]

REGIONS = [
    "Kawana Rockhampton",
    "Rockhampton",
    "Yeppoon",
    "Emu Park",
    "Capricorn Coast",
]
NICHES = [
    "cafe restaurant bar catering",
    "cleaning pest control",
    "landscaping excavation mini digger",
    "salon beauty barber",
    "art gallery workshops market",
]

existing = {(row.get("region", "").lower(), row.get("niche", "").lower()) for row in read_csv(p("prospect_intake.csv"))}
rows = []
for region in REGIONS:
    for niche in NICHES:
        query = f'"{region}" "{niche}" Facebook Instagram website'
        status = "active"
        if any(region.lower() in item_region and any(part in item_niche for part in niche.split()) for item_region, item_niche in existing):
            status = "covered-but-refresh"
        rows.append({
            "date": today(),
            "region": region,
            "niche": niche,
            "query": query,
            "evidence_required": "business name, public social URL, website status or visible website gap, source URL",
            "safe_next_action": "Research only; add to prospect_intake.csv only when evidence is sourced and business-owned.",
            "status": status,
            "notes": "No contact, scraping behind login, form submission, or account interaction.",
        })

write_csv(p("source_plan.csv"), rows, FIELDS)

os.makedirs(p("source_plans"), exist_ok=True)
path = p("source_plans", f"{today()}.md")
with open(path, "w", encoding="utf-8") as handle:
    handle.write("# Cap Coast Creative Source Plan\n\n")
    handle.write(f"- Date: {today()}\n")
    handle.write(f"- Search lanes: {len(rows)}\n")
    handle.write("- Safety: research-only discovery. Do not contact businesses.\n\n")
    for row in rows:
        handle.write(f"- {row['region']} / {row['niche']}: `{row['query']}` ({row['status']})\n")

print(rel(path))
