name: verify-integrity
description: Run local quality and compliance audits on all website directories to verify HTML/CSS integrity, descriptive title tags, single H1s, form IDs, proper pricing references, and niche trust badges.
triggers:
  - "run integrity check"
  - "verify website quality"
  - "audit html elements"
  - "check form ids and buttons"
  - "verify compliance with lessons or preferences"

# Skill: verify-integrity

This skill executes a programmatic audit across all 26 local business website mockups to ensure they conform to the styling rules in `PREFERENCES.md` and conversion hooks in `LESSONS.md`.

## Instructions
1. Run `.agent/skills/verify-integrity/scripts/run-audit.py` to audit all website folders.
2. If discrepancies are found, list the affected files, the specific failure reason, and recommendation to fix them.
3. The audit will return code 0 if all sites pass, or 1 if any sites fail.
