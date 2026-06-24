#!/usr/bin/env python3
import argparse
import json
import secrets
import subprocess
import time
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

from google_read_bridge import GOOGLE_TOKEN_URL, http_json, parse_google_client, read_json, write_json


DEFAULT_REDIRECT = "http://127.0.0.1:8766/oauth2callback"


class CallbackHandler(BaseHTTPRequestHandler):
    code = None
    error = None
    expected_state = None

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        if parsed.path != "/oauth2callback":
            self.send_response(404)
            self.end_headers()
            return
        state = (params.get("state") or [""])[0]
        if state != type(self).expected_state:
            type(self).error = "State mismatch."
        elif params.get("error"):
            type(self).error = (params.get("error") or ["unknown"])[0]
        else:
            type(self).code = (params.get("code") or [""])[0]
        body = b"Google read bridge authorization received. You can close this tab."
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        return


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--account", default="")
    parser.add_argument("--no-open", action="store_true")
    args = parser.parse_args()

    config = read_json(args.config)
    accounts = config.get("accounts") or [{
        "name": "personal",
        "email": "",
        "token_path": config["token_path"],
    }]
    account = accounts[0]
    if args.account:
        matches = [item for item in accounts if item.get("name") == args.account or item.get("email") == args.account]
        if not matches:
            raise SystemExit(f"Unknown account '{args.account}'. Add it to config.json accounts first.")
        account = matches[0]
    client = parse_google_client(config["client_secrets_path"])
    redirect_uri = config.get("redirect_uri", DEFAULT_REDIRECT)
    parsed_redirect = urllib.parse.urlparse(redirect_uri)
    state = secrets.token_urlsafe(24)
    scopes = config["scopes"]
    auth_params = urllib.parse.urlencode({
        "client_id": client["client_id"],
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": " ".join(scopes),
        "access_type": "offline",
        "prompt": "consent",
        "state": state,
    })
    if account.get("email"):
        auth_params += "&" + urllib.parse.urlencode({"login_hint": account["email"]})
    auth_url = "https://accounts.google.com/o/oauth2/v2/auth?" + auth_params
    print(auth_url)

    CallbackHandler.expected_state = state
    server = HTTPServer((parsed_redirect.hostname, parsed_redirect.port), CallbackHandler)
    if not args.no_open:
        subprocess.Popen(["open", auth_url])
    while not CallbackHandler.code and not CallbackHandler.error:
        server.handle_request()
    if CallbackHandler.error:
        raise SystemExit(CallbackHandler.error)

    token = http_json(GOOGLE_TOKEN_URL, method="POST", form={
        "code": CallbackHandler.code,
        "client_id": client["client_id"],
        "client_secret": client["client_secret"],
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    })
    token["expires_at"] = time.time() + int(token.get("expires_in", 3600))
    token["connected_at"] = time.time()
    write_json(account["token_path"], token)
    print(json.dumps({
        "connected": True,
        "account": account.get("name"),
        "email": account.get("email", ""),
        "scopes": token.get("scope", ""),
        "token_path": account["token_path"],
    }, indent=2))


if __name__ == "__main__":
    main()
