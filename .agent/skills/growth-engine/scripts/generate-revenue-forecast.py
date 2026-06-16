#!/usr/bin/env python3
import os
import re
from common import clean, p, read_csv, rel, today, write_csv

FIELDS = [
    "date",
    "stage",
    "count",
    "weighted_probability",
    "gross_monthly_fee",
    "weighted_mrr",
    "next_action",
    "safety_gate",
    "notes",
]


def fee_value(value):
    match = re.search(r"([0-9]+)", value or "")
    return int(match.group(1)) if match else 0


strategy = {clean(row.get("business")).casefold(): row for row in read_csv(p("offer_strategy.csv"))}
approval_queue = {clean(row.get("business")).casefold(): row for row in read_csv(p("approval_queue.csv"))}
prospects = read_csv(p("prospects.csv"))
clients = read_csv(p("clients.csv"))

stages = {
    "staged-intake": {"prob": 0.05, "items": []},
    "promotion-review": {"prob": 0.15, "items": []},
    "approved-prospect": {"prob": 0.30, "items": []},
    "active-client": {"prob": 1.00, "items": []},
}

for row in read_csv(p("prospect_intake.csv")):
    key = clean(row.get("business")).casefold()
    stage = "promotion-review" if key in approval_queue else "staged-intake"
    stages[stage]["items"].append(row)

for row in prospects:
    stages["approved-prospect"]["items"].append(row)

for row in clients:
    if clean(row.get("status"), "").casefold() in {"active", "won", "live"}:
        stages["active-client"]["items"].append(row)

rows = []
for stage, data in stages.items():
    gross = 0
    for item in data["items"]:
        key = clean(item.get("business")).casefold()
        fee = clean(item.get("monthly_fee"), "")
        if not fee:
            fee = clean(strategy.get(key, {}).get("monthly_fee"), "")
        gross += fee_value(fee)
    weighted = round(gross * data["prob"])
    if stage == "staged-intake":
        next_action = "Strengthen evidence; do not promote without approval."
    elif stage == "promotion-review":
        next_action = "Use approval packets for approve/reject/hold decisions."
    elif stage == "approved-prospect":
        next_action = "Generate compliance, delivery, and draft assets only after approvals."
    else:
        next_action = "Track retained MRR and review delivery promises."
    rows.append({
        "date": today(),
        "stage": stage,
        "count": str(len(data["items"])),
        "weighted_probability": str(data["prob"]),
        "gross_monthly_fee": f"${gross}/mo",
        "weighted_mrr": f"${weighted}/mo",
        "next_action": next_action,
        "safety_gate": "Forecast only; no invoices, charges, outreach, or client promises.",
        "notes": "Weighted forecast is planning math, not booked revenue.",
    })

write_csv(p("revenue_forecast.csv"), rows, FIELDS)

os.makedirs(p("revenue_forecasts"), exist_ok=True)
path = p("revenue_forecasts", f"{today()}.md")
with open(path, "w", encoding="utf-8") as handle:
    handle.write("# Revenue Forecast\n\n")
    handle.write(f"- Date: {today()}\n")
    handle.write("- Pricing model: $0 upfront, flat monthly fee.\n")
    handle.write("- Safety: forecast only; no invoices, charges, outreach, or promises.\n\n")
    for row in rows:
        handle.write(
            f"- {row['stage']}: {row['count']} items / gross {row['gross_monthly_fee']} / "
            f"weighted {row['weighted_mrr']} / {row['next_action']}\n"
        )

print(rel(path))
