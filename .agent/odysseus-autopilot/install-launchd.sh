#!/bin/sh
set -eu

SRC_DIR="/Users/danielkuschmierz/Documents/website ideas/.agent/odysseus-autopilot"
APP_DIR="$HOME/Library/Application Support/OdysseusAutopilot"
DST="$HOME/Library/LaunchAgents/com.kuschi.odysseus-autopilot.plist"

mkdir -p "$APP_DIR/reports"
cp "$SRC_DIR/autopilot.py" "$APP_DIR/autopilot.py"

if [ ! -f "$APP_DIR/config.json" ]; then
  cp "$SRC_DIR/config.example.json" "$APP_DIR/config.json"
fi

mkdir -p "$HOME/Library/LaunchAgents"
cat > "$DST" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.kuschi.odysseus-autopilot</string>

  <key>ProgramArguments</key>
  <array>
    <string>/usr/bin/python3</string>
    <string>$APP_DIR/autopilot.py</string>
    <string>--config</string>
    <string>$APP_DIR/config.json</string>
  </array>

  <key>WorkingDirectory</key>
  <string>$APP_DIR</string>

  <key>RunAtLoad</key>
  <true/>

  <key>StartInterval</key>
  <integer>300</integer>

  <key>StandardOutPath</key>
  <string>$APP_DIR/launchd.out.log</string>

  <key>StandardErrorPath</key>
  <string>$APP_DIR/launchd.err.log</string>
</dict>
</plist>
PLIST

launchctl unload "$DST" >/dev/null 2>&1 || true
launchctl load "$DST"
echo "Installed and started: $DST"
echo "Runtime files: $APP_DIR"
