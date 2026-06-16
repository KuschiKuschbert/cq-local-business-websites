# Command Permissions Allowlist & Verification Rules

This file sets command run rules for coding agents to maintain the repository integrity.

## Allowed Shell Commands
- `python3 update-socials.py` - Safe script execution to link footers.
- `./build-all.sh` - Safe shell compiler.
- `git status` / `git diff` - Code change review commands.
- `npm install` / `npm run dev` - Locally testing Vite folders.
- `python3 .agent/skills/verify-integrity/scripts/run-audit.py` / `bash .agent/skills/verify-integrity/scripts/assert-state.sh` - Codebase compliance audit.
- `python3 .agent/skills/audit-prospects/scripts/run-triage.py` / `bash .agent/skills/audit-prospects/scripts/assert-state.sh` - Prospect triage and candidate listing.
- `python3 .agent/skills/growth-engine/scripts/run-pipeline.py` / `bash .agent/skills/growth-engine/scripts/assert-state.sh` - Local prospect tracker validation and weekly planning report.
- `python3 .agent/skills/growth-engine/scripts/review-intake.py` - Local staged prospect intake review.
- `python3 .agent/skills/growth-engine/scripts/verify-intake-evidence.py` - Local evidence-readiness check for staged candidates.
- `python3 .agent/skills/growth-engine/scripts/generate-intake-opportunity-briefs.py` - Local private opportunity brief generation for evidence-ready staged candidates.
- `python3 .agent/skills/growth-engine/scripts/generate-approval-queue.py` - Local approval gate report generation; does not approve or execute actions.
- `python3 .agent/skills/growth-engine/scripts/promote-intake.py --business "Name" --approved-by "Daniel"` - Local approved promotion from staged intake into the prospect tracker; this is not outreach approval.
- `python3 .agent/skills/growth-engine/scripts/generate-dashboard.py` - Local HTML dashboard generation from tracker files.
- `python3 .agent/skills/growth-engine/scripts/generate-mockup-briefs.py` - Local website mockup brief generation.
- `python3 .agent/skills/growth-engine/scripts/generate-outreach-drafts.py` - Local approval-gated outreach draft pack generation.
- `python3 .agent/skills/growth-engine/scripts/generate-proposals.py` - Local draft proposal generation and proposal register update.
- `python3 .agent/skills/growth-engine/scripts/generate-retrospective.py` - Local KPI snapshot and retrospective generation.
- `python3 .agent/skills/growth-engine/scripts/run-ceo-loop.py` - Local supervised CEO-loop orchestration; safe reports and tracker refresh only.
- `python3 .agent/skills/growth-engine/scripts/audit-engine.py` - Local engine health check.
- `/prospect-scan`, `/intake-review`, `/verify-intake-evidence`, `/intake-opportunity-briefs`, `/approval-queue`, `/promote-intake`, `/mockup-briefs`, `/outreach-week`, `/outreach-drafts`, `/client-delivery`, `/proposal-admin`, `/growth-dashboard`, `/growth-ceo-loop`, `/growth-retrospective`, and `/growth-engine-audit` are planning workflows only: they may research, score, verify evidence, create private opportunity briefs, draft, update local tracker files, stage prospect intake rows, generate approval gates, promote Daniel-approved rows into the main tracker, prepare GitHub issue content, generate local reports, audit local files, and propose lessons, but must follow `.agent/protocols/outreach-safety.md` and must not send outbound messages without explicit approval.

## Blocked Commands
- Never run force push (`git push -f`).
- Never delete or quarantine database or memory logs without explicit authorization.
- Never write credentials or API keys directly to configuration files.
- Never send, schedule, post, DM, submit contact forms, or otherwise contact prospects without explicit authorization for that outreach action.
- Never move DNS, change hosting, publish client-facing claims, or alter client credentials without explicit authorization.
- Never create invoices, charge clients, or mark a proposal as approved without explicit authorization.
