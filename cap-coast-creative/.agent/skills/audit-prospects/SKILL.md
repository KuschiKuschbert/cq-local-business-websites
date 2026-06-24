name: audit-prospects
description: Triage directories to find prospects that are missing modern website layouts, have quality discrepancies, or lack required HIVE standard compliance. Lists the next candidates for digital transformation.
triggers:
  - "triage prospects"
  - "list unbuilt sites"
  - "find transform candidates"
  - "show digital transformation candidates"

# Skill: audit-prospects

This skill scans the workspace for websites that are non-compliant with standard styling, structure, or conversion hooks, formatting them as prioritized transformation prospects.

## Instructions
1. Run `.agent/skills/audit-prospects/scripts/run-triage.py`.
2. Display the prioritized markdown table of candidates, including their category, pricing tier, and outstanding issues.
