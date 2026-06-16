#!/usr/bin/env python3
import argparse
import re
from common import clean, p, read_csv, today, write_csv

FIELDS = [
    "business",
    "region",
    "niche",
    "socials",
    "website",
    "source_urls",
    "observed_social_signal",
    "observed_website_gap",
    "proposed_hook",
    "notes",
]
ATTEMPT_FIELDS = ["date", "business", "query", "source_checked", "result", "next_action", "notes"]
OUTREACH_TERMS = re.compile(r"\b(sent|emailed|dm(?:ed)?|messaged|called|submitted|posted|commented|followed)\b", re.I)


def public_url(value, label, required=True):
    value = clean(value, "")
    if not value and not required:
        return value
    if not value.startswith(("http://", "https://")):
        raise SystemExit(f"Refusing intake capture: {label} must be a public http(s) URL.")
    return value


def assert_research_only(label, value):
    if OUTREACH_TERMS.search(value or ""):
        raise SystemExit(f"Refusing intake capture: {label} appears to describe outreach, not research.")


parser = argparse.ArgumentParser()
parser.add_argument("--business", required=True)
parser.add_argument("--region", required=True)
parser.add_argument("--niche", required=True)
parser.add_argument("--socials", required=True)
parser.add_argument("--website", default="")
parser.add_argument("--source-urls", required=True)
parser.add_argument("--observed-social-signal", required=True)
parser.add_argument("--observed-website-gap", required=True)
parser.add_argument("--proposed-hook", required=True)
parser.add_argument("--notes", default="")
parser.add_argument("--query", required=True)
args = parser.parse_args()

socials = "; ".join(public_url(url.strip(), "socials") for url in args.socials.split(";") if url.strip())
source_urls = "; ".join(public_url(url.strip(), "source URLs") for url in args.source_urls.split(";") if url.strip())
website = public_url(args.website, "website", required=False)
if not socials:
    raise SystemExit("Refusing intake capture: at least one public business-owned social URL is required.")
if not source_urls:
    raise SystemExit("Refusing intake capture: at least one public source URL is required.")

for label, value in [
    ("observed social signal", args.observed_social_signal),
    ("observed website gap", args.observed_website_gap),
    ("proposed hook", args.proposed_hook),
    ("notes", args.notes),
]:
    assert_research_only(label, value)

candidate = {
    "business": clean(args.business),
    "region": clean(args.region),
    "niche": clean(args.niche),
    "socials": socials,
    "website": website,
    "source_urls": source_urls,
    "observed_social_signal": clean(args.observed_social_signal),
    "observed_website_gap": clean(args.observed_website_gap),
    "proposed_hook": clean(args.proposed_hook),
    "notes": clean(args.notes, "Captured from public research only; no outreach performed."),
}

rows = read_csv(p("prospect_intake.csv"))
business_key = candidate["business"].casefold()
updated = False
next_rows = []
for row in rows:
    if clean(row.get("business"), "").casefold() == business_key:
        next_rows.append(candidate)
        updated = True
    else:
        next_rows.append(row)
if not updated:
    next_rows.append(candidate)
write_csv(p("prospect_intake.csv"), next_rows, FIELDS)

attempts = read_csv(p("research_attempts.csv"))
attempts.append({
    "date": today(),
    "business": candidate["business"],
    "query": clean(args.query),
    "source_checked": source_urls,
    "result": "verified_candidate_found",
    "next_action": "Run CEO loop; review intake evidence and approval queue before any promotion.",
    "notes": "Candidate staged in prospect_intake.csv from public evidence only; no outreach performed.",
})
write_csv(p("research_attempts.csv"), attempts, ATTEMPT_FIELDS)

print(("Updated" if updated else "Captured") + f" intake candidate: {candidate['business']}")
print("No outreach, promotion, GitHub write, or third-party update was performed.")
