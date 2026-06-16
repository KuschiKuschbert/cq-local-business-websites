# `/post-approval-workflow`

Run `python3 .agent/skills/growth-engine/scripts/generate-post-approval-workflow.py`.

This maps the safe local sequence after Daniel records a promotion approval: record decision, promote approved intake, regenerate local artifacts, review compliance, and stop at outreach or remote-write gates. It does not approve outreach, publishing, billing, hosting, or remote GitHub writes.
