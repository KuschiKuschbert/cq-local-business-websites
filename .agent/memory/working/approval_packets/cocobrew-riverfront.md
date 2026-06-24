# Approval Packet: CocoBrew Riverfront

- Date: 2026-06-17
- Approval type: promotion
- Priority rank: 2
- Priority score: 161
- Evidence: .agent/memory/working/intake_opportunity_briefs/cocobrew-riverfront.md
- Offer tier: local-growth / $199/mo
- Trust hook: Fast mobile menu, booking/order path, catering or function enquiry
- Primary CTA: Make an enquiry

## Evidence Snapshot

- Public social signal: Public CocoBrew group site lists the Riverfront venue, and the Riverfront site itself displays Facebook and Instagram icons in the visible contact/footer area.
- Website gap: Current Riverfront site clearly supports dining, booking, and ordering, but the visible navigation does not surface a dedicated functions or events path, a stronger Legends Bar conversion page, or a broader venue-story funnel for groups and occasions.
- Proposed opportunity: Riverfront hospitality page set with dining, Legends Bar, group booking/functions, and event-night CTA flow for locals, visitors, and corporate catchups.

## Decision

- Recommended decision: approve for prospect promotion only if Daniel accepts the evidence packet.
- Record approval: `python3 .agent/skills/growth-engine/scripts/record-approval-decision.py --business "CocoBrew Riverfront" --decision approve --decided-by "Daniel" --notes "Approved for prospect promotion only."`
- After approval, promotion command: `python3 .agent/skills/growth-engine/scripts/promote-intake.py --business "CocoBrew Riverfront" --approved-by "Daniel"`

## Still Blocked

- Outreach send, remote GitHub writes, publishing, hosting, billing, and client-facing promises.
- Promotion does not approve outreach.
- Outreach requires separate compliance and send approval.

## Current Permission Context

- Promote candidate to prospect: approval-recorded / Daniel records an approve decision in approval_decisions.csv.
- Create remote GitHub issues: blocked / Daniel approves remote GitHub issue creation.
- Send or schedule outreach: blocked / Promoted prospect, compliant draft, sender ID, opt-out, contact basis, and explicit send approval.
