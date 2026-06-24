# [Prospect Review] CocoBrew Express Yeppoon

## Decision Needed

Approve or reject moving this staged candidate into `prospects.csv`.

## Candidate

- Business: CocoBrew Express Yeppoon
- Region: Yeppoon
- Niche: drive-thru cafe / catering
- Approval type: promotion
- Readiness: promotion-review-ready
- Source brief: `.agent/memory/working/intake_opportunity_briefs/cocobrew-express-yeppoon.md`

## Evidence

- Socials: https://www.facebook.com/CocoBrewYeppoon
- Website: https://cocobrewyeppoon.com.au/
- Source URLs: https://www.cocobrew.com.au/; https://cocobrewyeppoon.com.au/
- Social status: verified
- Website status: owned-website-found
- Source status: other-public-source

## Opportunity

Owned static/Bootstrap-style site exists with menu/contact; opportunity is a cleaner mobile menu, catering enquiry, and drive-thru ordering path.

Suggested hook: Drive-thru coffee and catering page with menu CTA, catering CTA, location proof, and breakfast/lunch commuter hook.

## Safety Gate

- Promotion is not outreach approval.
- Do not send email, SMS, DM, form submission, social post, or make calls from this issue.
- Outreach requires a separate explicit Daniel approval after the prospect is promoted.

## Safe Command After Approval

```bash
python3 .agent/skills/growth-engine/scripts/promote-intake.py --business "CocoBrew Express Yeppoon" --approved-by "Daniel"
```
