#!/usr/bin/env python3
import argparse
import os
from common import clean, p, read_csv, today, write_csv

FIELDS = ["business","region","niche","socials","website","region_fit","social_activity","website_gap","trust_opportunity","monthly_fit","contact_basis_quality","owner_accessibility","tier","contact_basis","hook","status","last_contact_date","next_action_date","next_action","opt_out","source_urls","notes"]
LOG = ["date","business","approved_by","source_score","recommendation","prospect_status","next_action","notes"]


def tier(niche):
    n = (niche or "").lower()
    return "$299/mo" if any(x in n for x in ["land", "digger", "earth"]) else "$199/mo" if any(x in n for x in ["market", "pizza", "gallery"]) else "$249/mo"


parser = argparse.ArgumentParser()
parser.add_argument("--list", action="store_true")
parser.add_argument("--business")
parser.add_argument("--approved-by")
args = parser.parse_args()
intake = read_csv(p("prospect_intake.csv"))
reviews = {clean(r.get("business"), "").casefold(): r for r in read_csv(p("intake_review.csv"))}
if args.list or not args.business:
    for row in intake:
        review = reviews.get(clean(row.get("business"), "").casefold(), {})
        print(f"- {clean(row.get('business'))} | score {clean(review.get('score'), 'unreviewed')} | {clean(review.get('recommendation'), 'unreviewed')}")
    raise SystemExit(0)
if not args.approved_by:
    raise SystemExit("Refusing promotion: --approved-by is required.")
match = next((row for row in intake if clean(row.get("business")).casefold() == args.business.casefold()), None)
if not match:
    raise SystemExit("Refusing promotion: no staged intake candidate matched.")
review = reviews.get(clean(match.get("business"), "").casefold(), {})
if review.get("recommendation") != "promote-review":
    raise SystemExit("Refusing promotion: candidate is not promote-review.")
decisions = {
    (clean(row.get("business")).casefold(), clean(row.get("approval_type")).casefold()): row
    for row in read_csv(p("approval_decisions.csv"))
}
decision = decisions.get((clean(match.get("business")).casefold(), "promotion"))
if not decision or clean(decision.get("decision")).casefold() != "approve":
    raise SystemExit("Refusing promotion: record an approve decision in approval_decisions.csv first.")
if clean(decision.get("decided_by")).casefold() != clean(args.approved_by).casefold():
    raise SystemExit("Refusing promotion: --approved-by must match the recorded approval decision.")
prospects = read_csv(p("prospects.csv"))
if any(clean(row.get("business")).casefold() == clean(match.get("business")).casefold() for row in prospects):
    raise SystemExit("Refusing promotion: already in prospects.csv.")
prospects.append({
    "business": clean(match.get("business")), "region": clean(match.get("region")), "niche": clean(match.get("niche")),
    "socials": clean(match.get("socials"), ""), "website": clean(match.get("website"), ""),
    "region_fit": "15", "social_activity": "15", "website_gap": "20", "trust_opportunity": "20", "monthly_fit": "10",
    "contact_basis_quality": "0", "owner_accessibility": "0", "tier": tier(match.get("niche")), "contact_basis": "none documented",
    "hook": clean(match.get("proposed_hook")), "status": "qualified", "last_contact_date": "", "next_action_date": "",
    "next_action": "Review for mockup brief and lawful contact basis before outreach", "opt_out": "No",
    "source_urls": clean(match.get("source_urls")), "notes": "Promoted from staged intake with Daniel approval.",
})
write_csv(p("prospects.csv"), prospects, FIELDS)
logs = read_csv(p("promotion_log.csv"))
logs.append({"date": today(), "business": clean(match.get("business")), "approved_by": args.approved_by, "source_score": clean(review.get("score")), "recommendation": clean(review.get("recommendation")), "prospect_status": "qualified", "next_action": "Review for mockup brief and lawful contact basis before outreach", "notes": "Promotion is not outreach approval."})
write_csv(p("promotion_log.csv"), logs, LOG)
print(f"Promoted {clean(match.get('business'))}. Contact basis remains none documented.")
