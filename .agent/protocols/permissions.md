# Command Permissions Allowlist & Verification Rules

This file sets command run rules for coding agents to maintain the repository integrity.

## Allowed Shell Commands
- `python3 update-socials.py` - Safe script execution to link footers.
- `./build-all.sh` - Safe shell compiler.
- `git status` / `git diff` - Code change review commands.
- `npm install` / `npm run dev` - Locally testing Vite folders.
- `python3 .agent/skills/verify-integrity/scripts/run-audit.py` / `bash .agent/skills/verify-integrity/scripts/assert-state.sh` - Codebase compliance audit.
- `python3 .agent/skills/audit-prospects/scripts/run-triage.py` / `bash .agent/skills/audit-prospects/scripts/assert-state.sh` - Prospect triage and candidate listing.

## Blocked Commands
- Never run force push (`git push -f`).
- Never delete or quarantine database or memory logs without explicit authorization.
- Never write credentials or API keys directly to configuration files.
