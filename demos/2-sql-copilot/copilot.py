from __future__ import annotations

import argparse
import os
import sqlite3
from pathlib import Path
from typing import Tuple

from rich.console import Console
from rich.markdown import Markdown

from src.llm import generate
from src.utils import load_env

console = Console()
DB_PATH = Path("demos/02-sql-copilot/demo.db")


SCHEMA = """Tabela: sales
Colunas:
- order_id (int)
- date (text, ISO: YYYY-MM-DD)
- category (text)
- region (text)
- quantity (int)
- unit_price (real)
- revenue (real)
"""


def template_sql(question: str) -> Tuple[str, str]:
    q = question.lower()
    if "mês" in q or "mes" in q:
        sql = """
SELECT substr(date, 1, 7) AS month,
       SUM(revenue) AS total_revenue
FROM sales
GROUP BY 1
ORDER BY 1;
""".strip()
        explanation = "Agrupa por mês (YYYY-MM) e soma a receita."
        return sql, explanation
    if "categoria" in q:
        sql = """
SELECT category,
       SUM(revenue) AS total_revenue
FROM sales
GROUP BY 1
ORDER BY total_revenue DESC;
""".strip()
        explanation = "Agrupa por categoria e ordena pela receita total."
        return sql, explanation

    # fallback
    sql = "SELECT COUNT(*) AS rows, SUM(revenue) AS total_revenue FROM sales;"
    explanation = "Resumo geral do dataset (linhas e receita total)."
    return sql, explanation


def llm_sql(question: str) -> Tuple[str, str]:
    prompt = f"""Você é um especialista em SQL.
Gere uma query SQLite para responder a pergunta usando o esquema.

Esquema:
{SCHEMA}

Pergunta:
{question}

Regras:
- Retorne APENAS um JSON com chaves: sql, explanation
- explanation deve ter no máximo 8 linhas

JSON:
"""
    text = generate(prompt).text.strip()
    if not text:
        return template_sql(question)

    # tolerância a pequenos desvios
    import json
    try:
        obj = json.loads(text)
        return obj["sql"].strip(), obj["explanation"].strip()
    except Exception:
        return template_sql(question)


def run(sql: str) -> str:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute(sql)
    cols = [d[0] for d in cur.description]
    rows = cur.fetchmany(20)
    con.close()

    lines = []
    lines.append("Colunas: " + ", ".join(cols))
    lines.append("Amostra (até 20 linhas):")
    for r in rows:
        lines.append(" - " + " | ".join(str(x) for x in r))
    return "\n".join(lines)


def main() -> None:
    load_env()
    parser = argparse.ArgumentParser()
    parser.add_argument("--question", required=True)
    args = parser.parse_args()

    if not DB_PATH.exists():
        raise SystemExit("Banco não encontrado. Rode: python demos/02-sql-copilot/create_db.py")

    provider = os.environ.get("LLM_PROVIDER", "none").lower()
    if provider == "none":
        sql, explanation = template_sql(args.question)
    else:
        sql, explanation = llm_sql(args.question)

    result_preview = run(sql)

    out = f"""## Pergunta
{args.question}

## SQL
```sql
{sql}
```

## Explicação
{explanation}

## Preview da execução
```text
{result_preview}
```
"""
    console.print(Markdown(out))


if __name__ == "__main__":
    main()
