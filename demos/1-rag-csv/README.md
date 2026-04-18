# Demo 01 — RAG em CSV (offline-first)
Objetivo: responder perguntas sobre um CSV usando recuperação local (TF‑IDF) e, opcionalmente, um LLM para gerar a resposta final.

## Rodar
```bash
python demos/1-rag-csv/app.py --question "Qual foi o faturamento total por mês?"
```

## Entradas
- `datasets/sales.csv`

## Saída
- Resposta em texto + citações no formato `[fonte:N]`.
