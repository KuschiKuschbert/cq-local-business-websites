# Approval Packet: CocoBrew Express Yeppoon

- Date: 2026-06-17
- Approval type: promotion
- Priority rank: 1
- Priority score: 161
- Evidence: .agent/memory/working/intake_opportunity_briefs/cocobrew-express-yeppoon.md
- Offer tier: local-growth / $199/mo
- Trust hook: Fast mobile menu, booking/order path, catering or function enquiry
- Primary CTA: Make an enquiry

## Evidence Snapshot

- Public social signal: CocoBrew public group site and Yeppoon footer link to Facebook profile.
- Website gap: Owned static/Bootstrap-style site exists with menu/contact; opportunity is a cleaner mobile menu, catering enquiry, and drive-thru ordering path.
- Proposed opportunity: Drive-thru coffee and catering page with menu CTA, catering CTA, location proof, and breakfast/lunch commuter hook.

## Decision

- Recommended decision: approve for prospect promotion only if Daniel accepts the evidence packet.
- Record approval: `python3 .agent/skills/growth-engine/scripts/record-approval-decision.py --business "CocoBrew Express Yeppoon" --decision approve --decided-by "Daniel" --notes "Approved for prospect promotion only."`
- After approval, promotion command: `python3 .agent/skills/growth-engine/scripts/promote-intake.py --business "CocoBrew Express Yeppoon" --approved-by "Daniel"`

## Still Blocked

- Outreach send, remote GitHub writes, publishing, hosting, billing, and client-facing promises.
- Promotion does not approve outreach.
- Outreach requires separate compliance and send approval.

## Current Permission Context

- Promote candidate to prospect: approval-recorded / Daniel records an approve decision in approval_decisions.csv.
- Create remote GitHub issues: blocked / Daniel approves remote GitHub issue creation.
- Send or schedule outreach: blocked / Promoted prospect, compliant draft, sender ID, opt-out, contact basis, and explicit send approval.
