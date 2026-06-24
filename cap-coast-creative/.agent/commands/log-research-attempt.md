# `/log-research-attempt`

Run `python3 .agent/skills/growth-engine/scripts/log-research-attempt.py --business "Business Name" --query "search terms used" --source-checked "https://source.example/page" --result no_verified_social_found --next-action "Try direct Facebook or Google Business Profile search" --notes "source confirms listing only"` to record a research pass.

Allowed results: `no_verified_business_candidate_found`, `no_verified_social_found`, `verified_candidate_found`, `duplicate_existing_candidate`, `source_unavailable`, `rejected_unsafe_source`, `needs_manual_review`.

This command only appends to `research_attempts.csv`. It does not add intake rows, promote prospects, contact businesses, create GitHub issues, or update third-party systems.
