"""
Pipeline end-to-end:
1) Generate report (agent.py)
2) Render PDF (render_pdf.py)
3) Send to Slack (send_slack.py) [optional]
4) Send email (send_email.py) [optional]

This is meant to be "production-shaped" without being complex:
- explicit steps
- deterministic artifacts (md/json/pdf/png)
- env-based integrations

Usage example:
  python pipeline.py --input sample_data.csv --out out --send slack email

Tip:
  Create a .env file (see .env.example) and export variables before running.
"""
from __future__ import annotations

import os
import subprocess
from pathlib import Path


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def pipeline(input_path: Path, out_dir: Path, send: list[str]) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)

    report_md = out_dir / "report.md"
    summary_json = out_dir / "summary.json"
    figures_dir = out_dir / "figures"
    pdf_path = out_dir / "report.pdf"

    # 1) Agent report
    run(["python", "agent.py", "--input", str(input_path), "--output", str(out_dir)])

    # 2) PDF
    run(["python", "render_pdf.py", "--report", str(report_md), "--figures", str(figures_dir), "--out", str(pdf_path)])

    # 3) Integrations (optional)
    summary_text = ""
    if summary_json.exists():
        try:
            import json
            data = json.loads(summary_json.read_text(encoding="utf-8"))
            headline = data.get("headline", "")
            kpis = data.get("kpis", {})
            if headline:
                summary_text += f"*{headline}*\n"
            if kpis:
                # Keep it short for Slack
                items = list(kpis.items())[:6]
                summary_text += " | ".join([f"{k}: {v}" for k, v in items])
        except Exception:
            pass

    send = [s.lower().strip() for s in send]

    if "slack" in send:
        run(["python", "send_slack.py", "--pdf", str(pdf_path), "--summary", summary_text])

    if "email" in send:
        body = "Segue relatório em PDF.\n\n" + (summary_text or "")
        run(["python", "send_email.py", "--pdf", str(pdf_path), "--body", body])

    print(f"✅ Pipeline concluído. Artefatos em: {out_dir.resolve()}")
    print(f"   - {pdf_path.name}")
    print(f"   - {report_md.name}")
    print(f"   - {summary_json.name}")
    print(f"   - figures/*.png")


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="CSV input")
    ap.add_argument("--out", default="out", help="Output folder")
    ap.add_argument("--send", nargs="*", default=[], help="Integrations: slack email")
    args = ap.parse_args()

    pipeline(Path(args.input), Path(args.out), args.send)
