# Demo 06 — Linguagem Natural → Código Python (com validação)

Este demo transforma uma tarefa em linguagem natural (PT‑BR) em um script Python **reprodutível**,
com **validação** (AST policies) e execução automatizada.

> Objetivo: não é “gerar qualquer código”. É gerar **código seguro, padrão e testável**.

## Como rodar
1) Escreva a tarefa em `examples/task.md`  
2) Rode:

```bash
python generate.py --task examples/task.md --data examples/input.csv --out out
```

Saídas esperadas:
- `out/generated_task.py` — script gerado
- `out/resumo.csv` — tabela agregada
- `out/plot.png` — gráfico

## Modos
- Offline-first: por padrão, usa heurísticas e templates (sem LLM).
- LLM opcional: configure `LLM_PROVIDER=ollama` ou `openai` para melhorar o parsing da tarefa.

## Segurança (policies)
- Bloqueia imports e chamadas perigosas (ex.: `os`, `subprocess`, `eval`, `exec`)
- Permite apenas bibliotecas esperadas para análise (`pandas`, `matplotlib`, `numpy`)

Veja `policies.py`.
