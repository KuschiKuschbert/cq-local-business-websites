#!/usr/bin/env python3
import os
from common import clean, p, read_csv, rel, today, write_csv

FIELDS = ["date", "business", "niche", "tier", "monthly_fee", "offer_angle", "trust_hook", "primary_cta", "outreach_angle", "notes"]


def tier_for(niche):
    text = niche.lower()
    if any(term in text for term in ["excavation", "landscaping", "mini digger", "specialty", "accommodation", "functions"]):
        return "specialty", "$299/mo"
    if any(term in text for term in ["cleaning", "pest", "electrician", "plumber"]):
        return "trade-service", "$249/mo"
    return "local-growth", "$199/mo"


def hooks_for(niche):
    text = niche.lower()
    if "pest" in text:
        return "Police-cleared technicians, liability insurance, and price-lock quote path", "Request a treatment quote"
    if "cleaning" in text:
        return "Police-cleared team, liability insurance, and simple quote request", "Request a clean quote"
    if any(term in text for term in ["landscaping", "mini digger"]):
        return "Pristine site guarantee, access checks, weather-aware scheduling", "Request a site visit"
    if any(term in text for term in ["restaurant", "bar", "cafe", "catering", "pizza"]):
        return "Fast mobile menu, booking/order path, catering or function enquiry", "Make an enquiry"
    if "market" in text:
        return "Clear stallholder info, visitor hours, vendor enquiry path", "View stallholder info"
    if "gallery" in text:
        return "Workshop calendar, artist story, visit and enquiry path", "Plan a visit"
    return "Clear offer, trust proof, and fast enquiry path", "Make an enquiry"


def offer_angle(niche):
    text = niche.lower()
    if any(term in text for term in ["restaurant", "bar", "cafe", "catering", "pizza"]):
        return "$0 upfront website refresh focused on mobile menus, bookings, orders, and local search."
    if any(term in text for term in ["cleaning", "pest", "landscaping", "mini digger"]):
        return "$0 upfront lead-generation website focused on trust, quote requests, and service-area search."
    if any(term in text for term in ["market", "gallery"]):
        return "$0 upfront local presence website focused on visitor clarity, events, and enquiries."
    return "$0 upfront local business website focused on search visibility and simple enquiries."


intake = read_csv(p("prospect_intake.csv"))
rows = []
for item in intake:
    niche = clean(item.get("niche"))
    tier, fee = tier_for(niche)
    hook, cta = hooks_for(niche)
    rows.append({
        "date": today(),
        "business": clean(item.get("business")),
        "niche": niche,
        "tier": tier,
        "monthly_fee": fee,
        "offer_angle": offer_angle(niche),
        "trust_hook": hook,
        "primary_cta": cta,
        "outreach_angle": f"Lead with a specific observed website gap, then offer the {fee} flat monthly model.",
        "notes": "Strategy only; no contact approval implied.",
    })

write_csv(p("offer_strategy.csv"), rows, FIELDS)

os.makedirs(p("offer_strategy"), exist_ok=True)
path = p("offer_strategy", f"{today()}.md")
with open(path, "w", encoding="utf-8") as handle:
    handle.write("# Cap Coast Creative Offer Strategy\n\n")
    handle.write(f"- Date: {today()}\n")
    handle.write("- Pricing model: $0 upfront, flat monthly fee.\n")
    handle.write("- Safety: strategy is not outreach approval.\n\n")
    for row in rows:
        handle.write(f"## {row['business']}\n\n")
        handle.write(f"- Tier: {row['tier']} / {row['monthly_fee']}\n")
        handle.write(f"- Offer: {row['offer_angle']}\n")
        handle.write(f"- Trust hook: {row['trust_hook']}\n")
        handle.write(f"- CTA: {row['primary_cta']}\n")
        handle.write(f"- Outreach angle: {row['outreach_angle']}\n\n")

print(rel(path))
