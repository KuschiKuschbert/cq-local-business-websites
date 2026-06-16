#!/usr/bin/env python3
import csv
import os
import stat
import sys
from common import ROOT

REQUIRED = [
    ".agent/protocols/outreach-safety.md",
    ".agent/memory/working/PROSPECT_PIPELINE.md",
    ".agent/memory/working/CLIENT_DELIVERY.md",
    ".agent/memory/working/RETROSPECTIVE_SYSTEM.md",
    ".agent/memory/working/AUTOMATIONS.md",
    ".agent/memory/working/prospect_intake.csv",
    ".agent/memory/working/intake_review.csv",
    ".agent/memory/working/intake_verification.csv",
    ".agent/memory/working/intake_opportunity_briefs.csv",
    ".agent/memory/working/approval_queue.csv",
    ".agent/memory/working/prospects.csv",
    ".agent/memory/working/dashboard/index.html",
    ".agent/commands/growth-ceo-loop.md",
    ".agent/commands/approval-queue.md",
    ".agent/commands/promote-intake.md",
    ".github/ISSUE_TEMPLATE/outreach-approval.md",
]

SCRIPTS = [
    ".agent/skills/growth-engine/scripts/assert-state.sh",
    ".agent/skills/growth-engine/scripts/run-pipeline.py",
    ".agent/skills/growth-engine/scripts/review-intake.py",
    ".agent/skills/growth-engine/scripts/verify-intake-evidence.py",
    ".agent/skills/growth-engine/scripts/generate-intake-opportunity-briefs.py",
    ".agent/skills/growth-engine/scripts/generate-approval-queue.py",
    ".agent/skills/growth-engine/scripts/promote-intake.py",
    ".agent/skills/growth-engine/scripts/generate-dashboard.py",
    ".agent/skills/growth-engine/scripts/run-ceo-loop.py",
    ".agent/skills/growth-engine/scripts/audit-engine.py",
]

SCHEMAS = {
    ".agent/memory/working/prospect_intake.csv": ["business","region","niche","socials","website","source_urls","observed_social_signal","observed_website_gap","proposed_hook","notes"],
    ".agent/memory/working/intake_review.csv": ["date","business","region","niche","score","recommendation","missing_evidence","next_action","notes"],
    ".agent/memory/working/intake_verification.csv": ["date","business","social_status","website_status","source_status","readiness","next_action","notes"],
    ".agent/memory/working/intake_opportunity_briefs.csv": ["date","business","region","niche","readiness","brief_path","primary_opportunity","safe_next_step","notes"],
    ".agent/memory/working/approval_queue.csv": ["date","approval_type","business","priority","source_path","requested_decision","safe_command","blocked_until_approved","notes"],
}

errors = []
for rel in REQUIRED + SCRIPTS:
    if not os.path.exists(os.path.join(ROOT, rel)):
        errors.append(f"Missing required file: {rel}")
for rel, expected in SCHEMAS.items():
    with open(os.path.join(ROOT, rel), newline="", encoding="utf-8") as handle:
        header = next(csv.reader(handle), [])
    if header != expected:
        errors.append(f"CSV schema mismatch in {rel}")
for rel in SCRIPTS:
    full = os.path.join(ROOT, rel)
    if rel.endswith(".py"):
        with open(full, encoding="utf-8") as handle:
            if "python3" not in handle.readline():
                errors.append(f"Python script missing python3 shebang: {rel}")
    if rel.endswith(".sh") and not (os.stat(full).st_mode & stat.S_IXUSR):
        errors.append(f"Shell script is not executable: {rel}")
text = ""
for rel in [".agent/protocols/outreach-safety.md", ".agent/protocols/permissions.md"]:
    with open(os.path.join(ROOT, rel), encoding="utf-8") as handle:
        text += handle.read().lower()
for phrase in ["daniel", "do not send", "opt-out", "harvested"]:
    if phrase not in text:
        errors.append(f"Missing safety concept: {phrase}")
print("\nCap Coast Creative Engine Audit")
print("==============================")
if errors:
    print("Status: FAIL\n")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)
print("Status: PASS")
print("- Required files present")
print("- CSV schemas match")
print("- Scripts are shaped correctly")
print("- Safety concepts present")
