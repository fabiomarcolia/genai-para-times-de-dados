# Demo 02 — SQL Copilot (com validação em SQLite)
Objetivo: converter perguntas em SQL, explicar a lógica e executar em um banco SQLite de exemplo.

## Rodar
1- Criar banco
```bash
python demos/2-sql-copilot/create_db.py
```

2- Perguntar
```bash
python demos/2-sql-copilot/copilot.py --question "Faturamento por mês"
```

## Observação
- O modo sem LLM usa “templates” simples.
- Com LLM (Ollama/OpenAI), ele gera SQL mais flexível.
