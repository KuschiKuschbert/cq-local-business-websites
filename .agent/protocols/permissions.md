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
- `python3 .agent/skills/growth-engine/scripts/generate-research-queue.py` - Local research queue generation; does not browse or contact businesses.
- `python3 .agent/skills/growth-engine/scripts/generate-regional-coverage-heatmap.py` - Local region/niche coverage scoring; research-only and cannot approve capture, promotion, outreach, publishing, billing, or remote GitHub writes.
- `python3 .agent/skills/growth-engine/scripts/generate-source-pivot-plan.py` - Local source-pivot planning after repeated failed research; does not browse or contact businesses.
- `python3 .agent/skills/growth-engine/scripts/generate-research-suppression-list.py` - Local advisory memory for repeated failed public research patterns; cannot approve capture, promotion, outreach, publishing, billing, or remote GitHub writes.
- `python3 .agent/skills/growth-engine/scripts/generate-intake-opportunity-briefs.py` - Local private opportunity brief generation for evidence-ready staged candidates.
- `python3 .agent/skills/growth-engine/scripts/generate-approval-queue.py` - Local approval gate report generation; does not approve or execute actions.
- `python3 .agent/skills/growth-engine/scripts/generate-private-concepts.py` - Local private concept-site generation; does not publish or contact businesses.
- `python3 .agent/skills/growth-engine/scripts/record-approval-decision.py --business "Name" --decision approve|reject|hold --decided-by "Daniel"` - Local approval decision logging only; this is not promotion or outreach approval.
- `python3 .agent/skills/growth-engine/scripts/generate-approval-decision-inbox.py` - Local approve/reject/hold decision inbox generation; does not approve or execute actions.
- `python3 .agent/skills/growth-engine/scripts/generate-decision-cockpit.py` - Local consolidated decision review generation; advisory only and cannot approve promotion, outreach, publishing, billing, or remote GitHub writes.
- `python3 .agent/skills/growth-engine/scripts/generate-post-approval-workflow.py` - Local post-approval workflow mapping; advisory only and cannot execute outreach, publishing, billing, hosting, or remote GitHub writes.
- `python3 .agent/skills/growth-engine/scripts/promote-intake.py --business "Name" --approved-by "Daniel"` - Local promotion from staged intake into the prospect tracker only after a matching recorded `approve` decision; this is not outreach approval.
- `python3 .agent/skills/growth-engine/scripts/generate-dashboard.py` - Local HTML dashboard generation from tracker files.
- `python3 .agent/skills/growth-engine/scripts/generate-council-ceo-brief.py` - Local council CEO brief generation; advisory only and does not approve actions.
- `python3 .agent/skills/growth-engine/scripts/generate-operator-action-queue.py` - Local unified action queue generation; advisory only and does not approve actions.
- `python3 .agent/skills/growth-engine/scripts/generate-mockup-briefs.py` - Local website mockup brief generation.
- `python3 .agent/skills/growth-engine/scripts/generate-outreach-playbook-library.py` - Local generic outreach playbook generation; templates are not approved copy and cannot be sent.
- `python3 .agent/skills/growth-engine/scripts/generate-outreach-drafts.py` - Local approval-gated outreach draft pack generation.
- `python3 .agent/skills/growth-engine/scripts/generate-proposals.py` - Local draft proposal generation and proposal register update.
- `python3 .agent/skills/growth-engine/scripts/generate-retrospective.py` - Local KPI snapshot and retrospective generation.
- `python3 .agent/skills/growth-engine/scripts/run-ceo-loop.py` - Local supervised CEO-loop orchestration; safe reports and tracker refresh only.
- `python3 .agent/skills/growth-engine/scripts/audit-engine.py` - Local engine health check.
- `/prospect-scan`, `/intake-review`, `/verify-intake-evidence`, `/research-queue`, `/regional-coverage-heatmap`, `/source-pivot-plan`, `/research-suppression-list`, `/intake-opportunity-briefs`, `/approval-queue`, `/approval-decision-inbox`, `/decision-cockpit`, `/post-approval-workflow`, `/private-concepts`, `/promote-intake`, `/mockup-briefs`, `/outreach-week`, `/outreach-playbook-library`, `/outreach-drafts`, `/client-delivery`, `/proposal-admin`, `/growth-dashboard`, `/growth-ceo-loop`, `/growth-retrospective`, and `/growth-engine-audit` are planning workflows only: they may research, score, verify evidence, generate research tasks, create private opportunity briefs, create internal concept sites, create generic playbooks, draft, update local tracker files, stage prospect intake rows, generate approval gates, promote Daniel-approved rows into the main tracker, prepare GitHub issue content, generate local reports, audit local files, and propose lessons, but must follow `.agent/protocols/outreach-safety.md` and must not send outbound messages without explicit approval.

## Blocked Commands
- Never run force push (`git push -f`).
- Never delete or quarantine database or memory logs without explicit authorization.
- Never write credentials or API keys directly to configuration files.
- Never send, schedule, post, DM, submit contact forms, or otherwise contact prospects without explicit authorization for that outreach action.
- Never move DNS, change hosting, publish client-facing claims, or alter client credentials without explicit authorization.
- Never create invoices, charge clients, or mark a proposal as approved without explicit authorization.
