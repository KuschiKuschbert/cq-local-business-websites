# `/safety-invariants`

Run `python3 .agent/skills/growth-engine/scripts/validate-safety-invariants.py` to validate cross-file safety rules for the business engine.

This command fails if prospects lack recorded approval, outreach lacks approval evidence, GitHub execution plans are marked runnable, or draft/delivery/compliance rows exist without approved prospects.
