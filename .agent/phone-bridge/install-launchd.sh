#!/bin/sh
set -eu

SRC_DIR="/Users/danielkuschmierz/Documents/website ideas/.agent/phone-bridge"
APP_DIR="$HOME/Library/Application Support/OdysseusPhoneBridge"
DST="$HOME/Library/LaunchAgents/com.kuschi.odysseus-phone-bridge.plist"

mkdir -p "$APP_DIR"
cp "$SRC_DIR/phone_bridge.py" "$APP_DIR/phone_bridge.py"
if [ ! -f "$APP_DIR/config.json" ]; then
  cp "$SRC_DIR/config.example.json" "$APP_DIR/config.json"
fi

python3 - <<PY
import json, pathlib, secrets
p = pathlib.Path("$APP_DIR/config.json")
cfg = json.loads(p.read_text())
if not cfg.get("auth_token") or str(cfg.get("auth_token")).startswith("CHANGE_ME"):
    cfg["auth_token"] = secrets.token_urlsafe(32)
if not cfg.get("setup_token") or str(cfg.get("setup_token")).startswith("CHANGE_ME"):
    cfg["setup_token"] = secrets.token_urlsafe(32)
tmp = p.with_suffix(".tmp")
tmp.write_text(json.dumps(cfg, indent=2) + "\\n")
tmp.replace(p)
p.chmod(0o600)
PY

mkdir -p "$HOME/Library/LaunchAgents"
cat > "$DST" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.kuschi.odysseus-phone-bridge</string>

  <key>ProgramArguments</key>
  <array>
    <string>/usr/bin/python3</string>
    <string>$APP_DIR/phone_bridge.py</string>
    <string>--config</string>
    <string>$APP_DIR/config.json</string>
  </array>

  <key>WorkingDirectory</key>
  <string>$APP_DIR</string>

  <key>RunAtLoad</key>
  <true/>

  <key>KeepAlive</key>
  <true/>

  <key>StandardOutPath</key>
  <string>$APP_DIR/phone-bridge.log</string>

  <key>StandardErrorPath</key>
  <string>$APP_DIR/phone-bridge.err.log</string>
</dict>
</plist>
PLIST

launchctl unload "$DST" >/dev/null 2>&1 || true
launchctl load "$DST"
echo "Installed and started: $DST"
echo "Runtime files: $APP_DIR"
