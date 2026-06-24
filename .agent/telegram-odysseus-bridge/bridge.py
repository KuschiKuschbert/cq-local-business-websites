#!/usr/bin/env python3
import argparse
import json
import math
import mimetypes
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


DOMAIN_PROMPTS = {
    "riviera": "Write for Riviera Yeppoon in warm, confident, unhurried coastal Australian English. Avoid: luxury, exquisite, amazing, awesome, delicious.",
    "proposal": "Build practical Riviera Yeppoon event and wedding proposal material. Cover event snapshot, food direction, beverage/service notes, timing assumptions, inclusions, open questions, and next steps.",
    "kitchen": "Act as Kuschi's kitchen operations assistant. Prioritise prep, service, consistency, food safety, GP%, ordering, stock control, allergens, mise en place, and waste reduction.",
    "recipe": "Format chef-ready recipes for Kuschi. Use metric. Include yield, portions, prep time, cook time, equipment, ingredients, method, holding/service notes, allergens, scaling notes, and costing prompts when prices are missing.",
    "business": "Help Kuschi with local business outreach, website audits, offers, proposals, and follow-ups. Be specific, useful, practical, and not spammy.",
    "dev": "Act as Kuschi's pragmatic software engineering copilot for PrepFlow, SLICK, CurbOS, Supabase, Vercel, Tailwind, Framer, Kotlin/Android, and web apps. Prefer concrete debugging steps and code-level guidance.",
    "nacho": "Help Kuschi build Nacho Taco and CurbOS. Cover menu, GP%, prep, equipment, market/event setup, launch planning, Square/POS, kitchen display, customer display, and chibi/manga sticker-style branding. Keep it practical.",
    "systems": "Act as Kuschi's local Odysseus systems operator. Help with Odysseus, Telegram bridge, Google read bridge, Microsoft read bridge, Ollama models, local LLM setup, safe automation, launch agents, and dashboard/status checks. Do not reveal secrets.",
    "finance": "Help Kuschi with practical finance/admin: Sharesies/Vanguard/Raiz/super, tax deductions, budgeting, home deposit planning, and long-term compounding. Be conservative, clear, and state assumptions.",
    "photo": "Help Kuschi with photography planning and critique. Camera context: Nikon D850, 70-200 f/2.8, 50 f/1.8, beach maternity/golden hour. Include ISO, aperture, focal length, distance, framing, and time of day when useful.",
    "moto": "Help Kuschi with motorcycle planning and SLICK ride ideas. Bike context: KTM 390 Adventure SW, Road 6 tyres, lowering/ECU research, sport-touring shortlist. Prioritise safety, fit, cost, and practical ride use.",
    "admin": "Act as Kuschi's daily admin assistant for planning, writing, finance notes, travel, photography, motorcycle notes, and general life admin.",
}

ROUTER_PROMPT = """You are Kuschi OS replying via Telegram.

Interpret the user's plain-language message. They should not need to remember
commands. Infer whether they need Riviera brand writing, event proposal help,
kitchen operations, recipe/costing, local business outreach, dev help, Nacho
Taco/CurbOS, Odysseus systems work, finance, photography, motorcycle help, or
daily admin. Reply as a useful assistant, not as a classifier.

Keep Telegram replies concise unless the user clearly needs a full draft.
Use metric units and 24-hour time. For Riviera copy, use warm, confident,
unhurried coastal language and avoid: luxury, exquisite, amazing, awesome,
delicious. Never claim you checked external accounts, files, web, calendar, or
email unless the tool actually did so. Never send email, delete data, change
passwords, or connect accounts without explicit approval.

User Telegram message:
"""


class TelegramBridge:
    def __init__(self, config):
        self.config = config
        self.tg_base = f"https://api.telegram.org/bot{config['telegram_bot_token']}"
        self.state_file = Path(__file__).with_name("state.json")
        self.offset = self._load_state().get("offset", 0)
        self.session_file = Path(__file__).with_name("sessions.json")
        self.sessions = self._load_sessions()
        self.phone_state_file = Path(__file__).with_name("phone_state.json")
        self.phone_state = self._load_phone_state()
        self.notes_file = Path(__file__).with_name("keep_notes.json")
        self.notes_state = self._load_notes_state()
        Path(config["outbox_dir"]).mkdir(parents=True, exist_ok=True)

    def _load_state(self):
        try:
            return json.loads(self.state_file.read_text(encoding="utf-8"))
        except Exception:
            return {}

    def _save_state(self):
        tmp = self.state_file.with_suffix(".tmp")
        tmp.write_text(json.dumps({"offset": self.offset}, indent=2), encoding="utf-8")
        tmp.replace(self.state_file)

    def _load_sessions(self):
        try:
            return json.loads(self.session_file.read_text(encoding="utf-8"))
        except Exception:
            return {}

    def _save_sessions(self):
        tmp = self.session_file.with_suffix(".tmp")
        tmp.write_text(json.dumps(self.sessions, indent=2), encoding="utf-8")
        tmp.replace(self.session_file)

    def _load_phone_state(self):
        try:
            return json.loads(self.phone_state_file.read_text(encoding="utf-8"))
        except Exception:
            return {"chats": {}}

    def _save_phone_state(self):
        tmp = self.phone_state_file.with_suffix(".tmp")
        tmp.write_text(json.dumps(self.phone_state, indent=2), encoding="utf-8")
        tmp.replace(self.phone_state_file)
        try:
            os.chmod(self.phone_state_file, 0o600)
        except Exception:
            pass

    def _load_notes_state(self):
        try:
            return json.loads(self.notes_file.read_text(encoding="utf-8"))
        except Exception:
            return {"notes": []}

    def _save_notes_state(self):
        tmp = self.notes_file.with_suffix(".tmp")
        tmp.write_text(json.dumps(self.notes_state, indent=2), encoding="utf-8")
        tmp.replace(self.notes_file)
        try:
            os.chmod(self.notes_file, 0o600)
        except Exception:
            pass

    def notes(self):
        self.notes_state.setdefault("notes", [])
        return self.notes_state["notes"]

    def phone_chat_state(self, chat_id):
        chats = self.phone_state.setdefault("chats", {})
        state = chats.setdefault(str(chat_id), {
            "latest_location": None,
            "history": [],
            "places": {},
            "geofence_reminders": [],
        })
        state.setdefault("history", [])
        state.setdefault("places", {})
        state.setdefault("geofence_reminders", [])
        return state

    def tg_request(self, method, payload=None, files=None):
        if files:
            return self._multipart_request(method, payload or {}, files)
        data = None
        headers = {}
        if payload is not None:
            data = json.dumps(payload).encode("utf-8")
            headers["Content-Type"] = "application/json"
        req = urllib.request.Request(f"{self.tg_base}/{method}", data=data, headers=headers)
        with urllib.request.urlopen(req, timeout=60) as res:
            return json.loads(res.read().decode("utf-8"))

    def _multipart_request(self, method, fields, files):
        boundary = f"----odysseus{int(time.time() * 1000)}"
        chunks = []
        for name, value in fields.items():
            chunks.append(f"--{boundary}\r\n".encode())
            chunks.append(f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode())
            chunks.append(str(value).encode())
            chunks.append(b"\r\n")
        for name, file_path in files.items():
            path = Path(file_path)
            mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
            chunks.append(f"--{boundary}\r\n".encode())
            chunks.append(
                f'Content-Disposition: form-data; name="{name}"; filename="{path.name}"\r\n'.encode()
            )
            chunks.append(f"Content-Type: {mime}\r\n\r\n".encode())
            chunks.append(path.read_bytes())
            chunks.append(b"\r\n")
        chunks.append(f"--{boundary}--\r\n".encode())
        body = b"".join(chunks)
        req = urllib.request.Request(
            f"{self.tg_base}/{method}",
            data=body,
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        )
        with urllib.request.urlopen(req, timeout=120) as res:
            return json.loads(res.read().decode("utf-8"))

    def ody_request(self, method, path, payload=None, form=None):
        headers = {"Authorization": f"Bearer {self.config['odysseus_api_token']}"}
        data = None
        if form is not None:
            data = urllib.parse.urlencode(form).encode("utf-8")
            headers["Content-Type"] = "application/x-www-form-urlencoded"
        elif payload is not None:
            data = json.dumps(payload).encode("utf-8")
            headers["Content-Type"] = "application/json"
        req = urllib.request.Request(
            self.config["odysseus_base_url"].rstrip("/") + path,
            data=data,
            headers=headers,
            method=method,
        )
        with urllib.request.urlopen(req, timeout=180) as res:
            raw = res.read().decode("utf-8")
            return json.loads(raw) if raw else {}

    def assistant_route(self, chat_id, text):
        try:
            decision = self.ody_request("POST", "/api/assistant/router", payload={
                "source": "telegram",
                "event_type": "message",
                "text": text,
                "chat_id": str(chat_id),
                "context_hints": ["telegram_bridge"],
            })
            if isinstance(decision, dict):
                return decision
        except Exception as exc:
            print(f"Assistant router unavailable, falling back to local classifier: {exc}", flush=True)
        return {}

    def allowed(self, chat_id):
        allowed = self.config.get("allowed_chat_ids") or []
        if not allowed:
            print(f"First-run chat id seen: {chat_id}", flush=True)
            return True
        return int(chat_id) in [int(x) for x in allowed]

    def send_text(self, chat_id, text):
        max_len = int(self.config.get("max_reply_chars", 3500))
        text = text.strip() or "No reply."
        parts = [text[i:i + max_len] for i in range(0, len(text), max_len)]
        for part in parts:
            self.tg_request("sendMessage", {
                "chat_id": chat_id,
                "text": part,
                "disable_web_page_preview": True,
            })

    def send_document(self, chat_id, path, caption=None):
        self.tg_request(
            "sendDocument",
            {"chat_id": chat_id, "caption": caption or ""},
            {"document": path},
        )

    def haversine_m(self, lat1, lon1, lat2, lon2):
        radius = 6371000.0
        p1 = math.radians(float(lat1))
        p2 = math.radians(float(lat2))
        dp = math.radians(float(lat2) - float(lat1))
        dl = math.radians(float(lon2) - float(lon1))
        a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
        return 2 * radius * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    def maps_link(self, lat, lon):
        return f"https://maps.google.com/?q={lat:.6f},{lon:.6f}"

    def read_json_file(self, path):
        try:
            return json.loads(Path(path).read_text(encoding="utf-8"))
        except Exception:
            return {}

    def phone_bridge_config(self):
        runtime = Path.home() / "Library/Application Support/OdysseusPhoneBridge/config.json"
        return self.read_json_file(runtime)

    def phone_bridge_tunnel_url(self):
        configured = self.config.get("phone_bridge_public_url")
        if configured:
            return str(configured).rstrip("/")
        log_paths = [
            Path.home() / "Library/Application Support/OdysseusPhoneBridge/phone-tunnel.err.log",
            Path.home() / "Library/Application Support/OdysseusPhoneBridge/phone-tunnel.log",
        ]
        for path in log_paths:
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            matches = re.findall(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com", text)
            if matches:
                return matches[-1].rstrip("/")
        return ""

    def phone_bridge_local_url(self):
        cfg = self.phone_bridge_config()
        port = int(cfg.get("port") or 8770)
        return f"http://127.0.0.1:{port}"

    def phone_bridge_health(self):
        try:
            req = urllib.request.Request(self.phone_bridge_local_url() + "/health")
            with urllib.request.urlopen(req, timeout=8) as res:
                return json.loads(res.read().decode("utf-8"))
        except Exception as exc:
            return {"ok": False, "error": str(exc)}

    def phone_setup_link(self):
        cfg = self.phone_bridge_config()
        tunnel = self.phone_bridge_tunnel_url()
        setup_token = cfg.get("setup_token") or ""
        if not tunnel:
            return ""
        if setup_token:
            return tunnel + "/setup?" + urllib.parse.urlencode({"setup": setup_token})
        return tunnel + "/setup"

    def phone_bridge_status_text(self):
        health = self.phone_bridge_health()
        tunnel = self.phone_bridge_tunnel_url()
        link = self.phone_setup_link()
        status = health.get("status") or {}
        lines = ["Phone bridge status:"]
        lines.append(f"- Mac bridge: {'online' if health.get('ok') else 'offline'}")
        lines.append(f"- Telegram push: {'configured' if status.get('telegram_configured') else 'not configured'}")
        lines.append(f"- Odysseus LLM: {'configured' if status.get('odysseus_configured') else 'not configured'}")
        if "events" in status:
            lines.append(f"- Phone events received: {status.get('events')}")
        latest = status.get("latest_types") or []
        lines.append(f"- Latest event types: {', '.join(latest) if latest else 'none yet'}")
        lines.append(f"- Public tunnel: {'online' if tunnel else 'not found'}")
        if link:
            lines.append("")
            lines.append("Open this on Android:")
            lines.append(link)
            lines.append("")
            lines.append("Use it for one-tap test, GPS push, and appointment-note push. Telegram remains the main command centre.")
        else:
            lines.append("")
            lines.append("No tunnel link found. The Cloudflare phone tunnel may need a restart on the Mac.")
        return "\n".join(lines)

    def phone_setup_text(self):
        link = self.phone_setup_link()
        health = self.phone_bridge_health()
        if not link:
            return (
                "Phone setup link is not available right now.\n"
                "The Mac phone bridge is "
                + ("online" if health.get("ok") else "offline")
                + ", but I could not find the public Cloudflare tunnel URL."
            )
        return (
            "Odysseus phone setup link:\n"
            f"{link}\n\n"
            "What this gives you now:\n"
            "- one-tap Telegram test from Android\n"
            "- one-tap GPS push to Telegram/Odysseus\n"
            "- quick appointment-note push with LLM summary\n\n"
            "For always-on alarms/notifications/calendar scraping, Android still needs Tasker, Automate, or a companion app permission."
        )

    def format_age(self, unix_seconds):
        age = max(0, int(time.time() - int(unix_seconds or time.time())))
        if age < 90:
            return f"{age}s ago"
        if age < 3600:
            return f"{age // 60}m ago"
        if age < 86400:
            return f"{age // 3600}h {(age % 3600) // 60}m ago"
        return f"{age // 86400}d ago"

    def note_tags(self, text):
        tags = {m.lower() for m in re.findall(r"#([a-zA-Z0-9_-]+)", text or "")}
        lower = (text or "").lower()
        domain_tags = {
            "riviera": r"\b(riviera|wedding|event|venue|tapas|kitchen|prep|coolroom|stock|function)\b",
            "prepflow": r"\b(prepflow|recipe|gp|costing|stocktake|supabase)\b",
            "odysseus": r"\b(odysseus|telegram|bot|bridge|ollama|qwen|llm)\b",
            "nacho": r"\b(nacho|taco|curbos|food truck|square|pos)\b",
            "finance": r"\b(tax|budget|sharesies|vanguard|raiz|super|deposit|etf)\b",
            "photo": r"\b(photo|nikon|d850|shoot|lens|maternity)\b",
            "moto": r"\b(ktm|bike|motorcycle|ride|tyre|road 6)\b",
            "shopping": r"\b(buy|shopping|bunnings|coles|woolies|order)\b",
        }
        for tag, pattern in domain_tags.items():
            if re.search(pattern, lower):
                tags.add(tag)
        return sorted(tags)

    def save_keep_note(self, chat_id, text, source="telegram"):
        clean = re.sub(r"\s+", " ", text or "").strip()
        if not clean:
            return "Nothing to save."
        note = {
            "id": str(int(time.time() * 1000))[-8:],
            "chat_id": int(chat_id),
            "text": clean,
            "tags": self.note_tags(clean),
            "source": source,
            "created_at": int(time.time()),
            "updated_at": int(time.time()),
            "archived": False,
        }
        notes = self.notes()
        notes.append(note)
        limit = int(self.config.get("keep_notes_limit", 1000))
        if len(notes) > limit:
            del notes[:-limit]
        self._save_notes_state()
        google_keep = self.create_google_keep_note(clean)
        note["google_keep"] = google_keep
        note["updated_at"] = int(time.time())
        self._save_notes_state()
        tags = f"\nTags: {', '.join(note['tags'])}" if note["tags"] else ""
        lines = [f"Saved local note {note['id']}."]
        if google_keep.get("ok"):
            lines.append(f"Saved to Google Keep: kitchen@rivierayeppoon.com")
        elif google_keep.get("skipped"):
            lines.append("Google Keep sync skipped.")
        else:
            lines.append("Google Keep sync failed.")
            lines.append(google_keep.get("message", "Unknown Google Keep error."))
        if tags:
            lines.append(tags.strip())
        return "\n".join(lines)

    def keep_note_title(self, text):
        clean = re.sub(r"\s+", " ", text or "").strip()
        if re.search(r"\b(riviera|wedding|event|prep|coolroom|stock|order|kitchen)\b", clean, flags=re.I):
            prefix = "Riviera"
        else:
            prefix = "Odysseus"
        return f"{prefix}: {clean[:70]}".strip()

    def create_google_keep_note(self, text):
        base = (self.config.get("google_bridge_url") or "").rstrip("/")
        if not base:
            return {"ok": False, "skipped": True, "message": "Google bridge URL is not configured."}
        account = self.config.get("google_keep_account", "riviera_kitchen")
        payload = {
            "account": account,
            "title": self.keep_note_title(text),
            "text": text,
        }
        try:
            req = urllib.request.Request(
                base + "/keep/create",
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=30) as res:
                data = json.loads(res.read().decode("utf-8"))
            data["ok"] = bool(data.get("ok"))
            return data
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            try:
                parsed = json.loads(detail)
                message = parsed.get("error") or parsed.get("detail") or detail
            except Exception:
                message = detail
            if "Keep write scope" in message or "keep" in message.lower() and "scope" in message.lower():
                message += (
                    "\nApprove Keep access on the Mac when available: "
                    "python3 ~/Library/Application\\ Support/GoogleReadBridge/authorize.py "
                    "--config ~/Library/Application\\ Support/GoogleReadBridge/config.json "
                    "--account riviera_kitchen"
                )
            return {"ok": False, "message": message[:1800]}
        except Exception as exc:
            return {"ok": False, "message": str(exc)[:1800]}

    def sync_notes_to_google_keep(self, chat_id, limit=25):
        candidates = [
            note for note in self.visible_notes(chat_id)
            if not (note.get("google_keep") or {}).get("ok")
        ]
        if not candidates:
            return "No unsynced local notes."
        synced = 0
        failed = 0
        last_error = ""
        for note in candidates[:limit]:
            result = self.create_google_keep_note(note.get("text", ""))
            note["google_keep"] = result
            note["updated_at"] = int(time.time())
            if result.get("ok"):
                synced += 1
            else:
                failed += 1
                last_error = result.get("message", "")
                break
        self._save_notes_state()
        lines = [f"Google Keep sync: {synced} synced, {failed} failed."]
        if last_error:
            lines.append(last_error)
        if len(candidates) > limit:
            lines.append(f"{len(candidates) - limit} unsynced notes left after this batch.")
        return "\n".join(lines)

    def visible_notes(self, chat_id, include_archived=False):
        return [
            note for note in self.notes()
            if int(note.get("chat_id", chat_id)) == int(chat_id)
            and (include_archived or not note.get("archived"))
        ]

    def note_matches(self, note, query):
        haystack = " ".join([
            note.get("text", ""),
            " ".join(note.get("tags") or []),
            note.get("id", ""),
        ]).lower()
        terms = [t for t in re.split(r"\s+", (query or "").lower().strip()) if t]
        return all(term in haystack for term in terms) if terms else True

    def format_note_line(self, note):
        tags = f" [{', '.join(note.get('tags') or [])}]" if note.get("tags") else ""
        age = self.format_age(note.get("created_at"))
        return f"{note.get('id')} - {age}{tags}: {note.get('text')}"

    def list_keep_notes(self, chat_id, query="", limit=10):
        matches = [
            note for note in reversed(self.visible_notes(chat_id))
            if self.note_matches(note, query)
        ]
        if not matches:
            if query:
                return f"No saved notes found for: {query}"
            return "No saved notes yet. Send: note: order more gloves"
        lines = ["Saved notes:" if not query else f"Saved notes matching '{query}':"]
        for note in matches[:limit]:
            lines.append(self.format_note_line(note))
        if len(matches) > limit:
            lines.append(f"...and {len(matches) - limit} more.")
        return "\n".join(lines)

    def delete_keep_note(self, chat_id, note_id):
        note_id = str(note_id or "").strip()
        for note in self.visible_notes(chat_id, include_archived=True):
            if str(note.get("id")) == note_id:
                note["archived"] = True
                note["updated_at"] = int(time.time())
                self._save_notes_state()
                return f"Archived note {note_id}."
        return f"No note found with id {note_id}."

    def export_keep_notes(self, chat_id):
        notes = list(reversed(self.visible_notes(chat_id)))
        if not notes:
            return None
        outbox = Path(self.config["outbox_dir"]).resolve()
        outbox.mkdir(parents=True, exist_ok=True)
        path = outbox / f"odysseus-keep-notes-{int(time.time())}.md"
        lines = ["# Odysseus Keep Notes", ""]
        for note in notes:
            tags = f" | tags: {', '.join(note.get('tags') or [])}" if note.get("tags") else ""
            lines.append(f"## {note.get('id')} | {self.format_age(note.get('created_at'))}{tags}")
            lines.append("")
            lines.append(note.get("text", ""))
            lines.append("")
        path.write_text("\n".join(lines), encoding="utf-8")
        return path

    def handle_keep_notes_text(self, chat_id, text):
        t = text.strip()
        lower = t.lower()
        if lower in ("/notes", "/keep", "notes", "keep notes", "my notes", "show notes", "list notes"):
            return self.list_keep_notes(chat_id)

        keep_colon_match = re.match(r"(?is)^\s*keep\s*[:\-]\s*(.+?)\s*$", t)
        if keep_colon_match:
            return self.save_keep_note(chat_id, keep_colon_match.group(1))

        save_match = re.match(
            r"(?is)^\s*(?:note|keep note|save note|add note|quick note|brain dump|braindump)\s*[:\-]?\s+(.+?)\s*$",
            t,
        )
        if save_match:
            return self.save_keep_note(chat_id, save_match.group(1))

        remember_match = re.match(r"(?is)^\s*remember\s*(?:this|that)?\s*[:\-]\s*(.+?)\s*$", t)
        if remember_match:
            return self.save_keep_note(chat_id, remember_match.group(1))

        if re.search(r"\b(export|send).*\b(notes|keep notes)\b", lower):
            path = self.export_keep_notes(chat_id)
            if path is None:
                return "No saved notes to export yet."
            self.send_document(chat_id, str(path), caption=f"Exported notes: {path.name}")
            return "__document_sent__"

        if re.search(r"\b(sync|upload|push).*\b(notes|keep notes).*\b(google keep|keep)\b", lower) or re.search(r"\b(sync|upload|push).*\b(google keep|keep).*\b(notes|keep notes)\b", lower):
            return self.sync_notes_to_google_keep(chat_id)

        delete_match = re.match(r"(?i)^\s*(?:delete|remove|archive)\s+note\s+([0-9]+)\s*$", t)
        if delete_match:
            return self.delete_keep_note(chat_id, delete_match.group(1))

        search_match = re.match(r"(?is)^\s*(?:find|search|show|list)\s+(?:my\s+)?(?:keep\s+)?notes?\s*(?:about|for|matching)?\s*(.*?)\s*$", t)
        if search_match and re.search(r"\b(note|notes|keep)\b", lower):
            return self.list_keep_notes(chat_id, search_match.group(1).strip())

        query_match = re.match(r"(?is)^\s*(?:what did i note|what have i noted|what notes do i have)\s*(?:about|for)?\s*(.*?)\s*$", t)
        if query_match:
            return self.list_keep_notes(chat_id, query_match.group(1).strip())

        return ""

    def should_use_notes(self, text):
        return bool(re.search(
            r"\b(note|notes|keep|remember|idea|ideas|todo|to-do|task|tasks|shopping|buy|prep|riviera|odysseus|telegram|nacho|prepflow)\b",
            text,
            flags=re.I,
        ))

    def notes_context(self, chat_id, text):
        if not self.should_use_notes(text):
            return ""
        query = ""
        match = re.search(r"\b(?:about|for|matching)\s+(.+)$", text or "", flags=re.I)
        if match:
            query = match.group(1).strip()
        visible = self.visible_notes(chat_id)
        if not visible:
            return ""
        matches = [n for n in visible if self.note_matches(n, query)] if query else visible
        recent = list(reversed(matches))[:20]
        payload = {
            "note_source": "Telegram/Odysseus Keep-style local notes",
            "query": query,
            "count_available": len(matches),
            "notes": [
                {
                    "id": note.get("id"),
                    "text": note.get("text"),
                    "tags": note.get("tags") or [],
                    "created_unix": note.get("created_at"),
                }
                for note in recent
            ],
        }
        limit = int(self.config.get("max_keep_notes_context_chars", 8000))
        return json.dumps(payload, indent=2)[:limit]

    def handle_location(self, chat_id, msg):
        if not self.config.get("phone_location_enabled", True):
            self.send_text(chat_id, "Phone location intake is disabled in the bridge config.")
            return
        location = msg.get("location") or {}
        if "latitude" not in location or "longitude" not in location:
            return
        state = self.phone_chat_state(chat_id)
        point = {
            "lat": float(location["latitude"]),
            "lon": float(location["longitude"]),
            "accuracy_m": location.get("horizontal_accuracy"),
            "heading": location.get("heading"),
            "live_period": location.get("live_period"),
            "proximity_alert_radius": location.get("proximity_alert_radius"),
            "telegram_message_id": msg.get("message_id"),
            "telegram_date": msg.get("date"),
            "received_at": int(time.time()),
        }
        state["latest_location"] = point
        history = state.setdefault("history", [])
        history.append(point)
        limit = int(self.config.get("phone_location_history_limit", 200))
        if len(history) > limit:
            del history[:-limit]
        self._save_phone_state()
        fired = self.check_geofence_reminders(chat_id, state, point)
        if not fired:
            self.send_text(
                chat_id,
                "Location updated.\n"
                f"{point['lat']:.6f}, {point['lon']:.6f}\n"
                f"{self.maps_link(point['lat'], point['lon'])}",
            )

    def latest_location_text(self, chat_id):
        state = self.phone_chat_state(chat_id)
        loc = state.get("latest_location")
        if not loc:
            return "No phone location stored yet. In Telegram on Android, open the bot -> attach -> Location -> Share My Live Location or Send Selected Location."
        lines = [
            "Latest phone location:",
            f"{loc['lat']:.6f}, {loc['lon']:.6f}",
            f"Updated: {self.format_age(loc.get('received_at'))}",
            self.maps_link(loc["lat"], loc["lon"]),
        ]
        accuracy = loc.get("accuracy_m")
        if accuracy:
            lines.insert(3, f"Accuracy: ~{accuracy}m")
        distances = []
        for name, place in state.get("places", {}).items():
            dist = self.haversine_m(loc["lat"], loc["lon"], place["lat"], place["lon"])
            distances.append((dist, name))
        if distances:
            lines.append("")
            lines.append("Saved places:")
            for dist, name in sorted(distances)[:6]:
                lines.append(f"- {name}: {dist:.0f}m away")
        return "\n".join(lines)

    def forget_location(self, chat_id):
        state = self.phone_chat_state(chat_id)
        state["latest_location"] = None
        state["history"] = []
        self._save_phone_state()
        return "Stored phone location/history deleted for this Telegram chat."

    def save_place_here(self, chat_id, name):
        name = re.sub(r"\s+", " ", name or "").strip()
        if not name:
            return "Use: set place Riviera here"
        state = self.phone_chat_state(chat_id)
        loc = state.get("latest_location")
        if not loc:
            return "No latest location stored. Send/share location first, then say: set place Riviera here"
        state.setdefault("places", {})[name] = {
            "lat": loc["lat"],
            "lon": loc["lon"],
            "created_at": int(time.time()),
        }
        self._save_phone_state()
        return f"Saved place '{name}' at {loc['lat']:.6f}, {loc['lon']:.6f}."

    def list_places(self, chat_id):
        state = self.phone_chat_state(chat_id)
        places = state.get("places", {})
        if not places:
            return "No saved places yet. Send/share location, then say: set place Riviera here"
        lines = ["Saved places:"]
        for name, place in sorted(places.items()):
            lines.append(f"- {name}: {place['lat']:.6f}, {place['lon']:.6f}")
        return "\n".join(lines)

    def delete_place(self, chat_id, name):
        name = re.sub(r"\s+", " ", name or "").strip()
        state = self.phone_chat_state(chat_id)
        places = state.get("places", {})
        match = next((key for key in places if key.lower() == name.lower()), None)
        if not match:
            return f"No saved place named '{name}'."
        places.pop(match, None)
        self._save_phone_state()
        return f"Deleted saved place '{match}'."

    def add_geofence_reminder(self, chat_id, place_name, reminder, radius_m=200):
        state = self.phone_chat_state(chat_id)
        places = state.get("places", {})
        place_key = next((key for key in places if key.lower() == place_name.lower()), None)
        if not place_key:
            return f"I don't have a place called '{place_name}'. Save one first with: set place {place_name} here"
        reminder = reminder.strip()
        if not reminder:
            return "Tell me what to remind you. Example: remind me when I get to Riviera to check the coolroom."
        item = {
            "id": str(int(time.time() * 1000)),
            "place": place_key,
            "text": reminder,
            "radius_m": int(radius_m),
            "created_at": int(time.time()),
            "fired_at": None,
            "enabled": True,
        }
        state.setdefault("geofence_reminders", []).append(item)
        self._save_phone_state()
        return f"Geofence reminder set for '{place_key}' within {int(radius_m)}m: {reminder}"

    def list_geofence_reminders(self, chat_id):
        state = self.phone_chat_state(chat_id)
        reminders = [r for r in state.get("geofence_reminders", []) if r.get("enabled")]
        if not reminders:
            return "No active geofence reminders."
        lines = ["Active geofence reminders:"]
        for r in reminders:
            status = "fired" if r.get("fired_at") else "waiting"
            lines.append(f"- {r.get('place')} ({r.get('radius_m', 200)}m, {status}): {r.get('text')}")
        return "\n".join(lines)

    def check_geofence_reminders(self, chat_id, state, point):
        places = state.get("places", {})
        fired = False
        cooldown = int(self.config.get("phone_geofence_repeat_cooldown_seconds", 12 * 3600))
        now = int(time.time())
        for reminder in state.get("geofence_reminders", []):
            if not reminder.get("enabled"):
                continue
            place = places.get(reminder.get("place"))
            if not place:
                continue
            if reminder.get("fired_at") and now - int(reminder["fired_at"]) < cooldown:
                continue
            dist = self.haversine_m(point["lat"], point["lon"], place["lat"], place["lon"])
            if dist <= float(reminder.get("radius_m", 200)):
                reminder["fired_at"] = now
                fired = True
                self.send_text(
                    chat_id,
                    f"Location reminder: {reminder.get('text')}\n"
                    f"Place: {reminder.get('place')} ({dist:.0f}m away)",
                )
        if fired:
            self._save_phone_state()
        return fired

    def handle_phone_text(self, chat_id, text):
        t = text.strip()
        lower = t.lower()
        if text in ("/phone", "/phone_setup", "/phone_status"):
            return self.phone_bridge_status_text() if text == "/phone_status" else self.phone_setup_text()
        if re.search(r"\b(phone|android).*(setup|link|dashboard|web|page)\b", lower):
            return self.phone_setup_text()
        if re.search(r"\b(telegram advantage|use telegram advantage|telegram.*phone setup)\b", lower):
            return self.phone_setup_text()
        if re.search(r"\b(phone bridge status|android bridge status|phone status)\b", lower):
            return self.phone_bridge_status_text()
        if re.search(r"\b(where am i|location status|gps status|phone location)\b", lower):
            return self.latest_location_text(chat_id)
        if re.search(r"\b(forget|delete|clear).*\b(location|gps)\b", lower):
            return self.forget_location(chat_id)
        match = re.match(r"(?i)^\s*set\s+place\s+(.+?)\s+here\s*$", t)
        if match:
            return self.save_place_here(chat_id, match.group(1))
        match = re.match(r"(?i)^\s*(delete|remove)\s+place\s+(.+?)\s*$", t)
        if match:
            return self.delete_place(chat_id, match.group(2))
        if re.search(r"\b(list places|saved places|places)\b", lower):
            return self.list_places(chat_id)
        if re.search(r"\b(geofence reminders|location reminders)\b", lower):
            return self.list_geofence_reminders(chat_id)
        match = re.match(
            r"(?i)^\s*remind\s+me\s+when\s+i\s+get\s+to\s+(.+?)\s+to\s+(.+?)(?:\s+within\s+(\d+)\s*m)?\s*$",
            t,
        )
        if match:
            radius = int(match.group(3) or self.config.get("phone_default_geofence_radius_m", 200))
            return self.add_geofence_reminder(chat_id, match.group(1), match.group(2), radius)
        return ""

    def latest_outbox_file(self):
        outbox = Path(self.config["outbox_dir"]).resolve()
        files = [p for p in outbox.iterdir() if p.is_file() and not p.name.startswith(".")]
        if not files:
            return None
        return max(files, key=lambda p: p.stat().st_mtime)

    def should_use_google(self, text):
        return bool(re.search(
            r"\b(google|calendar|calendars|schedule|agenda|appointment|appointments|drive|doc|docs|sheet|slides|gmail|email|mail|inbox|unread|notebooklm|notebook|riviera|event|events|wedding|function|venue|kitchen notes|prep info|prep requirements)\b",
            text,
            flags=re.I,
        ))

    def should_use_microsoft(self, text):
        return bool(re.search(
            r"\b(microsoft|office|outlook|365|calendar|calendars|schedule|agenda|appointment|appointments|riviera|lanegroup|lanegroupcq|lane group|event|events|wedding|function|venue|kitchen notes|prep info|prep requirements)\b",
            text,
            flags=re.I,
        ))

    def google_context(self, text):
        base = (self.config.get("google_bridge_url") or "").rstrip("/")
        if not base or not self.should_use_google(text):
            return ""
        try:
            url = base + "/context?" + urllib.parse.urlencode({"q": text})
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=45) as res:
                data = json.loads(res.read().decode("utf-8"))
            limit = int(self.config.get("max_google_context_chars", 30000))
            return json.dumps(data, indent=2)[:limit]
        except Exception as exc:
            return json.dumps({
                "google_read_bridge": "unavailable_or_not_connected",
                "error": str(exc),
                "note": "If the user asked for Google data, say the Google read bridge needs OAuth setup or is unavailable.",
            }, indent=2)

    def microsoft_context(self, text):
        base = (self.config.get("microsoft_bridge_url") or "").rstrip("/")
        if not base or not self.should_use_microsoft(text):
            return ""
        try:
            url = base + "/context?" + urllib.parse.urlencode({"q": text})
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=45) as res:
                data = json.loads(res.read().decode("utf-8"))
            limit = int(self.config.get("max_microsoft_context_chars", 30000))
            return json.dumps(data, indent=2)[:limit]
        except Exception as exc:
            return json.dumps({
                "microsoft_read_bridge": "unavailable_or_not_connected",
                "error": str(exc),
                "note": "If the user asked for Microsoft 365 data, say the Microsoft read bridge needs OAuth setup or is unavailable.",
            }, indent=2)

    def classify(self, text):
        t = text.lower()
        if re.search(r"\b(file|send.*file|latest file|document|pdf|download)\b", t):
            return "file"
        if re.search(r"\b(recipe|cost|gp|allergen|scale|yield|portion|pax)\b", t):
            return "recipe"
        if re.search(r"\b(odysseus|telegram|google bridge|microsoft bridge|ollama|local llm|qwen|dashboard|launch agent|launchagent|self monitoring|autopilot)\b", t):
            return "systems"
        if re.search(r"\b(nacho|taco|food truck|curbos|pos|square|kitchen display|customer display)\b", t):
            return "nacho"
        if re.search(r"\b(invest|sharesies|vanguard|raiz|super|tax|deduction|home deposit|budget|brokerage|etf|dividend)\b", t):
            return "finance"
        if re.search(r"\b(photo|photography|nikon|d850|lens|shoot|maternity|aperture|iso|golden hour)\b", t):
            return "photo"
        if re.search(r"\b(motorcycle|bike|ktm|390 adventure|tyre|tire|road 6|lowering|ecu|cardo|sena|convoy|ride)\b", t):
            return "moto"
        if re.search(r"\b(sop|prep|mise|stock|ordering|kitchen|service timeline)\b", t):
            return "kitchen"
        if re.search(r"\b(riviera|caption|instagram|facebook|wedding|event|venue|tapas)\b", t):
            if re.search(r"\b(proposal|package|quote|function|wedding brief)\b", t):
                return "proposal"
            return "riviera"
        if re.search(r"\b(website|audit|outreach|lead|client|offer|proposal|follow[- ]?up|business)\b", t):
            return "business"
        if re.search(r"\b(code|bug|app|prepflow|slick|curbos|supabase|vercel|kotlin|android|error)\b", t):
            return "dev"
        return "admin"

    def session_for_chat(self, chat_id, kind):
        key = f"{chat_id}:{kind}"
        if key in self.sessions:
            return self.sessions[key]
        form = {
            "name": f"Telegram {kind}",
            "endpoint_id": self.config["endpoint_id"],
            "model": self.config["fast_model"] if kind == "admin" else self.config["default_model"],
            "rag": "true",
        }
        session = self.ody_request("POST", "/api/session", form=form)
        self.sessions[key] = session["id"]
        self._save_sessions()
        return session["id"]

    def answer(self, chat_id, text):
        local_kind = self.classify(text)
        if local_kind == "file":
            kind = "file"
            decision = {}
        else:
            decision = self.assistant_route(chat_id, text)
            kind = decision.get("telegram_kind") or local_kind
        if kind == "file":
            latest = self.latest_outbox_file()
            if latest is None:
                self.send_text(chat_id, "No files are waiting in the Telegram outbox yet.")
                return
            self.send_document(chat_id, str(latest), caption=f"Latest outbox file: {latest.name}")
            return

        session_id = self.session_for_chat(chat_id, kind)
        google_context = self.google_context(text)
        microsoft_context = self.microsoft_context(text)
        notes_context = self.notes_context(chat_id, text)
        trusted_context = ""
        if notes_context:
            trusted_context += (
                "Trusted local Keep-style notes follow. These notes were saved by Kuschi through Telegram/Odysseus. "
                "Use them directly when the user asks about notes, reminders, ideas, shopping, prep, or previous thoughts.\n"
                + notes_context
                + "\n\n"
            )
        if google_context:
            trusted_context += (
                "Trusted Google read-only context follows. This context was fetched from Kuschi's connected Google accounts for this exact request. "
                "Use it directly. Do not say you lack access when this block contains calendar/email/drive data.\n"
                + google_context
                + "\n\n"
            )
        if microsoft_context:
            trusted_context += (
                "Trusted Microsoft 365 read-only context follows. This context was fetched from Kuschi's connected Microsoft accounts for this exact request. "
                "Use it directly. Do not say you lack access when this block contains calendar data.\n"
                + microsoft_context
                + "\n\n"
            )
        if decision:
            trusted_context += (
                "Trusted assistant router decision follows. Use this for intent and safety policy, but still answer the user's message.\n"
                + json.dumps({
                    "intent": decision.get("intent"),
                    "confidence": decision.get("confidence"),
                    "requires_approval": decision.get("requires_approval"),
                    "suggested_actions": decision.get("suggested_actions") or [],
                    "router_reply": decision.get("reply"),
                }, indent=2)
                + "\n\n"
            )
        routed_message = (
            DOMAIN_PROMPTS.get(kind, DOMAIN_PROMPTS["admin"])
            + "\n\n"
            + trusted_context
            + ROUTER_PROMPT
            + text
        )
        response = self.ody_request("POST", "/api/chat", payload={
            "message": routed_message,
            "session": session_id,
            "attachments": [],
            "use_web": bool(re.search(r"https?://|\\b(current|latest|research|look up|search)\\b", text.lower())),
            "use_research": False,
        })
        self.send_text(chat_id, response.get("response", "No response."))

    def handle_update(self, update):
        msg = update.get("message") or update.get("edited_message") or {}
        chat = msg.get("chat") or {}
        chat_id = chat.get("id")
        text = (msg.get("text") or msg.get("caption") or "").strip()
        if not chat_id:
            return
        if not self.allowed(chat_id):
            self.send_text(chat_id, "This bot is locked to Kuschi's approved Telegram chat.")
            return
        if msg.get("location"):
            self.handle_location(chat_id, msg)
            return
        if not text:
            return
        if text in ("/start", "/help"):
            self.send_text(chat_id, "Send normal messages. I will infer whether you need Riviera, kitchen, recipe, business, dev, admin, files, or phone-location help.")
            return
        try:
            notes_reply = self.handle_keep_notes_text(chat_id, text)
            if notes_reply:
                if notes_reply != "__document_sent__":
                    self.send_text(chat_id, notes_reply)
                return
            phone_reply = self.handle_phone_text(chat_id, text)
            if phone_reply:
                self.send_text(chat_id, phone_reply)
                return
            self.send_text(chat_id, "Working...")
            self.answer(chat_id, text)
        except Exception as exc:
            print(f"Error handling update: {exc}", file=sys.stderr, flush=True)
            self.send_text(chat_id, f"Error: {exc}")

    def run(self):
        print("Telegram Odysseus bridge running.", flush=True)
        while True:
            try:
                updates = self.tg_request("getUpdates", {
                    "offset": self.offset,
                    "timeout": int(self.config.get("poll_timeout_seconds", 25)),
                    "allowed_updates": ["message", "edited_message"],
                })
                for update in updates.get("result", []):
                    self.offset = max(self.offset, int(update["update_id"]) + 1)
                    self._save_state()
                    self.handle_update(update)
            except KeyboardInterrupt:
                raise
            except Exception as exc:
                print(f"Polling error: {exc}", file=sys.stderr, flush=True)
                time.sleep(5)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    config = json.loads(Path(args.config).read_text(encoding="utf-8"))
    required = ["telegram_bot_token", "odysseus_api_token"]
    missing = [key for key in required if not config.get(key) or str(config.get(key)).startswith("PASTE_")]
    if missing:
        raise SystemExit(f"Missing required config values: {', '.join(missing)}")
    TelegramBridge(config).run()


if __name__ == "__main__":
    main()
