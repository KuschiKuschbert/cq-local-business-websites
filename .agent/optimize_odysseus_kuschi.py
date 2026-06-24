#!/usr/bin/env python3
import json
import urllib.error
import urllib.request

BASE = "http://127.0.0.1:7860"
COOKIE = ".agent/odysseus.cookies"
ENDPOINT_ID = "da743bb4"
ENDPOINT_URL = "http://localhost:11434/v1"


def cookie_header():
    try:
        lines = open(COOKIE, "r", encoding="utf-8").read().splitlines()
    except FileNotFoundError:
        return ""
    pairs = []
    for line in lines:
        if not line:
            continue
        if line.startswith("#HttpOnly_"):
            line = line[len("#HttpOnly_"):]
        elif line.startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) >= 7:
            pairs.append(f"{parts[5]}={parts[6]}")
    return "; ".join(pairs)


COOKIE_HEADER = cookie_header()


def request(method, path, payload=None):
    data = None
    headers = {"Cookie": COOKIE_HEADER}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(BASE + path, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as res:
            raw = res.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"{method} {path} failed: {e.code} {body}") from e


DASHBOARD = """Kuschi OS Dashboard

Open this note when you want a practical starting point inside Odysseus.

Daily launch flow
1. Ask Kuschi OS: "Give me my daily command centre for Riviera, kitchen ops, business, dev, and admin."
2. Pick the right preset:
   - Riviera Brand Writer: captions, venue copy, proposal wording.
   - Riviera Event Proposal Builder: weddings, functions, event packs.
   - Kitchen Ops + SOP: prep, ordering, staff process.
   - Recipe + Costing: recipes, GP%, allergens, scaling.
   - Local Business Outreach: audits, offers, cold email, follow-up.
   - PrepFlow Dev Copilot: code and product planning.
   - Daily Admin: life admin, finance notes, German/English writing.
3. Use qwen3:14b for quality. Use qwen3:8b when speed matters.
4. Add important corrections as Memory, not just chat messages.

Riviera quick commands
- Draft a Riviera Instagram caption for [event/menu/photo] in our warm coastal tone.
- Turn this wedding brief into a proposal outline: [paste brief].
- Create a prep list and service timeline for [event], [pax], [service time].
- Rewrite this client email so it sounds polished but not salesy: [paste].

Kitchen quick commands
- Cost this recipe and flag GP%, allergens, substitutions, and scaling risks: [paste].
- Turn this rough process into an SOP for staff: [paste].
- Build a prep list for [menu/event/date/pax] with station ownership.
- Find waste-reduction options for these ingredients: [list].

Business quick commands
- Audit this local business website and give me the top 5 conversion fixes: [URL].
- Write a short outreach message for this business: [name + issue].
- Turn this idea into a simple offer with scope, price logic, and next step: [idea].

Dev quick commands
- Review this bug and give exact file-level fix steps: [paste error].
- Plan the next version of PrepFlow feature [feature].
- Turn this app idea into screens, data model, and build sequence: [idea].

Rules for Kuschi OS
- Be direct and practical.
- Metric units and 24-hour time.
- For Riviera, avoid: luxury, exquisite, amazing, awesome, delicious.
- Do not send email, delete data, change passwords, or connect accounts without explicit approval.
"""


CHECKLIST_ITEMS = [
    "Change Odysseus admin password when back at the Mac.",
    "Open /Applications/Odysseus.app once and confirm it launches the UI.",
    "Open Notes and pin this dashboard at the top.",
    "Upload or paste current Riviera menus, packages, SOPs, supplier lists, and recipe sheets.",
    "Test Riviera Brand Writer with one real caption.",
    "Test Recipe + Costing with one real kitchen recipe.",
    "Test Event Proposal Builder with one wedding/function brief.",
    "Decide later whether to connect email/calendar. Do not enable auto-send until reviewed.",
]


def upsert_note(title, payload):
    data = request("GET", "/api/notes")
    notes = data.get("notes", [])
    existing = next((n for n in notes if n.get("title") == title), None)
    if existing:
        return request("PUT", f"/api/notes/{existing['id']}", payload)
    create_payload = dict(payload)
    create_payload["title"] = title
    return request("POST", "/api/notes", create_payload)


def main():
    settings = request("GET", "/api/auth/settings")
    settings.update({
        "default_endpoint_id": ENDPOINT_ID,
        "default_model": "qwen3:14b",
        "default_model_fallbacks": [{"endpoint_id": ENDPOINT_ID, "model": "qwen3:8b"}],
        "utility_endpoint_id": ENDPOINT_ID,
        "utility_model": "qwen3:8b",
        "utility_model_fallbacks": [{"endpoint_id": ENDPOINT_ID, "model": "qwen3:14b"}],
        "task_endpoint_id": ENDPOINT_ID,
        "task_model": "qwen3:8b",
        "research_endpoint_id": ENDPOINT_ID,
        "research_model": "qwen3:14b",
        "agent_input_token_budget": 8000,
        "agent_max_rounds": 16,
        "search_result_count": 6,
    })
    updated_settings = request("POST", "/api/auth/settings", settings)

    prefs_to_set = {
        "memory_enabled": True,
        "auto_memory": True,
        "skills_enabled": True,
        "auto_skills": True,
        "auto_approve_skills": True,
        "skill_min_confidence": 0.85,
        "default_model_fallbacks": [{"endpoint_id": ENDPOINT_ID, "model": "qwen3:8b"}],
    }
    for key, value in prefs_to_set.items():
        request("PUT", f"/api/prefs/{key}", {"value": value})

    dashboard = upsert_note("Kuschi OS Dashboard", {
        "content": DASHBOARD,
        "note_type": "note",
        "color": "green",
        "label": "dashboard",
        "pinned": True,
        "archived": False,
        "sort_order": 0,
        "source": "codex_seed",
    })

    checklist = upsert_note("Odysseus Setup Checklist", {
        "content": "First useful setup steps for when you are at the Mac.",
        "items": [{"text": item, "done": False} for item in CHECKLIST_ITEMS],
        "note_type": "checklist",
        "color": "yellow",
        "label": "dashboard",
        "pinned": True,
        "archived": False,
        "sort_order": 1,
        "source": "codex_seed",
    })

    print(json.dumps({
        "default_model": updated_settings.get("default_model"),
        "utility_model": updated_settings.get("utility_model"),
        "task_model": updated_settings.get("task_model"),
        "research_model": updated_settings.get("research_model"),
        "dashboard_note_id": dashboard.get("id"),
        "checklist_note_id": checklist.get("id"),
    }, indent=2))


if __name__ == "__main__":
    main()
