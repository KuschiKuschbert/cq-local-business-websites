#!/usr/bin/env python3
import os
from common import clean, p, rel, read_csv, today, write_csv

FIELDS = [
    "date",
    "rank",
    "business",
    "trigger_decision",
    "step_order",
    "step",
    "owner",
    "safe_command_or_action",
    "expected_artifact",
    "blocked_until",
    "safety_gate",
    "notes",
]

cockpit = read_csv(p("decision_cockpit.csv"))
rows = []


def add(base, step_order, step, owner, action, artifact, blocked_until, gate, notes):
    rows.append({
        "date": today(),
        "rank": clean(base.get("rank"), "999"),
        "business": clean(base.get("business")),
        "trigger_decision": "promotion approve recorded by Daniel",
        "step_order": str(step_order),
        "step": step,
        "owner": owner,
        "safe_command_or_action": action,
        "expected_artifact": artifact,
        "blocked_until": blocked_until,
        "safety_gate": gate,
        "notes": notes,
    })


for item in cockpit:
    business = clean(item.get("business"))
    add(
        item,
        1,
        "Record local promotion decision",
        "Daniel",
        clean(item.get("approve_command")),
        ".agent/memory/working/approval_decisions.csv",
        "Daniel chooses approve after reviewing evidence.",
        "Decision recording is not promotion or outreach approval.",
        "Reject and hold commands remain available in the decision cockpit.",
    )
    add(
        item,
        2,
        "Promote approved staged candidate",
        "Codex",
        clean(item.get("after_approve")),
        ".agent/memory/working/prospects.csv and .agent/memory/working/promotion_log.csv",
        "Step 1 exists as a recorded approval decision.",
        "Promotion is not outreach approval and does not contact the business.",
        "Promotion script enforces the recorded approval decision before editing prospects.csv.",
    )
    add(
        item,
        3,
        "Regenerate local prospect artifacts",
        "Codex",
        "python3 .agent/skills/growth-engine/scripts/run-ceo-loop.py",
        "mockup_briefs.csv, delivery_readiness.csv, outreach_drafts.csv, contact_compliance.csv, pre_send_readiness.csv",
        "Step 2 has promoted the candidate into prospects.csv.",
        "Local generation only; no send, publish, hosting, billing, or remote GitHub write.",
        "This refreshes safe planning artifacts after promotion.",
    )
    add(
        item,
        4,
        "Review contact compliance and pre-send gates",
        "Daniel",
        "Review .agent/memory/working/contact_compliance.csv and .agent/memory/working/pre_send_readiness.csv",
        ".agent/memory/working/pre_send_readiness.csv",
        "Contact basis, sender identity, opt-out, exact copy, and outreach approval are documented.",
        "No email, SMS, DM, forms, social posts, calls, or scheduling without exact approval.",
        "The default promoted contact basis is none documented, so outreach should remain blocked until corrected.",
    )
    add(
        item,
        5,
        "Optional local GitHub issue review",
        "Daniel",
        f"Review {clean(item.get('github_issue_draft'), '-')}",
        ".agent/memory/working/github_issue_drafts/",
        "Daniel explicitly approves exact remote issue creation workflow.",
        "No remote GitHub writes from this workflow map.",
        f"GitHub readiness for {business}: {clean(item.get('github_status'), 'not-generated')}.",
    )

rows.sort(key=lambda row: (
    int(row["rank"]) if row["rank"].isdigit() else 999,
    int(row["step_order"]) if row["step_order"].isdigit() else 999,
))
write_csv(p("post_approval_workflow.csv"), rows, FIELDS)

os.makedirs(p("post_approval_workflow"), exist_ok=True)
path = p("post_approval_workflow", f"{today()}.md")
with open(path, "w", encoding="utf-8") as handle:
    handle.write("# Post-Approval Workflow\n\n")
    handle.write(f"- Date: {today()}\n")
    handle.write("- Purpose: map the safe sequence after Daniel records a promotion approval.\n")
    handle.write("- Safety: advisory workflow only. It does not approve promotion, outreach, publishing, billing, hosting, or remote GitHub writes.\n\n")
    current = None
    if not rows:
        handle.write("No pending promotion decisions are available for workflow mapping.\n")
    for row in rows:
        if row["business"] != current:
            current = row["business"]
            handle.write(f"## {current}\n\n")
        handle.write(f"{row['step_order']}. {row['step']} ({row['owner']})\n")
        handle.write(f"   - Action: `{row['safe_command_or_action']}`\n")
        handle.write(f"   - Artifact: {row['expected_artifact']}\n")
        handle.write(f"   - Blocked until: {row['blocked_until']}\n")
        handle.write(f"   - Gate: {row['safety_gate']}\n\n")

print(rel(path))
