# Telegram -> Odysseus Bridge

This bridge lets Telegram behave like a normal chat front end for Odysseus.
Slash commands are optional. Plain messages are routed by intent in the
background, then sent to the right Odysseus preset/model.

## What It Does

- Accepts normal Telegram messages.
- Allows only configured Telegram chat IDs.
- Keeps one Odysseus chat session per Telegram chat.
- Routes messages to Riviera, recipe/costing, kitchen SOP, business outreach,
  dev, or daily admin presets.
- Uses `qwen3:14b` for quality work and `qwen3:8b` for faster admin-style work.
- Can send files from the configured `outbox_dir` only.
- Can receive Telegram current/live location from Android and store it locally
  for location status and geofence reminders.
- Can save Keep-style quick notes from Telegram and provide them back to
  Odysseus as trusted local context.

## Setup

1. Create a Telegram bot with BotFather and get the bot token.
2. Copy `config.example.json` to `config.json`.
3. Add the Telegram bot token.
4. Leave `allowed_chat_ids` empty for the first run only.
5. Run the bridge and send any message to the bot.
6. The bridge will print your chat ID. Add it to `allowed_chat_ids`.
7. Restart the bridge.

## Run

```bash
python3 .agent/telegram-odysseus-bridge/bridge.py --config .agent/telegram-odysseus-bridge/config.json
```

## Natural Examples

```text
Draft a Riviera caption for Sunday tapas.
```

```text
Scale this recipe to 80 pax and flag allergens.
```

```text
Turn this into a staff SOP.
```

```text
Audit this website and write a short outreach message: https://example.com
```

```text
Send me the latest file.
```

```text
keep: order more blue gloves for Riviera
```

```text
show notes about Riviera
```

## Android Location

Open the bot on Android, tap attach, choose Location, then send either current
location or live location. The bridge stores the latest point in
`phone_state.json` beside the bridge runtime files.

## Android Phone Bridge

The bot can also act as the Telegram front door for the Mac phone bridge. These
messages send the current setup/dashboard link from the Cloudflare tunnel:

```text
phone setup
```

```text
phone dashboard
```

```text
telegram advantage
```

For status only:

```text
phone bridge status
```

The setup page can send a test message, browser GPS, and appointment notes back
to Telegram/Odysseus. Always-on alarms, notifications, and calendar snapshots
still require Android-side permission through Tasker, Automate, MacroDroid, or
a companion app.

Useful messages:

```text
where am I
```

```text
set place Riviera here
```

```text
places
```

```text
remind me when I get to Riviera to check the coolroom
```

```text
geofence reminders
```

```text
forget location
```

Geofence reminders only fire when Telegram sends a new location update. For
continuous background use, share live location to the bot from Android.

## Google Keep Notes

`keep:` and `note:` save a local Odysseus backup and also try to create a real
Google Keep note in the configured Google account. Default account:
`riviera_kitchen` / `kitchen@rivierayeppoon.com`.

Google Keep writes require the Google OAuth token for `riviera_kitchen` to have
the `https://www.googleapis.com/auth/keep` scope. If that scope is missing, the
Telegram bot still saves the local backup and replies with the re-authorisation
step.

Save notes:

```text
keep: order more blue gloves
```

```text
note: Jade and Simon need pig-on-spit prep checked
```

```text
remember this: PrepFlow stocktake needs voice capture
```

List/search notes:

```text
notes
```

```text
show notes about Riviera
```

```text
find notes prepflow
```

Archive a note:

```text
delete note 12345678
```

Export notes to Telegram:

```text
export notes
```

Push unsynced local backup notes after Google Keep OAuth has been approved:

```text
sync notes to google keep
```

## File Safety

The bot only sends files from `outbox_dir`. It will not send random files from
your Mac, Odysseus data, Google Drive exports, or project folders.

## Location Safety

The bridge does not pull GPS silently. It only receives location that you send
or live-share through Telegram. Location history stays local on the Mac and can
be cleared with `forget location`.
