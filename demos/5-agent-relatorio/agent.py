from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple

import pandas as pd
import matplotlib.pyplot as plt

from src.llm import generate as llm_generate


@dataclass
class ReportArtifacts:
    report_md: str
    summary: Dict


def _safe_mkdir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def _basic_profile(df: pd.DataFrame) -> Dict:
    profile = {
        "rows": int(df.shape[0]),
        "cols": int(df.shape[1]),
        "nulls": {c: int(df[c].isna().sum()) for c in df.columns},
        "dtypes": {c: str(df[c].dtype) for c in df.columns},
    }
    return profile


def _coerce_dates(df: pd.DataFrame, date_col: str = "data") -> pd.DataFrame:
    if date_col in df.columns:
        df = df.copy()
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
        df["mes"] = df[date_col].dt.to_period("M").astype(str)
    return df


def _kpis(df: pd.DataFrame) -> Dict:
    kpi = {}

    if "valor" in df.columns:
        kpi["valor_total"] = float(df["valor"].fillna(0).sum())
        kpi["valor_medio"] = float(df["valor"].dropna().mean()) if df["valor"].notna().any() else 0.0

    if {"mes", "valor"}.issubset(df.columns):
        by_month = df.groupby("mes", as_index=False)["valor"].sum().sort_values("mes")
        kpi["valor_por_mes"] = [{"mes": str(r["mes"]), "valor": float(r["valor"])} for _, r in by_month.iterrows()]

    if {"categoria", "valor"}.issubset(df.columns):
        by_cat = df.groupby("categoria", as_index=False)["valor"].sum().sort_values("valor", ascending=False)
        kpi["top_categorias"] = [
            {"categoria": str(r["categoria"]), "valor": float(r["valor"])} for _, r in by_cat.head(5).iterrows()
        ]

    return kpi


def _plot_monthly(df: pd.DataFrame, out_dir: Path) -> Tuple[str, str] | Tuple[None, None]:
    if not {"mes", "valor"}.issubset(df.columns):
        return None, None

    by_month = df.groupby("mes", as_index=False)["valor"].sum().sort_values("mes")
    fig_path = out_dir / "figures" / "valor_por_mes.png"
    plt.figure()
    plt.plot(by_month["mes"], by_month["valor"])
    plt.xticks(rotation=45, ha="right")
    plt.title("Valor por mês")
    plt.tight_layout()
    plt.savefig(fig_path, dpi=160)
    plt.close()
    return "Valor por mês", str(fig_path)


def _plot_top_categories(df: pd.DataFrame, out_dir: Path) -> Tuple[str, str] | Tuple[None, None]:
    if not {"categoria", "valor"}.issubset(df.columns):
        return None, None

    by_cat = df.groupby("categoria", as_index=False)["valor"].sum().sort_values("valor", ascending=False).head(8)
    fig_path = out_dir / "figures" / "top_categorias.png"
    plt.figure()
    plt.bar(by_cat["categoria"].astype(str), by_cat["valor"])
    plt.xticks(rotation=45, ha="right")
    plt.title("Top categorias (valor)")
    plt.tight_layout()
    plt.savefig(fig_path, dpi=160)
    plt.close()
    return "Top categorias", str(fig_path)


def _offline_narrative(summary: Dict) -> str:
    rows = summary["profile"]["rows"]
    cols = summary["profile"]["cols"]
    nulls = summary["profile"]["nulls"]

    top_nulls = sorted(nulls.items(), key=lambda x: x[1], reverse=True)[:3]
    null_lines = "\n".join([f"- `{c}`: {n} nulos" for c, n in top_nulls if n > 0]) or "- Sem nulos relevantes."

    k = summary["kpis"]
    valor_total = k.get("valor_total")
    valor_medio = k.get("valor_medio")

    insights = []
    if valor_total is not None:
        insights.append(f"- Valor total (coluna `valor`): **{valor_total:,.2f}**")
    if valor_medio is not None:
        insights.append(f"- Valor médio (coluna `valor`): **{valor_medio:,.2f}**")
    if k.get("top_categorias"):
        insights.append(f"- Top categoria: **{k['top_categorias'][0]['categoria']}**")

    insights_md = "\n".join(insights) or "- KPIs não disponíveis (faltam colunas esperadas)."

    return f"""## Resumo executivo

Base analisada: **{rows} linhas** e **{cols} colunas**.

### Qualidade do dado (sinais rápidos)
{null_lines}

### KPIs e sinais de negócio
{insights_md}

### Limitações
- Este demo usa regras simples (offline-first). Para narrativa mais rica, habilite `LLM_PROVIDER`.
- Recomenda-se validar a semântica das colunas e a granularidade antes de decisões.
"""


def _llm_enrich(report_md: str, summary: Dict) -> str:
    # Se LLM_PROVIDER=none, src.llm.generate retorna texto vazio.
    prompt = f"""Você é um analista sênior. Reescreva o relatório abaixo para ficar mais executivo,
com 5 bullets de insights acionáveis e 3 riscos (qualidade/custo/viés). Não invente fatos.

RELATORIO_ATUAL:
{report_md}

DADOS_RESUMIDOS(JSON):
{json.dumps(summary, ensure_ascii=False)}
"""
    resp = llm_generate(prompt).text.strip()
    return resp if resp else report_md


def build_report(df: pd.DataFrame, out_dir: Path) -> ReportArtifacts:
    df = _coerce_dates(df, "data")

    profile = _basic_profile(df)
    kpis = _kpis(df)

    _safe_mkdir(out_dir / "figures")
    plots = []
    for fn in (_plot_monthly, _plot_top_categories):
        title, path = fn(df, out_dir)
        if title and path:
            plots.append({"title": title, "path": path})

    summary = {"profile": profile, "kpis": kpis, "plots": plots}

    report_md = _offline_narrative(summary)
    report_md = _llm_enrich(report_md, summary)

    if plots:
        report_md += "\n\n## Gráficos\n"
        for p in plots:
            # Caminho relativo para funcionar no GitHub
            rel = os.path.relpath(p["path"], out_dir)
            report_md += f"\n### {p['title']}\n\n![]({rel})\n"

    return ReportArtifacts(report_md=report_md, summary=summary)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="CSV de entrada")
    ap.add_argument("--output", required=True, help="Pasta de saída (ex.: out)")
    args = ap.parse_args()

    out_dir = Path(args.output)
    _safe_mkdir(out_dir)

    df = pd.read_csv(args.input)
    artifacts = build_report(df, out_dir)

    (out_dir / "report.md").write_text(artifacts.report_md, encoding="utf-8")
    (out_dir / "summary.json").write_text(json.dumps(artifacts.summary, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"OK: relatório gerado em {out_dir/'report.md'}")


if __name__ == "__main__":
    main()
