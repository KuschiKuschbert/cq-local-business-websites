#!/usr/bin/env python3
import os
from common import clean, p, read_csv, rel, today, write_csv

FIELDS = [
    "date",
    "rank",
    "region",
    "niche",
    "lane_status",
    "attempts_logged",
    "intake_matches",
    "priority_score",
    "recommended_query",
    "next_action",
    "safety_gate",
    "notes",
]


def lane_matches_text(region, niche, text):
    text = (text or "").casefold()
    region_hit = region.casefold() in text
    niche_terms = [term for term in niche.casefold().split() if len(term) > 3]
    niche_hit = any(term in text for term in niche_terms)
    return region_hit and niche_hit


def intake_matches_lane(region, niche, intake):
    matches = 0
    for row in intake:
        item_region = clean(row.get("region"), "").casefold()
        item_niche = clean(row.get("niche"), "").casefold()
        region_hit = region.casefold() in item_region or item_region in region.casefold()
        niche_hit = any(term in item_niche for term in niche.casefold().split())
        if region_hit and niche_hit:
            matches += 1
    return matches


source_plan = read_csv(p("source_plan.csv"))
attempts = read_csv(p("research_attempts.csv"))
intake = read_csv(p("prospect_intake.csv"))
rows = []

for row in source_plan:
    region = clean(row.get("region"))
    niche = clean(row.get("niche"))
    query = clean(row.get("query"))
    logged = [
        attempt for attempt in attempts
        if lane_matches_text(region, niche, " ".join([
            attempt.get("business", ""),
            attempt.get("query", ""),
            attempt.get("notes", ""),
        ]))
    ]
    matches = intake_matches_lane(region, niche, intake)
    base = 100
    if row.get("status") == "covered-but-refresh":
        base -= 25
    base -= min(matches * 12, 36)
    base -= min(len(logged) * 10, 30)
    if len(logged) == 0:
        base += 15
    score = max(base, 10)
    lane_status = "work-next"
    if matches >= 2 and len(logged) >= 1:
        lane_status = "refresh-later"
    elif matches >= 1:
        lane_status = "verify-gap"
    elif len(logged) >= 2:
        lane_status = "try-new-source"
    rows.append({
        "date": today(),
        "rank": "0",
        "region": region,
        "niche": niche,
        "lane_status": lane_status,
        "attempts_logged": str(len(logged)),
        "intake_matches": str(matches),
        "priority_score": str(score),
        "recommended_query": query,
        "next_action": "Run research-only source checks and log each attempt before adding intake evidence.",
        "safety_gate": "No contact, account login, form submission, DM, call, or social interaction.",
        "notes": clean(row.get("notes")),
    })

rows.sort(key=lambda item: (-int(item["priority_score"]), item["region"], item["niche"]))
for index, row in enumerate(rows, start=1):
    row["rank"] = str(index)

write_csv(p("research_controller.csv"), rows, FIELDS)

os.makedirs(p("research_controller"), exist_ok=True)
path = p("research_controller", f"{today()}.md")
with open(path, "w", encoding="utf-8") as handle:
    handle.write("# Research Controller\n\n")
    handle.write(f"- Date: {today()}\n")
    handle.write(f"- Lanes ranked: {len(rows)}\n")
    handle.write("- Safety: research-only. Do not contact businesses or interact with accounts.\n\n")
    handle.write("## Work Next\n\n")
    for row in rows[:8]:
        handle.write(
            f"- #{row['rank']} {row['region']} / {row['niche']} "
            f"({row['lane_status']}, score {row['priority_score']}): `{row['recommended_query']}`\n"
        )
    handle.write("\n## Gate\n\n")
    handle.write("Adding intake evidence is allowed only when the source is public, business-owned, and recorded. Outreach remains separately gated.\n")

print(rel(path))
