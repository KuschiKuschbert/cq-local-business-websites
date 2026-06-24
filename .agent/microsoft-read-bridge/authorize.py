#!/usr/bin/env python3
import argparse
import urllib.error
import json
import time
from pathlib import Path

from microsoft_read_bridge import MicrosoftReadBridge, http_json, read_json, write_json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--account", default="")
    args = parser.parse_args()

    config = read_json(args.config)
    if not config.get("client_id") or str(config.get("client_id")).startswith("PASTE_"):
        raise SystemExit(
            "Missing Microsoft client_id. Create an Entra ID app registration, enable public client flows, "
            "then put its Application (client) ID in config.json."
        )

    bridge = MicrosoftReadBridge(args.config)
    accounts = config.get("accounts") or []
    if not accounts:
        raise SystemExit("No accounts configured.")
    account = accounts[0]
    if args.account:
        matches = [item for item in accounts if item.get("name") == args.account or item.get("email") == args.account]
        if not matches:
            raise SystemExit(f"Unknown account '{args.account}'. Add it to config.json accounts first.")
        account = matches[0]

    scope = " ".join(config["scopes"])
    device = http_json(bridge.device_code_url(account), method="POST", form={
        "client_id": config["client_id"],
        "scope": scope,
    })

    print(json.dumps({
        "account": account.get("name"),
        "email": account.get("email", ""),
        "verification_uri": device.get("verification_uri"),
        "user_code": device.get("user_code"),
        "message": device.get("message"),
        "expires_in": device.get("expires_in"),
    }, indent=2), flush=True)

    interval = int(device.get("interval", 5))
    deadline = time.time() + int(device.get("expires_in", 900))
    while time.time() < deadline:
        time.sleep(interval)
        try:
            token = http_json(bridge.token_url(account), method="POST", form={
                "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                "client_id": config["client_id"],
                "device_code": device["device_code"],
            })
            token["expires_at"] = time.time() + int(token.get("expires_in", 3600))
            token["connected_at"] = time.time()
            write_json(account["token_path"], token)
            print(json.dumps({
                "connected": True,
                "account": account.get("name"),
                "email": account.get("email", ""),
                "scopes": token.get("scope", ""),
                "token_path": account["token_path"],
            }, indent=2))
            return
        except urllib.error.HTTPError as exc:
            text = exc.read().decode("utf-8", errors="replace")
            if "authorization_pending" in text:
                continue
            if "slow_down" in text:
                interval += 5
                continue
            raise
        except Exception as exc:
            text = str(exc)
            if "authorization_pending" in text:
                continue
            if "slow_down" in text:
                interval += 5
                continue
            raise

    raise SystemExit("Microsoft device login expired. Run authorize.py again.")


if __name__ == "__main__":
    main()
