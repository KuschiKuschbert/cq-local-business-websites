#!/usr/bin/env python3
import os
from common import clean, p, read_csv, rel, slug, today, write_csv

FIELDS = ["date", "business", "channel", "draft_path", "approval_status", "contact_basis", "opt_out", "next_action", "notes"]

strategies = {row.get("business"): row for row in read_csv(p("offer_strategy.csv"))}
prospects = read_csv(p("prospects.csv"))
out_dir = p("outreach_drafts")
os.makedirs(out_dir, exist_ok=True)

rows = []
for prospect in prospects:
    status = clean(prospect.get("status"), "").lower()
    if status not in {"qualified", "briefed", "mockup-needed", "mockup-ready", "follow-up-draft"}:
        continue
    business = clean(prospect.get("business"))
    strategy = strategies.get(business, {})
    fee = clean(strategy.get("monthly_fee"), clean(prospect.get("tier")))
    hook = clean(strategy.get("trust_hook"), clean(prospect.get("hook")))
    angle = clean(strategy.get("outreach_angle"), "Lead with a specific observed website gap.")
    path = os.path.join(out_dir, f"{slug(business)}.md")
    body = f"""# Outreach Draft Pack: {business}

Safety status: draft only, not approved, not sent.

## Short Email Draft

Subject: Quick website idea for {business}

Hi {business} team,

I noticed an opportunity to make your online presence clearer for local customers around {clean(prospect.get("region"))}.

The idea: {angle}

I build small-business websites on a $0 upfront, flat monthly model ({fee}) with a focus on fast mobile pages, clear enquiries, and practical trust proof like: {hook}.

Would it be useful if I showed you a private concept first?

If this is not relevant, no worries - I will not follow up.

## DM Draft

Hi, I am local to the CQ/Cap Coast area and had a small website idea for {business}: {angle} The model is $0 upfront, {fee}, and I can show a private concept before anything else. If not relevant, no worries.

## Approval Checklist

- Daniel has approved this exact draft.
- Contact basis is documented.
- Opt-out wording is present.
- No claim is made that the business requested this.
- No message is sent from this generator.
"""
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(body)
    rows.append({
        "date": today(),
        "business": business,
        "channel": "email-or-dm-draft",
        "draft_path": rel(path),
        "approval_status": "needs-explicit-outreach-approval",
        "contact_basis": clean(prospect.get("contact_basis"), "none documented"),
        "opt_out": "included",
        "next_action": "Daniel review only; do not send without separate approval.",
        "notes": "Generated locally from approved prospect and offer strategy.",
    })

write_csv(p("outreach_drafts.csv"), rows, FIELDS)
print(f"Generated {len(rows)} outreach draft records." if rows else "No eligible prospect rows for outreach draft packs.")
