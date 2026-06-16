# The HIVE / Agentic Stack Map

This folder contains the portable brain layers, protocols, and commands configured for the **Central Queensland Local Business Websites** project.

## Layout Overview

- **`memory/`**:
  - `personal/PREFERENCES.md`: Core developer rules, styling, and pricing structures.
  - `semantic/LESSONS.md`: Validated lessons about region context, plumber rules, landscaper checks.
  - `working/WORKSPACE.md`: A live list of the 26 websites and their development state.
  - `working/PROSPECT_PIPELINE.md`: Cap Coast Creative prospect tracker, weekly rhythm, stage model, and outreach approval templates.
  - `working/prospect_intake.csv`: Staging table for sourced but not-yet-approved prospect candidates.
  - `working/intake_review.csv`: Review summary for staged candidates.
  - `working/intake_reviews/`: Generated staged-candidate review reports.
  - `working/intake_verification.csv`: Evidence-readiness table for staged candidates.
  - `working/intake_verifications/`: Generated staged-candidate evidence reports.
  - `working/intake_opportunity_briefs.csv`: Register of private opportunity briefs for evidence-ready staged candidates.
  - `working/intake_opportunity_briefs/`: Generated private opportunity briefs for staged candidates.
  - `working/approval_queue.csv`: Current explicit approval gates for promotion, outreach, mockup use, proposals, and other blocked actions.
  - `working/approval_reports/`: Generated approval queue reports.
  - `working/promotion_log.csv`: Audit log for Daniel-approved moves from staged intake into the main prospect tracker.
  - `working/prospects.csv`: Structured prospect register used by the growth-engine scoring script.
  - `working/mockup_briefs.csv`: Structured register of generated website mockup briefs.
  - `working/mockup_briefs/`: Generated website mockup brief documents.
  - `working/outreach_log.csv`: Structured event log for approved outreach, replies, opt-outs, and follow-up outcomes.
  - `working/outreach_drafts/`: Generated approval packs for prospect-specific walk-in and follow-up messages.
  - `working/proposals.csv`: Structured proposal register.
  - `working/proposals/`: Generated draft proposal documents.
  - `working/clients.csv`: Structured client register for active and past clients.
  - `working/revenue.csv`: Monthly revenue and MRR tracking.
  - `working/kpi_history.csv`: Weekly KPI snapshots produced by the growth retrospective.
  - `working/RETROSPECTIVE_SYSTEM.md`: Self-improvement and evidence rules for weekly reviews.
  - `working/CLIENT_DELIVERY.md`: Delivery, onboarding, go-live, and maintenance operating system for converted clients.
  - `working/AUTOMATIONS.md`: Active recurring jobs and their safety boundaries.
  - `working/OPERATOR_MANUAL.md`: Practical weekly operating manual for the growth engine.
  - `working/ceo_reports/`: Generated supervised CEO-loop operating reports.
  - `working/OUTREACH_CHAT_IMPORT.md`: Imported context from the "Review outreach scripts" Codex chat, including the outreach playbook pointer and reply-monitor details.
- **`protocols/`**:
  - `permissions.md`: Command allowlists and git protection rules.
  - `outreach-safety.md`: Supervised-autonomy rules for prospect research, cold/warm outreach, follow-up, compliance, and self-improvement loops.
- **`commands/`**:
  - `update-socials.md`: `/update-socials` instruction schema.
  - `build-all.md`: `/build-all` instruction schema.
  - `verify-integrity.md`: `/verify-integrity` audit loop schema.
  - `audit-prospects.md`: `/audit-prospects` triage loop schema.
  - `prospect-scan.md`: `/prospect-scan` instruction schema for finding and scoring local prospects without contacting them.
  - `intake-review.md`: `/intake-review` instruction schema for reviewing staged candidates before promotion.
  - `verify-intake-evidence.md`: `/verify-intake-evidence` instruction schema for checking staged social, website, and source evidence.
  - `intake-opportunity-briefs.md`: `/intake-opportunity-briefs` instruction schema for private website opportunity briefs before promotion.
  - `approval-queue.md`: `/approval-queue` instruction schema for explicit Daniel decision gates.
  - `promote-intake.md`: `/promote-intake` instruction schema for approval-gated promotion into the main prospect tracker.
  - `mockup-briefs.md`: `/mockup-briefs` instruction schema for generating website build briefs.
  - `outreach-week.md`: `/outreach-week` instruction schema for weekly planning, mockups, approval-gated outreach, and review.
  - `outreach-drafts.md`: `/outreach-drafts` instruction schema for generating approval-gated prospect message packs.
  - `client-delivery.md`: `/client-delivery` instruction schema for onboarding, go-live, and maintenance planning.
  - `proposal-admin.md`: `/proposal-admin` instruction schema for draft proposals and local proposal tracking.
  - `growth-dashboard.md`: `/growth-dashboard` instruction schema for generating the local CEO dashboard.
  - `growth-ceo-loop.md`: `/growth-ceo-loop` instruction schema for the safe supervised operating loop.
  - `growth-retrospective.md`: `/growth-retrospective` instruction schema for KPI snapshots and self-improvement review.
  - `growth-engine-audit.md`: `/growth-engine-audit` instruction schema for full engine health checks.
- **`skills/`**:
  - `growth-engine/`: Scores and validates `.agent/memory/working/prospects.csv`, produces weekly action reports, generates the local CEO dashboard, writes retrospectives, and audits engine health.
  - `audit-prospects/`: Triage script for existing mockup quality gaps.
  - `verify-integrity/`: Integrity audit for active website mockups.
- **`.github/ISSUE_TEMPLATE/`**:
  - `prospect.md`: GitHub issue template for local business prospects.
  - `mockup-build.md`: GitHub issue template for website mockup work.
  - `outreach-approval.md`: GitHub issue template for approval-gated outbound messages.
  - `client-delivery.md`: GitHub issue template for onboarding, go-live, and maintenance work.

## Harness Adapters
- **Antigravity**: Wired via `ANTIGRAVITY.md` in the workspace root.
- **Claude Code**: Wired via `CLAUDE.md` in the workspace root.
