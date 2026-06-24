#!/usr/bin/env python3
import json
import mimetypes
import os
import subprocess
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from common import ROOT, WORKING, clean, p, read_csv

HOST = "127.0.0.1"
PORT = int(os.environ.get("CAP_COAST_DASHBOARD_PORT", "8787"))
BASE = os.path.dirname(__file__)


def run_script(name, *args):
    cmd = [sys.executable, os.path.join(BASE, name), *args]
    done = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    output = (done.stdout or done.stderr or "").strip()
    if done.returncode:
        raise RuntimeError(output or f"{name} failed")
    return output


def already_promoted(business):
    key = clean(business).casefold()
    return any(clean(row.get("business")).casefold() == key for row in read_csv(p("prospects.csv")))


def safe_file(path):
    wanted = os.path.abspath(os.path.join(WORKING, path.lstrip("/")))
    if not wanted.startswith(os.path.abspath(WORKING) + os.sep):
        return ""
    return wanted


class Handler(BaseHTTPRequestHandler):
    server_version = "CapCoastDashboard/1.0"

    def log_message(self, fmt, *args):
        return

    def send_json(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        if self.path == "/api/health":
            self.send_json(200, {"ok": True, "message": "Local dashboard approval server is running."})
            return
        path = "/dashboard/index.html" if self.path in {"/", ""} else self.path.split("?", 1)[0]
        file_path = safe_file(path)
        if not file_path or not os.path.exists(file_path) or os.path.isdir(file_path):
            self.send_error(404)
            return
        mime = mimetypes.guess_type(file_path)[0] or "application/octet-stream"
        with open(file_path, "rb") as handle:
            body = handle.read()
        self.send_response(200)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if self.path != "/api/approval":
            self.send_error(404)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            business = clean(payload.get("business"), "")
            decision = clean(payload.get("decision"), "").lower()
            if not business:
                raise ValueError("Missing business.")
            if decision not in {"approve", "hold", "reject"}:
                raise ValueError("Decision must be approve, hold, or reject.")
            notes = {
                "approve": "Approved from local dashboard for prospect promotion only.",
                "hold": "Held from local dashboard for more review.",
                "reject": "Rejected from local dashboard for prospect promotion.",
            }[decision]
            steps = []
            steps.append(run_script(
                "record-approval-decision.py",
                "--business", business,
                "--decided-by", "Daniel",
                "--decision", decision,
                "--notes", notes,
            ))
            if decision == "approve":
                if already_promoted(business):
                    steps.append(f"{business} is already on prospects.csv.")
                else:
                    steps.append(run_script("promote-intake.py", "--business", business, "--approved-by", "Daniel"))
            steps.append(run_script("run-ceo-loop.py"))
            self.send_json(200, {
                "ok": True,
                "decision": decision,
                "business": business,
                "message": "Decision saved locally. Outreach is still blocked until separately approved.",
                "steps": steps,
            })
        except Exception as error:
            self.send_json(400, {"ok": False, "message": str(error)})


if __name__ == "__main__":
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"Cap Coast dashboard running at http://{HOST}:{PORT}/dashboard/index.html")
    print("Approval buttons are local-only. Promotion approval is not outreach approval.")
    server.serve_forever()
