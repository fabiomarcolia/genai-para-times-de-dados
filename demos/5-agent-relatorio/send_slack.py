"""
Send a PDF/report summary to Slack.

Two modes:
1) Webhook-only (simple): SLACK_WEBHOOK_URL
   - Sends a message and (optionally) a short summary text.
   - Webhooks CANNOT upload files, so PDF won't be attached.

2) Bot token (file upload): SLACK_BOT_TOKEN + SLACK_CHANNEL
   - Uploads the PDF as a file and posts an initial comment.

Environment variables:
  SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
  SLACK_BOT_TOKEN=xoxb-...
  SLACK_CHANNEL=C01234567 or #channel-name

Requires: requests
"""
from __future__ import annotations

import os
from pathlib import Path

import requests


def _post_webhook(webhook_url: str, text: str) -> None:
    r = requests.post(webhook_url, json={"text": text}, timeout=30)
    r.raise_for_status()


def _upload_file(token: str, channel: str, file_path: Path, initial_comment: str) -> None:
    url = "https://slack.com/api/files.upload"
    with file_path.open("rb") as f:
        r = requests.post(
            url,
            headers={"Authorization": f"Bearer {token}"},
            data={"channels": channel, "initial_comment": initial_comment},
            files={"file": (file_path.name, f, "application/pdf")},
            timeout=60,
        )
    r.raise_for_status()
    data = r.json()
    if not data.get("ok"):
        raise RuntimeError(f"Slack API error: {data}")


def send_slack(pdf_path: Path, summary_text: str) -> None:
    webhook = os.getenv("SLACK_WEBHOOK_URL", "").strip()
    token = os.getenv("SLACK_BOT_TOKEN", "").strip()
    channel = os.getenv("SLACK_CHANNEL", "").strip()

    message = summary_text.strip() if summary_text.strip() else f"Relatório gerado: {pdf_path.name}"

    if token and channel:
        _upload_file(token, channel, pdf_path, message)
        return

    if webhook:
        # Webhook can't upload files; we still send message.
        if pdf_path.exists():
            message += f"\n(Arquivo PDF pronto localmente: {pdf_path.name}. Para anexar, use SLACK_BOT_TOKEN + SLACK_CHANNEL.)"
        _post_webhook(webhook, message)
        return

    raise RuntimeError("Slack não configurado. Defina SLACK_WEBHOOK_URL ou SLACK_BOT_TOKEN + SLACK_CHANNEL.")


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", required=True)
    ap.add_argument("--summary", default="")
    args = ap.parse_args()

    send_slack(Path(args.pdf), args.summary)
