#!/usr/bin/env python3
import argparse
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

try:
    from zoneinfo import ZoneInfo
except Exception:
    ZoneInfo = None


GRAPH_BASE = "https://graph.microsoft.com/v1.0"


def read_json(path, default=None):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception:
        return default if default is not None else {}


def write_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


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


def clean_terms(value, stop_words):
    cleaned = re.sub(r"[^A-Za-z0-9@._+-]+", " ", value or "").lower()
    terms = []
    for part in cleaned.split():
        if part in stop_words or len(part) < 2:
            continue
        terms.append(part)
    return terms


def strip_html(value):
    value = re.sub(r"<br\s*/?>", "\n", value or "", flags=re.I)
    value = re.sub(r"</p\s*>", "\n", value, flags=re.I)
    value = re.sub(r"<[^>]+>", " ", value)
    value = re.sub(r"[ \t]+", " ", value)
    value = re.sub(r"\n\s+", "\n", value)
    return value.strip()


class MicrosoftReadBridge:
    def __init__(self, config_path):
        self.config_path = Path(config_path)
        self.config = read_json(self.config_path)
        self.accounts = self.config.get("accounts") or []
        for account in self.accounts:
            account.setdefault("name", account.get("email") or "default")
            account.setdefault("email", "")
            account.setdefault("token_path", self.config.get("token_path", "token.json"))

    def authority(self, account=None):
        tenant = (account or {}).get("tenant") or self.config.get("tenant") or "organizations"
        return f"https://login.microsoftonline.com/{tenant}"

    def token_url(self, account=None):
        return self.authority(account).rstrip("/") + "/oauth2/v2.0/token"

    def device_code_url(self, account=None):
        return self.authority(account).rstrip("/") + "/oauth2/v2.0/devicecode"

    def account_by_name(self, name):
        for account in self.accounts:
            if account.get("name") == name or account.get("email") == name:
                return account
        raise RuntimeError(f"Unknown Microsoft bridge account: {name}")

    def connected_accounts(self):
        connected = []
        for account in self.accounts:
            tok = read_json(account["token_path"])
            if tok.get("refresh_token") or tok.get("access_token"):
                connected.append(account)
        return connected

    def accounts_for_query(self, query):
        q = query.lower()
        connected = self.connected_accounts()
        if any(term in q for term in ("riviera", "lanegroup", "lanegroupcq", "lane group", "kitchen.riviera")):
            preferred = [
                account for account in connected
                if (
                    account.get("name") in ("lan_kitchen", "riviera_kitchen")
                    or "lanegroupcq" in account.get("email", "").lower()
                    or "riviera" in " ".join(account.get("tags", [])).lower()
                    or "kitchen" in " ".join(account.get("tags", [])).lower()
                )
            ]
            if preferred:
                return preferred
        return connected or self.accounts

    def token(self, account=None):
        account = account or (self.accounts[0] if self.accounts else {})
        token_path = Path(account["token_path"])
        tok = read_json(token_path)
        if not tok.get("refresh_token") and not tok.get("access_token"):
            raise RuntimeError(f"Microsoft OAuth is not connected yet for {account.get('name')}.")
        expires_at = float(tok.get("expires_at") or 0)
        if tok.get("access_token") and expires_at > time.time() + 90:
            return tok["access_token"]
        if not tok.get("refresh_token"):
            raise RuntimeError(f"Microsoft OAuth token cannot refresh for {account.get('name')}. Re-authorize the bridge.")
        refreshed = http_json(self.token_url(account), method="POST", form={
            "client_id": self.config["client_id"],
            "grant_type": "refresh_token",
            "refresh_token": tok["refresh_token"],
            "scope": " ".join(self.config["scopes"]),
        })
        tok.update(refreshed)
        tok["expires_at"] = time.time() + int(refreshed.get("expires_in", 3600))
        write_json(token_path, tok)
        return tok["access_token"]

    def headers(self, account=None):
        return {
            "Authorization": f"Bearer {self.token(account)}",
            "Accept": "application/json",
            "Prefer": f'outlook.timezone="{self.config.get("timezone", "Australia/Brisbane")}"',
        }

    def status(self):
        account_statuses = []
        for account in self.accounts:
            tok = read_json(account["token_path"])
            account_statuses.append({
                "name": account.get("name"),
                "email": account.get("email"),
                "connected": bool(tok.get("refresh_token") or tok.get("access_token")),
                "scopes": tok.get("scope", ""),
                "expires_at": tok.get("expires_at"),
            })
        return {
            "configured": bool(self.config.get("client_id") and not str(self.config.get("client_id")).startswith("PASTE_")),
            "connected": any(account["connected"] for account in account_statuses),
            "accounts": account_statuses,
        }

    def local_timezone(self):
        name = self.config.get("timezone", "Australia/Brisbane")
        if ZoneInfo:
            try:
                return ZoneInfo(name)
            except Exception:
                pass
        return timezone.utc

    def expand_calendar_terms(self, query):
        stop_words = {
            "microsoft", "office", "outlook", "calendar", "calendars", "related",
            "show", "list", "see", "find", "for", "to", "my", "the", "any",
            "linked", "schedule", "diary", "agenda", "appointment", "appointments",
            "event", "events", "today", "tomorrow", "week", "next", "days",
            "day", "what", "what's", "on", "available", "which", "are", "is",
            "with", "and", "or",
        }
        terms = clean_terms(query, stop_words)
        aliases = self.config.get("calendar_aliases", {})
        expanded = list(terms)
        for term in terms:
            expanded.extend(aliases.get(term, []))
        return sorted({str(term).lower() for term in expanded if str(term).strip()})

    def calendar_matches(self, item, terms):
        haystack = " ".join([
            item.get("id", ""),
            item.get("name", ""),
            item.get("owner", {}).get("name", ""),
            item.get("owner", {}).get("address", ""),
        ]).lower()
        return any(term in haystack for term in terms)

    def calendar_list(self, query="", accounts=None):
        accounts = accounts or self.connected_accounts() or self.accounts
        terms = self.expand_calendar_terms(query)
        calendars = []
        for account in accounts:
            data = http_json(GRAPH_BASE + "/me/calendars?$top=100", headers=self.headers(account))
            for item in data.get("value", []):
                if terms and not self.calendar_matches(item, terms):
                    continue
                calendars.append({
                    "account": account.get("name"),
                    "account_email": account.get("email"),
                    "id": item.get("id", ""),
                    "summary": item.get("name", ""),
                    "name": item.get("name", ""),
                    "owner": item.get("owner") or {},
                    "can_edit": bool(item.get("canEdit")),
                    "can_share": bool(item.get("canShare")),
                    "can_view_private_items": bool(item.get("canViewPrivateItems")),
                    "is_default": bool(item.get("isDefaultCalendar")),
                })
        return {"query": query, "terms": terms, "calendars": calendars}

    def calendars_for_query(self, query):
        terms = self.expand_calendar_terms(query)
        if not terms:
            return [
                {"account": account.get("name"), "account_email": account.get("email"), "id": "calendar", "summary": "Primary", "is_default": True}
                for account in self.accounts_for_query(query)
            ]
        matches = self.calendar_list(query, accounts=self.accounts_for_query(query))["calendars"]
        if matches:
            return matches
        return [
            {"account": account.get("name"), "account_email": account.get("email"), "id": "calendar", "summary": "Primary", "is_default": True}
            for account in self.accounts_for_query(query)
        ]

    def calendar_event_payload(self, item, account, calendar):
        description_limit = int(self.config.get("calendar_description_chars", 8000))
        body = item.get("body") or {}
        description = body.get("content") or ""
        if body.get("contentType", "").lower() == "html":
            description = strip_html(description)
        attendees = []
        for attendee in item.get("attendees") or []:
            email = attendee.get("emailAddress") or {}
            attendees.append({
                "email": email.get("address", ""),
                "display_name": email.get("name", ""),
                "type": attendee.get("type", ""),
                "status": (attendee.get("status") or {}).get("response", ""),
            })
        organizer = item.get("organizer") or {}
        organizer_email = organizer.get("emailAddress") or {}
        attachments = []
        if item.get("hasAttachments"):
            attachments.append({"note": "Event has attachments. Attachment detail is not fetched by the read bridge yet."})
        return {
            "source": "microsoft_graph",
            "account": account.get("name"),
            "account_email": account.get("email"),
            "calendar_id": calendar.get("id", ""),
            "calendar_summary": calendar.get("summary", calendar.get("name", "")),
            "id": item.get("id", ""),
            "i_cal_uid": item.get("iCalUId", ""),
            "status": item.get("showAs", ""),
            "summary": item.get("subject") or "(no title)",
            "description": description[:description_limit],
            "description_truncated": len(description) > description_limit,
            "location": ((item.get("location") or {}).get("displayName") or ""),
            "locations": item.get("locations") or [],
            "start": (item.get("start") or {}).get("dateTime", ""),
            "end": (item.get("end") or {}).get("dateTime", ""),
            "start_raw": item.get("start") or {},
            "end_raw": item.get("end") or {},
            "all_day": bool(item.get("isAllDay")),
            "html_link": item.get("webLink", ""),
            "created": item.get("createdDateTime", ""),
            "updated": item.get("lastModifiedDateTime", ""),
            "organizer": {
                "email": organizer_email.get("address", ""),
                "display_name": organizer_email.get("name", ""),
            },
            "attendees": attendees,
            "attachments": attachments,
            "online_meeting": item.get("onlineMeeting") or {},
            "recurrence": item.get("recurrence") or {},
            "sensitivity": item.get("sensitivity", ""),
            "categories": item.get("categories") or [],
        }

    def calendar_events(self, query):
        local_tz = self.local_timezone()
        now = datetime.now(local_tz)
        q = query.lower()
        if "tomorrow" in q:
            start = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
            end = start + timedelta(days=1)
        elif "week" in q or "next 7" in q or re.search(r"\b(riviera|event|events|wedding|function|venue|prep|kitchen notes|lanegroup|lane group)\b", q):
            start = now
            end = now + timedelta(days=7)
        else:
            start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end = start + timedelta(days=1)

        events = []
        calendars = self.calendars_for_query(query)
        max_results = int(self.config.get("calendar_max_results", 20))
        select = ",".join([
            "id", "subject", "body", "bodyPreview", "start", "end", "isAllDay",
            "location", "locations", "attendees", "organizer", "webLink",
            "iCalUId", "showAs", "createdDateTime", "lastModifiedDateTime",
            "hasAttachments", "onlineMeeting", "recurrence", "sensitivity", "categories",
        ])
        for calendar in calendars:
            account = self.account_by_name(calendar.get("account") or self.accounts[0]["name"])
            calendar_id = calendar.get("id") or "calendar"
            if calendar_id == "calendar":
                path = "/me/calendar/calendarView"
            else:
                path = f"/me/calendars/{urllib.parse.quote(calendar_id, safe='')}/calendarView"
            params = urllib.parse.urlencode({
                "startDateTime": start.isoformat(),
                "endDateTime": end.isoformat(),
                "$top": str(max_results),
                "$orderby": "start/dateTime",
                "$select": select,
            })
            data = http_json(GRAPH_BASE + path + "?" + params, headers=self.headers(account))
            for item in data.get("value", []):
                events.append(self.calendar_event_payload(item, account, calendar))
        events.sort(key=lambda item: item.get("start") or "")
        return {
            "range_start": start.isoformat(),
            "range_end": end.isoformat(),
            "calendars": [
                {
                    "account": c.get("account"),
                    "account_email": c.get("account_email"),
                    "id": c.get("id"),
                    "summary": c.get("summary"),
                    "is_default": bool(c.get("is_default")),
                }
                for c in calendars
            ],
            "events": events[:max_results],
        }

    def context_for(self, query):
        q = query.lower()
        out = {"query": query, "services": {}}
        if re.search(r"\b(calendar|calendars)\b", q) and re.search(r"\b(list|show|find|see|linked|related|available|which)\b", q):
            out["services"]["calendars"] = self.calendar_list(query)
        if re.search(r"\b(calendar|schedule|diary|agenda|appointment|appointments|today|tomorrow|week|riviera|event|events|wedding|function|venue|prep|kitchen notes|lanegroup|lane group)\b", q):
            out["services"]["calendar"] = self.calendar_events(query)
        return out


class Handler(BaseHTTPRequestHandler):
    bridge = None

    def send_json(self, status, data):
        raw = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        try:
            if parsed.path == "/health":
                self.send_json(200, {"ok": True, "status": self.bridge.status()})
            elif parsed.path == "/status":
                self.send_json(200, self.bridge.status())
            elif parsed.path == "/context":
                q = (params.get("q") or [""])[0]
                self.send_json(200, self.bridge.context_for(q))
            elif parsed.path == "/calendar":
                q = (params.get("q") or ["today"])[0]
                self.send_json(200, self.bridge.calendar_events(q))
            elif parsed.path == "/calendars":
                q = (params.get("q") or [""])[0]
                self.send_json(200, self.bridge.calendar_list(q))
            else:
                self.send_json(404, {"error": "not_found"})
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            self.send_json(exc.code, {"error": "microsoft_http_error", "detail": detail[:2000]})
        except Exception as exc:
            self.send_json(500, {"error": str(exc)})

    def log_message(self, fmt, *args):
        return


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    bridge = MicrosoftReadBridge(args.config)
    Handler.bridge = bridge
    host = bridge.config.get("host", "127.0.0.1")
    port = int(bridge.config.get("port", 8767))
    server = ThreadingHTTPServer((host, port), Handler)
    print(f"Microsoft read bridge running on http://{host}:{port}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
