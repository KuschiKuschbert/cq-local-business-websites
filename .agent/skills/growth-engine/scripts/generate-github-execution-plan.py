#!/usr/bin/env python3
import os
import shlex
from common import clean, p, read_csv, rel, today, write_csv

FIELDS = ["date", "business", "issue_title", "labels", "draft_path", "command_path", "approval_status", "safe_next_action", "notes"]

drafts = read_csv(p("github_issue_drafts.csv"))
out_dir = p("github_execution_plan")
os.makedirs(out_dir, exist_ok=True)
commands_path = os.path.join(out_dir, "create-issues.sh")

rows = []
commands = [
    "#!/usr/bin/env bash",
    "set -euo pipefail",
    "",
    "# Generated local plan only. Do not run without explicit Daniel approval.",
]
for draft in drafts:
    business = clean(draft.get("business"))
    title = clean(draft.get("issue_title"))
    labels = clean(draft.get("labels"))
    body_file = clean(draft.get("draft_path"))
    command = " ".join([
        "gh", "issue", "create",
        "--title", shlex.quote(title),
        "--body-file", shlex.quote(body_file),
        "--label", shlex.quote(labels),
    ])
    commands.append("")
    commands.append(f"# {business}")
    commands.append(f"# Requires explicit approval before execution.")
    commands.append(command)
    rows.append({
        "date": today(),
        "business": business,
        "issue_title": title,
        "labels": labels,
        "draft_path": body_file,
        "command_path": rel(commands_path),
        "approval_status": "not-approved-not-run",
        "safe_next_action": "Daniel may approve exact issue creation; until then this remains a local plan.",
        "notes": "No GitHub issue created by this generator.",
    })

with open(commands_path, "w", encoding="utf-8") as handle:
    handle.write("\n".join(commands) + "\n")

write_csv(p("github_execution_plan.csv"), rows, FIELDS)

report = os.path.join(out_dir, f"{today()}.md")
with open(report, "w", encoding="utf-8") as handle:
    handle.write("# GitHub Execution Plan\n\n")
    handle.write(f"- Date: {today()}\n")
    handle.write(f"- Planned issue creates: {len(rows)}\n")
    handle.write("- Safety: no GitHub commands were executed.\n\n")
    handle.write(f"- Command artifact: `{rel(commands_path)}`\n\n")
    for row in rows:
        handle.write(f"- {row['business']}: {row['issue_title']} / {row['approval_status']}\n")

print(rel(report))
