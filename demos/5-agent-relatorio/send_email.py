"""
Send the PDF report via SMTP email.

Environment variables:
  EMAIL_SMTP_HOST=smtp.gmail.com
  EMAIL_SMTP_PORT=587
  EMAIL_SMTP_USER=...
  EMAIL_SMTP_PASS=...  (use app password when needed)
  EMAIL_FROM="MentorDados <contato@mentordados.com>"
  EMAIL_TO="you@company.com,other@company.com"
  EMAIL_SUBJECT="Relatório automático - Demo 05"

This uses STARTTLS (port 587). For SSL (465), adapt accordingly.

No extra deps.
"""
from __future__ import annotations

import os
import smtplib
from email.message import EmailMessage
from pathlib import Path


def send_email(pdf_path: Path, body_text: str) -> None:
    host = os.getenv("EMAIL_SMTP_HOST", "").strip()
    port = int(os.getenv("EMAIL_SMTP_PORT", "587"))
    user = os.getenv("EMAIL_SMTP_USER", "").strip()
    password = os.getenv("EMAIL_SMTP_PASS", "").strip()

    sender = os.getenv("EMAIL_FROM", "").strip()
    to = os.getenv("EMAIL_TO", "").strip()
    subject = os.getenv("EMAIL_SUBJECT", "Relatório automático - Demo 05").strip()

    if not (host and sender and to):
        raise RuntimeError("Email não configurado. Defina EMAIL_SMTP_HOST, EMAIL_FROM e EMAIL_TO (e credenciais se necessário).")

    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body_text or "Segue relatório em anexo.")

    if pdf_path.exists():
        msg.add_attachment(pdf_path.read_bytes(), maintype="application", subtype="pdf", filename=pdf_path.name)

    with smtplib.SMTP(host, port, timeout=60) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        if user and password:
            smtp.login(user, password)
        smtp.send_message(msg)


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", required=True)
    ap.add_argument("--body", default="")
    args = ap.parse_args()

    send_email(Path(args.pdf), args.body)
