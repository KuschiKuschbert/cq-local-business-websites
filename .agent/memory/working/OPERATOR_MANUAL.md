# Operator Manual

Run `python3 .agent/skills/growth-engine/scripts/run-ceo-loop.py` for the supervised local operating cycle.

Use the approval queue before any action that crosses a safety gate.

## Daily Control Rhythm

1. Run the CEO loop.
2. Read `.agent/memory/working/operating_reviews/YYYY-MM-DD.md`.
3. Review `.agent/memory/working/weekly_plan.csv`.
4. Review `.agent/memory/working/improvement_scorecard.csv`.
5. Review `.agent/memory/working/capability_matrix.csv`.
6. Review `.agent/memory/working/safety_invariants.csv`.
7. Review `.agent/memory/working/action_permissions.csv` before any operational step.
8. Review `.agent/memory/working/source_plan.csv` for new research lanes.
9. Review `.agent/memory/working/source_quality_map.csv` for targeted source routes.
10. Review `.agent/memory/working/research_controller.csv` for the next safe prospecting lane.
11. Log each research pass with `python3 .agent/skills/growth-engine/scripts/log-research-attempt.py`.
12. Capture only strongly sourced candidates with `python3 .agent/skills/growth-engine/scripts/capture-intake-candidate.py`.
13. Review `.agent/memory/working/priority_board.csv`.
14. Review `.agent/memory/working/offer_strategy.csv`.
15. Review `.agent/memory/working/revenue_forecast.csv`.
16. Review `.agent/memory/working/approval_queue.csv` and `.agent/memory/working/approval_packets.csv`.
17. Review `.agent/memory/working/github_issue_drafts.csv`.
18. Review `.agent/memory/working/github_execution_plan.csv` without running it.
19. Record approval decisions in `.agent/memory/working/approval_decisions.csv`.
20. Approve promotions only when the evidence is strong enough.
21. Review `.agent/memory/working/delivery_readiness.csv` after promotion.
22. Review `.agent/memory/working/contact_compliance.csv`.
23. Approve outreach separately, after a promoted prospect has a draft, lawful contact basis, sender ID, and clear opt-out path.

## Do Not Cross Without Approval

- Promote staged candidates into `prospects.csv`.
- Create remote GitHub issues from local drafts.
- Publish private concepts.
- Send email, SMS, DMs, form submissions, social posts, or make calls.
- Change domains, hosting, billing, invoices, or client-facing promises.
