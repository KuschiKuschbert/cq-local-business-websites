#!/usr/bin/env python3
import os
from common import clean, p, read_csv, rel, today, write_csv

FIELDS = ["date", "business", "region", "niche", "score", "recommendation", "missing_evidence", "next_action", "notes"]
WEAK = ["not verified", "unverified", "staged for follow-up", "needs verification", "not yet verified"]


def has_url(value):
    value = (value or "").lower()
    return "http://" in value or "https://" in value or "www." in value


def verified_social(row):
    social = (row.get("socials") or "").lower()
    observed = (row.get("observed_social_signal") or "").lower()
    return has_url(social) or (observed and not any(phrase in observed for phrase in WEAK))


def score(row):
    missing = []
    points = 0
    for field, label in [("business", "business name"), ("region", "region"), ("niche", "niche")]:
        if clean(row.get(field), ""):
            points += 10
        else:
            missing.append(label)
    if has_url(row.get("source_urls")):
        points += 20
    else:
        missing.append("source URL")
    if verified_social(row):
        points += 20
    else:
        missing.append("social signal")
    if clean(row.get("website"), "") or clean(row.get("observed_website_gap"), ""):
        points += 20
    else:
        missing.append("website or website gap")
    if clean(row.get("proposed_hook"), ""):
        points += 10
    else:
        missing.append("proposed trust hook")
    return points, missing


def recommendation(points, missing):
    if "social signal" in missing:
        return "research-more"
    return "promote-review" if points >= 80 else "research-more" if points >= 60 else "hold"


def next_action(points, missing):
    if "social signal" in missing:
        return "Find verified Facebook, Instagram, Google Business Profile, or TikTok URL"
    if points >= 80:
        return "Daniel review for possible promotion into prospects.csv"
    return "Find missing evidence: " + ", ".join(missing) if missing else "Keep staged"


rows = []
for row in read_csv(p("prospect_intake.csv")):
    points, missing = score(row)
    rows.append({
        "date": today(),
        "business": clean(row.get("business")),
        "region": clean(row.get("region")),
        "niche": clean(row.get("niche")),
        "score": str(points),
        "recommendation": recommendation(points, missing),
        "missing_evidence": ", ".join(missing),
        "next_action": next_action(points, missing),
        "notes": clean(row.get("notes")),
    })
write_csv(p("intake_review.csv"), rows, FIELDS)
os.makedirs(p("intake_reviews"), exist_ok=True)
report = p("intake_reviews", f"{today()}.md")
with open(report, "w", encoding="utf-8") as handle:
    handle.write("# Prospect Intake Review\n\n")
    handle.write(f"- Candidates reviewed: {len(rows)}\n\n")
    for row in rows:
        handle.write(f"- {row['business']}: {row['score']} / {row['recommendation']} / {row['next_action']}\n")
print(rel(report))
