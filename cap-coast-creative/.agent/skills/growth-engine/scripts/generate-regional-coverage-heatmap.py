#!/usr/bin/env python3
import os
from common import clean, p, rel, read_csv, today, write_csv

FIELDS = [
    "date",
    "rank",
    "region",
    "niche",
    "coverage_status",
    "intake_count",
    "evidence_ready_count",
    "attempts_logged",
    "suppressed_patterns",
    "priority_score",
    "recommended_query",
    "safe_next_action",
    "safety_gate",
    "notes",
]


def terms(value):
    return [term for term in clean(value, "").casefold().replace("/", " ").split() if len(term) > 3]


def region_hit(region, value):
    source = clean(value, "").casefold()
    target = region.casefold()
    return target in source or source in target


def niche_hit(niche, value):
    source = clean(value, "").casefold()
    return any(term in source for term in terms(niche))


def lane_hit(region, niche, *values):
    text = " ".join(values)
    return region.casefold() in text.casefold() and any(term in text.casefold() for term in terms(niche))


source_plan = read_csv(p("source_plan.csv"))
intake = read_csv(p("prospect_intake.csv"))
verification = {clean(row.get("business")).casefold(): row for row in read_csv(p("intake_verification.csv"))}
attempts = read_csv(p("research_attempts.csv"))
suppression = read_csv(p("research_suppression_list.csv"))
controller = {
    (clean(row.get("region")).casefold(), clean(row.get("niche")).casefold()): row
    for row in read_csv(p("research_controller.csv"))
}

rows = []
for lane in source_plan:
    region = clean(lane.get("region"))
    niche = clean(lane.get("niche"))
    key = (region.casefold(), niche.casefold())
    lane_intake = [
        row for row in intake
        if region_hit(region, row.get("region", "")) and niche_hit(niche, row.get("niche", ""))
    ]
    ready = [
        row for row in lane_intake
        if verification.get(clean(row.get("business")).casefold(), {}).get("readiness") == "promotion-review-ready"
    ]
    logged = [
        row for row in attempts
        if lane_hit(region, niche, row.get("business", ""), row.get("query", ""), row.get("notes", ""))
    ]
    suppressed = [
        row for row in suppression
        if any(clean(row.get("business")).casefold() == clean(item.get("business")).casefold() for item in lane_intake)
    ]
    score = 100
    score += 25 if not lane_intake else 0
    score += 10 if not logged else 0
    score -= min(len(lane_intake) * 10, 30)
    score -= min(len(ready) * 20, 40)
    score -= min(len(logged) * 8, 32)
    score -= min(len(suppressed) * 20, 40)
    score = max(score, 5)
    status = "under-covered"
    safe_next = "Run public research for this lane and log every source checked before adding intake evidence."
    if ready:
        status = "has-approval-ready-candidate"
        safe_next = "Prioritize Daniel decision review before more discovery in this lane."
    elif suppressed:
        status = "needs-new-source-family"
        safe_next = "Avoid suppressed repeat searches; use a new public source family before more broad search."
    elif lane_intake:
        status = "needs-verification"
        safe_next = "Verify social and website evidence for staged candidates before adding more similar intake."
    elif logged:
        status = "researched-no-intake"
        safe_next = "Try a higher-quality public source family and log the result."
    control = controller.get(key, {})
    rows.append({
        "date": today(),
        "rank": "0",
        "region": region,
        "niche": niche,
        "coverage_status": status,
        "intake_count": str(len(lane_intake)),
        "evidence_ready_count": str(len(ready)),
        "attempts_logged": str(len(logged)),
        "suppressed_patterns": str(len(suppressed)),
        "priority_score": str(score),
        "recommended_query": clean(control.get("recommended_query"), clean(lane.get("query"))),
        "safe_next_action": safe_next,
        "safety_gate": "Coverage heatmap is research-only and cannot approve capture, promotion, outreach, publishing, billing, or remote GitHub writes.",
        "notes": "Use to balance Kawana, Capricorn Coast, Rockhampton, Yeppoon, and Emu Park coverage.",
    })

rows.sort(key=lambda row: (-int(row["priority_score"]), row["region"], row["niche"]))
for index, row in enumerate(rows, start=1):
    row["rank"] = str(index)

write_csv(p("regional_coverage_heatmap.csv"), rows, FIELDS)

os.makedirs(p("regional_coverage_heatmap"), exist_ok=True)
path = p("regional_coverage_heatmap", f"{today()}.md")
with open(path, "w", encoding="utf-8") as handle:
    handle.write("# Regional Coverage Heatmap\n\n")
    handle.write(f"- Date: {today()}\n")
    handle.write("- Purpose: balance research across requested regions and niches without contacting businesses.\n")
    handle.write("- Safety: research-only. No capture, promotion, outreach, publishing, billing, or remote GitHub writes are approved here.\n\n")
    for row in rows[:12]:
        handle.write(
            f"- #{row['rank']} {row['region']} / {row['niche']}: {row['coverage_status']} "
            f"(score {row['priority_score']}, intake {row['intake_count']}, ready {row['evidence_ready_count']}, attempts {row['attempts_logged']})\n"
        )

print(rel(path))
