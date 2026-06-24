#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


LABEL_TELEGRAM = "com.kuschi.odysseus-telegram"
LABEL_GOOGLE = "com.kuschi.google-read-bridge"


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def load_json(path, default=None):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception:
        return default if default is not None else {}


def save_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def http_json(url, *, method="GET", payload=None, headers=None, timeout=8):
    data = None
    req_headers = dict(headers or {})
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        req_headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=req_headers, method=method)
    with urllib.request.urlopen(req, timeout=timeout) as res:
        raw = res.read().decode("utf-8")
        return json.loads(raw) if raw else {}


class Autopilot:
    def __init__(self, config_path):
        self.config_path = Path(config_path)
        self.config = load_json(self.config_path)
        self.base_dir = self.config_path.parent
        self.state_path = self.base_dir / "state.json"
        self.log_path = self.base_dir / "autopilot.log"
        self.reports_dir = self.base_dir / "reports"
        self.state = load_json(self.state_path, {})
        self.telegram_config = load_json(self.config["telegram_config_path"])

    def log(self, message):
        line = f"{now_iso()} {message}\n"
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        with self.log_path.open("a", encoding="utf-8") as f:
            f.write(line)

    def tg_send(self, text):
        token = self.telegram_config.get("telegram_bot_token")
        chat_ids = self.telegram_config.get("allowed_chat_ids") or []
        if not token or not chat_ids:
            return False
        payload = {
            "chat_id": chat_ids[0],
            "text": text[:3900],
            "disable_web_page_preview": True,
        }
        try:
            http_json(
                f"https://api.telegram.org/bot{token}/sendMessage",
                method="POST",
                payload=payload,
                timeout=20,
            )
            return True
        except Exception as exc:
            self.log(f"telegram_send_failed error={exc}")
            return False

    def api_headers(self):
        token = self.telegram_config.get("odysseus_api_token")
        return {"Authorization": f"Bearer {token}"} if token else {}

    def check_odysseus(self):
        url = self.telegram_config.get("odysseus_base_url", "http://127.0.0.1:7860").rstrip("/")
        try:
            data = http_json(f"{url}/api/health", timeout=5)
            return {"ok": data.get("status") == "healthy", "detail": data}
        except Exception as exc:
            return {"ok": False, "error": str(exc)}

    def check_ollama(self):
        url = self.config.get("ollama_base_url", "http://127.0.0.1:11434").rstrip("/")
        try:
            data = http_json(f"{url}/api/tags", timeout=5)
            models = [m.get("name") for m in data.get("models", []) if m.get("name")]
            return {"ok": True, "models": models}
        except Exception as exc:
            return {"ok": False, "error": str(exc)}

    def check_telegram_bridge(self):
        return self.check_launch_agent(LABEL_TELEGRAM)

    def check_google_bridge(self):
        url = (self.config.get("google_bridge_url") or "").rstrip("/")
        if url:
            try:
                data = http_json(f"{url}/health", timeout=5)
                launchd = self.check_launch_agent(LABEL_GOOGLE)
                return {"ok": bool(data.get("ok")) and launchd.get("ok"), "health": data, "launchd": launchd}
            except Exception as exc:
                launchd = self.check_launch_agent(LABEL_GOOGLE)
                return {"ok": False, "error": str(exc), "launchd": launchd}
        return self.check_launch_agent(LABEL_GOOGLE)

    def check_launch_agent(self, label):
        try:
            result = subprocess.run(
                ["launchctl", "list", label],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=8,
            )
            return {"ok": result.returncode == 0, "stdout": result.stdout[-1000:], "stderr": result.stderr[-1000:]}
        except Exception as exc:
            return {"ok": False, "error": str(exc)}

    def cooldown_ready(self, key):
        minutes = int(self.config.get("restart_cooldown_minutes", 10))
        last = float(self.state.get("last_restart", {}).get(key, 0))
        return time.time() - last > minutes * 60

    def mark_restart(self, key):
        self.state.setdefault("last_restart", {})[key] = time.time()
        save_json(self.state_path, self.state)

    def restart_odysseus(self):
        if not self.cooldown_ready("odysseus"):
            return "cooldown"
        odysseus_dir = self.config["odysseus_dir"]
        screen_name = self.config.get("odysseus_screen_name", "odysseus-autopilot")
        cmd = f'cd "{odysseus_dir}" && ODYSSEUS_NO_OPEN=1 ./start-macos.sh'
        subprocess.Popen(
            ["/usr/bin/screen", "-dmS", screen_name, "/bin/zsh", "-lc", cmd],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
        self.mark_restart("odysseus")
        return "started"

    def restart_ollama(self):
        if not self.cooldown_ready("ollama"):
            return "cooldown"
        ollama = self.config.get("ollama_bin", "/opt/homebrew/bin/ollama")
        subprocess.Popen(
            [ollama, "serve"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
        self.mark_restart("ollama")
        return "started"

    def restart_telegram_bridge(self):
        if not self.cooldown_ready("telegram_bridge"):
            return "cooldown"
        return self.kickstart_launch_agent(LABEL_TELEGRAM, "telegram_bridge")

    def restart_google_bridge(self):
        if not self.cooldown_ready("google_bridge"):
            return "cooldown"
        return self.kickstart_launch_agent(LABEL_GOOGLE, "google_bridge")

    def kickstart_launch_agent(self, label, key):
        uid = os.getuid()
        result = subprocess.run(
            ["launchctl", "kickstart", "-k", f"gui/{uid}/{label}"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=15,
        )
        self.mark_restart(key)
        return "restarted" if result.returncode == 0 else f"kickstart_failed: {result.stderr.strip()}"

    def rotate_large_logs(self):
        max_bytes = int(self.config.get("max_log_bytes", 2_000_000))
        rotated = []
        for path in [
            self.log_path,
            self.base_dir / "telegram-bridge.log",
            self.base_dir / "telegram-bridge.err.log",
            Path(self.config["telegram_config_path"]).parent / "telegram-bridge.log",
            Path(self.config["telegram_config_path"]).parent / "telegram-bridge.err.log",
        ]:
            try:
                if path.exists() and path.stat().st_size > max_bytes:
                    archive = path.with_suffix(path.suffix + f".{int(time.time())}.old")
                    path.rename(archive)
                    path.write_text("", encoding="utf-8")
                    rotated.append(str(path))
            except Exception as exc:
                self.log(f"log_rotate_failed path={path} error={exc}")
        return rotated

    def read_tail(self, path, max_lines=80):
        try:
            lines = Path(path).read_text(encoding="utf-8", errors="replace").splitlines()
            return "\n".join(lines[-max_lines:])
        except Exception:
            return ""

    def odysseus_review(self, status, actions):
        url = self.telegram_config.get("odysseus_base_url", "http://127.0.0.1:7860").rstrip("/")
        prompt = f"""You are Kuschi OS doing autonomous local self-review.

Review this local assistant health snapshot. Be direct and practical.
Return:
1. Status
2. Problems
3. Improvements applied
4. Next low-risk improvement

Guardrails: do not recommend deleting data, sending emails, spending money,
changing passwords, connecting new accounts, or sending arbitrary files.

Status JSON:
{json.dumps(status, indent=2)}

Actions:
{json.dumps(actions, indent=2)}

Recent autopilot log:
{self.read_tail(self.log_path, 60)}
"""
        try:
            form = urllib.parse.urlencode({
                "name": "Autopilot daily self-review",
                "endpoint_id": self.telegram_config.get("endpoint_id", ""),
                "model": self.telegram_config.get("fast_model", "qwen3:8b"),
                "rag": "false",
            }).encode("utf-8")
            req = urllib.request.Request(
                f"{url}/api/session",
                data=form,
                headers={**self.api_headers(), "Content-Type": "application/x-www-form-urlencoded"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=30) as res:
                session = json.loads(res.read().decode("utf-8"))

            payload = {
                "message": prompt,
                "session": session["id"],
                "attachments": [],
                "use_web": False,
                "use_research": False,
            }
            data = http_json(
                f"{url}/api/chat",
                method="POST",
                payload=payload,
                headers=self.api_headers(),
                timeout=240,
            )
            return data.get("response", "").strip()
        except Exception as exc:
            self.log(f"odysseus_review_failed error={exc}")
            return ""

    def maybe_daily_report(self, status, actions):
        hour = int(self.config.get("daily_report_hour", 7))
        now = datetime.now()
        today_key = now.strftime("%Y-%m-%d")
        if now.hour < hour:
            return
        if self.state.get("last_daily_report") == today_key:
            return
        if not status["odysseus"]["ok"]:
            return

        review = self.odysseus_review(status, actions)
        if not review:
            review = "Daily self-review could not be generated, but health checks completed."
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        report_path = self.reports_dir / f"{today_key}.md"
        report_path.write_text(f"# Odysseus Autopilot {today_key}\n\n{review}\n", encoding="utf-8")
        self.state["last_daily_report"] = today_key
        save_json(self.state_path, self.state)
        self.tg_send("Odysseus daily self-review\n\n" + review[:3300])

    def alert_on_change(self, status, actions):
        compact = {
            "odysseus": bool(status["odysseus"]["ok"]),
            "ollama": bool(status["ollama"]["ok"]),
            "telegram_bridge": bool(status["telegram_bridge"]["ok"]),
            "google_bridge": bool(status["google_bridge"]["ok"]),
        }
        previous = self.state.get("last_compact_status")
        self.state["last_compact_status"] = compact
        save_json(self.state_path, self.state)

        if actions or previous != compact:
            lines = [
                "Odysseus autopilot update",
                f"Odysseus: {'OK' if compact['odysseus'] else 'DOWN'}",
                f"Ollama: {'OK' if compact['ollama'] else 'DOWN'}",
                f"Telegram bridge: {'OK' if compact['telegram_bridge'] else 'DOWN'}",
                f"Google read bridge: {'OK' if compact['google_bridge'] else 'DOWN'}",
            ]
            if actions:
                lines.append("Actions: " + ", ".join(actions))
            self.tg_send("\n".join(lines))

    def run_once(self):
        rotated = self.rotate_large_logs()
        actions = [f"rotated log {p}" for p in rotated]

        status = {
            "odysseus": self.check_odysseus(),
            "ollama": self.check_ollama(),
            "telegram_bridge": self.check_telegram_bridge(),
            "google_bridge": self.check_google_bridge(),
            "timestamp": now_iso(),
        }

        if not status["ollama"]["ok"]:
            actions.append(f"ollama restart {self.restart_ollama()}")
            time.sleep(5)
            status["ollama_after_restart"] = self.check_ollama()

        if not status["odysseus"]["ok"]:
            actions.append(f"odysseus restart {self.restart_odysseus()}")
            time.sleep(8)
            status["odysseus_after_restart"] = self.check_odysseus()

        if not status["telegram_bridge"]["ok"]:
            actions.append(f"telegram bridge {self.restart_telegram_bridge()}")
            time.sleep(3)
            status["telegram_bridge_after_restart"] = self.check_telegram_bridge()

        if not status["google_bridge"]["ok"]:
            actions.append(f"google bridge {self.restart_google_bridge()}")
            time.sleep(3)
            status["google_bridge_after_restart"] = self.check_google_bridge()

        self.log("status=" + json.dumps(status, sort_keys=True) + " actions=" + json.dumps(actions))
        self.alert_on_change(status, actions)
        self.maybe_daily_report(status, actions)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    Autopilot(args.config).run_once()


if __name__ == "__main__":
    main()
