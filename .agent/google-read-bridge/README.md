# Google Read Bridge

Local read-only Google bridge for Odysseus and Telegram.

## Scope

Configured OAuth scopes:

- Google Calendar read-only
- Google Calendar events read-only
- Google Drive read-only
- Gmail read-only
- Google Contacts read-only
- Google Tasks read-only

This bridge does not send email, edit files, create calendar events, delete data,
share files, or write to Google services.

## NotebookLM

NotebookLM is not queried directly. Use the source material behind NotebookLM:
Google Docs, PDFs, Sheets, Slides, and exported notebook material in Drive.

## First-Time Setup

Create a Google OAuth Desktop client:

1. Open Google Cloud Console.
2. Create or choose a project.
3. Enable these APIs:
   - Google Calendar API
   - Google Drive API
   - Gmail API
   - People API
   - Google Tasks API
4. Configure OAuth consent for personal/testing use.
5. Add your Google account as a test user if the app is in testing mode.
6. Create OAuth Client ID -> Desktop app.
7. Download the JSON file.
8. Place the downloaded JSON here:

```text
~/Library/Application Support/GoogleReadBridge/client_secret.json
```

Then run:

```bash
python3 "$HOME/Library/Application Support/GoogleReadBridge/authorize.py" --config "$HOME/Library/Application Support/GoogleReadBridge/config.json"
```

The browser will open for the one-time Google consent flow. Tokens are stored
locally at:

```text
~/Library/Application Support/GoogleReadBridge/token.json
```

## Endpoints

```text
GET http://127.0.0.1:8765/health
GET http://127.0.0.1:8765/context?q=what%20is%20on%20today
GET http://127.0.0.1:8765/calendar?q=tomorrow
GET http://127.0.0.1:8765/drive/search?q=Riviera%20menu
GET http://127.0.0.1:8765/gmail/search?q=unread%20venue
```
