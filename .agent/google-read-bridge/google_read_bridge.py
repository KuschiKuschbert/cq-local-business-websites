#!/usr/bin/env python3
import argparse
import base64
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


GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"


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


def http_json(url, *, method="GET", payload=None, form=None, headers=None, timeout=30):
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


def parse_google_client(path):
    data = read_json(path)
    obj = data.get("installed") or data.get("web") or data
    return {
        "client_id": obj.get("client_id", ""),
        "client_secret": obj.get("client_secret", ""),
    }


def html_to_text(value):
    value = re.sub(r"<[^>]+>", " ", value or "")
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def decode_gmail_body(payload, limit=1200):
    texts = []

    def walk(part):
        mime = part.get("mimeType", "")
        body = part.get("body") or {}
        data = body.get("data")
        if data and mime in ("text/plain", "text/html"):
            try:
                raw = base64.urlsafe_b64decode(data + "=" * (-len(data) % 4)).decode("utf-8", errors="replace")
                texts.append(html_to_text(raw) if mime == "text/html" else raw.strip())
            except Exception:
                pass
        for child in part.get("parts") or []:
            walk(child)

    walk(payload or {})
    text = "\n".join(t for t in texts if t)
    return text[:limit].strip()


def clean_terms(value, stop_words):
    cleaned = re.sub(r"[^A-Za-z0-9@._+-]+", " ", value or "").lower()
    terms = []
    for part in cleaned.split():
        if part in stop_words or len(part) < 2:
            continue
        terms.append(part)
    return terms


class GoogleReadBridge:
    def __init__(self, config_path):
        self.config_path = Path(config_path)
        self.config = read_json(self.config_path)
        self.client = parse_google_client(self.config["client_secrets_path"])
        self.accounts = self.config.get("accounts") or [{
            "name": "personal",
            "email": "",
            "token_path": self.config["token_path"],
        }]
        for account in self.accounts:
            account.setdefault("name", account.get("email") or "default")
            account.setdefault("email", "")
            account.setdefault("token_path", self.config["token_path"])

    def account_by_name(self, name):
        for account in self.accounts:
            if account.get("name") == name or account.get("email") == name:
                return account
        raise RuntimeError(f"Unknown Google bridge account: {name}")

    def connected_accounts(self):
        connected = []
        for account in self.accounts:
            tok = read_json(account["token_path"])
            if tok.get("refresh_token") or tok.get("access_token"):
                connected.append(account)
        return connected

    def accounts_for_query(self, query):
        q = query.lower()
        if any(term in q for term in ("riviera", "kitchen@rivierayeppoon", "kitchen.riviera@lanegroupcq", "lanegroup", "lane group", "adaraze", "admin@adarazecatering")):
            preferred = [
                account for account in self.connected_accounts()
                if (
                    account.get("name") in ("riviera_kitchen", "lan_kitchen")
                    or "rivierayeppoon" in account.get("email", "")
                    or "lanegroupcq" in account.get("email", "")
                    or "riviera" in " ".join(account.get("tags", [])).lower()
                    or "kitchen" in " ".join(account.get("tags", [])).lower()
                )
            ]
            if preferred:
                return preferred
        return self.connected_accounts() or self.accounts

    def token(self, account=None):
        account = account or self.accounts[0]
        token_path = Path(account["token_path"])
        tok = read_json(token_path)
        if not tok.get("refresh_token") and not tok.get("access_token"):
            raise RuntimeError(f"Google OAuth is not connected yet for {account.get('name')}.")
        expires_at = float(tok.get("expires_at") or 0)
        if tok.get("access_token") and expires_at > time.time() + 90:
            return tok["access_token"]
        if not tok.get("refresh_token"):
            raise RuntimeError(f"Google OAuth token cannot refresh for {account.get('name')}. Re-authorize the bridge.")
        refreshed = http_json(GOOGLE_TOKEN_URL, method="POST", form={
            "client_id": self.client["client_id"],
            "client_secret": self.client["client_secret"],
            "refresh_token": tok["refresh_token"],
            "grant_type": "refresh_token",
        })
        tok["access_token"] = refreshed["access_token"]
        tok["expires_at"] = time.time() + int(refreshed.get("expires_in", 3600))
        if refreshed.get("scope"):
            tok["scope"] = refreshed["scope"]
        write_json(token_path, tok)
        return tok["access_token"]

    def headers(self, account=None):
        return {"Authorization": f"Bearer {self.token(account)}"}

    def status(self):
        account_statuses = []
        for account in self.accounts:
            tok = read_json(account["token_path"])
            account_statuses.append({
                "name": account.get("name"),
                "email": account.get("email"),
                "connected": bool(tok.get("refresh_token") or tok.get("access_token")),
                "keep_write": "https://www.googleapis.com/auth/keep" in tok.get("scope", ""),
                "scopes": tok.get("scope", ""),
                "expires_at": tok.get("expires_at"),
            })
        return {
            "configured": bool(self.client.get("client_id") and self.client.get("client_secret")),
            "connected": any(account["connected"] for account in account_statuses),
            "accounts": account_statuses,
        }

    def keep_note_title(self, title, text):
        title = re.sub(r"\s+", " ", title or "").strip()
        if title:
            return title[:100]
        first = re.sub(r"\s+", " ", text or "").strip()
        return (first[:80] or "Odysseus note")

    def keep_create_note(self, text, title="", account_name="riviera_kitchen"):
        account = self.account_by_name(account_name)
        tok = read_json(account["token_path"])
        if "https://www.googleapis.com/auth/keep" not in tok.get("scope", ""):
            raise RuntimeError(
                f"Google Keep write scope is not approved for {account.get('email') or account.get('name')}. "
                "Re-authorize this Google account with the Keep scope."
            )
        text = str(text or "").strip()
        if not text:
            raise RuntimeError("Cannot create an empty Google Keep note.")
        payload = {
            "title": self.keep_note_title(title, text),
            "body": {
                "text": {
                    "text": text,
                },
            },
        }
        note = http_json(
            "https://keep.googleapis.com/v1/notes",
            method="POST",
            payload=payload,
            headers=self.headers(account),
            timeout=30,
        )
        return {
            "ok": True,
            "account": account.get("name"),
            "account_email": account.get("email"),
            "name": note.get("name", ""),
            "title": note.get("title", ""),
            "create_time": note.get("createTime", ""),
            "update_time": note.get("updateTime", ""),
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
            "google", "calendar", "calendars", "related", "show", "list", "see", "find",
            "for", "to", "my", "the", "any", "linked", "schedule", "diary", "agenda",
            "appointment", "appointments", "event", "events", "today", "tomorrow",
            "week", "next", "days", "day", "what", "what's", "on", "available",
            "which", "are", "is", "with", "and", "or",
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
            item.get("summary", ""),
            item.get("description", ""),
        ]).lower()
        return any(term in haystack for term in terms)

    def calendar_list(self, query="", accounts=None):
        accounts = accounts or self.connected_accounts() or self.accounts
        params = urllib.parse.urlencode({
            "showHidden": "true",
            "minAccessRole": "reader",
            "fields": "items(id,summary,description,primary,selected,accessRole,backgroundColor,timeZone)",
            "maxResults": "250",
        })
        terms = self.expand_calendar_terms(query)
        calendars = []
        for account in accounts:
            data = http_json(
                "https://www.googleapis.com/calendar/v3/users/me/calendarList?" + params,
                headers=self.headers(account),
            )
            for item in data.get("items", []):
                if terms and not self.calendar_matches(item, terms):
                    continue
                calendars.append({
                    "account": account.get("name"),
                    "account_email": account.get("email"),
                    "id": item.get("id", ""),
                    "summary": item.get("summary", ""),
                    "description": item.get("description", ""),
                    "primary": bool(item.get("primary")),
                    "selected": bool(item.get("selected")),
                    "access_role": item.get("accessRole", ""),
                    "time_zone": item.get("timeZone", ""),
                    "background_color": item.get("backgroundColor", ""),
                })
        return {"query": query, "terms": terms, "calendars": calendars}

    def calendars_for_query(self, query):
        terms = self.expand_calendar_terms(query)
        if not terms:
            return [
                {"account": account.get("name"), "account_email": account.get("email"), "id": "primary", "summary": "Primary", "primary": True}
                for account in self.accounts_for_query(query)
            ]
        matches = self.calendar_list(query, accounts=self.accounts_for_query(query))["calendars"]
        if matches:
            return matches
        return [
            {"account": account.get("name"), "account_email": account.get("email"), "id": "primary", "summary": "Primary", "primary": True}
            for account in self.accounts_for_query(query)
        ]

    def calendar_event_payload(self, item, account, calendar_id, calendar):
        description_limit = int(self.config.get("calendar_description_chars", 8000))
        attachments = []
        for attachment in item.get("attachments") or []:
            attachments.append({
                "title": attachment.get("title", ""),
                "mime_type": attachment.get("mimeType", ""),
                "file_url": attachment.get("fileUrl", ""),
                "icon_link": attachment.get("iconLink", ""),
                "file_id": attachment.get("fileId", ""),
            })
        attendees = []
        for attendee in item.get("attendees") or []:
            attendees.append({
                "email": attendee.get("email", ""),
                "display_name": attendee.get("displayName", ""),
                "organizer": bool(attendee.get("organizer")),
                "self": bool(attendee.get("self")),
                "resource": bool(attendee.get("resource")),
                "optional": bool(attendee.get("optional")),
                "response_status": attendee.get("responseStatus", ""),
            })
        conference = item.get("conferenceData") or {}
        conference_points = []
        for point in conference.get("entryPoints") or []:
            conference_points.append({
                "type": point.get("entryPointType", ""),
                "label": point.get("label", ""),
                "uri": point.get("uri", ""),
                "pin": point.get("pin", ""),
            })
        return {
            "account": account.get("name"),
            "account_email": account.get("email"),
            "calendar_id": calendar_id,
            "calendar_summary": calendar.get("summary", calendar_id),
            "id": item.get("id", ""),
            "i_cal_uid": item.get("iCalUID", ""),
            "status": item.get("status", ""),
            "summary": item.get("summary", "(no title)"),
            "description": (item.get("description") or "")[:description_limit],
            "description_truncated": len(item.get("description") or "") > description_limit,
            "location": item.get("location", ""),
            "start": (item.get("start") or {}).get("dateTime") or (item.get("start") or {}).get("date"),
            "end": (item.get("end") or {}).get("dateTime") or (item.get("end") or {}).get("date"),
            "start_raw": item.get("start") or {},
            "end_raw": item.get("end") or {},
            "all_day": bool((item.get("start") or {}).get("date") and not (item.get("start") or {}).get("dateTime")),
            "html_link": item.get("htmlLink", ""),
            "hangout_link": item.get("hangoutLink", ""),
            "event_type": item.get("eventType", ""),
            "transparency": item.get("transparency", ""),
            "visibility": item.get("visibility", ""),
            "color_id": item.get("colorId", ""),
            "created": item.get("created", ""),
            "updated": item.get("updated", ""),
            "creator": item.get("creator") or {},
            "organizer": item.get("organizer") or {},
            "attendees": attendees,
            "attendees_omitted": bool(item.get("attendeesOmitted")),
            "attachments": attachments,
            "conference": {
                "solution": ((conference.get("conferenceSolution") or {}).get("name") or ""),
                "entry_points": conference_points,
            },
            "recurrence": item.get("recurrence") or [],
            "recurring_event_id": item.get("recurringEventId", ""),
            "original_start_time": item.get("originalStartTime") or {},
            "reminders": item.get("reminders") or {},
            "source": item.get("source") or {},
            "extended_properties": item.get("extendedProperties") or {},
        }

    def calendar_events(self, query):
        local_tz = self.local_timezone()
        now = datetime.now(local_tz)
        q = query.lower()
        if "tomorrow" in q:
            start = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
            end = start + timedelta(days=1)
        elif "week" in q or "next 7" in q or re.search(r"\b(riviera|event|events|wedding|function|venue|prep|kitchen notes)\b", q):
            start = now
            end = now + timedelta(days=7)
        else:
            start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end = start + timedelta(days=1)

        events = []
        calendars = self.calendars_for_query(query)
        max_results = int(self.config.get("calendar_max_results", 20))
        for calendar in calendars:
            account = self.account_by_name(calendar.get("account") or self.accounts[0]["name"])
            calendar_id = calendar.get("id") or "primary"
            params = urllib.parse.urlencode({
                "timeMin": start.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
                "timeMax": end.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
                "singleEvents": "true",
                "orderBy": "startTime",
                "maxResults": str(max_results),
            })
            encoded_id = urllib.parse.quote(calendar_id, safe="")
            data = http_json(
                f"https://www.googleapis.com/calendar/v3/calendars/{encoded_id}/events?" + params,
                headers=self.headers(account),
            )
            for item in data.get("items", []):
                events.append(self.calendar_event_payload(item, account, calendar_id, calendar))
        events.sort(key=lambda item: item.get("start") or "")
        return {
            "range_start": start.isoformat(),
            "range_end": end.isoformat(),
            "calendars": [{"account": c.get("account"), "account_email": c.get("account_email"), "id": c.get("id"), "summary": c.get("summary"), "primary": bool(c.get("primary"))} for c in calendars],
            "events": events[:max_results],
        }


    def drive_search(self, query):
        terms = re.sub(r"\b(google|drive|docs?|sheets?|slides?|file|find|search|look for|show me)\b", " ", query, flags=re.I)
        terms = re.sub(r"\s+", " ", terms).strip()
        if not terms:
            terms = query.strip()
        drive_q = "trashed=false"
        if terms:
            safe = terms.replace("\\", "\\\\").replace("'", "\\'")
            drive_q += f" and fullText contains '{safe}'"
        params = urllib.parse.urlencode({
            "q": drive_q,
            "pageSize": str(self.config.get("drive_max_results", 10)),
            "fields": "files(id,name,mimeType,webViewLink,modifiedTime,size)",
            "orderBy": "modifiedTime desc",
            "supportsAllDrives": "true",
            "includeItemsFromAllDrives": "true",
        })
        files = []
        for account in self.accounts_for_query(query):
            data = http_json("https://www.googleapis.com/drive/v3/files?" + params, headers=self.headers(account))
            for item in data.get("files", []):
                item["account"] = account.get("name")
                item["account_email"] = account.get("email")
                files.append(item)
        return {"query": terms, "files": files}

    def gmail_search(self, query):
        q = query.lower()
        gmail_q = []
        if "unread" in q:
            gmail_q.append("is:unread")
        if "today" in q:
            gmail_q.append("newer_than:1d")
        if "week" in q:
            gmail_q.append("newer_than:7d")
        from_match = re.search(r"\bfrom:?\s*([^\s]+@[^\s]+|[A-Za-z0-9._-]+)", query, flags=re.I)
        if from_match:
            gmail_q.append(f"from:{from_match.group(1)}")
        text_terms = re.sub(r"\b(gmail|email|emails|mail|inbox|unread|today|week|from)\b", " ", query, flags=re.I)
        text_terms = re.sub(r"\s+", " ", text_terms).strip()
        if text_terms:
            gmail_q.append(text_terms)
        params = urllib.parse.urlencode({
            "q": " ".join(gmail_q).strip() or "newer_than:7d",
            "maxResults": str(self.config.get("gmail_max_results", 8)),
        })
        messages = []
        for account in self.accounts_for_query(query):
            data = http_json("https://gmail.googleapis.com/gmail/v1/users/me/messages?" + params, headers=self.headers(account))
            for msg in data.get("messages", []):
                detail = http_json(
                    f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{msg['id']}?format=full",
                    headers=self.headers(account),
                )
                headers = {h.get("name", "").lower(): h.get("value", "") for h in (detail.get("payload") or {}).get("headers", [])}
                messages.append({
                    "account": account.get("name"),
                    "account_email": account.get("email"),
                    "id": detail.get("id"),
                    "from": headers.get("from", ""),
                    "subject": headers.get("subject", ""),
                    "date": headers.get("date", ""),
                    "snippet": detail.get("snippet", ""),
                    "body_preview": decode_gmail_body(detail.get("payload"), self.config.get("gmail_body_preview_chars", 1200)),
                })
        return {"query": " ".join(gmail_q).strip() or "newer_than:7d", "messages": messages}

    def context_for(self, query):
        q = query.lower()
        out = {"query": query, "services": {}}
        if re.search(r"\b(calendar|calendars)\b", q) and re.search(r"\b(list|show|find|see|linked|related|available|which)\b", q):
            out["services"]["calendars"] = self.calendar_list(query)
        if re.search(r"\b(calendar|schedule|diary|agenda|appointment|appointments|today|tomorrow|week|riviera|event|events|wedding|function|venue|prep|kitchen notes)\b", q):
            out["services"]["calendar"] = self.calendar_events(query)
        if re.search(r"\b(drive|doc|docs|sheet|slides|file|pdf|menu|sop|proposal|recipe|notebooklm|notebook)\b", q):
            out["services"]["drive"] = self.drive_search(query)
        if re.search(r"\b(gmail|email|mail|inbox|unread|client|venue|enquiry|enquiries)\b", q):
            out["services"]["gmail"] = self.gmail_search(query)
        if "notebooklm" in q or "notebook" in q:
            out["services"]["notebooklm_note"] = {
                "status": "no_public_api",
                "message": "NotebookLM is not queried directly. Use Drive source files and exported notebook material.",
            }
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

    def read_json_body(self):
        length = int(self.headers.get("Content-Length") or 0)
        if length <= 0:
            return {}
        raw = self.rfile.read(length).decode("utf-8")
        return json.loads(raw) if raw else {}

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
            elif parsed.path == "/drive/search":
                q = (params.get("q") or [""])[0]
                self.send_json(200, self.bridge.drive_search(q))
            elif parsed.path == "/gmail/search":
                q = (params.get("q") or [""])[0]
                self.send_json(200, self.bridge.gmail_search(q))
            else:
                self.send_json(404, {"error": "not_found"})
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            self.send_json(exc.code, {"error": "google_http_error", "detail": detail[:2000]})
        except Exception as exc:
            self.send_json(500, {"error": str(exc)})

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        try:
            if parsed.path == "/keep/create":
                body = self.read_json_body()
                self.send_json(200, self.bridge.keep_create_note(
                    body.get("text", ""),
                    title=body.get("title", ""),
                    account_name=body.get("account", "riviera_kitchen"),
                ))
            else:
                self.send_json(404, {"error": "not_found"})
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            self.send_json(exc.code, {"error": "google_http_error", "detail": detail[:2000]})
        except Exception as exc:
            self.send_json(500, {"error": str(exc)})

    def log_message(self, fmt, *args):
        return


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    bridge = GoogleReadBridge(args.config)
    Handler.bridge = bridge
    host = bridge.config.get("host", "127.0.0.1")
    port = int(bridge.config.get("port", 8765))
    server = ThreadingHTTPServer((host, port), Handler)
    print(f"Google read bridge running on http://{host}:{port}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
