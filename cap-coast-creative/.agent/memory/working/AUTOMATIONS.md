# Automations

- `cap-coast-prospect-scan`: active Codex cron automation, weekdays 8:00 AM, research-only. It works the highest-ranked lane from `research_controller.csv`, logs checked sources, and stages candidates only through `capture-intake-candidate.py` when public evidence is strong.
- `cap-coast-source-plan`: weekly Monday before scanning, local search-lane planning only.
- `cap-coast-ceo-loop`: operator-triggered or scheduled, local reports only.
- `cap-coast-weekly-plan`: generated inside the CEO loop, planning only.
- `cap-coast-improvement-scorecard`: generated inside the CEO loop, diagnostics only.
- `cap-coast-approval-decisions`: records human approve/reject/hold decisions only.
- `cap-coast-github-execution-plan`: prepares local GitHub commands only; does not run them.
- `cap-coast-delivery-readiness`: prepares internal delivery plans only.
- `cap-coast-contact-compliance`: checks contact basis and opt-out readiness only.
- `cap-coast-capability-matrix`: audits readiness against the full business-engine objective.
- `cap-coast-safety-invariants`: hard-stop logical safety checks across tracker files.
- `cap-coast-operating-review`: generated inside the CEO loop, safety/control board only.

Automations must not contact prospects, submit forms, send messages, or promote candidates without approval.
