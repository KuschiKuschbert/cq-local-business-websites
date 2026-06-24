# Odysseus Phone Bridge

Local bridge for Android automation tools such as Tasker, Automate, MacroDroid,
or a future custom Odysseus Android companion app.

## What This Enables

- Android sends phone events to the Mac.
- The Mac stores the event locally.
- Important events can be pushed to Telegram.
- Appointment-style events can be summarised through Odysseus before Telegram.

This is a bridge, not a silent phone exploit. Android still requires explicit
permissions on the phone side.

## Runtime

- Service: `com.kuschi.odysseus-phone-bridge`
- Default URL on Mac LAN: `http://<mac-ip>:8770`
- Health: `http://<mac-ip>:8770/health`
- Runtime folder: `~/Library/Application Support/OdysseusPhoneBridge`
- Config: `~/Library/Application Support/OdysseusPhoneBridge/config.json`
- State: `~/Library/Application Support/OdysseusPhoneBridge/phone_state.json`

All POSTs require the token from config:

```text
X-Phone-Bridge-Token: <auth_token>
```

## Telegram Setup Page

The phone bridge serves a mobile setup page at:

```text
/setup?setup=<setup_token>
```

The Telegram bridge generates the live Cloudflare link from the runtime config
and sends it to Kuschi's approved Telegram chat when he says `phone setup`,
`phone dashboard`, or `telegram advantage`.

The page can send a bridge test message, current browser GPS, and a quick
appointment note through Odysseus back to Telegram. It only sends events when
tapped. It does not silently read alarms, notifications, or calendars in the
background.

## Android Side Options

| Method | Best for | Notes |
|---|---|---|
| Tasker | Fastest serious setup | Can send HTTP POSTs for location, battery, notifications, calendar/alarms if configured. |
| Automate/MacroDroid | Easier visual flows | Similar idea, less flexible than Tasker. |
| Custom Odysseus Android app | Best long-term | Can use Calendar Provider, NotificationListenerService, location foreground service, and alarm intents. |
| Telegram only | Basic fallback | Good for messages/location sharing, weak for phone state. |

## Android Limits

- Calendar can be read by a granted app through Android Calendar Provider.
- Notifications can be observed by a granted Notification Listener.
- Location requires location permission and usually a foreground/live service.
- Android can set alarms through supported alarm intents.
- Android does not expose a clean public API to list every existing Clock alarm
  for arbitrary apps. Use Tasker/device variables, notification cues, or a
  companion-app workaround.

## Event Endpoint

```bash
curl -X POST "http://<mac-ip>:8770/event" \
  -H "Content-Type: application/json" \
  -H "X-Phone-Bridge-Token: <auth_token>" \
  -d '{
    "type": "appointment_reminder",
    "notify": true,
    "ask_llm": true,
    "data": {
      "title": "Riviera tasting",
      "start": "2026-06-22 14:00",
      "location": "Riviera Yeppoon",
      "notes": "Bring prep notes"
    }
  }'
```

## Useful Event Types

### `appointment_reminder`

Send a Telegram-ready appointment reminder. If `ask_llm` is true, Odysseus
summarises it first.

```json
{
  "type": "appointment_reminder",
  "notify": true,
  "ask_llm": true,
  "data": {
    "title": "Riviera wedding consult",
    "start": "2026-06-22 15:30",
    "location": "Riviera Yeppoon",
    "notes": "Ask about dietaries and run sheet"
  }
}
```

### `alarm_snapshot`

Report what the phone automation layer can see about alarms.

```json
{
  "type": "alarm_snapshot",
  "notify": true,
  "data": {
    "next_alarm": "2026-06-23 05:30",
    "alarms": ["05:30 Work", "07:00 Day off"]
  }
}
```

### `calendar_snapshot`

Report phone-side calendar entries if Tasker/companion app has calendar access.

```json
{
  "type": "calendar_snapshot",
  "notify": true,
  "data": {
    "events": [
      {"start": "2026-06-22 14:00", "title": "Riviera tasting", "location": "Riviera"}
    ]
  }
}
```

### `notification`

Forward a notification if it is appointment/work relevant.

```json
{
  "type": "notification",
  "notify": false,
  "data": {
    "app": "Calendar",
    "title": "Upcoming event",
    "text": "Riviera tasting at 14:00"
  }
}
```

### `battery`

```json
{
  "type": "battery",
  "notify": false,
  "data": {"level": 47, "charging": false}
}
```

## First Tasker Setup

1. Install Tasker on Android.
2. Create a task: `POST Phone Event`.
3. Add action: `Net -> HTTP Request`.
4. Method: `POST`.
5. URL: `http://<mac-ip>:8770/event`.
6. Headers:
   - `Content-Type: application/json`
   - `X-Phone-Bridge-Token: <auth_token>`
7. Body: use one of the JSON event examples above.

Start with appointment reminders and alarm snapshots. Once those work, add
notification/calendar/location profiles.
