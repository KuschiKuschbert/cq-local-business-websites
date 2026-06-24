# Approval Packet: Her. Hair

- Date: 2026-06-24
- Approval type: promotion
- Priority rank: 8
- Priority score: 155
- Evidence: .agent/memory/working/intake_opportunity_briefs/her-hair.md
- Offer tier: local-growth / $199/mo
- Trust hook: Clear offer, trust proof, and fast enquiry path
- Primary CTA: Make an enquiry

## Evidence Snapshot

- Public social signal: Public Facebook metadata identifies Her. Hair as a Yeppoon QLD hair stylist page.
- Website gap: No dedicated owned website was visible in the exact named search results; the public result set surfaced the Facebook page plus generic directories and competitor sites.
- Proposed opportunity: Hair stylist site with service list, before-and-after gallery, booking CTA, and local Yeppoon search landing page.

## Decision

- Recommended decision: approve for prospect promotion only if Daniel accepts the evidence packet.
- Record approval: `python3 .agent/skills/growth-engine/scripts/record-approval-decision.py --business "Her. Hair" --decision approve --decided-by "Daniel" --notes "Approved for prospect promotion only."`
- After approval, promotion command: `python3 .agent/skills/growth-engine/scripts/promote-intake.py --business "Her. Hair" --approved-by "Daniel"`

## Still Blocked

- Outreach send, remote GitHub writes, publishing, hosting, billing, and client-facing promises.
- Promotion does not approve outreach.
- Outreach requires separate compliance and send approval.

## Current Permission Context

- Promote candidate to prospect: approval-recorded / Daniel records an approve decision in approval_decisions.csv.
- Create remote GitHub issues: blocked / Daniel approves remote GitHub issue creation.
- Send or schedule outreach: blocked / Promoted prospect, compliant draft, sender ID, opt-out, contact basis, and explicit send approval.
