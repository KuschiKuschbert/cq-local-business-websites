#!/bin/sh
set -eu

SRC_DIR="/Users/danielkuschmierz/Documents/website ideas/.agent/google-read-bridge"
APP_DIR="$HOME/Library/Application Support/GoogleReadBridge"
DST="$HOME/Library/LaunchAgents/com.kuschi.google-read-bridge.plist"

mkdir -p "$APP_DIR"
cp "$SRC_DIR/google_read_bridge.py" "$APP_DIR/google_read_bridge.py"
cp "$SRC_DIR/authorize.py" "$APP_DIR/authorize.py"
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
  <string>com.kuschi.google-read-bridge</string>

  <key>ProgramArguments</key>
  <array>
    <string>/usr/bin/python3</string>
    <string>$APP_DIR/google_read_bridge.py</string>
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
  <string>$APP_DIR/google-read-bridge.log</string>

  <key>StandardErrorPath</key>
  <string>$APP_DIR/google-read-bridge.err.log</string>
</dict>
</plist>
PLIST

launchctl unload "$DST" >/dev/null 2>&1 || true
launchctl load "$DST"
echo "Installed and started: $DST"
echo "Runtime files: $APP_DIR"
