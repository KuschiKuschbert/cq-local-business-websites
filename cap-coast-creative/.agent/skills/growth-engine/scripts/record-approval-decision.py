#!/usr/bin/env python3
import argparse
from common import clean, locked_csv_update, p, read_csv, today

FIELDS = ["date", "business", "approval_type", "decision", "decided_by", "evidence_path", "follow_up_action", "notes"]

parser = argparse.ArgumentParser()
parser.add_argument("--business", required=True)
parser.add_argument("--decision", required=True, choices=["approve", "reject", "hold"])
parser.add_argument("--decided-by", required=True)
parser.add_argument("--notes", default="")
args = parser.parse_args()

queue = read_csv(p("approval_queue.csv"))
match = next((row for row in queue if clean(row.get("business")).casefold() == args.business.casefold()), None)
if not match:
    raise SystemExit("Refusing decision: business is not currently in approval_queue.csv.")

if args.decision == "approve":
    follow_up = clean(match.get("safe_command"))
elif args.decision == "reject":
    follow_up = "Leave out of prospects.csv unless new evidence changes the decision."
else:
    follow_up = "Keep pending; gather more evidence or review later."

def upsert_decision(rows):
    rows = [row for row in rows if not (
        clean(row.get("business")).casefold() == clean(match.get("business")).casefold()
        and clean(row.get("approval_type")).casefold() == clean(match.get("approval_type")).casefold()
    )]
    rows.append({
        "date": today(),
        "business": clean(match.get("business")),
        "approval_type": clean(match.get("approval_type")),
        "decision": args.decision,
        "decided_by": args.decided_by,
        "evidence_path": clean(match.get("source_path")),
        "follow_up_action": follow_up,
        "notes": clean(args.notes, "Decision recorded only; promotion and outreach remain separate gates."),
    })
    return rows


def append_generic_log(rows):
    rows.append({
        "date": today(),
        "decision": f"{args.decision}: {clean(match.get('business'))}",
        "area": clean(match.get("approval_type")),
        "approved_by": args.decided_by,
        "evidence_path": clean(match.get("source_path")),
        "notes": clean(args.notes, "Approval decision recorded. Promotion is still separate from outreach approval."),
    })
    return rows


locked_csv_update(p("approval_decisions.csv"), FIELDS, upsert_decision)
locked_csv_update(
    p("decision_log.csv"),
    ["date", "decision", "area", "approved_by", "evidence_path", "notes"],
    append_generic_log,
)

print(f"Recorded {args.decision} decision for {clean(match.get('business'))}.")
print(f"Follow-up: {follow_up}")
