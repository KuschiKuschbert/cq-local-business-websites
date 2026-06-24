#!/usr/bin/env bash
set -euo pipefail

# Generated local plan only. Do not run without explicit Daniel approval.

# Yeppoon Community Market
# Requires explicit approval before execution.
gh issue create --title '[Prospect Review] Yeppoon Community Market' --body-file .agent/memory/working/github_issue_drafts/yeppoon-community-market.md --label 'prospect, approval-needed, safety-gated'

# CocoBrew Riverfront
# Requires explicit approval before execution.
gh issue create --title '[Prospect Review] CocoBrew Riverfront' --body-file .agent/memory/working/github_issue_drafts/cocobrew-riverfront.md --label 'prospect, approval-needed, safety-gated'

# CocoBrew Rockhampton
# Requires explicit approval before execution.
gh issue create --title '[Prospect Review] CocoBrew Rockhampton' --body-file .agent/memory/working/github_issue_drafts/cocobrew-rockhampton.md --label 'prospect, approval-needed, safety-gated'

# CocoBrew Express Yeppoon
# Requires explicit approval before execution.
gh issue create --title '[Prospect Review] CocoBrew Express Yeppoon' --body-file .agent/memory/working/github_issue_drafts/cocobrew-express-yeppoon.md --label 'prospect, approval-needed, safety-gated'

# Pine Beach Hotel
# Requires explicit approval before execution.
gh issue create --title '[Prospect Review] Pine Beach Hotel' --body-file .agent/memory/working/github_issue_drafts/pine-beach-hotel.md --label 'prospect, approval-needed, safety-gated'
