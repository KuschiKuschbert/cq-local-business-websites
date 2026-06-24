#!/usr/bin/env python3
import argparse
import os
from datetime import date, timedelta
from common import p, read_csv, rel, write_csv

parser = argparse.ArgumentParser()
parser.add_argument("--append-kpi", action="store_true")
args = parser.parse_args()
week = (date.today() - timedelta(days=date.today().weekday())).isoformat()
intake = read_csv(p("prospect_intake.csv"))
prospects = read_csv(p("prospects.csv"))
scorecard = read_csv(p("improvement_scorecard.csv"))
row = {"week_start": week, "intake_candidates": str(len(intake)), "approved_prospects": str(len(prospects)), "mockups_needed": "0", "mockups_ready": "0", "outreach_events": "0", "replies": "0", "meetings": "0", "wins": "0", "lost": "0", "opt_outs": "0", "notes": ""}
fields = list(row.keys())
if args.append_kpi:
    write_csv(p("kpi_history.csv"), [row], fields)
os.makedirs(p("retrospectives"), exist_ok=True)
path = p("retrospectives", f"{week}.md")
with open(path, "w", encoding="utf-8") as handle:
    handle.write(f"# Cap Coast Creative Weekly Retrospective\n\n- Week start: {week}\n- Intake candidates: {len(intake)}\n- Approved prospects: {len(prospects)}\n")
    handle.write(f"- Improvement checks: {len(scorecard)}\n\n")
    handle.write("## Improvement Actions\n\n")
    for item in scorecard:
        handle.write(f"- {item.get('area')}: {item.get('status')} / {item.get('improvement_action')}\n")
print(rel(path))
