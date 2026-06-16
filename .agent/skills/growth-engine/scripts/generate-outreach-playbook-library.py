#!/usr/bin/env python3
import os
from common import p, rel, today, write_csv

FIELDS = [
    "date",
    "playbook_id",
    "niche",
    "channel",
    "recipient_type",
    "opening_principle",
    "observation_type",
    "safe_message_template",
    "follow_up_template",
    "opt_out",
    "required_personalization",
    "blocked_until",
    "safety_gate",
    "notes",
]

SAFETY_GATE = (
    "Template library only; not approved copy; requires approved prospect, contact basis, opt-out, "
    "sender identity, exact Daniel approval, and manual send."
)

PLAYBOOKS = [
    {
        "playbook_id": "social-active-website-gap",
        "niche": "social-active local business",
        "channel": "email-or-dm-template",
        "recipient_type": "owner or manager",
        "opening_principle": "Start with a concrete public observation from [social channel], not a generic compliment.",
        "observation_type": "[recent post] plus [website gap]",
        "safe_message_template": (
            "Hi [business] team, I saw [specific observation] on [social channel] and noticed [website gap]. "
            "I build simple local websites around [region] on a $0 upfront, flat monthly model. "
            "Would a private concept showing [specific improvement] be useful to review?"
        ),
        "follow_up_template": (
            "Hi [business] team, quick follow-up on the private website concept idea for [specific improvement]. "
            "No pressure if it is not useful."
        ),
        "opt_out": "If this is not relevant, no worries - I will not follow up.",
        "required_personalization": "[business], [region], [social channel], [specific observation], [website gap], [specific improvement]",
        "blocked_until": "Approved prospect, documented contact basis, and exact Daniel outreach approval.",
        "notes": "Best for businesses with visible social activity but no clear owned website or weak conversion path.",
    },
    {
        "playbook_id": "trust-proof-service",
        "niche": "trade, cleaning, pest, landscaping, excavation",
        "channel": "email-template",
        "recipient_type": "owner or bookings contact",
        "opening_principle": "Lead with customer-risk reduction, not design taste.",
        "observation_type": "[service promise gap] plus [local proof opportunity]",
        "safe_message_template": (
            "Hi [business] team, I noticed [specific observation] and thought your site could make [trust proof] "
            "clearer for customers in [region]. My local website model is $0 upfront and [monthly fee] per month. "
            "Would you be open to seeing a private mockup focused on [trust proof] and enquiry flow?"
        ),
        "follow_up_template": (
            "Hi [business] team, checking whether a private mockup around [trust proof] and faster enquiries "
            "would be worth reviewing."
        ),
        "opt_out": "If this is not relevant, no worries - I will not follow up.",
        "required_personalization": "[business], [region], [specific observation], [trust proof], [monthly fee]",
        "blocked_until": "Approved prospect, documented contact basis, and exact Daniel outreach approval.",
        "notes": "Use only after niche-specific claims are evidence-backed; do not invent guarantees, licenses, or certifications.",
    },
    {
        "playbook_id": "hospitality-menu-events",
        "niche": "cafe, restaurant, venue, market, gallery",
        "channel": "email-or-dm-template",
        "recipient_type": "owner, manager, or events contact",
        "opening_principle": "Tie the idea to a visible customer decision point.",
        "observation_type": "[menu/event/product visibility gap]",
        "safe_message_template": (
            "Hi [business] team, I saw [specific observation] and noticed customers may have to work harder to find "
            "[menu/event/product detail]. I build local sites with $0 upfront and a flat monthly fee. "
            "Would a private concept for [customer action] be useful?"
        ),
        "follow_up_template": (
            "Hi [business] team, circling back on the private concept idea for making [customer action] easier online."
        ),
        "opt_out": "If this is not relevant, no worries - I will not follow up.",
        "required_personalization": "[business], [specific observation], [menu/event/product detail], [customer action]",
        "blocked_until": "Approved prospect, documented contact basis, and exact Daniel outreach approval.",
        "notes": "Works when social content is strong but bookings, menus, events, or enquiry paths are unclear.",
    },
]

rows = []
for playbook in PLAYBOOKS:
    row = {"date": today(), "safety_gate": SAFETY_GATE}
    row.update(playbook)
    rows.append(row)

write_csv(p("outreach_playbook_library.csv"), rows, FIELDS)

out_dir = p("outreach_playbook_library")
os.makedirs(out_dir, exist_ok=True)
path = os.path.join(out_dir, f"{today()}.md")
with open(path, "w", encoding="utf-8") as handle:
    handle.write("# Outreach Playbook Library\n\n")
    handle.write("Safety status: generic strategy only, not prospect-specific copy, not approved, not sent.\n\n")
    handle.write(f"Global gate: {SAFETY_GATE}\n\n")
    for row in rows:
        handle.write(f"## {row['playbook_id']}\n\n")
        handle.write(f"- Niche: {row['niche']}\n")
        handle.write(f"- Channel: {row['channel']}\n")
        handle.write(f"- Recipient: {row['recipient_type']}\n")
        handle.write(f"- Opening principle: {row['opening_principle']}\n")
        handle.write(f"- Required personalization: {row['required_personalization']}\n")
        handle.write(f"- Blocked until: {row['blocked_until']}\n\n")
        handle.write("Template:\n\n")
        handle.write(f"{row['safe_message_template']}\n\n")
        handle.write("Follow-up:\n\n")
        handle.write(f"{row['follow_up_template']}\n\n")
        handle.write(f"Opt-out: {row['opt_out']}\n\n")

print(f"Generated {len(rows)} generic outreach playbooks at {rel(path)}.")
