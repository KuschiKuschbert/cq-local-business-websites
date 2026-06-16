# Project Instructions (Antigravity)

This project uses the **agentic-stack** portable brain layout. All memory, skills, and protocols live in the `.agent/` directory.

## Core Rules & Context
1. Read `.agent/AGENTS.md` - it maps our stack structure.
2. Read `.agent/memory/personal/PREFERENCES.md` - defines styling rules, business logic, and coding standards.
3. Read `.agent/memory/semantic/LESSONS.md` - outlines verified guidelines for plumbing, catering, excavation, and pest sites.
4. Read `.agent/protocols/permissions.md` - safety guidelines and allowlists for commands/scripts.

## Slash Commands (Session-Scoped Loops)
We have custom loop-able operations defined in `.agent/commands/`. You can trigger them to manage the codebase:
- `/update-socials` - Run the python script to sync social links in footers.
- `/build-all` - Compile and verify the static distribution of all websites.
- `/verify-integrity` - Run local quality check on HTML, CSS, assets, and SEO metadata.
- `/audit-prospects` - Scan for missing assets or components across directories.
- `/prospect-scan` - Research and score new local business prospects without contacting them.
- `/intake-review` - Review staged prospect candidates before approval for the main tracker.
- `/verify-intake-evidence` - Check whether staged candidates have verified social, website, and source evidence.
- `/intake-opportunity-briefs` - Generate private website opportunity briefs for evidence-ready staged candidates.
- `/approval-queue` - Generate explicit Daniel approval gates for promotion, outreach, proposal, and publishing decisions.
- `/promote-intake` - Promote one Daniel-approved staged candidate into the main prospect tracker.
- `/mockup-briefs` - Generate website mockup build briefs for eligible prospects.
- `/outreach-week` - Plan the weekly prospecting, mockup, outreach, follow-up, and review cycle with approval gates.
- `/outreach-drafts` - Generate approval-gated walk-in and follow-up draft packs.
- `/client-delivery` - Plan onboarding, go-live, and maintenance work after a prospect becomes a client.
- `/proposal-admin` - Generate draft proposals and update local proposal tracking.
- `/growth-dashboard` - Generate the local Cap Coast Creative CEO dashboard.
- `/growth-ceo-loop` - Run the supervised CEO operating loop and write a local executive report.
- `/growth-retrospective` - Generate weekly KPIs, proposed lessons, and next experiment.
- `/growth-engine-audit` - Verify required files, schemas, scripts, command wiring, and safety gates.

## Outreach & Autonomy Rules
- Read `.agent/protocols/outreach-safety.md` before any prospecting or outreach work.
- The agent may research, score, draft, plan, track, and improve the pipeline autonomously.
- The agent must not send emails, SMS, DMs, contact-form submissions, social posts, or other outbound messages without explicit approval.
- Track prospect status in `.agent/memory/working/PROSPECT_PIPELINE.md`.
- Stage uncertain candidates in `.agent/memory/working/prospect_intake.csv` until they are approved for the main tracker.
- Review staged candidates with `python3 .agent/skills/growth-engine/scripts/review-intake.py`.
- Verify staged candidate evidence with `python3 .agent/skills/growth-engine/scripts/verify-intake-evidence.py`.
- Generate private opportunity briefs with `python3 .agent/skills/growth-engine/scripts/generate-intake-opportunity-briefs.py`.
- Generate approval gates with `python3 .agent/skills/growth-engine/scripts/generate-approval-queue.py`.
- Promote approved staged candidates with `python3 .agent/skills/growth-engine/scripts/promote-intake.py --business "Name" --approved-by "Daniel"`; promotion is not outreach approval.
- Use `.agent/memory/working/prospects.csv` as the structured prospect register and validate it with `bash .agent/skills/growth-engine/scripts/assert-state.sh`.
- Generate mockup briefs with `python3 .agent/skills/growth-engine/scripts/generate-mockup-briefs.py`.
- Track outreach/reply/opt-out events in `.agent/memory/working/outreach_log.csv`.
- Use `.agent/memory/working/CLIENT_DELIVERY.md` for proposal, onboarding, go-live, and maintenance workflows.
- Track recurring research jobs in `.agent/memory/working/AUTOMATIONS.md`.
- Generate the local dashboard with `python3 .agent/skills/growth-engine/scripts/generate-dashboard.py`.
- Run the supervised CEO loop with `python3 .agent/skills/growth-engine/scripts/run-ceo-loop.py`.
- Generate approval-gated outreach packs with `python3 .agent/skills/growth-engine/scripts/generate-outreach-drafts.py`.
- Generate draft proposals with `python3 .agent/skills/growth-engine/scripts/generate-proposals.py`.
- Generate the weekly retrospective with `python3 .agent/skills/growth-engine/scripts/generate-retrospective.py --append-kpi`.
- Audit the full engine with `python3 .agent/skills/growth-engine/scripts/audit-engine.py`.

## Visual guidelines & Design Aesthetics
- Use premium Vanilla CSS (strict dark/light systems, harmonious HSL palettes).
- Use Outfit and Inter fonts.
- Avoid default browser components or generic colors.
- Maintain high-trust hooks (On-Time Guarantees, Police-Cleared Checkboxes) tailored to the local Central QLD target market.
