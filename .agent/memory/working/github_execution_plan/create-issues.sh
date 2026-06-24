#!/usr/bin/env bash
set -euo pipefail

# Generated local plan only. Do not run without explicit Daniel approval.

# Ella Anderson beauty
# Requires explicit approval before execution.
gh issue create --title '[Prospect Review] Ella Anderson beauty' --body-file .agent/memory/working/github_issue_drafts/ella-anderson-beauty.md --label 'prospect, approval-needed, safety-gated'

# Her. Hair
# Requires explicit approval before execution.
gh issue create --title '[Prospect Review] Her. Hair' --body-file .agent/memory/working/github_issue_drafts/her-hair.md --label 'prospect, approval-needed, safety-gated'

# CQ Gutter Cleaning
# Requires explicit approval before execution.
gh issue create --title '[Prospect Review] CQ Gutter Cleaning' --body-file .agent/memory/working/github_issue_drafts/cq-gutter-cleaning.md --label 'prospect, approval-needed, safety-gated'
