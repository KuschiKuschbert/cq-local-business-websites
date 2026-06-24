# `/growth-dashboard`

Run `python3 .agent/skills/growth-engine/scripts/generate-dashboard.py`.

For interactive local approval buttons, run:

`python3 .agent/skills/growth-engine/scripts/serve-dashboard.py`

Then open:

`http://127.0.0.1:8787/dashboard/index.html`

Dashboard approvals are local-only. Approving a lead records Daniel's promotion decision, promotes the staged candidate into `prospects.csv`, and regenerates local planning files. It does not send outreach, publish work, create invoices, change hosting, or write to remote GitHub.
