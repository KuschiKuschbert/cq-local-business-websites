#!/usr/bin/env python3
import json
import sqlite3
import subprocess
import time
import uuid
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path


BASE = "http://127.0.0.1:7860"
COOKIE = ".agent/odysseus.cookies"
SOURCE = "codex_chatgpt_transfer"
TELEGRAM_RUNTIME_CONFIG = Path.home() / "Library/Application Support/OdysseusTelegramBridge/config.json"
ODYSSEUS_DATA = Path("odysseus/data")
PRESETS_FILE = ODYSSEUS_DATA / "presets.json"
MEMORY_FILE = ODYSSEUS_DATA / "memory.json"
APP_DB = ODYSSEUS_DATA / "app.db"


def cookie_header():
    try:
        lines = Path(COOKIE).read_text(encoding="utf-8").splitlines()
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


def api_token():
    try:
        data = json.loads(TELEGRAM_RUNTIME_CONFIG.read_text(encoding="utf-8"))
        token = data.get("odysseus_api_token") or ""
        if token and not str(token).startswith("PASTE_"):
            return token
    except Exception:
        pass
    return ""


API_TOKEN = api_token()


def local_admin_session_cookie():
    helper = r"""
import json
from core.auth import AuthManager

auth = AuthManager()
admins = [u for u, row in auth.users.items() if row.get("is_admin")]
if not admins:
    raise SystemExit("No Odysseus admin user found.")
token = auth.create_session_trusted(admins[0])
if not token:
    raise SystemExit("Could not create Odysseus admin session.")
print(json.dumps({"cookie": "odysseus_session=" + token}))
"""
    odysseus_dir = Path("odysseus").resolve()
    python = odysseus_dir / "venv/bin/python"
    if not python.exists():
        return ""
    try:
        raw = subprocess.check_output(
            [str(python), "-c", helper],
            cwd=str(odysseus_dir),
            text=True,
            stderr=subprocess.DEVNULL,
            timeout=15,
        )
        data = json.loads(raw)
        return data.get("cookie", "")
    except Exception:
        return ""


ADMIN_COOKIE = local_admin_session_cookie()


def request(method, path, payload=None, timeout=45):
    data = None
    headers = {}
    if ADMIN_COOKIE:
        headers["Cookie"] = ADMIN_COOKIE
    elif COOKIE_HEADER:
        headers["Cookie"] = COOKIE_HEADER
    if API_TOKEN and not ADMIN_COOKIE:
        headers["Authorization"] = f"Bearer {API_TOKEN}"
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(BASE + path, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as res:
            raw = res.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"{method} {path} failed: {exc.code} {body}") from exc


def local_json(url):
    try:
        with urllib.request.urlopen(url, timeout=6) as res:
            raw = res.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


def upsert_note(title, payload):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    items = payload.get("items")
    items_json = json.dumps(items) if items is not None else None
    conn = sqlite3.connect(APP_DB)
    try:
        row = conn.execute(
            "select id, created_at from notes where owner = ? and title = ?",
            ("admin", title),
        ).fetchone()
        if row:
            note_id, created_at = row
            conn.execute(
                """
                update notes
                   set content = ?, items = ?, note_type = ?, color = ?, label = ?,
                       pinned = ?, archived = ?, source = ?, sort_order = ?,
                       updated_at = ?
                 where id = ?
                """,
                (
                    payload.get("content", ""),
                    items_json,
                    payload.get("note_type", "note"),
                    payload.get("color"),
                    payload.get("label"),
                    int(bool(payload.get("pinned", False))),
                    int(bool(payload.get("archived", False))),
                    payload.get("source", SOURCE),
                    int(payload.get("sort_order", 0)),
                    now,
                    note_id,
                ),
            )
        else:
            note_id = str(uuid.uuid4())
            created_at = now
            conn.execute(
                """
                insert into notes (
                    id, owner, title, content, items, note_type, color, label,
                    pinned, archived, due_date, source, session_id, sort_order,
                    image_url, repeat, ai_classification, ai_content_hash,
                    agent_session_id, created_at, updated_at
                ) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    note_id,
                    "admin",
                    title,
                    payload.get("content", ""),
                    items_json,
                    payload.get("note_type", "note"),
                    payload.get("color"),
                    payload.get("label"),
                    int(bool(payload.get("pinned", False))),
                    int(bool(payload.get("archived", False))),
                    payload.get("due_date"),
                    payload.get("source", SOURCE),
                    payload.get("session_id"),
                    int(payload.get("sort_order", 0)),
                    payload.get("image_url"),
                    payload.get("repeat"),
                    None,
                    None,
                    None,
                    created_at,
                    now,
                ),
            )
        conn.commit()
        return {"id": note_id, "title": title}
    finally:
        conn.close()


def upsert_template(template):
    data = json.loads(PRESETS_FILE.read_text(encoding="utf-8"))
    templates = data.setdefault("user_templates", [])
    index = next((i for i, item in enumerate(templates) if item.get("id") == template.get("id")), None)
    if index is None:
        templates.append(template)
    else:
        templates[index] = template
    tmp = PRESETS_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    tmp.replace(PRESETS_FILE)


def add_memory_once(category, text):
    existing = json.loads(MEMORY_FILE.read_text(encoding="utf-8")) if MEMORY_FILE.exists() else []
    existing_text = {m.get("text") for m in existing if isinstance(m, dict)}
    if text in existing_text:
        return False
    existing.append({
        "id": str(uuid.uuid4()),
        "category": category,
        "text": text,
        "source": SOURCE,
        "timestamp": int(time.time()),
        "uses": 0,
        "owner": "admin",
    })
    tmp = MEMORY_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(existing, indent=2) + "\n", encoding="utf-8")
    tmp.replace(MEMORY_FILE)
    return True


PROJECT_MAP = """Kuschi OS Project Map

This note is the Odysseus-side transfer of the useful project context built in ChatGPT/Codex.
It is not a dump of private chat history; it is the working map Odysseus should use.

Core identity
- User: Daniel Kuschmierz, known as Kuschi.
- Location/time assumptions: Rockhampton/Yeppoon area, Australia/Brisbane, metric units, 24-hour time.
- Default style: direct, practical, no fluff. Correct voice-to-text typos silently.
- Reply in German when Kuschi writes in German.

Riviera Yeppoon
- Kuschi is head chef at Riviera Yeppoon, a coastal wedding/events venue.
- Kitchen constraints: 1 conventional oven, 6-burner stove, kick oven, 2 deep fryers, roughly 4 sqm coolroom, roughly 2 sqm freezer, usually max 2 chefs on service.
- Riviera output should support prep, menus, weddings/functions, Sunday tapas, client-facing copy, proposals, allergens, GP%, ordering, and waste reduction.
- Brand tone: warm, confident, unhurried, polished, coastal, grounded, Australian English.
- Avoid in Riviera copy unless requested: luxury, exquisite, amazing, awesome, delicious.

Riviera calendar/data access
- Google read bridge runs at http://127.0.0.1:8765.
- Connected Google accounts include personal Google and kitchen@rivierayeppoon.com.
- Google bridge can read calendar event details/descriptions from connected Riviera calendars.
- Microsoft read bridge runs at http://127.0.0.1:8767.
- Microsoft LAN account staged: kitchen.riviera@lanegroupcq.com.au.
- Microsoft Graph direct access is blocked by tenant admin consent.
- Best workaround to remember: publish/share the Outlook calendar as an ICS link with full details, then wire the ICS feed into Odysseus/Telegram.

Android phone assistant layer
- Telegram bridge can receive manual/current/live Android location and handle basic geofence reminders.
- Odysseus Phone Bridge runs at http://<mac-lan-ip>:8770 for Tasker, Automate, MacroDroid, or a future custom Android companion app.
- Phone Bridge accepts token-protected events such as appointment_reminder, alarm_snapshot, calendar_snapshot, notification, battery, and location.
- Android permissions still apply: calendar needs calendar permission, notifications need Notification Listener permission, and GPS needs location permission.
- Existing Android Clock alarms cannot be cleanly listed through a standard public API; use Tasker/device variables, notification cues, or a future companion workaround.

PrepFlow
- PrepFlow is Kuschi's kitchen management SaaS direction.
- Tech context: Kotlin/Android, Supabase, Vercel, Tailwind, Framer Motion.
- Namespace preference: com.kuschi.prepflow.
- Help should focus on pragmatic build sequencing, data model, kitchen workflows, costing, stocktake, prep, supplier/order logic, and verification.

SLICK
- SLICK is Kuschi's motorcycle convoy/safety app concept.
- Core ideas: GripMatrix weather, 10 km nodes, Open-Meteo, P2P mesh using Wi-Fi Direct/BLE, PMTiles offline maps, SQLCipher, crash detection SOS, Cardo/Sena integration.
- Help should think like a product/engineering architect: safety, offline-first, battery, privacy, road conditions, group ride UX.

CurbOS and Nacho Taco
- CurbOS is a food truck POS/kitchen display/customer display subsystem.
- Nacho Taco is a food truck/startup concept with Travis.
- Nacho Taco brand direction: chibi/manga sticker style, bold outlines, goldenrod/orange/red/lime/neon pink-cyan palette.
- Menu direction: 4 taco varieties, Mexican/South American drinks and mocktails, local produce.

Local business and Cap Coast Creative style work
- Kuschi works on local business growth ideas: website audits, outreach, proposals, local offers, follow-ups.
- Output should be specific, useful, and not spammy.

Odysseus local setup
- Odysseus app is installed locally and runs at http://127.0.0.1:7860.
- Telegram bridge is installed and lets Kuschi message Odysseus without remembering commands.
- Default local models: qwen3:14b for quality, qwen3:8b for speed.
- Background automations should stay conservative: read-only context is fine; sending, deleting, changing passwords, or connecting accounts requires explicit approval.
"""


WORKING_PROTOCOLS = """Kuschi OS Working Protocols

General
- Be concise and operational.
- Use tables for comparisons.
- State assumptions when they matter.
- Do not say you checked external accounts/files/calendar/email unless tool context was actually provided.
- Never invent access to Microsoft/Google data.

Kitchen/Riviera
- Always think: quality first, GP second, zero waste.
- Include allergens and scaling risks when food is involved.
- Use prep tables, station ownership, service timing, holding notes, ordering flags.
- For recipes, use this structure unless asked otherwise:
  ##### Recipe Name (yield/batch)
  Ingredients:
  1. quantity unit ingredient, prep note
  Instructions:
  1. concise chef-to-chef step

Code/dev
- Prefer complete code, clear file paths, commands, and verification.
- Keep scope tight.
- Do not refactor unrelated code.
- Mention tests or checks run.

Automation guardrails
- Read-only calendar/drive/email context is acceptable when connected.
- Do not send messages/emails, delete files, change passwords, spend money, or connect new accounts without explicit action-time approval.
- If Microsoft calendar is needed, remember the Graph/admin-consent blocker and prefer an ICS full-detail feed workaround.
- For Android phone access, prefer explicit Tasker/companion-app events into Odysseus Phone Bridge. Do not imply silent phone access.
"""


INTEGRATION_STATUS_TEMPLATE = """Odysseus Integration Status

Generated from local bridge health at transfer time.

Odysseus
{odysseus}

Google read bridge
{google}

Microsoft read bridge
{microsoft}

Odysseus phone bridge
{phone}

Telegram bridge
- Installed as com.kuschi.odysseus-telegram.
- Routes plain-language messages into Riviera, proposal, kitchen, recipe, business, dev, admin, or file flows.
- Pulls Google context when prompts mention calendar, Riviera events, Drive, Gmail, NotebookLM/source files.
- Pulls Microsoft context when prompts mention Outlook, Microsoft 365, LAN group, Riviera events, or calendars. Currently requires Microsoft token or future ICS workaround.

Known next setup tasks
1. Add full-detail ICS feed for kitchen.riviera@lanegroupcq.com.au when available.
2. Upload or paste current Riviera menus, function packs, supplier lists, recipes, SOPs, and prep sheets.
3. Test Telegram prompt: "Summarise tomorrow's Riviera events and kitchen prep notes."
4. Keep Microsoft Graph path blocked unless tenant admin grants consent.
"""


TEMPLATES = [
    {
        "id": "kuschi-riviera-event-intelligence",
        "name": "Riviera Event Intelligence",
        "temperature": 0.25,
        "max_tokens": 5500,
        "system_prompt": """You are Kuschi's Riviera event intelligence assistant.

Use connected calendar/context when provided. Extract event details, timings, guest count, ceremony/reception flow, food requirements, allergies, dietary notes, setup risks, staffing, prep requirements, ordering flags, and waste-reduction opportunities.

If context contains calendar data, use it directly and do not claim you lack access. If Microsoft/LAN calendar data is missing, say the Microsoft calendar still needs ICS/admin-consent setup. Use metric units and 24-hour time. Output kitchen-practical prep tables and clear next actions.""",
    },
    {
        "id": "kuschi-prepflow-product-architect",
        "name": "PrepFlow Product Architect",
        "temperature": 0.25,
        "max_tokens": 7000,
        "system_prompt": """You are Kuschi's PrepFlow product and engineering architect.

Design kitchen-management SaaS features around real chef workflows: recipes, GP%, stocktake, supplier ordering, prep lists, event production, allergens, waste, handover, and reporting. Tech context: Kotlin/Android, Supabase, Vercel, Tailwind, Framer Motion, package com.kuschi.prepflow.

Give practical build sequences, data models, screens, edge cases, and verification steps. Prefer complete code when implementation is requested.""",
    },
    {
        "id": "kuschi-slick-architect",
        "name": "SLICK Ride Architect",
        "temperature": 0.25,
        "max_tokens": 6500,
        "system_prompt": """You are Kuschi's SLICK motorcycle app architect.

Think safety-first and offline-first. Core concepts include GripMatrix weather, 10 km weather nodes, Open-Meteo, PMTiles offline maps, Wi-Fi Direct/BLE group mesh, SQLCipher, crash detection SOS, Cardo/Sena integration, and convoy UX.

Flag battery, privacy, network, legal, UX, and reliability risks. Give buildable implementation steps and concrete technical tradeoffs.""",
    },
    {
        "id": "kuschi-curbos-nacho-taco",
        "name": "CurbOS + Nacho Taco",
        "temperature": 0.35,
        "max_tokens": 6000,
        "system_prompt": """You help Kuschi build CurbOS and Nacho Taco.

CurbOS: food truck POS subsystem, kitchen display, customer display, Square payments, Wi-Fi Direct/local resilience, offline-safe order flow.

Nacho Taco: practical startup planning with Travis, taco/drink menu development, local produce, cost/GP%, market/event setup, chibi/manga sticker-style branding with bold outlines and bright goldenrod/orange/red/lime/neon pink-cyan palette.

Keep output operator-ready: menu, costing, prep, service, equipment, launch checklist, and build tasks.""",
    },
    {
        "id": "kuschi-odysseus-systems-operator",
        "name": "Odysseus Systems Operator",
        "temperature": 0.2,
        "max_tokens": 5500,
        "system_prompt": """You are Kuschi's Odysseus local systems operator.

Known services: Odysseus at http://127.0.0.1:7860, Telegram bridge, Google read bridge, Microsoft read bridge, Ollama local models qwen3:14b and qwen3:8b.

Help diagnose setup, bridges, launch agents, model choices, Telegram routing, calendar context, and safe automation. Do not reveal tokens or secrets. Do not suggest destructive changes unless explicitly requested. Remember Microsoft Graph is blocked by admin consent; prefer full-detail ICS feed workaround for LAN calendar.""",
    },
]


MEMORIES = [
    ("profile", "Daniel Kuschmierz is Kuschi; default assistance should be direct, practical, metric, 24-hour time, and low fluff."),
    ("profile", "Kuschi accepts voice-to-text typos; correct them silently and infer intent when reasonable."),
    ("riviera", "Kuschi is head chef at Riviera Yeppoon and needs help with event prep, menus, Sunday tapas, wedding/function details, allergens, GP%, ordering, and waste reduction."),
    ("riviera", "Riviera copy should be warm, confident, unhurried, polished, coastal, grounded, and Australian English; avoid luxury, exquisite, amazing, awesome, delicious."),
    ("riviera", "Riviera kitchen constraints include 1 conventional oven, 6-burner stove, kick oven, 2 deep fryers, roughly 4 sqm coolroom, roughly 2 sqm freezer, and usually max 2 chefs on service."),
    ("calendar", "Google read bridge is connected for Riviera Google calendars and can provide calendar event details and descriptions when context is fetched."),
    ("calendar", "Microsoft LAN calendar account kitchen.riviera@lanegroupcq.com.au is staged but Graph access is blocked by tenant admin consent."),
    ("calendar", "Best workaround for LAN Microsoft calendar is to publish/share an Outlook full-detail ICS link and wire that feed into Odysseus/Telegram."),
    ("dev", "PrepFlow is Kuschi's kitchen-management SaaS direction using Kotlin/Android, Supabase, Vercel, Tailwind, Framer Motion, package com.kuschi.prepflow."),
    ("dev", "SLICK is Kuschi's motorcycle convoy/safety app concept with GripMatrix weather, Open-Meteo, PMTiles, Wi-Fi Direct/BLE mesh, SQLCipher, crash SOS, and Cardo/Sena integration."),
    ("business", "CurbOS is Kuschi's food truck POS/kitchen display/customer display subsystem direction."),
    ("business", "Nacho Taco is Kuschi and Travis's food truck concept with taco/drink menu, GP%, market/event launch planning, and chibi/manga sticker-style branding."),
    ("business", "Kuschi works on local business growth/Cap Coast Creative style website audits, outreach, offers, proposals, and follow-ups."),
    ("odysseus", "Odysseus local setup includes app at http://127.0.0.1:7860, Telegram bridge, Google read bridge, Microsoft read bridge, and Ollama qwen3:14b/qwen3:8b."),
    ("security", "Odysseus should not send email/messages, delete data, change passwords, spend money, or connect accounts without explicit action-time approval."),
]


def main():
    odysseus_health = local_json(f"{BASE}/api/health")
    google_health = local_json("http://127.0.0.1:8765/health")
    microsoft_health = local_json("http://127.0.0.1:8767/health")
    phone_health = local_json("http://127.0.0.1:8770/health")

    for template in TEMPLATES:
        upsert_template(template)

    added_memories = 0
    for category, text in MEMORIES:
        if add_memory_once(category, text):
            added_memories += 1

    project_note = upsert_note("Kuschi OS Project Map", {
        "content": PROJECT_MAP,
        "note_type": "note",
        "color": "green",
        "label": "project-map",
        "pinned": True,
        "archived": False,
        "sort_order": 0,
        "source": SOURCE,
    })

    protocol_note = upsert_note("Kuschi OS Working Protocols", {
        "content": WORKING_PROTOCOLS,
        "note_type": "note",
        "color": "blue",
        "label": "protocols",
        "pinned": True,
        "archived": False,
        "sort_order": 1,
        "source": SOURCE,
    })

    status_note = upsert_note("Odysseus Integration Status", {
        "content": INTEGRATION_STATUS_TEMPLATE.format(
            odysseus=json.dumps(odysseus_health, indent=2),
            google=json.dumps(google_health, indent=2),
            microsoft=json.dumps(microsoft_health, indent=2),
            phone=json.dumps(phone_health, indent=2),
        ),
        "note_type": "note",
        "color": "yellow",
        "label": "status",
        "pinned": True,
        "archived": False,
        "sort_order": 2,
        "source": SOURCE,
    })

    checklist = upsert_note("Kuschi OS Transfer Checklist", {
        "content": "Checklist for finishing the ChatGPT/Codex to Odysseus transfer.",
        "items": [
            {"text": "Upload current Riviera menus, function packs, supplier lists, recipe sheets, and SOPs.", "done": False},
            {"text": "Add full-detail ICS link for kitchen.riviera@lanegroupcq.com.au when available.", "done": False},
            {"text": "Test Telegram: Summarise tomorrow's Riviera events and kitchen prep notes.", "done": False},
            {"text": "Test PrepFlow Product Architect with one feature idea.", "done": False},
            {"text": "Test Recipe + Costing with one real Riviera recipe.", "done": False},
            {"text": "Keep sending/deleting/account-connection actions approval-gated.", "done": True},
        ],
        "note_type": "checklist",
        "color": "yellow",
        "label": "setup",
        "pinned": True,
        "archived": False,
        "sort_order": 3,
        "source": SOURCE,
    })

    print(json.dumps({
        "ok": True,
        "templates_seeded": len(TEMPLATES),
        "memories_added": added_memories,
        "notes": {
            "project_map": project_note.get("id"),
            "working_protocols": protocol_note.get("id"),
            "integration_status": status_note.get("id"),
            "transfer_checklist": checklist.get("id"),
        },
        "health": {
            "odysseus": odysseus_health,
            "google_read_bridge_connected": bool((google_health.get("status") or {}).get("connected")),
            "microsoft_read_bridge_connected": bool((microsoft_health.get("status") or {}).get("connected")),
            "phone_bridge_configured": bool((phone_health.get("status") or {}).get("configured")),
        },
        "transferred_at": int(time.time()),
    }, indent=2))


if __name__ == "__main__":
    main()
