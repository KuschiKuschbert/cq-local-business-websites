#!/usr/bin/env python3
import os
from common import clean, p, rel, read_csv, today, write_csv

FIELDS = [
    "date",
    "business",
    "failed_attempts",
    "suppressed_query_pattern",
    "suppression_reason",
    "replacement_source_family",
    "safe_next_action",
    "status",
    "safety_gate",
    "notes",
]

attempts = read_csv(p("research_attempts.csv"))
pivots = {clean(row.get("business")).casefold(): row for row in read_csv(p("source_pivot_plan.csv"))}
failed = {}

for attempt in attempts:
    if not clean(attempt.get("result")).startswith("no_"):
        continue
    business = clean(attempt.get("business"), "")
    if not business:
        continue
    failed.setdefault(business.casefold(), {"business": business, "rows": []})
    failed[business.casefold()]["rows"].append(attempt)

rows = []
for key, bundle in failed.items():
    count = len(bundle["rows"])
    if count < 3:
        continue
    pivot = pivots.get(key, {})
    replacement = clean(pivot.get("primary_source_family"), "official source, directory, or local tourism source")
    last_query = clean(bundle["rows"][-1].get("query"))
    rows.append({
        "date": today(),
        "business": bundle["business"],
        "failed_attempts": str(count),
        "suppressed_query_pattern": last_query,
        "suppression_reason": "Repeated no-result or no-social verification attempts for the same candidate.",
        "replacement_source_family": replacement,
        "safe_next_action": "Do not repeat the suppressed query pattern until a new source family or stronger public source appears.",
        "status": "suppress-repeat-search",
        "safety_gate": "Research suppression is advisory only; it cannot approve capture, promotion, outreach, publishing, or GitHub writes.",
        "notes": "Use public-source verification only. No contact, login, form submission, DM, call, or social interaction.",
    })

write_csv(p("research_suppression_list.csv"), rows, FIELDS)

os.makedirs(p("research_suppression"), exist_ok=True)
path = p("research_suppression", f"{today()}.md")
with open(path, "w", encoding="utf-8") as handle:
    handle.write("# Research Suppression List\n\n")
    handle.write(f"- Date: {today()}\n")
    handle.write("- Purpose: prevent repeated low-yield public searches from consuming the research loop.\n")
    handle.write("- Safety: advisory research memory only; no prospect approval or outreach authority.\n\n")
    if not rows:
        handle.write("No repeated failed query patterns currently require suppression.\n")
    for row in rows:
        handle.write(f"## {row['business']}\n\n")
        handle.write(f"- Failed attempts: {row['failed_attempts']}\n")
        handle.write(f"- Suppressed pattern: `{row['suppressed_query_pattern']}`\n")
        handle.write(f"- Replacement source family: {row['replacement_source_family']}\n")
        handle.write(f"- Safe next action: {row['safe_next_action']}\n")
        handle.write(f"- Gate: {row['safety_gate']}\n\n")

print(rel(path))
