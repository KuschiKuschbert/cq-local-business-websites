#!/bin/sh
set -eu

SRC_DIR="/Users/danielkuschmierz/Documents/website ideas/.agent/telegram-odysseus-bridge"
APP_DIR="$HOME/Library/Application Support/OdysseusTelegramBridge"
DST="$HOME/Library/LaunchAgents/com.kuschi.odysseus-telegram.plist"

mkdir -p "$APP_DIR/outbox"
cp "$SRC_DIR/bridge.py" "$APP_DIR/bridge.py"
cp "$SRC_DIR/config.json" "$APP_DIR/config.json"
if [ -f "$SRC_DIR/state.json" ] && [ ! -f "$APP_DIR/state.json" ]; then cp "$SRC_DIR/state.json" "$APP_DIR/state.json"; fi
if [ -f "$SRC_DIR/sessions.json" ] && [ ! -f "$APP_DIR/sessions.json" ]; then cp "$SRC_DIR/sessions.json" "$APP_DIR/sessions.json"; fi
python3 - "$APP_DIR/config.json" "$APP_DIR/outbox" <<'PY'
import json
import sys
from pathlib import Path

config_path = Path(sys.argv[1])
outbox_dir = sys.argv[2]
config = json.loads(config_path.read_text(encoding="utf-8"))
config["outbox_dir"] = outbox_dir
config_path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
PY

mkdir -p "$HOME/Library/LaunchAgents"
cat > "$DST" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.kuschi.odysseus-telegram</string>

  <key>ProgramArguments</key>
  <array>
    <string>/usr/bin/python3</string>
    <string>$APP_DIR/bridge.py</string>
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
  <string>$APP_DIR/telegram-bridge.log</string>

  <key>StandardErrorPath</key>
  <string>$APP_DIR/telegram-bridge.err.log</string>
</dict>
</plist>
PLIST

launchctl unload "$DST" >/dev/null 2>&1 || true
launchctl load "$DST"
echo "Installed and started: $DST"
echo "Runtime files: $APP_DIR"
