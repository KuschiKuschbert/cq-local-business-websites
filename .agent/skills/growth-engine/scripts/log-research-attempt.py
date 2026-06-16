#!/usr/bin/env python3
import argparse
import re
from common import clean, p, read_csv, today, write_csv

FIELDS = ["date", "business", "query", "source_checked", "result", "next_action", "notes"]
RESULTS = [
    "no_verified_business_candidate_found",
    "no_verified_social_found",
    "verified_candidate_found",
    "duplicate_existing_candidate",
    "source_unavailable",
    "rejected_unsafe_source",
    "needs_manual_review",
]
OUTREACH_TERMS = re.compile(r"\b(sent|emailed|dm(?:ed)?|messaged|called|submitted|posted|commented|followed)\b", re.I)


def assert_safe_text(label, value):
    if OUTREACH_TERMS.search(value or ""):
        raise SystemExit(f"Refusing log: {label} appears to describe outreach, not research.")


parser = argparse.ArgumentParser()
parser.add_argument("--business", required=True)
parser.add_argument("--query", required=True)
parser.add_argument("--source-checked", required=True)
parser.add_argument("--result", required=True, choices=RESULTS)
parser.add_argument("--next-action", required=True)
parser.add_argument("--notes", default="")
args = parser.parse_args()

source = clean(args.source_checked, "")
if not source.startswith(("http://", "https://")):
    raise SystemExit("Refusing log: --source-checked must be a public http(s) URL.")
for label, value in [
    ("query", args.query),
    ("next action", args.next_action),
    ("notes", args.notes),
]:
    assert_safe_text(label, value)

rows = read_csv(p("research_attempts.csv"))
rows.append({
    "date": today(),
    "business": clean(args.business),
    "query": clean(args.query),
    "source_checked": source,
    "result": args.result,
    "next_action": clean(args.next_action),
    "notes": clean(args.notes, "Research-only log; no outreach or promotion performed."),
})
write_csv(p("research_attempts.csv"), rows, FIELDS)

print(f"Logged research attempt for {clean(args.business)}.")
print("No outreach, promotion, or third-party update was performed.")
