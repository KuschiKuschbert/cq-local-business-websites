# Command Hook: /audit-prospects
description: Triage directories to find prospects that are missing modern website directories or components.

When this slash command is triggered:
1. Execute the triage script: `bash .agent/skills/audit-prospects/scripts/assert-state.sh`.
2. This script automatically:
   - Scans directories on disk for validation failures.
   - Outputs a prioritized table of high-priority candidates for digital transformation, including their category, monthly tier, and outstanding issues.
