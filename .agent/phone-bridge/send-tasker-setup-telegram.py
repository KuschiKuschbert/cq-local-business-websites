#!/usr/bin/env python3
import json
import os
import urllib.request
from pathlib import Path


PHONE_CONFIG = Path.home() / "Library/Application Support/OdysseusPhoneBridge/config.json"
TELEGRAM_CONFIG = Path.home() / "Library/Application Support/OdysseusTelegramBridge/config.json"
TUNNEL_LOG = Path.home() / "Library/Application Support/OdysseusPhoneBridge/phone-tunnel.err.log"


def post_json(url, payload):
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as res:
        return json.loads(res.read().decode("utf-8"))


def main():
    phone = json.loads(PHONE_CONFIG.read_text(encoding="utf-8"))
    telegram = json.loads(TELEGRAM_CONFIG.read_text(encoding="utf-8"))
    token = telegram["telegram_bot_token"]
    chat_ids = telegram.get("allowed_chat_ids") or []
    if not chat_ids:
        raise SystemExit("No allowed Telegram chat IDs configured.")
    tunnel_urls = []
    if TUNNEL_LOG.exists():
        for part in TUNNEL_LOG.read_text(encoding="utf-8", errors="replace").split():
            if part.startswith("https://") and "trycloudflare.com" in part:
                tunnel_urls.append(part.strip())
    base = tunnel_urls[-1].rstrip("/") if tunnel_urls else ""
    if not base:
        mac_ip = os.popen("ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null").read().strip()
        base = f"http://{mac_ip or '192.168.20.26'}:{phone.get('port', 8770)}"
    url = f"{base}/event"
    text = f"""Odysseus Phone Bridge Tasker setup

URL:
{url}

Headers:
Content-Type: application/json
X-Phone-Bridge-Token: {phone['auth_token']}

Tasker:
Net -> HTTP Request
Method: POST
URL: {url}
Headers:
Content-Type:application/json
X-Phone-Bridge-Token:{phone['auth_token']}

Start with this battery test body:
{{
  "type": "battery",
  "notify": false,
  "data": {{
    "level": "%BATT",
    "charging": "%PACTIVE"
  }}
}}

Appointment body:
{{
  "type": "appointment_reminder",
  "notify": true,
  "ask_llm": true,
  "data": {{
    "title": "%CALTITLE",
    "start": "%CALSTART",
    "location": "%CALLOC",
    "notes": "%CALDESCR"
  }}
}}

Alarm snapshot body:
{{
  "type": "alarm_snapshot",
  "notify": true,
  "data": {{
    "next_alarm": "%na_time"
  }}
}}
"""
    for chat_id in chat_ids[:3]:
        post_json(
            f"https://api.telegram.org/bot{token}/sendMessage",
            {
                "chat_id": chat_id,
                "text": text[:3900],
                "disable_web_page_preview": True,
            },
        )
    print("sent")


if __name__ == "__main__":
    main()
