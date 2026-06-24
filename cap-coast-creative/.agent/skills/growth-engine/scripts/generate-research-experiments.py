#!/usr/bin/env python3
from common import clean, p, read_csv, today, write_csv

FIELDS = ["date", "rank", "region", "niche", "experiment_type", "query", "hypothesis", "prior_failure_signal", "success_criteria", "safe_next_action", "status", "notes"]


def lane_key(region, niche):
    return (clean(region).casefold(), clean(niche).casefold())


attempts = read_csv(p("research_attempts.csv"))
controller = read_csv(p("research_controller.csv"))
source_routes = read_csv(p("source_quality_map.csv"))
research_queue = read_csv(p("research_queue.csv"))

routes_by_lane = {}
for route in source_routes:
    key = lane_key(route.get("region"), route.get("niche"))
    routes_by_lane.setdefault(key, []).append(route)

failed_by_lane = {}
failed_by_business = {}
for attempt in attempts:
    text = " ".join([
        attempt.get("business", ""),
        attempt.get("query", ""),
        attempt.get("next_action", ""),
        attempt.get("notes", ""),
    ]).casefold()
    for lane in controller:
        region = clean(lane.get("region"))
        niche = clean(lane.get("niche"))
        terms = [term for term in niche.casefold().split() if len(term) > 3]
        if region.casefold() in text and any(term in text for term in terms):
            failed_by_lane.setdefault(lane_key(region, niche), 0)
            if clean(attempt.get("result")).startswith("no_"):
                failed_by_lane[lane_key(region, niche)] += 1
    business = clean(attempt.get("business"), "").casefold()
    if business:
        failed_by_business.setdefault(business, 0)
        if clean(attempt.get("result")).startswith("no_"):
            failed_by_business[business] += 1

rows = []
for item in research_queue:
    business = clean(item.get("business"))
    failures = failed_by_business.get(business.casefold(), 0)
    if failures >= 3:
        status = "suppressed-repeat-search"
        safe_next_action = "Stop repeating this candidate until a genuinely new source family appears; replace with a stronger named lead or map/direct registry route."
    elif failures >= 2:
        status = "needs-new-source-family"
        safe_next_action = "Switch to named directory or official-site verification before repeating social search."
    else:
        status = "ready-to-test"
        safe_next_action = "Run named-candidate verification; capture only public business-owned social/website evidence or log failed attempt."
    rows.append({
        "date": today(),
        "rank": "0",
        "region": clean(item.get("region")),
        "niche": clean(item.get("niche")),
        "experiment_type": "named-candidate-verification",
        "query": clean(item.get("search_query")),
        "hypothesis": "A named candidate from the intake research queue should yield stronger social or website evidence than a generic regional lane.",
        "prior_failure_signal": f"{failures} failed/no-social attempts recorded for this business",
        "success_criteria": "Capture only public business-owned social/profile, owned website status, region fit, and source URL evidence.",
        "safe_next_action": safe_next_action,
        "status": status,
        "notes": f"Business: {business}. Source hint: {clean(item.get('source_hint'))}. No contact, login, form submission, DM, call, or social interaction.",
    })

for lane in controller:
    status = clean(lane.get("lane_status"))
    if status not in {"work-next", "try-new-source", "verify-gap"}:
        continue
    region = clean(lane.get("region"))
    niche = clean(lane.get("niche"))
    key = lane_key(region, niche)
    failures = failed_by_lane.get(key, 0)
    routes = routes_by_lane.get(key, [])
    route = routes[0] if routes else {}
    source_family = clean(route.get("source_family"), "targeted public source route")
    experiment_type = "source-route-shift" if failures else "first-pass-source-route"
    if status == "verify-gap":
        experiment_type = "gap-verification"
    experiment_status = "ready-to-test"
    safe_next_action = "Run research-only check; capture candidate only with strong public evidence, otherwise log attempt."
    if failures >= 2 and source_family == "Facebook public page":
        experiment_type = "suppressed-generic-social-route"
        experiment_status = "deprioritized-after-failures"
        safe_next_action = "Prefer named-candidate or directory verification before repeating this generic social route."
    rows.append({
        "date": today(),
        "rank": "0",
        "region": region,
        "niche": niche,
        "experiment_type": experiment_type,
        "query": clean(route.get("query"), clean(lane.get("recommended_query"))),
        "hypothesis": f"{source_family} will produce stronger business-owned social or website-gap evidence than broad locality search.",
        "prior_failure_signal": f"{failures} failed/no-social attempts recorded for this lane",
        "success_criteria": "Capture only if a public business-owned social/profile URL, region fit, and website-gap evidence are all present.",
        "safe_next_action": safe_next_action,
        "status": experiment_status,
        "notes": "No contact, login, scraping behind login, form submission, DM, call, or social interaction.",
    })

rows.sort(key=lambda row: (
    2 if row["status"] == "suppressed-repeat-search" else 1 if row["status"].startswith("deprioritized") else 0,
    0 if row["experiment_type"] == "named-candidate-verification" else 1 if row["experiment_type"] == "source-route-shift" else 2,
    int(next((lane.get("rank", "999") for lane in controller if lane_key(lane.get("region"), lane.get("niche")) == lane_key(row["region"], row["niche"])), "999")),
))
rows = rows[:12]
for index, row in enumerate(rows, start=1):
    row["rank"] = str(index)

write_csv(p("research_experiments.csv"), rows, FIELDS)

folder = p("research_experiments")
import os
os.makedirs(folder, exist_ok=True)
path = p("research_experiments", f"{today()}.md")
with open(path, "w", encoding="utf-8") as handle:
    handle.write("# Research Experiments\n\n")
    handle.write(f"- Date: {today()}\n")
    handle.write("- Safety: research-only experiments. Do not contact businesses or interact with accounts.\n\n")
    for row in rows:
        handle.write(f"- #{row['rank']} {row['region']} / {row['niche']} / {row['experiment_type']}: `{row['query']}`\n")

print(f".agent/memory/working/research_experiments/{today()}.md")
