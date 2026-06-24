#!/usr/bin/env python3
from common import clean, p, read_csv

prospects = read_csv(p("prospects.csv"))
outreach = read_csv(p("outreach_log.csv"))
print("Cap Coast Creative Growth Engine Report")
print("======================================")
print(f"Rows: {len(prospects)} total")
print(f"Outreach events: {len(outreach)}")
if not prospects:
    print("No active real prospects yet. Use approval queue before promotion.")
else:
    for row in prospects:
        score = sum(int(row.get(field) or 0) for field in ["region_fit","social_activity","website_gap","trust_opportunity","monthly_fit","contact_basis_quality","owner_accessibility"])
        print(f"- {clean(row.get('business'))}: {score} / {clean(row.get('status'))} / {clean(row.get('next_action'))}")
print("Safety Warnings")
print("- none")
