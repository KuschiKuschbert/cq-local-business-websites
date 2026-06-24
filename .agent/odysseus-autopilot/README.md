# Odysseus Autopilot

Local background monitor for Kuschi's Odysseus setup.

## What It Does

- Checks Odysseus liveness.
- Checks Ollama liveness.
- Checks the Telegram bridge LaunchAgent.
- Restarts Odysseus, Ollama, or the Telegram bridge when safely possible.
- Sends Telegram alerts on status changes or repair actions.
- Writes a daily self-review report once Odysseus is healthy.
- Rotates oversized local logs.

## Guardrails

Autopilot may restart local services, rotate logs, create reports, and send
status alerts to the approved Telegram chat.

It must not delete project data, send email, spend money, change passwords,
connect accounts, install software, or send arbitrary files.

## Runtime

Installed runtime path:

```text
~/Library/Application Support/OdysseusAutopilot
```

LaunchAgent:

```text
~/Library/LaunchAgents/com.kuschi.odysseus-autopilot.plist
```
