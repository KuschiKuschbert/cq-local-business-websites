#!/usr/bin/env python3
from common import clean, p, read_csv, today, write_csv

FIELDS = ["date","business","region","niche","tier","status","brief_path","recommended_pattern","primary_cta","trust_hook","next_action","notes"]
rows = []
for prospect in read_csv(p("prospects.csv")):
    if clean(prospect.get("status"), "").lower() in {"qualified","briefed","mockup-needed","mockup-ready"}:
        rows.append({"date": today(), "business": clean(prospect.get("business")), "region": clean(prospect.get("region")), "niche": clean(prospect.get("niche")), "tier": clean(prospect.get("tier")), "status": clean(prospect.get("status")), "brief_path": "-", "recommended_pattern": "closest completed niche mockup", "primary_cta": "Request quote", "trust_hook": clean(prospect.get("hook")), "next_action": clean(prospect.get("next_action")), "notes": "Generated locally; not client-approved."})
write_csv(p("mockup_briefs.csv"), rows, FIELDS)
print(f"Generated {len(rows)} mockup brief records." if rows else "No eligible prospect rows for mockup brief generation.")
