from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import List

import pandas as pd
from rich.console import Console
from rich.markdown import Markdown

from src.chunking import chunk_text
from src.llm import generate
from src.retrieval import DocChunk, TfidfRetriever
from src.utils import load_env

console = Console()


def build_corpus(df: pd.DataFrame) -> str:
    # Transforme a tabela em um texto "consultável"
    # (Em produção você faria chunking por entidades/linhas e guardaria metadados melhores.)
    lines = []
    lines.append("Tabela: sales.csv")
    lines.append("Colunas: " + ", ".join(df.columns))
    lines.append("Amostra:")
    lines.append(df.head(20).to_csv(index=False))
    lines.append("Estatísticas rápidas:")
    lines.append(df.describe(include='all').to_string())
    return "\n".join(lines)


def answer_offline(question: str, chunks: List[DocChunk], top_k: int) -> str:
    retriever = TfidfRetriever(chunks)
    hits = retriever.search(question, top_k=top_k)

    if not hits:
        return "Não encontrei contexto suficiente no dataset para responder com segurança."

    context_blocks = []
    for i, (chunk, score) in enumerate(hits, start=1):
        context_blocks.append(f"[fonte:{i}] {chunk.text}")

    context = "\n\n".join(context_blocks)
    prompt = f"""Você é um analista de dados sênior.
Responda a pergunta usando APENAS o contexto fornecido.
- Se faltar informação, diga o que faltou.
- Quando citar fatos, use as citações [fonte:N].

Contexto:
{context}

Pergunta:
{question}

Resposta (em português, objetiva):
"""

    llm = generate(prompt)
    if llm.text.strip():
        return llm.text.strip()

    # Modo sem LLM: devolve um resumo do que foi recuperado.
    return "Modo offline (sem LLM). Contexto mais relevante:\n\n" + context


def main() -> None:
    load_env()
    parser = argparse.ArgumentParser()
    parser.add_argument("--question", required=True)
    parser.add_argument("--csv", default="datasets/sales.csv")
    args = parser.parse_args()

    df = pd.read_csv(args.csv)
    corpus = build_corpus(df)

    # Chunking
    raw_chunks = chunk_text(corpus, chunk_size=900, overlap=150)
    chunks = [DocChunk(text=c, source_id=f"sales:{i}") for i, c in enumerate(raw_chunks)]

    top_k = int(os.environ.get("TOP_K", "5"))
    out = answer_offline(args.question, chunks, top_k=top_k)

    console.print(Markdown(out))


if __name__ == "__main__":
    main()
