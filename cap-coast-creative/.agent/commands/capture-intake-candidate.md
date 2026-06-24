# `/capture-intake-candidate`

Run `python3 .agent/skills/growth-engine/scripts/capture-intake-candidate.py --business "Business Name" --region "Yeppoon" --niche "cafe" --socials "https://facebook.example/page" --website "https://business.example" --source-urls "https://public-source.example/page" --observed-social-signal "public page confirms business-owned social profile" --observed-website-gap "owned site exists but booking path is unclear" --proposed-hook "mobile menu and booking CTA" --query "search terms used"` to stage a sourced candidate.

This command requires at least one public social URL and one public source URL. It only updates `prospect_intake.csv` and logs the research attempt. It does not promote prospects, send outreach, create GitHub issues, publish concepts, or update third-party systems.
