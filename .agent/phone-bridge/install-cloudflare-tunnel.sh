#!/bin/sh
set -eu

APP_DIR="$HOME/Library/Application Support/OdysseusPhoneBridge"
DST="$HOME/Library/LaunchAgents/com.kuschi.odysseus-phone-tunnel.plist"
CLOUDFLARED="/opt/homebrew/bin/cloudflared"

if [ ! -x "$CLOUDFLARED" ]; then
  echo "cloudflared not found at $CLOUDFLARED" >&2
  exit 1
fi

mkdir -p "$APP_DIR"
mkdir -p "$HOME/Library/LaunchAgents"

cat > "$DST" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.kuschi.odysseus-phone-tunnel</string>

  <key>ProgramArguments</key>
  <array>
    <string>$CLOUDFLARED</string>
    <string>tunnel</string>
    <string>--url</string>
    <string>http://127.0.0.1:8770</string>
  </array>

  <key>WorkingDirectory</key>
  <string>$APP_DIR</string>

  <key>RunAtLoad</key>
  <true/>

  <key>KeepAlive</key>
  <true/>

  <key>StandardOutPath</key>
  <string>$APP_DIR/phone-tunnel.log</string>

  <key>StandardErrorPath</key>
  <string>$APP_DIR/phone-tunnel.err.log</string>
</dict>
</plist>
PLIST

launchctl unload "$DST" >/dev/null 2>&1 || true
launchctl load "$DST"
echo "Installed and started: $DST"
