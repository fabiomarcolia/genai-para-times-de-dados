from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, List

import pandas as pd

from src.llm import generate
from src.utils import load_env

OUT = Path("demos/04-data-quality/REPORT.md")


def suggest_rules(df: pd.DataFrame) -> List[str]:
    rules = []
    if "revenue" in df.columns and "quantity" in df.columns and "unit_price" in df.columns:
        rules.append("revenue deve ser igual a quantity * unit_price (tolerância pequena por arredondamento).")
    if "date" in df.columns:
        rules.append("date deve estar no formato ISO YYYY-MM-DD e não pode estar vazio.")
    if "quantity" in df.columns:
        rules.append("quantity deve ser >= 1.")
    if "unit_price" in df.columns:
        rules.append("unit_price deve ser > 0.")
    return rules


def main() -> None:
    load_env()
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True)
    args = parser.parse_args()

    df = pd.read_csv(args.csv)
    profile = df.describe(include="all").to_string()

    rules = suggest_rules(df)
    rules_md = "\n".join([f"- {r}" for r in rules])

    base = f"""# Relatório de Data Quality
Fonte: `{args.csv}`

## Resumo do dataset
- Linhas: {len(df)}
- Colunas: {len(df.columns)}
- Colunas: {", ".join(df.columns)}

## Perfil estatístico
```text
{profile}
```

## Regras sugeridas (mínimo viável)
{rules_md}

## Próximos passos
- Implementar validações automáticas (pytest ou Great Expectations)
- Criar alertas para anomalias
- Versionar o dataset de avaliação (ex.: casos de erro)
"""

    prompt = f"""Transforme o relatório abaixo em uma versão mais executiva e acionável.
- Mantenha as seções.
- Não invente informações.

Relatório:
{base}
"""
    llm = generate(prompt).text.strip()
    OUT.write_text(llm if llm else base, encoding="utf-8")
    print(f"Gerado: {OUT}")


if __name__ == "__main__":
    main()
