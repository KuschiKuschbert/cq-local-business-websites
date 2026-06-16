#!/usr/bin/env python3
import os
from common import clean, p, read_csv, rel, today, write_csv

FIELDS = ["date","business","region","niche","missing_evidence","search_query","source_hint","next_action","notes"]
intake = {clean(row.get("business"), "").casefold(): row for row in read_csv(p("prospect_intake.csv"))}
rows = []
for row in read_csv(p("intake_verification.csv")):
    if row.get("readiness") == "promotion-review-ready":
        continue
    business = clean(row.get("business"), "")
    source = intake.get(business.casefold(), {})
    missing = []
    if row.get("social_status") != "verified":
        missing.append("verified social profile")
    if row.get("website_status") == "unknown":
        missing.append("website status")
    region = clean(source.get("region"))
    niche = clean(source.get("niche"))
    query = f'"{business}" "{region}" Facebook Instagram website'
    rows.append({
        "date": today(),
        "business": business,
        "region": region,
        "niche": niche,
        "missing_evidence": ", ".join(missing) if missing else "stronger public evidence",
        "search_query": query,
        "source_hint": clean(source.get("source_urls")),
        "next_action": "Verify public social profile and owned website status; update prospect_intake.csv only with sourced evidence.",
        "notes": "Research only. Do not contact the business.",
    })
write_csv(p("research_queue.csv"), rows, FIELDS)
os.makedirs(p("research_reports"), exist_ok=True)
report = p("research_reports", f"{today()}.md")
with open(report, "w", encoding="utf-8") as handle:
    handle.write("# Research Queue\n\n")
    handle.write(f"- Tasks: {len(rows)}\n")
    handle.write("- Safety: research only; no outreach.\n\n")
    for row in rows:
        handle.write(f"- {row['business']}: `{row['search_query']}`\n")
print(rel(report))
