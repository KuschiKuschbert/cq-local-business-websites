#!/usr/bin/env python3
import os
from common import clean, p, read_csv, rel, today, write_csv

FIELDS = [
    "date",
    "rank",
    "business",
    "region",
    "niche",
    "quality_band",
    "decision_state",
    "readiness",
    "priority_score",
    "why_it_matters",
    "evidence_gap",
    "safe_next_step",
    "approval_gate",
]

intake = {clean(row.get("business")).casefold(): row for row in read_csv(p("prospect_intake.csv"))}
verification = {clean(row.get("business")).casefold(): row for row in read_csv(p("intake_verification.csv"))}
priority = {clean(row.get("business")).casefold(): row for row in read_csv(p("priority_board.csv"))}
decisions = {clean(row.get("business")).casefold(): row for row in read_csv(p("approval_decision_summary.csv"))}
prospects = {clean(row.get("business")).casefold(): row for row in read_csv(p("prospects.csv"))}
suppressed = {clean(row.get("business")).casefold(): row for row in read_csv(p("research_suppression_list.csv"))}


def band_for(key, verify, decision, score):
    if key in prospects:
        return "approved prospect"
    if clean(decision.get("decision")) == "hold":
        return "on hold"
    if key in suppressed:
        return "cooled down"
    if verify.get("readiness") == "promotion-review-ready" and score >= 140:
        return "strong lead"
    if verify.get("readiness") == "promotion-review-ready":
        return "review-ready"
    return "needs proof"


def gap_for(verify, decision, key):
    if clean(decision.get("decision")) == "hold":
        return "Daniel put promotion on hold; sharpen evidence or offer before asking again."
    if key in suppressed:
        return "Repeated weak public searches; use a genuinely new source family."
    gaps = []
    if verify.get("social_status") != "verified":
        gaps.append("verified owned social/profile")
    if verify.get("website_status") == "owned-website-missing":
        gaps.append("owned website gap")
    if verify.get("source_status") in {"directory-source", ""}:
        gaps.append("stronger public source")
    return ", ".join(gaps) if gaps else "No major evidence gap recorded."


def next_step_for(band, priority_row):
    if band == "approved prospect":
        return "Prepare mockup, compliance, and outreach draft; do not send without exact approval."
    if band == "on hold":
        return "Gather sharper proof or a clearer offer before asking Daniel to reopen promotion."
    if band == "cooled down":
        return "Do not repeat the same search; wait for a new source family."
    if band in {"strong lead", "review-ready"}:
        return "Keep ready for Daniel review; promotion is still not outreach approval."
    return clean(priority_row.get("next_best_action"), "Research public evidence only.")


rows = []
for key, item in intake.items():
    verify = verification.get(key, {})
    priority_row = priority.get(key, {})
    decision = decisions.get(key, {})
    score = int(clean(priority_row.get("priority_score"), "0"))
    band = band_for(key, verify, decision, score)
    rows.append({
        "date": today(),
        "rank": "0",
        "business": clean(item.get("business")),
        "region": clean(item.get("region")),
        "niche": clean(item.get("niche")),
        "quality_band": band,
        "decision_state": clean(decision.get("decision"), "none"),
        "readiness": clean(verify.get("readiness"), "unchecked"),
        "priority_score": str(score),
        "why_it_matters": clean(item.get("proposed_hook"), clean(item.get("observed_website_gap"), "Potential website opportunity.")),
        "evidence_gap": gap_for(verify, decision, key),
        "safe_next_step": next_step_for(band, priority_row),
        "approval_gate": "No outreach, publishing, billing, hosting, or remote write without Daniel's exact approval.",
    })

weight = {
    "approved prospect": 0,
    "strong lead": 1,
    "review-ready": 2,
    "on hold": 3,
    "needs proof": 4,
    "cooled down": 5,
}
rows.sort(key=lambda row: (weight.get(row["quality_band"], 9), -int(row["priority_score"]), row["business"]))
for index, row in enumerate(rows, start=1):
    row["rank"] = str(index)

write_csv(p("lead_quality_map.csv"), rows, FIELDS)

os.makedirs(p("lead_quality_maps"), exist_ok=True)
path = p("lead_quality_maps", f"{today()}.md")
with open(path, "w", encoding="utf-8") as handle:
    handle.write("# Lead Quality Map\n\n")
    handle.write(f"- Date: {today()}\n")
    handle.write("- Purpose: plain-English lead quality state for Daniel.\n")
    handle.write("- Safety: quality is not approval and never sends outreach.\n\n")
    for row in rows:
        handle.write(f"## {row['rank']}. {row['business']} - {row['quality_band']}\n\n")
        handle.write(f"- Decision: {row['decision_state']}\n")
        handle.write(f"- Evidence gap: {row['evidence_gap']}\n")
        handle.write(f"- Safe next step: {row['safe_next_step']}\n")
        handle.write(f"- Gate: {row['approval_gate']}\n\n")

print(rel(path))
