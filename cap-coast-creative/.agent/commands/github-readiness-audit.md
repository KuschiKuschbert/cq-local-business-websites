# `/github-readiness-audit`

Run `python3 .agent/skills/growth-engine/scripts/generate-github-readiness-audit.py` to verify local GitHub planning artifacts before any remote issue creation is considered.

This command checks approval packets, local issue drafts, execution-plan rows, command lock status, and referenced files. It does not run `gh`, create issues, push branches, or approve remote GitHub writes.
