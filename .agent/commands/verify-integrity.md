# Command Hook: /verify-integrity
description: Audit the directories of all 26 website folders for HTML/CSS/JS integrity.

When this slash command is triggered:
1. Scan all active website folders for:
   - Presence of `index.html` and matching assets/style files.
   - Descriptive title tag and one single `<h1>` element.
   - Unique, descriptive IDs on forms and buttons.
   - Correct pricing tiers matching their niche category in PREFERENCES.md.
   - Correct target trust badges matching their niche category in LESSONS.md.
2. Output a checklist of directories audited and report any validation discrepancies.
