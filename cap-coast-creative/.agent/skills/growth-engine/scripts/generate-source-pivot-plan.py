#!/usr/bin/env python3
import os
from common import clean, p, read_csv, rel, today, write_csv

FIELDS = [
    "date",
    "business",
    "region",
    "niche",
    "pivot_reason",
    "primary_source_family",
    "primary_query",
    "secondary_source_family",
    "secondary_query",
    "evidence_required",
    "safe_next_action",
    "status",
    "notes",
]


def business_from_notes(notes):
    value = clean(notes, "")
    marker = "Business:"
    if marker not in value:
        return ""
    rest = value.split(marker, 1)[1].strip()
    return clean(rest.split(".", 1)[0], "")


research_queue = {clean(row.get("business")).casefold(): row for row in read_csv(p("research_queue.csv"))}
experiments = read_csv(p("research_experiments.csv"))

rows = []
for experiment in experiments:
    if clean(experiment.get("status")) != "needs-new-source-family":
        continue
    business = business_from_notes(experiment.get("notes"))
    queued = research_queue.get(business.casefold(), {})
    region = clean(queued.get("region"), clean(experiment.get("region")))
    niche = clean(queued.get("niche"), clean(experiment.get("niche")))
    source_hint = clean(queued.get("source_hint"), "")
    primary_family = "source-hint directory"
    primary_query = f'"{business}" "{region}" "{source_hint}"'
    secondary_family = "official or council source"
    secondary_query = f'"{business}" "{region}" official website contact hours'
    if "art" in niche.casefold() or "gallery" in niche.casefold():
        secondary_family = "local arts or tourism source"
        secondary_query = f'"{business}" "{region}" gallery workshop official'
    rows.append({
        "date": today(),
        "business": business,
        "region": region,
        "niche": niche,
        "pivot_reason": clean(experiment.get("prior_failure_signal")),
        "primary_source_family": primary_family,
        "primary_query": primary_query,
        "secondary_source_family": secondary_family,
        "secondary_query": secondary_query,
        "evidence_required": "Public source URL, business identity, region fit, owned website status, and any business-owned social/profile link.",
        "safe_next_action": "Research only; update intake only with public evidence or log the pivot attempt as failed.",
        "status": "ready-for-pivot-research",
        "notes": "No contact, account login, form submission, DM, call, social interaction, promotion, or outreach.",
    })

write_csv(p("source_pivot_plan.csv"), rows, FIELDS)

os.makedirs(p("source_pivot_plans"), exist_ok=True)
path = p("source_pivot_plans", f"{today()}.md")
with open(path, "w", encoding="utf-8") as handle:
    handle.write("# Source Pivot Plan\n\n")
    handle.write(f"- Date: {today()}\n")
    handle.write("- Purpose: shift repeated no-social candidates away from tired generic searches into safer alternate source families.\n")
    handle.write("- Safety: research-only; no contact, account interaction, promotion, or outreach.\n\n")
    if not rows:
        handle.write("No candidates currently need a source-family pivot.\n")
    for row in rows:
        handle.write(f"## {row['business']}\n\n")
        handle.write(f"- Reason: {row['pivot_reason']}\n")
        handle.write(f"- Primary: {row['primary_source_family']} / `{row['primary_query']}`\n")
        handle.write(f"- Secondary: {row['secondary_source_family']} / `{row['secondary_query']}`\n")
        handle.write(f"- Required evidence: {row['evidence_required']}\n")
        handle.write(f"- Gate: {row['safe_next_action']}\n\n")

print(rel(path))
