# `/record-approval-decision`

Run `python3 .agent/skills/growth-engine/scripts/record-approval-decision.py --business "Business Name" --decision approve|reject|hold --decided-by "Daniel" --notes "reason"` to record a supervised approval decision.

Recording an approval decision does not send outreach. An `approve` decision prints the safe promotion command, but promotion remains a separate explicit action.
