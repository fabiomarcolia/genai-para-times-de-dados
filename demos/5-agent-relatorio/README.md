# Demo 05 — Agente de análise → Relatório (MD/JSON) → PDF → Slack/Email

Este demo mostra um pipeline “com cara de produção” para um caso comum em times de dados:

1- Um **agente** analisa um dataset e gera um **relatório em Markdown** + **JSON** + **figuras**  
2- O relatório é convertido em **PDF** (render simples, limpo e reproduzível)  
3- O PDF pode ser enviado para **Slack** e/ou **Email** via variáveis de ambiente  

---

## Quickstart (local)

```bash
# na raiz do repo
pip install -r requirements.txt

python demos/5-agent-relatorio/pipeline.py \
  --input demos/5-agent-relatorio/sample_data.csv \
  --out out
```

Artefatos gerados em `out/`:
- `report.md`
- `summary.json`
- `report.pdf`
- `figures/*.png`

---

## Enviar para Slack

### Opção A) Webhook (mais simples)
> Observação: Webhook **não** faz upload de arquivo. Ele só envia a mensagem (o PDF fica local).

```bash
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."
python demos/05-agent-relatorio/pipeline.py --input demos/05-agent-relatorio/sample_data.csv --out out --send slack
```

### Opção B) Upload do PDF (Slack Bot Token)
Requer um app/bot com permissão para upload de arquivos (ex.: `files:write`) e acesso ao canal.

```bash
export SLACK_BOT_TOKEN="xoxb-..."
export SLACK_CHANNEL="#data-alertas"   # ou ID do canal (ex.: C0123...)
python demos/5-agent-relatorio/pipeline.py --input demos/5-agent-relatorio/sample_data.csv --out out --send slack
```

---

## Enviar por Email (SMTP)

```bash
export EMAIL_SMTP_HOST="smtp.gmail.com"
export EMAIL_SMTP_PORT="587"
export EMAIL_SMTP_USER="seu-email@gmail.com"
export EMAIL_SMTP_PASS="SUA_APP_PASSWORD"
export EMAIL_FROM="MentorDados <contato@mentordados.com>"
export EMAIL_TO="destino@empresa.com"
export EMAIL_SUBJECT="Relatório automático — Demo 05"

python demos/5-agent-relatorio/pipeline.py --input demos/5-agent-relatorio/sample_data.csv --out out --send email
```

---

## Customização rápida (KPI e narrativa)
- KPIs e cortes do relatório estão no `agent.py`.  
- O PDF é gerado por `render_pdf.py` (fácil de ajustar layout).  
- Integrações: `send_slack.py` e `send_email.py` (env-based).

> Dica de autoridade: rode isso em cron / GitHub Actions e poste o PDF em um canal semanal do time.
