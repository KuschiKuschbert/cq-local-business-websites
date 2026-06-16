#!/usr/bin/env python3
import os
from common import clean, p, read_csv, rel, today, write_csv

FIELDS = ["date", "business", "social_status", "website_status", "source_status", "readiness", "next_action", "notes"]
SOCIAL = ["facebook.com", "instagram.com", "tiktok.com", "google.com/maps", "g.page"]
DIRS = ["emuparkonline.com.au", "yeppooncapricorncoast.com.au", "yellowpages.com.au", "localsearch.com.au"]
WEAK = ["not verified", "unverified", "staged for follow-up", "needs verification", "not yet verified"]


def contains(value, needles):
    value = (value or "").lower()
    return any(needle in value for needle in needles)


def weak(value):
    value = (value or "").lower().strip()
    return not value or any(phrase in value for phrase in WEAK)


rows = []
for row in read_csv(p("prospect_intake.csv")):
    social = "verified" if contains(row.get("socials"), SOCIAL) else "link-found-review-needed" if contains(row.get("source_urls"), SOCIAL) and not weak(row.get("observed_social_signal")) else "needs-verification"
    website = "owned-website-found" if row.get("website") else "owned-website-missing" if "no dedicated" in (row.get("observed_website_gap") or "").lower() or "directory-only" in (row.get("observed_website_gap") or "").lower() else "unknown"
    source = "directory-and-social" if contains(row.get("source_urls"), SOCIAL) and contains(row.get("source_urls"), DIRS) else "social-source" if contains(row.get("source_urls"), SOCIAL) else "directory-source" if contains(row.get("source_urls"), DIRS) else "other-public-source"
    has_gap = bool(clean(row.get("observed_website_gap"), ""))
    readiness = "promotion-review-ready" if social == "verified" and (has_gap or website in {"owned-website-missing", "directory-only", "unknown"}) else "research-more"
    rows.append({
        "date": today(),
        "business": clean(row.get("business")),
        "social_status": social,
        "website_status": website,
        "source_status": source,
        "readiness": readiness,
        "next_action": "Daniel can review for promotion; still no outreach without separate approval" if readiness == "promotion-review-ready" else "Find verified social evidence",
        "notes": clean(row.get("notes")),
    })
write_csv(p("intake_verification.csv"), rows, FIELDS)
os.makedirs(p("intake_verifications"), exist_ok=True)
report = p("intake_verifications", f"{today()}.md")
with open(report, "w", encoding="utf-8") as handle:
    handle.write("# Intake Evidence Verification\n\n")
    handle.write(f"- Rows checked: {len(rows)}\n")
    handle.write(f"- Promotion review ready: {sum(1 for row in rows if row['readiness'] == 'promotion-review-ready')}\n")
print(rel(report))
