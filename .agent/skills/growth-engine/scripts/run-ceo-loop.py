#!/usr/bin/env python3
import os
import subprocess
import sys
from common import p, read_csv, rel

STEPS = [
    "review-intake.py",
    "verify-intake-evidence.py",
    "generate-intake-opportunity-briefs.py",
    "generate-approval-queue.py",
    "run-pipeline.py",
    "generate-mockup-briefs.py",
    "generate-outreach-drafts.py",
    "generate-proposals.py",
    "generate-retrospective.py --append-kpi",
    "generate-dashboard.py",
    "audit-engine.py",
]

base = os.path.dirname(__file__)
results = []
for step in STEPS:
    parts = step.split()
    cmd = [sys.executable, os.path.join(base, parts[0])] + parts[1:]
    done = subprocess.run(cmd, cwd=os.path.abspath(os.path.join(base, "../../../..")), text=True, capture_output=True)
    results.append((step, done.returncode, (done.stdout or done.stderr).strip()))

os.makedirs(p("ceo_reports"), exist_ok=True)
path = p("ceo_reports", "2026-06-16.md")
intake = read_csv(p("prospect_intake.csv"))
verify = read_csv(p("intake_verification.csv"))
approvals = read_csv(p("approval_queue.csv"))
prospects = read_csv(p("prospects.csv"))
with open(path, "w", encoding="utf-8") as handle:
    handle.write("# Cap Coast Creative CEO Loop\n\n")
    handle.write(f"- Status: {'FAIL' if any(code for _, code, _ in results) else 'PASS'}\n")
    handle.write("- Safety: no outreach sent; local reports and tracker files only.\n\n")
    handle.write("## Operating Snapshot\n\n")
    handle.write(f"- Intake candidates: {len(intake)}\n")
    handle.write(f"- Evidence-ready candidates: {sum(1 for row in verify if row.get('readiness') == 'promotion-review-ready')}\n")
    handle.write(f"- Pending approvals: {len(approvals)}\n")
    handle.write(f"- Approved prospects: {len(prospects)}\n\n")
    handle.write("## Step Results\n\n")
    for step, code, output in results:
        handle.write(f"- {step}: {'PASS' if code == 0 else 'FAIL'} - {output}\n")
    handle.write("\n## Safety Gate\n\nPromotion is not outreach approval. Outreach needs separate explicit approval.\n")
print(rel(path))
raise SystemExit(1 if any(code for _, code, _ in results) else 0)
