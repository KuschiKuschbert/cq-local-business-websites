# `/promote-intake`

Promote one staged candidate only after Daniel records an explicit `approve` decision:

`python3 .agent/skills/growth-engine/scripts/record-approval-decision.py --business "Business Name" --decision approve --decided-by "Daniel" --notes "reason"`

Then run:

`python3 .agent/skills/growth-engine/scripts/promote-intake.py --business "Business Name" --approved-by "Daniel"`

Promotion is not outreach approval.
