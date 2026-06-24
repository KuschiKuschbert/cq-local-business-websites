# Microsoft Read Bridge

Local read-only Microsoft Graph bridge for Odysseus/Telegram context.

## What it reads

- Outlook/Microsoft 365 calendars through Microsoft Graph.
- Event title, date/time, body/details, location, organiser, attendees, recurrence, categories, and web link.

It does not write, send, delete, or modify anything.

## Runtime

- Service URL: `http://127.0.0.1:8767`
- Runtime folder: `~/Library/Application Support/MicrosoftReadBridge`
- LaunchAgent: `com.kuschi.microsoft-read-bridge`

## Required Microsoft app setup

Create an Entra ID app registration for device-code auth:

1. Azure portal -> Microsoft Entra ID -> App registrations -> New registration.
2. Name: `Odysseus Microsoft Read Bridge`.
3. Supported account types: accounts in this organisational directory, or multitenant if needed.
4. Authentication -> Allow public client flows: `Yes`.
5. API permissions -> Microsoft Graph delegated:
   - `User.Read`
   - `Calendars.Read`
   - `offline_access`
6. Copy the Application (client) ID into:
   `~/Library/Application Support/MicrosoftReadBridge/config.json`

If the tenant blocks user consent, a Microsoft 365 admin must grant consent.

## Authorise account

```sh
python3 "$HOME/Library/Application Support/MicrosoftReadBridge/authorize.py" \
  --config "$HOME/Library/Application Support/MicrosoftReadBridge/config.json" \
  --account lan_kitchen
```

The script prints a Microsoft device-login URL and code.

## Check

```sh
curl -s http://127.0.0.1:8767/health | python3 -m json.tool
curl -s 'http://127.0.0.1:8767/calendar?q=riviera%20events%20this%20week' | python3 -m json.tool
```
