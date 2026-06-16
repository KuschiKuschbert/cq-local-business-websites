#!/usr/bin/env python3
import os
from common import clean, p, read_csv, rel, today, write_csv

FIELDS = ["date", "rank", "business", "region", "niche", "priority_score", "status", "next_best_action", "evidence_path", "notes"]

intake = {row.get("business"): row for row in read_csv(p("prospect_intake.csv"))}
review = {row.get("business"): row for row in read_csv(p("intake_review.csv"))}
verify = {row.get("business"): row for row in read_csv(p("intake_verification.csv"))}
approvals = {row.get("business"): row for row in read_csv(p("approval_queue.csv"))}
concepts = {row.get("business"): row for row in read_csv(p("private_concepts.csv"))}
research = {row.get("business"): row for row in read_csv(p("research_queue.csv"))}


def niche_weight(niche):
    text = niche.lower()
    if any(term in text for term in ["functions", "accommodation", "restaurant", "bar", "catering"]):
        return 18
    if any(term in text for term in ["pest", "cleaning", "landscaping", "mini digger"]):
        return 16
    if any(term in text for term in ["market", "gallery", "workshop"]):
        return 12
    return 8


rows = []
for business, item in intake.items():
    check = verify.get(business, {})
    reviewed = review.get(business, {})
    score = int(reviewed.get("score") or 0)
    readiness = check.get("readiness", "")
    status = "promotion-review" if business in approvals else "research-more"
    points = score + niche_weight(clean(item.get("niche"), ""))
    if readiness == "promotion-review-ready":
        points += 25
    if business in concepts:
        points += 10
    if "owned-website-missing" in check.get("website_status", ""):
        points += 12
    elif clean(item.get("observed_website_gap"), ""):
        points += 8
    if business in research:
        points -= 10
    if business in approvals:
        next_action = "Daniel promotion review; do not send outreach."
        evidence_path = approvals[business].get("source_path", "")
    else:
        next_action = research.get(business, {}).get("next_action", "Keep researching evidence.")
        evidence_path = ".agent/memory/working/research_queue.csv"
    rows.append({
        "date": today(),
        "rank": "0",
        "business": business,
        "region": clean(item.get("region")),
        "niche": clean(item.get("niche")),
        "priority_score": str(points),
        "status": status,
        "next_best_action": next_action,
        "evidence_path": clean(evidence_path),
        "notes": "Prioritized for supervised review; no outreach approval implied.",
    })

rows.sort(key=lambda row: (-int(row["priority_score"]), row["business"]))
for index, row in enumerate(rows, start=1):
    row["rank"] = str(index)

write_csv(p("priority_board.csv"), rows, FIELDS)

os.makedirs(p("priority_boards"), exist_ok=True)
path = p("priority_boards", f"{today()}.md")
with open(path, "w", encoding="utf-8") as handle:
    handle.write("# Cap Coast Creative Priority Board\n\n")
    handle.write(f"- Date: {today()}\n")
    handle.write(f"- Candidates ranked: {len(rows)}\n")
    handle.write("- Safety: priority is not promotion approval and not outreach approval.\n\n")
    for row in rows:
        handle.write(f"{row['rank']}. {row['business']} - {row['priority_score']} - {row['status']} - {row['next_best_action']}\n")

print(rel(path))
