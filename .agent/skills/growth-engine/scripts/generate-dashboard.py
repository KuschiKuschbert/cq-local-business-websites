#!/usr/bin/env python3
import os
from common import p, read_csv, rel

intake = read_csv(p("prospect_intake.csv"))
verification = read_csv(p("intake_verification.csv"))
briefs = read_csv(p("intake_opportunity_briefs.csv"))
approvals = read_csv(p("approval_queue.csv"))
prospects = read_csv(p("prospects.csv"))
os.makedirs(p("dashboard"), exist_ok=True)
path = p("dashboard", "index.html")
with open(path, "w", encoding="utf-8") as handle:
    handle.write("<!doctype html><html><head><meta charset='utf-8'><title>Cap Coast Creative Growth Dashboard</title>")
    handle.write("<style>body{font-family:Arial,sans-serif;background:#101418;color:#edf3f1;padding:24px}section{border:1px solid #314047;border-radius:8px;padding:16px;margin:12px 0}td,th{padding:8px;border-bottom:1px solid #314047;text-align:left}</style></head><body>")
    handle.write("<h1>Cap Coast Creative Growth Dashboard</h1>")
    handle.write(f"<section><h2>Snapshot</h2><p>Intake: {len(intake)} | Evidence ready: {sum(1 for r in verification if r.get('readiness') == 'promotion-review-ready')} | Opportunity briefs: {len(briefs)} | Pending approvals: {len(approvals)} | Prospects: {len(prospects)}</p></section>")
    handle.write("<section><h2>Approval Queue</h2><table><tr><th>Type</th><th>Business</th><th>Decision</th></tr>")
    for row in approvals:
        handle.write(f"<tr><td>{row.get('approval_type')}</td><td>{row.get('business')}</td><td>{row.get('requested_decision')}</td></tr>")
    handle.write("</table></section><p>Research and planning only. Outbound contact needs approval.</p></body></html>")
print(rel(path))
