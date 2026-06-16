#!/usr/bin/env python3
import os
from common import clean, p, read_csv, rel, slug, today, write_csv

FIELDS = ["date", "business", "approval_type", "issue_title", "labels", "draft_path", "safe_next_step", "notes"]

approvals = read_csv(p("approval_queue.csv"))
verify = {row.get("business"): row for row in read_csv(p("intake_verification.csv"))}
intake = {row.get("business"): row for row in read_csv(p("prospect_intake.csv"))}

out_dir = p("github_issue_drafts")
os.makedirs(out_dir, exist_ok=True)

rows = []
for approval in approvals:
    business = clean(approval.get("business"), "Unknown business")
    approval_type = clean(approval.get("approval_type"), "approval")
    source_path = clean(approval.get("source_path"), "-")
    item = intake.get(business, {})
    check = verify.get(business, {})
    title = f"[Prospect Review] {business}"
    labels = "prospect, approval-needed, safety-gated"
    draft_path = os.path.join(out_dir, f"{slug(business)}.md")
    body = f"""# {title}

## Decision Needed

Approve or reject moving this staged candidate into `prospects.csv`.

## Candidate

- Business: {business}
- Region: {clean(item.get("region"))}
- Niche: {clean(item.get("niche"))}
- Approval type: {approval_type}
- Readiness: {clean(check.get("readiness"))}
- Source brief: `{source_path}`

## Evidence

- Socials: {clean(item.get("socials"))}
- Website: {clean(item.get("website"))}
- Source URLs: {clean(item.get("source_urls"))}
- Social status: {clean(check.get("social_status"))}
- Website status: {clean(check.get("website_status"))}
- Source status: {clean(check.get("source_status"))}

## Opportunity

{clean(item.get("observed_website_gap"))}

Suggested hook: {clean(item.get("proposed_hook"))}

## Safety Gate

- Promotion is not outreach approval.
- Do not send email, SMS, DM, form submission, social post, or make calls from this issue.
- Outreach requires a separate explicit Daniel approval after the prospect is promoted.

## Safe Command After Approval

```bash
{clean(approval.get("safe_command"))}
```
"""
    with open(draft_path, "w", encoding="utf-8") as handle:
        handle.write(body)
    rows.append({
        "date": today(),
        "business": business,
        "approval_type": approval_type,
        "issue_title": title,
        "labels": labels,
        "draft_path": rel(draft_path),
        "safe_next_step": "Review draft and create GitHub issue manually or through approved GitHub workflow.",
        "notes": "Local issue draft only; no GitHub issue created.",
    })

write_csv(p("github_issue_drafts.csv"), rows, FIELDS)
if rows:
    print("\n".join(row["draft_path"] for row in rows))
else:
    print("No pending approvals for GitHub issue draft generation.")
