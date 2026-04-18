from __future__ import annotations

import json
import os
from pathlib import Path

from src.llm import generate
from src.utils import load_env

INPUT = Path("demos/03-dashboard-docs/metadata.sample.json")
OUTPUT = Path("demos/03-dashboard-docs/OUTPUT.md")


def md_from_metadata(meta: dict) -> str:
    pages = "\n".join([f"- {p['name']}: " + ", ".join(p["visuals"]) for p in meta["pages"]])
    metrics = "\n".join([f"- **{m['name']}**: `{m['definition']}`" for m in meta["metrics"]])
    limitations = "\n".join([f"- {x}" for x in meta.get("limitations", [])])

    return f"""# {meta['dashboard_name']}
## Visão geral
- Público-alvo: {meta['audience']}
- Atualização: {meta['refresh']}
- Fontes: {", ".join(meta['sources'])}

## Páginas e visuais
{pages}

## Métricas e definições
{metrics}

## Como interpretar
- Use a página “Visão Geral” para tendência (mês a mês).
- Use a página “Detalhe” para investigar variações.

## Limitações
{limitations}
"""


def main() -> None:
    load_env()
    meta = json.loads(INPUT.read_text(encoding="utf-8"))

    base_md = md_from_metadata(meta)

    # Se tiver LLM, melhora o texto (mantendo estrutura)
    prompt = f"""Reescreva a documentação abaixo para ficar mais clara e profissional.
- Mantenha títulos e estrutura.
- Não invente dados.

Documento:
{base_md}
"""
    llm = generate(prompt).text.strip()
    OUTPUT.write_text(llm if llm else base_md, encoding="utf-8")
    print(f"Gerado: {OUTPUT}")


if __name__ == "__main__":
    main()
