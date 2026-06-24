# Approval Packet: Yeppoon Community Market

- Date: 2026-06-17
- Approval type: promotion
- Priority rank: 5
- Priority score: 159
- Evidence: .agent/memory/working/intake_opportunity_briefs/yeppoon-community-market.md
- Offer tier: local-growth / $199/mo
- Trust hook: Clear stallholder info, visitor hours, vendor enquiry path
- Primary CTA: View stallholder info

## Evidence Snapshot

- Public social signal: Directory page links the market to a Facebook page for more information.
- Website gap: No dedicated owned website identified in this scan beyond directory and social listing.
- Proposed opportunity: Simple vendor/stallholder page with weekly produce calendar, visitor FAQs, and enquiry CTA.

## Decision

- Recommended decision: approve for prospect promotion only if Daniel accepts the evidence packet.
- Record approval: `python3 .agent/skills/growth-engine/scripts/record-approval-decision.py --business "Yeppoon Community Market" --decision approve --decided-by "Daniel" --notes "Approved for prospect promotion only."`
- After approval, promotion command: `python3 .agent/skills/growth-engine/scripts/promote-intake.py --business "Yeppoon Community Market" --approved-by "Daniel"`

## Still Blocked

- Outreach send, remote GitHub writes, publishing, hosting, billing, and client-facing promises.
- Promotion does not approve outreach.
- Outreach requires separate compliance and send approval.

## Current Permission Context

- Promote candidate to prospect: approval-recorded / Daniel records an approve decision in approval_decisions.csv.
- Create remote GitHub issues: blocked / Daniel approves remote GitHub issue creation.
- Send or schedule outreach: blocked / Promoted prospect, compliant draft, sender ID, opt-out, contact basis, and explicit send approval.
