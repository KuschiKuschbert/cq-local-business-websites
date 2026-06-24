#!/usr/bin/env python3
import json
import os
from datetime import datetime
from html import escape

from common import p, read_csv, rel


def rows(name):
    return read_csv(p(name))


def count_where(items, key, value):
    return sum(1 for item in items if item.get(key) == value)


def first_value(items, key, fallback="0"):
    return items[0].get(key, fallback) if items else fallback


def working_link(path):
    value = (path or "").strip()
    if not value or value == "-":
        return ""
    prefix = ".agent/memory/working/"
    if value.startswith(prefix):
        return "../" + value[len(prefix):]
    return value


def js_safe(value):
    return json.dumps(value, ensure_ascii=True).replace("</", "<\\/")


data = {
    "generatedAt": datetime.now().strftime("%Y-%m-%d %H:%M"),
    "intake": rows("prospect_intake.csv"),
    "verification": rows("intake_verification.csv"),
    "briefs": rows("intake_opportunity_briefs.csv"),
    "approvals": rows("approval_queue.csv"),
    "approvalDecisions": rows("approval_decision_summary.csv"),
    "approvalInbox": rows("approval_decision_inbox.csv"),
    "decisionCockpit": rows("decision_cockpit.csv"),
    "postApproval": rows("post_approval_workflow.csv"),
    "approvalPackets": rows("approval_packets.csv"),
    "revenueForecast": rows("revenue_forecast.csv"),
    "objectiveCoverage": rows("objective_coverage_audit.csv"),
    "prospects": rows("prospects.csv"),
    "concepts": rows("private_concepts.csv"),
    "issueDrafts": rows("github_issue_drafts.csv"),
    "githubPlan": rows("github_execution_plan.csv"),
    "githubReadiness": rows("github_readiness_audit.csv"),
    "operating": rows("operating_review.csv"),
    "priority": rows("priority_board.csv"),
    "leadQuality": rows("lead_quality_map.csv"),
    "strategy": rows("offer_strategy.csv"),
    "drafts": rows("outreach_drafts.csv"),
    "playbooks": rows("outreach_playbook_library.csv"),
    "delivery": rows("delivery_readiness.csv"),
    "compliance": rows("contact_compliance.csv"),
    "preSend": rows("pre_send_readiness.csv"),
    "proposals": rows("proposals.csv"),
    "sourcePlan": rows("source_plan.csv"),
    "researchController": rows("research_controller.csv"),
    "regionalHeatmap": rows("regional_coverage_heatmap.csv"),
    "sourceQuality": rows("source_quality_map.csv"),
    "researchExperiments": rows("research_experiments.csv"),
    "sourcePivots": rows("source_pivot_plan.csv"),
    "researchSuppression": rows("research_suppression_list.csv"),
    "councilRegistry": rows("council_registry.csv"),
    "councilDebates": rows("council_debates.csv"),
    "councilQuality": rows("council_quality_audit.csv"),
    "councilBrief": rows("council_ceo_brief.csv"),
    "automationStatus": rows("automation_status.csv"),
    "actionPermissions": rows("action_permissions.csv"),
    "councilDecisionGates": rows("council_decision_gates.csv"),
    "weeklyPlan": rows("weekly_plan.csv"),
    "scorecard": rows("improvement_scorecard.csv"),
    "learningQueue": rows("learning_queue.csv"),
    "operatorQueue": rows("operator_action_queue.csv"),
    "capabilities": rows("capability_matrix.csv"),
    "safetyInvariants": rows("safety_invariants.csv"),
    "research": rows("research_queue.csv"),
    "attempts": rows("research_attempts.csv"),
}

evidence_ready = count_where(data["verification"], "readiness", "promotion-review-ready")
safety_pass = count_where(data["safetyInvariants"], "status", "pass")
blocked_actions = sum(1 for row in data["operatorQueue"] if "blocked" in row.get("status", ""))
pending_decisions = len(data["approvalInbox"])
held_promotions = sum(1 for row in data["approvalDecisions"] if row.get("decision") == "hold")
strong_leads = sum(1 for row in data["leadQuality"] if row.get("quality_band") in {"strong lead", "review-ready"})
needs_proof = sum(1 for row in data["leadQuality"] if row.get("quality_band") == "needs proof")
cooled_down = sum(1 for row in data["leadQuality"] if row.get("quality_band") == "cooled down")

summary = {
    "intake": len(data["intake"]),
    "evidenceReady": evidence_ready,
    "pendingApprovals": pending_decisions,
    "heldPromotions": held_promotions,
    "strongLeads": strong_leads,
    "needsProof": needs_proof,
    "cooledDown": cooled_down,
    "decisionInbox": pending_decisions,
    "prospects": len(data["prospects"]),
    "privateConcepts": len(data["concepts"]),
    "researchAttempts": len(data["attempts"]),
    "researchLanes": len(data["regionalHeatmap"]),
    "safetyPass": safety_pass,
    "safetyTotal": len(data["safetyInvariants"]),
    "operatorActions": len(data["operatorQueue"]),
    "blockedActions": blocked_actions,
    "weightedMrr": first_value(
        [row for row in data["revenueForecast"] if row.get("stage") == "promotion-review"],
        "weighted_mrr",
        "$0/mo",
    ),
    "grossReviewMrr": first_value(
        [row for row in data["revenueForecast"] if row.get("stage") == "promotion-review"],
        "gross_monthly_fee",
        "$0/mo",
    ),
}

for collection in [
    "approvalInbox",
    "decisionCockpit",
    "approvalPackets",
    "concepts",
    "issueDrafts",
    "githubPlan",
    "githubReadiness",
]:
    for row in data[collection]:
        for key, value in list(row.items()):
            if key.endswith("_path") or key in {"evidence_path", "packet_path", "private_concept", "draft_path", "concept_path", "command_path"}:
                row[key + "_href"] = working_link(value)

dashboard = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Cap Coast Creative CEO Cockpit</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@500;600;700;800&family=Outfit:wght@600;700;800&display=swap');
    :root {{
      color-scheme: dark;
      --bg: #101315;
      --panel: #171d20;
      --panel-2: #1e262a;
      --line: #314047;
      --muted: #9fb0ae;
      --text: #edf4f1;
      --teal: #2dd4bf;
      --blue: #60a5fa;
      --amber: #f4b860;
      --coral: #ff7a66;
      --green: #7dd87d;
      --red: #fb7185;
      --shadow: rgba(0, 0, 0, .25);
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font-family: Inter, Arial, sans-serif;
      line-height: 1.45;
    }}
    button, input {{ font: inherit; }}
    .shell {{
      display: grid;
      grid-template-columns: 252px minmax(0, 1fr);
      min-height: 100vh;
    }}
    .sidebar {{
      position: sticky;
      top: 0;
      height: 100vh;
      padding: 20px 16px;
      border-right: 1px solid var(--line);
      background: #121719;
      overflow-y: auto;
    }}
    .brand {{
      display: flex;
      align-items: center;
      gap: 10px;
      min-height: 48px;
      margin-bottom: 18px;
    }}
    .brand-mark {{
      width: 38px;
      height: 38px;
      border-radius: 8px;
      display: grid;
      place-items: center;
      background: #203139;
      color: var(--teal);
      font-weight: 800;
      box-shadow: inset 0 0 0 1px rgba(45, 212, 191, .25);
    }}
    .brand strong {{
      display: block;
      font-family: Outfit, Inter, sans-serif;
      font-size: 1rem;
    }}
    .brand span {{
      color: var(--muted);
      font-size: .78rem;
    }}
    .nav {{
      display: grid;
      gap: 6px;
    }}
    .tab-btn {{
      border: 0;
      border-radius: 8px;
      color: var(--muted);
      background: transparent;
      padding: 10px 12px;
      text-align: left;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 10px;
      min-height: 40px;
    }}
    .tab-btn:hover {{ background: #1a2225; color: var(--text); }}
    .tab-btn.active {{
      background: #213039;
      color: var(--text);
      box-shadow: inset 3px 0 0 var(--teal);
    }}
    .dot {{
      width: 8px;
      height: 8px;
      border-radius: 99px;
      background: var(--blue);
      flex: 0 0 auto;
    }}
    .dot.approvals {{ background: var(--amber); }}
    .dot.pipeline {{ background: var(--teal); }}
    .dot.research {{ background: var(--blue); }}
    .dot.safety {{ background: var(--green); }}
    .dot.councils {{ background: var(--coral); }}
    .dot.revenue {{ background: #c084fc; }}
    .dot.github {{ background: #94a3b8; }}
    main {{
      padding: 22px;
      max-width: 1480px;
      width: 100%;
      min-width: 0;
    }}
    .topbar {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) minmax(280px, 420px);
      gap: 18px;
      align-items: end;
      margin-bottom: 18px;
    }}
    h1, h2, h3 {{
      font-family: Outfit, Inter, sans-serif;
      letter-spacing: 0;
      margin: 0;
    }}
    h1 {{ font-size: 2.55rem; line-height: 1; }}
    .lede {{
      max-width: 780px;
      color: var(--muted);
      margin: 10px 0 0;
    }}
    .search-box {{
      display: grid;
      gap: 8px;
    }}
    .search-box label {{
      color: var(--muted);
      font-size: .78rem;
      text-transform: uppercase;
      letter-spacing: .08em;
    }}
    #searchInput {{
      width: 100%;
      min-height: 44px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #121719;
      color: var(--text);
      padding: 0 14px;
      outline: none;
    }}
    #searchInput:focus {{
      border-color: var(--teal);
      box-shadow: 0 0 0 3px rgba(45, 212, 191, .12);
    }}
    .cards {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
      gap: 12px;
      margin: 16px 0;
    }}
    .metric {{
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--panel);
      padding: 14px;
      min-height: 112px;
      box-shadow: 0 10px 30px var(--shadow);
    }}
    .metric .label {{
      color: var(--muted);
      font-size: .78rem;
      text-transform: uppercase;
      letter-spacing: .08em;
    }}
    .metric .value {{
      display: block;
      margin-top: 8px;
      font-family: Outfit, Inter, sans-serif;
      font-size: 2rem;
      line-height: 1;
    }}
    .metric .note {{
      display: block;
      margin-top: 8px;
      color: var(--muted);
      font-size: .86rem;
    }}
    .alert-strip {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 12px;
      align-items: center;
      border: 1px solid rgba(244, 184, 96, .35);
      border-radius: 8px;
      background: rgba(244, 184, 96, .08);
      padding: 12px 14px;
      margin: 14px 0;
    }}
    .alert-strip strong {{ color: var(--amber); }}
    .why-panel {{
      border: 1px solid rgba(45, 212, 191, .28);
      border-radius: 8px;
      background: linear-gradient(135deg, rgba(45, 212, 191, .08), rgba(96, 165, 250, .06));
      padding: 18px;
      box-shadow: 0 10px 30px var(--shadow);
      margin: 0 0 16px;
    }}
    .why-panel h2 {{ font-size: 1.28rem; margin-bottom: 8px; }}
    .why-panel p {{
      color: #dfe8e5;
      margin: 0;
      max-width: 980px;
    }}
    .why-flow {{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 10px;
      margin-top: 14px;
    }}
    .why-step {{
      border: 1px solid rgba(255, 255, 255, .08);
      border-radius: 8px;
      background: rgba(18, 23, 25, .78);
      padding: 12px;
    }}
    .why-step span {{
      display: inline-grid;
      place-items: center;
      width: 26px;
      height: 26px;
      border-radius: 8px;
      background: rgba(45, 212, 191, .12);
      color: var(--teal);
      font-weight: 800;
      margin-bottom: 8px;
    }}
    .why-step strong {{
      display: block;
      margin-bottom: 4px;
    }}
    .why-step small {{
      color: var(--muted);
      line-height: 1.35;
    }}
    .plain-panel {{
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--panel);
      padding: 16px;
      box-shadow: 0 10px 30px var(--shadow);
      margin-bottom: 14px;
    }}
    .plain-panel h2 {{ font-size: 1.18rem; margin-bottom: 8px; }}
    .plain-panel p {{ color: var(--muted); margin: 0; }}
    .plain-grid {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 12px;
      margin: 14px 0;
    }}
    .explain-card {{
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #121719;
      padding: 14px;
      min-height: 132px;
    }}
    .explain-card strong {{
      display: block;
      font-family: Outfit, Inter, sans-serif;
      font-size: 1.05rem;
      margin-bottom: 8px;
    }}
    .explain-card p {{
      color: var(--muted);
      margin: 0;
      font-size: .92rem;
    }}
    .step-list {{
      display: grid;
      gap: 10px;
    }}
    .step-card {{
      display: grid;
      grid-template-columns: auto minmax(0, 1fr);
      gap: 12px;
      align-items: start;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #121719;
      padding: 13px;
    }}
    .step-number {{
      width: 32px;
      height: 32px;
      border-radius: 8px;
      display: grid;
      place-items: center;
      background: #203139;
      color: var(--teal);
      font-weight: 800;
    }}
    .step-card strong {{
      display: block;
      margin-bottom: 4px;
    }}
    .step-card p {{
      color: var(--muted);
      margin: 0;
      font-size: .9rem;
    }}
    .owner-action {{
      border: 1px solid rgba(244, 184, 96, .35);
      background: rgba(244, 184, 96, .08);
    }}
    .owner-action .step-number {{
      background: rgba(244, 184, 96, .14);
      color: var(--amber);
    }}
    .pill {{
      display: inline-flex;
      align-items: center;
      min-height: 24px;
      border-radius: 999px;
      padding: 2px 9px;
      font-size: .76rem;
      font-weight: 800;
      border: 1px solid var(--line);
      color: var(--muted);
      white-space: nowrap;
    }}
    .pill.pass, .pill.ready, .pill.allowed-now, .pill.safe, .pill.i-can-do-this-now {{ color: var(--green); border-color: rgba(125, 216, 125, .35); background: rgba(125, 216, 125, .08); }}
    .pill.pending, .pill.planned, .pill.promotion-review {{ color: var(--amber); border-color: rgba(244, 184, 96, .35); background: rgba(244, 184, 96, .08); }}
    .pill.blocked, .pill.blocked-external-write, .pill.blocked-no-approved-prospects {{ color: var(--red); border-color: rgba(251, 113, 133, .35); background: rgba(251, 113, 133, .08); }}
    .pill.local {{ color: var(--blue); border-color: rgba(96, 165, 250, .35); background: rgba(96, 165, 250, .08); }}
    .tab-panel {{ display: none; }}
    .tab-panel.active {{ display: block; }}
    .section-grid {{
      display: grid;
      grid-template-columns: minmax(0, 1.15fr) minmax(320px, .85fr);
      gap: 14px;
      align-items: start;
    }}
    .panel {{
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--panel);
      overflow: hidden;
      margin-bottom: 14px;
      box-shadow: 0 10px 30px var(--shadow);
    }}
    .panel-head {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      padding: 14px 16px;
      border-bottom: 1px solid var(--line);
      background: var(--panel-2);
    }}
    .panel-head h2 {{ font-size: 1.05rem; }}
    .panel-body {{ padding: 14px 16px; }}
    .decision-list {{
      display: grid;
      gap: 12px;
    }}
    .decision-card {{
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #121719;
      padding: 14px;
    }}
    .decision-card h3 {{
      font-size: 1rem;
      margin-bottom: 8px;
    }}
    .decision-meta {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-bottom: 10px;
    }}
    .command-row {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 8px;
      margin-top: 8px;
    }}
    code {{
      display: block;
      overflow-x: auto;
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 8px;
      color: #dbeafe;
      background: #0d1113;
      font-size: .8rem;
      white-space: pre-wrap;
      overflow-wrap: anywhere;
    }}
    .copy-btn, .link-btn {{
      min-height: 36px;
      border: 1px solid var(--line);
      border-radius: 8px;
      color: var(--text);
      background: #1c2529;
      cursor: pointer;
      padding: 0 10px;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      font-weight: 800;
      font-size: .82rem;
      white-space: nowrap;
    }}
    .copy-btn:hover, .link-btn:hover {{ border-color: var(--teal); }}
    .link-chip-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
    }}
    .link-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: 12px;
    }}
    .link-card {{
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #121719;
      padding: 14px;
      min-height: 148px;
    }}
    .link-card h3 {{
      font-size: 1rem;
      margin: 0 0 4px;
    }}
    .link-card small {{
      color: var(--muted);
      display: block;
      margin-bottom: 10px;
    }}
    .link-group {{
      display: grid;
      gap: 8px;
    }}
    .link-group > div {{
      display: grid;
      grid-template-columns: 68px minmax(0, 1fr);
      gap: 8px;
      align-items: start;
    }}
    .link-label {{
      color: var(--muted);
      font-size: .72rem;
      font-weight: 800;
      letter-spacing: .07em;
      text-transform: uppercase;
      padding-top: 7px;
    }}
    .decision-actions {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 8px;
      margin: 12px 0 8px;
    }}
    .decision-btn {{
      min-height: 38px;
      border: 1px solid var(--line);
      border-radius: 8px;
      color: var(--text);
      background: #1c2529;
      cursor: pointer;
      padding: 0 10px;
      font-weight: 800;
    }}
    .decision-btn.approve {{ border-color: rgba(125, 216, 125, .38); background: rgba(125, 216, 125, .1); }}
    .decision-btn.hold {{ border-color: rgba(244, 184, 96, .38); background: rgba(244, 184, 96, .1); }}
    .decision-btn.reject {{ border-color: rgba(251, 113, 133, .38); background: rgba(251, 113, 133, .1); }}
    .decision-btn:disabled {{ cursor: wait; opacity: .68; }}
    .server-note {{
      color: var(--muted);
      font-size: .82rem;
      margin-top: 8px;
    }}
    .table-wrap {{
      overflow-x: auto;
      -webkit-overflow-scrolling: touch;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      min-width: 760px;
      table-layout: fixed;
    }}
    th, td {{
      padding: 10px 11px;
      border-bottom: 1px solid var(--line);
      text-align: left;
      vertical-align: top;
      font-size: .88rem;
      overflow-wrap: anywhere;
    }}
    th {{
      color: var(--muted);
      font-size: .72rem;
      letter-spacing: .07em;
      text-transform: uppercase;
      background: #151b1e;
    }}
    td {{ color: #dfe8e5; }}
    tr[data-hidden="true"] {{ display: none; }}
    .empty {{
      color: var(--muted);
      padding: 18px;
      border: 1px dashed var(--line);
      border-radius: 8px;
      background: #121719;
    }}
    .progress {{
      height: 8px;
      border-radius: 99px;
      overflow: hidden;
      background: #0d1113;
      border: 1px solid var(--line);
      margin-top: 8px;
    }}
    .progress span {{
      display: block;
      height: 100%;
      width: 0;
      background: linear-gradient(90deg, var(--teal), var(--blue));
    }}
    .footer-note {{
      color: var(--muted);
      font-size: .86rem;
      margin-top: 22px;
    }}
    @media (max-width: 1180px) {{
      .shell {{ grid-template-columns: 220px minmax(0, 1fr); }}
      .topbar {{ grid-template-columns: 1fr; align-items: stretch; }}
      h1 {{ font-size: 2.2rem; }}
    }}
    @media (max-width: 980px) {{
      .shell {{ grid-template-columns: 1fr; }}
      .sidebar {{
        position: sticky;
        z-index: 20;
        height: auto;
        top: 0;
        padding: 12px 14px;
        border-right: 0;
        border-bottom: 1px solid var(--line);
      }}
      .brand {{ margin-bottom: 10px; min-height: 40px; }}
      .brand-mark {{ width: 34px; height: 34px; }}
      .nav {{
        display: flex;
        gap: 8px;
        overflow-x: auto;
        padding-bottom: 3px;
        scrollbar-width: thin;
      }}
      .tab-btn {{
        flex: 0 0 auto;
        min-height: 38px;
        padding: 9px 11px;
        background: #161d20;
        border: 1px solid transparent;
      }}
      .tab-btn.active {{
        border-color: rgba(45, 212, 191, .35);
        box-shadow: inset 0 -3px 0 var(--teal);
      }}
      .topbar, .section-grid {{ grid-template-columns: 1fr; }}
      main {{ max-width: none; }}
    }}
    @media (max-width: 760px) {{
      body {{ overflow-x: hidden; }}
      main {{ padding: 14px; }}
      h1 {{ font-size: 2rem; }}
      .lede {{ font-size: .94rem; }}
      .why-flow {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
      .cards {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
      .metric {{ min-height: 102px; padding: 12px; }}
      .metric .value {{ font-size: 1.65rem; }}
      .panel-head {{
        align-items: flex-start;
        flex-direction: column;
        gap: 8px;
      }}
      .plain-grid {{ grid-template-columns: 1fr; }}
      .alert-strip {{ grid-template-columns: 1fr; }}
      .decision-actions {{ grid-template-columns: 1fr; }}
      .command-row {{ grid-template-columns: 1fr; }}
      .copy-btn, .link-btn {{ width: 100%; }}
      .link-chip-row .link-btn {{ width: auto; }}
      .link-group > div {{ grid-template-columns: 1fr; gap: 4px; }}
      .table-wrap {{ overflow-x: visible; }}
      table {{
        min-width: 0;
        table-layout: auto;
      }}
      thead {{ display: none; }}
      tbody, tr, td {{ display: block; width: 100%; }}
      tr {{
        border-bottom: 1px solid var(--line);
        padding: 10px 0;
      }}
      td {{
        display: grid;
        grid-template-columns: minmax(86px, 34%) minmax(0, 1fr);
        gap: 10px;
        border-bottom: 0;
        padding: 7px 12px;
      }}
      td::before {{
        content: attr(data-label);
        color: var(--muted);
        font-size: .7rem;
        letter-spacing: .07em;
        text-transform: uppercase;
      }}
    }}
    @media (max-width: 460px) {{
      main {{ padding: 12px; }}
      h1 {{ font-size: 1.72rem; }}
      .cards {{ grid-template-columns: 1fr; }}
      .why-flow {{ grid-template-columns: 1fr; }}
      .brand span {{ display: none; }}
      td {{ grid-template-columns: 1fr; gap: 4px; }}
    }}
  </style>
</head>
<body>
  <div class="shell">
    <aside class="sidebar">
      <div class="brand">
        <div class="brand-mark">CC</div>
        <div>
          <strong>CEO Cockpit</strong>
          <span>Generated {escape(data["generatedAt"])}</span>
        </div>
      </div>
      <nav class="nav" aria-label="Dashboard sections">
        <button class="tab-btn active" data-tab="overview"><span class="dot"></span>Start Here</button>
        <button class="tab-btn" data-tab="approvals"><span class="dot approvals"></span>Your Decisions</button>
        <button class="tab-btn" data-tab="pipeline"><span class="dot pipeline"></span>Lead List</button>
        <button class="tab-btn" data-tab="research"><span class="dot research"></span>Research</button>
        <button class="tab-btn" data-tab="safety"><span class="dot safety"></span>Safety</button>
        <button class="tab-btn" data-tab="councils"><span class="dot councils"></span>Councils</button>
        <button class="tab-btn" data-tab="revenue"><span class="dot revenue"></span>Money</button>
        <button class="tab-btn" data-tab="github"><span class="dot github"></span>Build Tasks</button>
      </nav>
    </aside>
    <main>
      <div class="topbar">
        <div>
          <h1>Your Business Control Room</h1>
          <p class="lede">Plain-English view of what the engine found, what is waiting for you, what I am allowed to do safely, and what is still blocked.</p>
        </div>
        <div class="search-box">
          <label for="searchInput">Find something</label>
          <input id="searchInput" type="search" placeholder="Search a business, place, decision, or task...">
        </div>
      </div>

      <section class="why-panel" aria-labelledby="why-heading">
        <h2 id="why-heading">Why we are doing this</h2>
        <p>We are building a small, steady business engine for Cap Coast Creative. The goal is to find real local businesses that could benefit from a better website, prepare useful ideas for them, and grow into paid website work without rushing, guessing, or contacting anyone before you approve it.</p>
        <div class="why-flow">
          <div class="why-step"><span>1</span><strong>Find local opportunities</strong><small>Look around Rockhampton, Yeppoon, Emu Park, Kawana, and the Capricorn Coast for businesses with public evidence.</small></div>
          <div class="why-step"><span>2</span><strong>Check if they are worth it</strong><small>Separate strong leads from weak directory-only leads so your time does not get wasted.</small></div>
          <div class="why-step"><span>3</span><strong>Prepare a useful offer</strong><small>Create private website ideas, positioning, and next steps before anything becomes client-facing.</small></div>
          <div class="why-step"><span>4</span><strong>Keep you in control</strong><small>You approve promotion, outreach, publishing, billing, and external actions separately.</small></div>
        </div>
      </section>

      <div class="cards">
        <div class="metric"><span class="label">Possible Leads Found</span><span class="value">{summary["intake"]}</span><span class="note">{summary["evidenceReady"]} have enough evidence to review</span></div>
        <div class="metric"><span class="label">Need Your Choice</span><span class="value">{summary["pendingApprovals"]}</span><span class="note">{summary["heldPromotions"]} promotions currently on hold</span></div>
        <div class="metric"><span class="label">Held / Cooled</span><span class="value">{summary["heldPromotions"]}</span><span class="note">{summary["cooledDown"]} weak leads cooled down</span></div>
        <div class="metric"><span class="label">Ready For Outreach</span><span class="value">{summary["prospects"]}</span><span class="note">still requires separate send approval</span></div>
        <div class="metric"><span class="label">Safety System</span><span class="value">{summary["safetyPass"]}/{summary["safetyTotal"]}</span><span class="note">checks currently passing</span></div>
      </div>

      <div class="alert-strip">
        <div><strong>What matters right now:</strong> choose what to do with the {summary["pendingApprovals"]} leads waiting for you. Approving them only moves them onto the working prospect list. It does not send messages.</div>
        <span class="pill blocked-no-approved-prospects">outreach locked</span>
      </div>

      <section class="tab-panel active" id="tab-overview"></section>
      <section class="tab-panel" id="tab-approvals"></section>
      <section class="tab-panel" id="tab-pipeline"></section>
      <section class="tab-panel" id="tab-research"></section>
      <section class="tab-panel" id="tab-safety"></section>
      <section class="tab-panel" id="tab-councils"></section>
      <section class="tab-panel" id="tab-revenue"></section>
      <section class="tab-panel" id="tab-github"></section>
      <p class="footer-note">Research and planning only. Outbound contact, publishing, billing, domain changes, hosting changes, and remote writes require explicit approval.</p>
    </main>
  </div>
  <script id="dashboardData" type="application/json">{js_safe({"data": data, "summary": summary})}</script>
  <script>
    const payload = JSON.parse(document.getElementById('dashboardData').textContent);
    const data = payload.data;
    const summary = payload.summary;

    const esc = (value) => String(value ?? '').replace(/[&<>"']/g, (char) => ({{
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#39;'
    }}[char]));

    const chip = (value, extra = '') => {{
      const text = String(value || '-');
      const cls = text.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
      return `<span class="pill ${{cls}} ${{extra}}">${{esc(text)}}</span>`;
    }};

    const link = (href, label = 'Open') => href ? `<a class="link-btn" href="${{esc(href)}}" target="_blank" rel="noreferrer">${{esc(label)}}</a>` : '<span class="pill">none</span>';

    const splitLinks = (value) => String(value || '')
      .split(/;|\\n|,/)
      .map(item => item.trim())
      .filter(item => /^https?:\\/\\//i.test(item));

    const linkChips = (value, label = 'Link') => {{
      const links = splitLinks(value);
      if (!links.length) return '<span class="pill">none</span>';
      return `<div class="link-chip-row">${{links.map((href, index) => link(href, `${{label}} ${{index + 1}}`)).join('')}}</div>`;
    }};

    const prospectLinkRows = () => {{
      const seen = new Set();
      return [...data.prospects, ...data.intake].filter(row => {{
        const key = String(row.business || '').toLowerCase();
        if (!key || seen.has(key)) return false;
        const hasLinks = splitLinks(row.website).length || splitLinks(row.socials).length || splitLinks(row.source_urls).length;
        if (!hasLinks) return false;
        seen.add(key);
        return true;
      }});
    }};

    const linkCards = () => {{
      const rows = prospectLinkRows();
      if (!rows.length) return '<div class="empty">No website or social links recorded yet.</div>';
      return `<div class="link-grid">${{rows.map(row => `
        <article class="link-card" data-search="${{esc(JSON.stringify(row).toLowerCase())}}">
          <h3>${{esc(row.business)}}</h3>
          <small>${{esc([row.region, row.niche].filter(Boolean).join(' / '))}}</small>
          <div class="link-group">
            <div><span class="link-label">Website</span><span>${{linkChips(row.website, 'Website')}}</span></div>
            <div><span class="link-label">Social</span><span>${{linkChips(row.socials, 'Social')}}</span></div>
            <div><span class="link-label">Source</span><span>${{linkChips(row.source_urls, 'Source')}}</span></div>
          </div>
        </article>`).join('')}}</div>`;
    }};

    const commandBlock = (command, label) => command ? `
      <div class="command-row">
        <code>${{esc(command)}}</code>
        <button class="copy-btn" data-copy="${{esc(command)}}">${{esc(label)}}</button>
      </div>` : '';

    const decisionButton = (row, decision, label) => `
      <button class="decision-btn ${{decision}}" data-approval-business="${{esc(row.business)}}" data-approval-decision="${{decision}}">${{esc(label)}}</button>`;

    const words = {{
      'allowed-now': 'I can do this now',
      'needs-daniel-decision': 'Waiting for your decision',
      'planned': 'Planned, not urgent',
      'blocked': 'Blocked',
      'blocked-external-write': 'Blocked until you approve external write',
      'blocked-no-approved-prospects': 'Blocked because no prospects are approved',
      'promotion-review': 'Ready for you to review',
      'pass': 'Safe',
      'ready-to-test': 'Ready to research',
      'suppress-repeat-search': 'Stop repeating weak searches'
    }};

    const plain = (value) => words[String(value || '').toLowerCase()] || String(value || '-').replace(/[-_]+/g, ' ');

    const ownerSummary = () => {{
      if (summary.pendingApprovals > 0) {{
        return {{
          title: 'Your next job',
          body: `Review ${{summary.pendingApprovals}} possible leads and choose approve, hold, or reject. Approve means "add to my working prospect list"; it does not contact anyone.`,
          status: 'Waiting for your decision'
        }};
      }}
      if (summary.prospects === 0) {{
        return {{
          title: 'Your next job',
          body: 'There are no approved prospects yet. Keep researching or approve one of the evidence-ready leads before outreach can even be prepared.',
          status: 'No approved prospects'
        }};
      }}
      return {{
        title: 'Your next job',
        body: 'Review the approved prospects and outreach drafts. Messages still cannot be sent until you approve the exact send.',
        status: 'Review before sending'
      }};
    }};

    const explainAction = (row) => {{
      const status = plain(row.status);
      const gate = row.safety_gate || 'Research and planning only.';
      return `${{status}}. ${{gate}}`;
    }};

    const simpleActionCards = (rows, limit = 5) => {{
      const visible = rows.slice(0, limit);
      if (!visible.length) return '<div class="empty">Nothing urgent right now.</div>';
      return `<div class="step-list">${{visible.map((row, index) => `
        <article class="step-card ${{row.owner === 'Daniel' ? 'owner-action' : ''}}" data-search="${{esc(JSON.stringify(row).toLowerCase())}}">
          <div class="step-number">${{index + 1}}</div>
          <div>
            <strong>${{esc(row.owner === 'Daniel' ? 'You decide' : 'Codex can work')}}: ${{esc(row.action)}}</strong>
            <p>${{esc(explainAction(row))}}</p>
          </div>
        </article>`).join('')}}</div>`;
    }};

    const table = (title, rows, columns, limit = 0) => {{
      const visible = limit ? rows.slice(0, limit) : rows;
      if (!visible.length) {{
        return `<article class="panel"><div class="panel-head"><h2>${{esc(title)}}</h2>${{chip('empty')}}</div><div class="panel-body"><div class="empty">No rows yet.</div></div></article>`;
      }}
      return `<article class="panel"><div class="panel-head"><h2>${{esc(title)}}</h2>${{chip(visible.length + ' rows')}}</div><div class="table-wrap"><table><thead><tr>${{columns.map(col => `<th>${{esc(col.label)}}</th>`).join('')}}</tr></thead><tbody>${{visible.map(row => `<tr data-search="${{esc(JSON.stringify(row).toLowerCase())}}">${{columns.map(col => `<td data-label="${{esc(col.label)}}">${{col.render ? col.render(row) : esc(row[col.key])}}</td>`).join('')}}</tr>`).join('')}}</tbody></table></div></article>`;
    }};

    const decisionCards = () => {{
      const rows = data.approvalInbox;
      if (!rows.length) return '<div class="empty">No pending approval decisions.</div>';
      return `<div class="decision-list">${{rows.map(row => `
        <article class="decision-card" data-search="${{esc(JSON.stringify(row).toLowerCase())}}">
          <h3>${{esc(row.rank)}}. ${{esc(row.business)}}</h3>
          <div class="decision-meta">
            ${{chip(row.approval_type || 'promotion')}}
            ${{chip('local decision', 'local')}}
            ${{chip('not outreach')}}
          </div>
          <p><strong>Plain English:</strong> decide whether this business is worth keeping on the prospect list. This is only a filing decision. It does not send outreach.</p>
          <p>${{esc(row.recommended_decision)}}</p>
          <div class="decision-meta">
            ${{link(row.evidence_path_href, 'Evidence')}}
            ${{link(row.packet_path_href, 'Packet')}}
          </div>
          <div class="decision-actions">
            ${{decisionButton(row, 'approve', 'Approve lead')}}
            ${{decisionButton(row, 'hold', 'Hold for later')}}
            ${{decisionButton(row, 'reject', 'Reject lead')}}
          </div>
          <div class="server-note">Button approvals work when the local dashboard server is running. They update your local files only; they do not send outreach.</div>
          ${{commandBlock(row.approve_command, 'Copy approve')}}
          ${{commandBlock(row.hold_command, 'Copy hold')}}
          ${{commandBlock(row.reject_command, 'Copy reject')}}
        </article>`).join('')}}</div>`;
    }};

    const overview = () => `
      <article class="plain-panel">
        <h2>${{esc(ownerSummary().title)}}</h2>
        <p>${{esc(ownerSummary().body)}}</p>
      </article>
      <div class="plain-grid">
        <div class="explain-card">
          <strong>What the engine is doing</strong>
          <p>It researches local businesses, stores evidence, drafts private ideas, and prepares review packets. It does not contact people by itself.</p>
        </div>
        <div class="explain-card">
          <strong>What you control</strong>
          <p>You approve whether a lead becomes a prospect. Later, you separately approve any real outreach, publishing, billing, or external write.</p>
        </div>
        <div class="explain-card">
          <strong>What is blocked</strong>
          <p>Cold outreach is locked even with ${{summary.prospects}} approved prospects until contact basis and exact send approval are recorded. That is intentional safety, not a failure.</p>
        </div>
      </div>
      <div class="section-grid">
        <div>
          <article class="panel">
            <div class="panel-head"><h2>Do These Next</h2>${{chip(ownerSummary().status)}}</div>
            <div class="panel-body">${{simpleActionCards(data.operatorQueue, 7)}}</div>
          </article>
          ${{table('Detailed Action Queue', data.operatorQueue, [
            {{ key: 'rank', label: 'Rank' }},
            {{ key: 'status', label: 'Meaning', render: row => chip(plain(row.status)) }},
            {{ key: 'owner', label: 'Owner' }},
            {{ key: 'action', label: 'Action' }},
            {{ key: 'safety_gate', label: 'Why It Is Safe / Blocked' }}
          ], 10)}}
          ${{table('Lead Quality Map', data.leadQuality, [
            {{ key: 'rank', label: 'Rank' }},
            {{ key: 'business', label: 'Business' }},
            {{ key: 'quality_band', label: 'Quality', render: row => chip(plain(row.quality_band)) }},
            {{ key: 'decision_state', label: 'Decision' }},
            {{ key: 'safe_next_step', label: 'Safe Next Step' }}
          ], 12)}}
          ${{table('Best Leads To Look At', data.priority, [
            {{ key: 'rank', label: 'Rank' }},
            {{ key: 'business', label: 'Business' }},
            {{ key: 'priority_score', label: 'Score' }},
            {{ key: 'status', label: 'Meaning', render: row => chip(plain(row.status)) }},
            {{ key: 'next_best_action', label: 'What Happens Next' }}
          ], 10)}}
        </div>
        <div>
          <article class="panel">
            <div class="panel-head"><h2>Business Health</h2>${{chip(summary.safetyPass === summary.safetyTotal ? 'safe' : 'review')}}</div>
            <div class="panel-body">
              <p>${{summary.privateConcepts}} private website ideas are ready for internal review. ${{summary.blockedActions}} actions are blocked until you approve the next gate.</p>
              <div class="progress"><span style="width:${{summary.safetyTotal ? Math.round(summary.safetyPass / summary.safetyTotal * 100) : 0}}%"></span></div>
            </div>
          </article>
          ${{table('Outreach Send Lock', data.preSend, [
            {{ key: 'business', label: 'Business' }},
            {{ key: 'readiness_status', label: 'Can We Send?', render: row => chip(plain(row.readiness_status)) }},
            {{ key: 'failure_reason', label: 'Why Not' }},
            {{ key: 'next_action', label: 'What Fixes It' }}
          ])}}
          ${{table('Engine Checkup', data.operating, [
            {{ key: 'area', label: 'Area' }},
            {{ key: 'status', label: 'Meaning', render: row => chip(plain(row.status)) }},
            {{ key: 'next_action', label: 'Next Step' }},
            {{ key: 'safety_gate', label: 'Safety Rule' }}
          ], 8)}}
        </div>
      </div>`;

    const approvals = () => `
      <article class="plain-panel">
        <h2>Your decisions are simple</h2>
        <p>Approve means "keep this lead and allow the engine to prepare the next internal step." Hold means "not sure yet." Reject means "remove it from the working list." None of these send a message.</p>
      </article>
      <div class="section-grid">
        <article class="panel">
          <div class="panel-head"><h2>Leads Waiting For You</h2>${{chip(data.approvalInbox.length + ' pending')}}</div>
          <div class="panel-body">${{decisionCards()}}</div>
        </article>
        <div>
          ${{table('Why They Are Waiting', data.approvals, [
            {{ key: 'approval_type', label: 'Type', render: row => chip(row.approval_type) }},
            {{ key: 'business', label: 'Business' }},
            {{ key: 'requested_decision', label: 'What You Decide' }},
            {{ key: 'blocked_until_approved', label: 'What Is Blocked' }}
          ])}}
          ${{table('What Happens After Approval', data.postApproval, [
            {{ key: 'business', label: 'Business' }},
            {{ key: 'step_order', label: 'Step' }},
            {{ key: 'step', label: 'Action' }},
            {{ key: 'owner', label: 'Owner' }},
            {{ key: 'safety_gate', label: 'Gate' }}
          ], 15)}}
        </div>
      </div>`;

    const pipeline = () => `
      <article class="plain-panel">
        <h2>Lead list in plain English</h2>
        <p>These are businesses the engine has found. A lead is not a client, and it is not someone we have contacted. It is just a researched opportunity.</p>
      </article>
      <article class="panel">
        <div class="panel-head"><h2>Open Their Links</h2>${{chip(prospectLinkRows().length + ' businesses')}}</div>
        <div class="panel-body">${{linkCards()}}</div>
      </article>
      ${{table('Lead Quality Map', data.leadQuality, [
        {{ key: 'rank', label: 'Rank' }},
        {{ key: 'business', label: 'Business' }},
        {{ key: 'region', label: 'Region' }},
        {{ key: 'quality_band', label: 'Quality', render: row => chip(plain(row.quality_band)) }},
        {{ key: 'evidence_gap', label: 'Evidence Gap' }},
        {{ key: 'safe_next_step', label: 'Safe Next Step' }}
      ])}}
      ${{table('Possible Leads Found', data.intake, [
        {{ key: 'business', label: 'Business' }},
        {{ key: 'region', label: 'Region' }},
        {{ key: 'niche', label: 'Niche' }},
        {{ key: 'website', label: 'Website', render: row => linkChips(row.website, 'Website') }},
        {{ key: 'socials', label: 'Socials', render: row => linkChips(row.socials, 'Social') }},
        {{ key: 'source_urls', label: 'Sources', render: row => linkChips(row.source_urls, 'Source') }},
        {{ key: 'proposed_hook', label: 'Hook' }}
      ])}}
      ${{table('Approved Working Prospect List', data.prospects, [
        {{ key: 'business', label: 'Business' }},
        {{ key: 'region', label: 'Region' }},
        {{ key: 'niche', label: 'Niche' }},
        {{ key: 'website', label: 'Website', render: row => linkChips(row.website, 'Website') }},
        {{ key: 'socials', label: 'Socials', render: row => linkChips(row.socials, 'Social') }},
        {{ key: 'tier', label: 'Tier' }},
        {{ key: 'status', label: 'Meaning', render: row => chip(plain(row.status)) }},
        {{ key: 'next_action', label: 'What Happens Next' }}
      ])}}
      ${{table('Private Website Ideas', data.concepts, [
        {{ key: 'business', label: 'Business' }},
        {{ key: 'primary_cta', label: 'CTA' }},
        {{ key: 'concept_path', label: 'Idea File', render: row => link(row.concept_path_href, 'Open') }}
      ])}}`;

    const research = () => `
      <article class="plain-panel">
        <h2>Research means looking, not contacting</h2>
        <p>This section shows where the engine is searching for public evidence. If evidence is weak, the lead gets cooled down instead of forced into the pipeline.</p>
      </article>
      ${{table('Where We Are Looking', data.regionalHeatmap, [
        {{ key: 'rank', label: 'Rank' }},
        {{ key: 'region', label: 'Region' }},
        {{ key: 'niche', label: 'Niche' }},
        {{ key: 'coverage_status', label: 'Meaning', render: row => chip(plain(row.coverage_status)) }},
        {{ key: 'priority_score', label: 'Score' }},
        {{ key: 'safe_next_action', label: 'Safe Next Step' }}
      ])}}
      ${{table('Evidence Still Missing', data.research, [
        {{ key: 'business', label: 'Business' }},
        {{ key: 'missing_evidence', label: 'Missing' }},
        {{ key: 'search_query', label: 'Query' }}
      ])}}
      ${{table('Recent Research Attempts', data.attempts, [
        {{ key: 'date', label: 'Date' }},
        {{ key: 'business', label: 'Business/Lane' }},
        {{ key: 'result', label: 'Result', render: row => chip(plain(row.result)) }},
        {{ key: 'query', label: 'Query' }},
        {{ key: 'next_action', label: 'What We Learned' }}
      ], 18)}}
      ${{table('Weak Leads We Are Rechecking Differently', data.sourcePivots, [
        {{ key: 'business', label: 'Business' }},
        {{ key: 'pivot_reason', label: 'Reason' }},
        {{ key: 'primary_query', label: 'Primary Query' }},
        {{ key: 'status', label: 'Meaning', render: row => chip(plain(row.status)) }}
      ])}}`;

    const safety = () => `
      <article class="plain-panel">
        <h2>Safety rules are the brakes</h2>
        <p>These rules stop the engine from sending messages, publishing, charging, or writing to outside systems without your exact approval.</p>
      </article>
      ${{table('Safety Rules', data.safetyInvariants, [
        {{ key: 'invariant', label: 'Rule' }},
        {{ key: 'status', label: 'Result', render: row => chip(plain(row.status)) }},
        {{ key: 'evidence', label: 'Evidence' }},
        {{ key: 'required_action', label: 'What To Do If It Fails' }}
      ])}}
      ${{table('What The Engine Is Allowed To Do', data.actionPermissions, [
        {{ key: 'action', label: 'Action' }},
        {{ key: 'status', label: 'Allowed?', render: row => chip(plain(row.status)) }},
        {{ key: 'safety_gate', label: 'Rule' }},
        {{ key: 'blocked_until', label: 'Blocked Until' }}
      ])}}
      ${{table('Engine Capabilities', data.capabilities, [
        {{ key: 'capability', label: 'Capability' }},
        {{ key: 'status', label: 'Meaning', render: row => chip(plain(row.status)) }},
        {{ key: 'evidence', label: 'Evidence' }},
        {{ key: 'remaining_gap', label: 'Still Missing' }}
      ])}}`;

    const councils = () => `
      ${{table('Council CEO Brief', data.councilBrief, [
        {{ key: 'priority', label: 'Priority' }},
        {{ key: 'council', label: 'Council' }},
        {{ key: 'allowed_next_move', label: 'Allowed Move' }},
        {{ key: 'blocked_actions', label: 'Blocked' }},
        {{ key: 'daniel_decision_needed', label: 'Daniel Decision' }}
      ])}}
      ${{table('Council Debates', data.councilDebates, [
        {{ key: 'council', label: 'Council' }},
        {{ key: 'decision_id', label: 'Decision' }},
        {{ key: 'verdict', label: 'Verdict' }},
        {{ key: 'next_test', label: 'Next Test' }}
      ])}}
      ${{table('Council Decision Gates', data.councilDecisionGates, [
        {{ key: 'action', label: 'Action' }},
        {{ key: 'council', label: 'Council' }},
        {{ key: 'council_verdict', label: 'Verdict' }},
        {{ key: 'gate_status', label: 'Gate', render: row => chip(row.gate_status) }}
      ])}}`;

    const revenue = () => `
      <article class="plain-panel">
        <h2>Money view is only a forecast</h2>
        <p>This is possible future monthly revenue if leads eventually become clients. It is not money earned yet.</p>
      </article>
      <div class="cards">
        <div class="metric"><span class="label">Possible Monthly Value</span><span class="value">${{esc(summary.grossReviewMrr)}}</span><span class="note">if review leads became clients</span></div>
        <div class="metric"><span class="label">Weighted Forecast</span><span class="value">${{esc(summary.weightedMrr)}}</span><span class="note">risk-adjusted guess</span></div>
      </div>
      ${{table('Revenue Forecast', data.revenueForecast, [
        {{ key: 'stage', label: 'Stage', render: row => chip(row.stage) }},
        {{ key: 'count', label: 'Count' }},
        {{ key: 'gross_monthly_fee', label: 'Gross' }},
        {{ key: 'weighted_mrr', label: 'Weighted' }},
        {{ key: 'next_action', label: 'What Improves This' }}
      ])}}
      ${{table('What We Might Offer', data.strategy, [
        {{ key: 'business', label: 'Business' }},
        {{ key: 'monthly_fee', label: 'Fee' }},
        {{ key: 'primary_cta', label: 'CTA' }},
        {{ key: 'trust_hook', label: 'Trust Hook' }}
      ])}}
      ${{table('Message Playbooks', data.playbooks, [
        {{ key: 'playbook_id', label: 'Playbook' }},
        {{ key: 'niche', label: 'Niche' }},
        {{ key: 'channel', label: 'Channel' }},
        {{ key: 'safety_gate', label: 'Safety Rule' }}
      ])}}`;

    const github = () => `
      <article class="plain-panel">
        <h2>Build tasks are internal</h2>
        <p>These are possible GitHub tasks for building websites or improving the engine. Remote writes stay blocked until you approve them.</p>
      </article>
      ${{table('Build Task Drafts', data.issueDrafts, [
        {{ key: 'business', label: 'Business' }},
        {{ key: 'issue_title', label: 'Title' }},
        {{ key: 'draft_path', label: 'Draft', render: row => link(row.draft_path_href, 'Open') }}
      ])}}
      ${{table('Can These Be Written To GitHub?', data.githubReadiness, [
        {{ key: 'business', label: 'Business' }},
        {{ key: 'readiness_status', label: 'Allowed?', render: row => chip(plain(row.readiness_status)) }},
        {{ key: 'command_status', label: 'Command' }},
        {{ key: 'failure_reason', label: 'Why Not' }}
      ])}}
      ${{table('GitHub Execution Plan', data.githubPlan, [
        {{ key: 'business', label: 'Business' }},
        {{ key: 'approval_status', label: 'Allowed?', render: row => chip(plain(row.approval_status)) }},
        {{ key: 'command_path', label: 'Command Artifact', render: row => link(row.command_path_href, 'Open') }}
      ])}}`;

    const renderers = {{ overview, approvals, pipeline, research, safety, councils, revenue, github }};
    Object.entries(renderers).forEach(([name, render]) => {{
      document.getElementById(`tab-${{name}}`).innerHTML = render();
    }});

    document.querySelectorAll('.tab-btn').forEach((button) => {{
      button.addEventListener('click', () => {{
        document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
        document.querySelectorAll('.tab-panel').forEach(panel => panel.classList.remove('active'));
        button.classList.add('active');
        document.getElementById(`tab-${{button.dataset.tab}}`).classList.add('active');
        applyFilter();
      }});
    }});

    document.addEventListener('click', async (event) => {{
      const approvalButton = event.target.closest('[data-approval-business]');
      if (approvalButton) {{
        const business = approvalButton.dataset.approvalBusiness;
        const decision = approvalButton.dataset.approvalDecision;
        const original = approvalButton.textContent;
        approvalButton.disabled = true;
        approvalButton.textContent = 'Saving...';
        try {{
          const response = await fetch('http://127.0.0.1:8787/api/approval', {{
            method: 'POST',
            headers: {{ 'Content-Type': 'application/json' }},
            body: JSON.stringify({{ business, decision }})
          }});
          const result = await response.json();
          if (!response.ok || !result.ok) throw new Error(result.message || 'Could not save decision');
          approvalButton.textContent = 'Saved';
          setTimeout(() => window.location.reload(), 900);
        }} catch (error) {{
          approvalButton.textContent = 'Server not running';
          approvalButton.title = error.message;
          setTimeout(() => {{
            approvalButton.disabled = false;
            approvalButton.textContent = original;
          }}, 2200);
        }}
        return;
      }}
      const button = event.target.closest('[data-copy]');
      if (!button) return;
      try {{
        await navigator.clipboard.writeText(button.dataset.copy);
        const old = button.textContent;
        button.textContent = 'Copied';
        setTimeout(() => button.textContent = old, 1200);
      }} catch (error) {{
        button.textContent = 'Copy failed';
      }}
    }});

    const searchInput = document.getElementById('searchInput');
    function applyFilter() {{
      const term = searchInput.value.trim().toLowerCase();
      document.querySelectorAll('.tab-panel.active [data-search]').forEach((row) => {{
        row.dataset.hidden = term && !row.dataset.search.includes(term) ? 'true' : 'false';
      }});
    }}
    searchInput.addEventListener('input', applyFilter);
  </script>
</body>
</html>
"""

os.makedirs(p("dashboard"), exist_ok=True)
path = p("dashboard", "index.html")
with open(path, "w", encoding="utf-8") as handle:
    handle.write(dashboard)

print(rel(path))
