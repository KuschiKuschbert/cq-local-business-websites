#!/usr/bin/env python3
import os
from common import clean, p, read_csv, rel, today, write_csv

FIELDS = ["date", "decision_id", "council", "quality_status", "score", "missing_elements", "argument_test", "evidence_path", "safety_gate", "next_action", "notes"]


def has_words(value, minimum):
    return len(clean(value, "").split()) >= minimum


def exists_rel(path):
    value = clean(path, "")
    return value.startswith(".agent/") and os.path.exists(os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")), value))


rows = []
for debate in read_csv(p("council_debates.csv")):
    missing = []
    if not has_words(debate.get("decision"), 8):
        missing.append("decision too thin")
    if not has_words(debate.get("best_case"), 8):
        missing.append("best case too thin")
    if not has_words(debate.get("hard_pushback"), 8):
        missing.append("hard pushback too thin")
    split = clean(debate.get("council_split"), "")
    if not has_words(split, 12) or split.count(";") < 2:
        missing.append("role split lacks distinct disagreement")
    if clean(debate.get("verdict"), "") in {"", "-", "missing"}:
        missing.append("verdict missing")
    if not has_words(debate.get("next_test"), 4):
        missing.append("next test too vague")
    if not exists_rel(debate.get("evidence_path")):
        missing.append("evidence path missing")
    if not has_words(debate.get("safety_gate"), 6):
        missing.append("safety gate too thin")
    score = max(100 - len(missing) * 15, 0)
    status = "pass" if not missing else "needs-rework"
    rows.append({
        "date": today(),
        "decision_id": clean(debate.get("decision_id")),
        "council": clean(debate.get("council")),
        "quality_status": status,
        "score": str(score),
        "missing_elements": "; ".join(missing) if missing else "-",
        "argument_test": "Includes concrete pro/con tension, distinct role split, verdict, next test, evidence, and safety gate." if not missing else "Rework debate before using it to influence decisions.",
        "evidence_path": clean(debate.get("evidence_path")),
        "safety_gate": clean(debate.get("safety_gate")),
        "next_action": "Use debate as advisory pressure only." if not missing else "Regenerate council debates with stronger disagreement.",
        "notes": "Quality audit only; does not approve actions.",
    })

write_csv(p("council_quality_audit.csv"), rows, FIELDS)

os.makedirs(p("councils"), exist_ok=True)
path = p("councils", f"quality-audit-{today()}.md")
with open(path, "w", encoding="utf-8") as handle:
    handle.write("# Council Quality Audit\n\n")
    handle.write(f"- Date: {today()}\n")
    handle.write("- Purpose: ensure council debates contain useful disagreement before influencing decisions.\n\n")
    for row in rows:
        handle.write(f"- {row['decision_id']}: {row['quality_status']} ({row['score']}) / Missing: {row['missing_elements']}\n")

print(rel(path))
