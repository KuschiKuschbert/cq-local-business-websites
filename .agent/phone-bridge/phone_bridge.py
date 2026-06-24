#!/usr/bin/env python3
import argparse
import html
import json
import secrets
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def read_json(path, default=None):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception:
        return default if default is not None else {}


def write_json(path, data, mode=0o600):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)
    try:
        path.chmod(mode)
    except Exception:
        pass


def http_json(url, *, method="GET", payload=None, form=None, headers=None, timeout=45):
    req_headers = dict(headers or {})
    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        req_headers["Content-Type"] = "application/json"
    elif form is not None:
        data = urllib.parse.urlencode(form).encode("utf-8")
        req_headers["Content-Type"] = "application/x-www-form-urlencoded"
    req = urllib.request.Request(url, data=data, headers=req_headers, method=method)
    with urllib.request.urlopen(req, timeout=timeout) as res:
        raw = res.read().decode("utf-8")
        return json.loads(raw) if raw else {}


class PhoneBridge:
    def __init__(self, config_path):
        self.config_path = Path(config_path)
        self.config = read_json(self.config_path)
        if not self.config.get("auth_token") or str(self.config.get("auth_token")).startswith("CHANGE_ME"):
            self.config["auth_token"] = secrets.token_urlsafe(32)
            write_json(self.config_path, self.config)
        if not self.config.get("setup_token") or str(self.config.get("setup_token")).startswith("CHANGE_ME"):
            self.config["setup_token"] = secrets.token_urlsafe(32)
            write_json(self.config_path, self.config)
        self.state_path = Path(self.config.get("state_path") or self.config_path.with_name("phone_state.json"))
        self.state = read_json(self.state_path, {
            "events": [],
            "latest": {},
            "sessions": {},
            "created_at": now_iso(),
        })
        self.telegram_config = read_json(self.config.get("telegram_config_path", ""))

    def save_state(self):
        write_json(self.state_path, self.state)

    def check_token(self, headers):
        expected = self.config.get("auth_token") or ""
        supplied = headers.get("X-Phone-Bridge-Token") or ""
        auth = headers.get("Authorization") or ""
        if auth.startswith("Bearer "):
            supplied = auth[7:]
        return bool(expected and secrets.compare_digest(str(expected), str(supplied)))

    def status(self):
        events = self.state.get("events") or []
        latest = self.state.get("latest") or {}
        return {
            "configured": bool(self.config.get("auth_token")),
            "events": len(events),
            "latest_types": sorted(latest.keys()),
            "telegram_configured": bool(self.telegram_config.get("telegram_bot_token") and self.telegram_config.get("allowed_chat_ids")),
            "odysseus_configured": bool(self.telegram_config.get("odysseus_api_token")),
        }

    def setup_authorized(self, query):
        params = urllib.parse.parse_qs(query or "")
        supplied = (params.get("setup") or [""])[0]
        expected = self.config.get("setup_token") or ""
        return bool(expected and secrets.compare_digest(str(expected), str(supplied)))

    def setup_page(self, authorized=False):
        token = self.config.get("auth_token") if authorized else ""
        setup_state = "ready" if authorized else "locked"
        token_js = json.dumps(token)
        state_js = json.dumps(setup_state)
        return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Odysseus Phone Link</title>
  <style>
    :root {{
      color-scheme: light dark;
      --bg: #0d1117;
      --panel: #151b23;
      --text: #e6edf3;
      --muted: #8b949e;
      --line: #30363d;
      --accent: #2f81f7;
      --ok: #238636;
      --danger: #da3633;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.45;
    }}
    main {{
      width: min(720px, 100%);
      margin: 0 auto;
      padding: 18px;
    }}
    h1 {{
      font-size: 24px;
      margin: 10px 0 6px;
      letter-spacing: 0;
    }}
    p {{ color: var(--muted); margin: 0 0 16px; }}
    section {{
      border: 1px solid var(--line);
      background: var(--panel);
      border-radius: 8px;
      padding: 14px;
      margin: 12px 0;
    }}
    h2 {{ font-size: 16px; margin: 0 0 10px; }}
    button, input {{
      width: 100%;
      min-height: 44px;
      border-radius: 8px;
      border: 1px solid var(--line);
      font: inherit;
    }}
    button {{
      background: var(--accent);
      color: white;
      font-weight: 650;
      margin: 6px 0;
    }}
    button.secondary {{ background: transparent; color: var(--text); }}
    input {{
      background: #0d1117;
      color: var(--text);
      padding: 10px 12px;
      margin: 5px 0 9px;
    }}
    label {{
      display: block;
      color: var(--muted);
      font-size: 13px;
      margin-top: 8px;
    }}
    pre {{
      white-space: pre-wrap;
      overflow-wrap: anywhere;
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 10px;
      color: var(--text);
      background: #010409;
      min-height: 52px;
    }}
    .locked {{ border-color: var(--danger); }}
    .ok {{ border-color: var(--ok); }}
  </style>
</head>
<body>
  <main>
    <h1>Odysseus Phone Link</h1>
    <p>Telegram stays the control centre. This page only sends phone-side events when you tap a button.</p>

    <section id="gate" class="{html.escape(setup_state)}">
      <h2>Status</h2>
      <pre id="status">Checking bridge...</pre>
      <button class="secondary" onclick="checkHealth()">Refresh status</button>
    </section>

    <section>
      <h2>One-Tap Phone Events</h2>
      <button onclick="sendTest()">Send test to Telegram</button>
      <button onclick="sendLocation()">Send current GPS to Telegram</button>
    </section>

    <section>
      <h2>Appointment Note</h2>
      <label for="title">Title</label>
      <input id="title" placeholder="Riviera tasting">
      <label for="time">Time</label>
      <input id="time" placeholder="2026-06-22 14:00">
      <label for="location">Location</label>
      <input id="location" placeholder="Riviera Yeppoon">
      <button onclick="sendAppointment()">Send appointment note</button>
    </section>

    <section>
      <h2>Result</h2>
      <pre id="result">Ready.</pre>
    </section>
  </main>
  <script>
    const PHONE_TOKEN = {token_js};
    const SETUP_STATE = {state_js};
    const statusEl = document.getElementById("status");
    const resultEl = document.getElementById("result");

    function show(target, value) {{
      target.textContent = typeof value === "string" ? value : JSON.stringify(value, null, 2);
    }}

    async function postEvent(payload) {{
      if (!PHONE_TOKEN) {{
        throw new Error("This setup link is locked. Ask Telegram for a fresh phone setup link.");
      }}
      const res = await fetch("/event", {{
        method: "POST",
        headers: {{
          "Content-Type": "application/json",
          "X-Phone-Bridge-Token": PHONE_TOKEN
        }},
        body: JSON.stringify(payload)
      }});
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Phone bridge request failed");
      return data;
    }}

    async function checkHealth() {{
      try {{
        const res = await fetch("/health");
        const data = await res.json();
        show(statusEl, {{
          setup: SETUP_STATE,
          bridge: data.ok ? "online" : "unknown",
          ...data.status
        }});
      }} catch (err) {{
        show(statusEl, "Bridge unreachable: " + err.message);
      }}
    }}

    async function sendTest() {{
      try {{
        show(resultEl, "Sending test...");
        const data = await postEvent({{
          type: "notification",
          notify: true,
          data: {{
            app: "Odysseus Phone Link",
            title: "Phone link test",
            text: "Android browser reached the Mac bridge through Telegram setup."
          }}
        }});
        show(resultEl, data);
      }} catch (err) {{
        show(resultEl, err.message);
      }}
    }}

    async function sendLocation() {{
      try {{
        show(resultEl, "Waiting for GPS permission...");
        navigator.geolocation.getCurrentPosition(async pos => {{
          try {{
            const data = await postEvent({{
              type: "location",
              notify: true,
              data: {{
                lat: pos.coords.latitude,
                lon: pos.coords.longitude,
                accuracy_m: pos.coords.accuracy
              }}
            }});
            show(resultEl, data);
          }} catch (err) {{
            show(resultEl, err.message);
          }}
        }}, err => show(resultEl, err.message), {{
          enableHighAccuracy: true,
          timeout: 20000,
          maximumAge: 30000
        }});
      }} catch (err) {{
        show(resultEl, err.message);
      }}
    }}

    async function sendAppointment() {{
      try {{
        const title = document.getElementById("title").value.trim() || "Appointment";
        const time = document.getElementById("time").value.trim();
        const location = document.getElementById("location").value.trim();
        show(resultEl, "Sending appointment note...");
        const data = await postEvent({{
          type: "appointment_reminder",
          notify: true,
          ask_llm: true,
          data: {{ title, start: time, location }}
        }});
        show(resultEl, data);
      }} catch (err) {{
        show(resultEl, err.message);
      }}
    }}

    checkHealth();
  </script>
</body>
</html>
"""

    def record_event(self, event):
        event = dict(event or {})
        event_type = str(event.get("type") or "generic").strip().lower()
        event["type"] = event_type
        event.setdefault("source", "android")
        event.setdefault("received_at", now_iso())
        event.setdefault("received_unix", int(time.time()))
        event.setdefault("id", f"{int(time.time() * 1000)}-{secrets.token_hex(3)}")
        events = self.state.setdefault("events", [])
        events.append(event)
        max_events = int(self.config.get("max_events", 500))
        if len(events) > max_events:
            del events[:-max_events]
        self.state.setdefault("latest", {})[event_type] = event
        self.save_state()
        return event

    def telegram_chat_ids(self):
        return [int(x) for x in (self.telegram_config.get("allowed_chat_ids") or [])]

    def send_telegram(self, text):
        token = self.telegram_config.get("telegram_bot_token")
        chat_ids = self.telegram_chat_ids()
        if not token or not chat_ids:
            return False
        ok = True
        for chat_id in chat_ids[:3]:
            try:
                http_json(
                    f"https://api.telegram.org/bot{token}/sendMessage",
                    method="POST",
                    payload={
                        "chat_id": chat_id,
                        "text": text[:3900],
                        "disable_web_page_preview": True,
                    },
                    timeout=30,
                )
            except Exception:
                ok = False
        return ok

    def odysseus_headers(self):
        token = self.telegram_config.get("odysseus_api_token")
        return {"Authorization": f"Bearer {token}"} if token else {}

    def odysseus_request(self, method, path, payload=None, form=None, timeout=90):
        base = (self.telegram_config.get("odysseus_base_url") or "http://127.0.0.1:7860").rstrip("/")
        headers = self.odysseus_headers()
        if form is not None:
            headers["Content-Type"] = "application/x-www-form-urlencoded"
        return http_json(base + path, method=method, payload=payload, form=form, headers=headers, timeout=timeout)

    def assistant_route(self, event):
        try:
            decision = self.odysseus_request("POST", "/api/assistant/router", payload={
                "source": "phone",
                "event_type": event.get("type") or "event",
                "text": self.event_message(event),
                "timestamp": event.get("received_at") or event.get("created_at"),
                "payload": event,
                "context_hints": ["phone_bridge"],
            }, timeout=30)
            if isinstance(decision, dict):
                return decision
        except Exception:
            pass
        return {}

    def odysseus_session(self):
        sessions = self.state.setdefault("sessions", {})
        if sessions.get("phone_assistant"):
            return sessions["phone_assistant"]
        form = {
            "name": "Android Phone Assistant",
            "endpoint_id": self.telegram_config.get("endpoint_id", ""),
            "model": self.telegram_config.get("fast_model", "qwen3:8b"),
            "rag": "false",
        }
        session = self.odysseus_request("POST", "/api/session", form=form, timeout=30)
        sessions["phone_assistant"] = session["id"]
        self.save_state()
        return session["id"]

    def summarize_with_odysseus(self, event, decision=None):
        if not self.config.get("llm_enabled", True):
            return ""
        try:
            session_id = self.odysseus_session()
            router_block = ""
            if decision:
                router_block = "\nAssistant router decision:\n" + json.dumps({
                    "intent": decision.get("intent"),
                    "confidence": decision.get("confidence"),
                    "requires_approval": decision.get("requires_approval"),
                    "suggested_actions": decision.get("suggested_actions") or [],
                    "router_reply": decision.get("reply"),
                }, indent=2) + "\n"
            prompt = """You are Kuschi OS phone assistant.

Interpret this Android phone event and reply with a concise Telegram-ready action message.
Use metric units and 24-hour time. Do not claim extra access beyond this event.
For appointment/calendar events: include time, title, location, prep/travel risk if obvious.
For alarm snapshots: state the next alarm clearly.
For notifications: summarise only if it looks appointment/work relevant.
Never send, post, book, delete, pay, or change anything without explicit approval.
""" + router_block + """

Android event JSON:
""" + json.dumps(event, indent=2)
            response = self.odysseus_request("POST", "/api/chat", payload={
                "message": prompt,
                "session": session_id,
                "attachments": [],
                "use_web": False,
                "use_research": False,
            }, timeout=120)
            return (response.get("response") or "").strip()
        except Exception:
            return ""

    def event_message(self, event):
        event_type = event.get("type")
        data = event.get("data") or {}
        if event.get("message"):
            return str(event["message"])
        if event_type == "appointment_reminder":
            title = data.get("title") or event.get("title") or "Appointment"
            start = data.get("start") or data.get("time") or ""
            location = data.get("location") or ""
            bits = [f"Appointment: {title}"]
            if start:
                bits.append(f"Time: {start}")
            if location:
                bits.append(f"Location: {location}")
            return "\n".join(bits)
        if event_type == "alarm_snapshot":
            next_alarm = data.get("next_alarm") or data.get("next") or event.get("next_alarm")
            alarms = data.get("alarms") or []
            if next_alarm:
                return f"Phone alarm update\nNext alarm: {next_alarm}"
            return f"Phone alarm update\nAlarms reported: {len(alarms)}"
        if event_type == "calendar_snapshot":
            items = data.get("events") or data.get("appointments") or []
            if not items:
                return "Phone calendar snapshot: no events reported."
            lines = ["Phone calendar snapshot:"]
            for item in items[:6]:
                if isinstance(item, dict):
                    lines.append(f"- {item.get('start', '')} {item.get('title') or item.get('summary') or 'Event'}".strip())
                else:
                    lines.append(f"- {item}")
            return "\n".join(lines)
        if event_type == "notification":
            app = data.get("app") or event.get("app") or "Android"
            title = data.get("title") or ""
            text = data.get("text") or ""
            return f"Phone notification from {app}\n{title}\n{text}".strip()
        if event_type == "battery":
            level = data.get("level") or event.get("level")
            charging = data.get("charging")
            suffix = " charging" if charging else ""
            return f"Phone battery: {level}%{suffix}" if level is not None else "Phone battery update."
        if event_type == "location":
            lat = data.get("lat") or data.get("latitude") or event.get("lat")
            lon = data.get("lon") or data.get("longitude") or event.get("lon")
            if lat is not None and lon is not None:
                return f"Phone location update\n{float(lat):.6f}, {float(lon):.6f}\nhttps://maps.google.com/?q={float(lat):.6f},{float(lon):.6f}"
            return "Phone location update."
        return f"Phone event: {event_type}"

    def should_notify(self, event):
        if event.get("notify") is True:
            return True
        notify_types = set(self.config.get("notify_event_types") or [])
        return event.get("type") in notify_types

    def should_llm(self, event):
        if event.get("ask_llm") is True:
            return True
        llm_types = set(self.config.get("llm_event_types") or [])
        return event.get("type") in llm_types

    def handle_event(self, event):
        event = self.record_event(event)
        decision = self.assistant_route(event)
        message = ""
        if self.should_llm(event):
            message = self.summarize_with_odysseus(event, decision)
        if not message:
            message = self.event_message(event)
        notified = False
        if self.should_notify(event):
            notified = self.send_telegram(message)
        return {
            "ok": True,
            "event_id": event.get("id"),
            "type": event.get("type"),
            "notified": notified,
            "message": message,
            "assistant_router": {
                "intent": decision.get("intent"),
                "confidence": decision.get("confidence"),
                "requires_approval": decision.get("requires_approval"),
            } if decision else None,
        }


class Handler(BaseHTTPRequestHandler):
    bridge = None

    def send_json(self, status, payload):
        raw = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def send_html(self, status, html_text):
        raw = html_text.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def read_body(self):
        length = int(self.headers.get("Content-Length") or 0)
        if length <= 0:
            return {}
        raw = self.rfile.read(length).decode("utf-8")
        return json.loads(raw) if raw else {}

    def require_auth(self):
        if self.bridge.check_token(self.headers):
            return True
        self.send_json(401, {"error": "unauthorized"})
        return False

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path in ("/", "/setup", "/phone"):
            self.send_html(200, self.bridge.setup_page(self.bridge.setup_authorized(parsed.query)))
            return
        if parsed.path.startswith("/health"):
            self.send_json(200, {"ok": True, "status": self.bridge.status()})
            return
        if parsed.path.startswith("/state"):
            if not self.require_auth():
                return
            self.send_json(200, self.bridge.state)
            return
        self.send_json(404, {"error": "not_found"})

    def do_POST(self):
        if self.path.startswith("/event"):
            if not self.require_auth():
                return
            try:
                self.send_json(200, self.bridge.handle_event(self.read_body()))
            except Exception as exc:
                self.send_json(500, {"error": str(exc)})
            return
        self.send_json(404, {"error": "not_found"})

    def log_message(self, fmt, *args):
        return


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    bridge = PhoneBridge(args.config)
    Handler.bridge = bridge
    host = bridge.config.get("host", "0.0.0.0")
    port = int(bridge.config.get("port", 8770))
    server = ThreadingHTTPServer((host, port), Handler)
    print(f"Odysseus phone bridge running on http://{host}:{port}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
