from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from src.llm import generate as llm_generate


BASE_TEMPLATE = """import pandas as pd
import matplotlib.pyplot as plt

def main():
    df = pd.read_csv(r"{DATA_PATH}")
{STEPS}

if __name__ == "__main__":
    main()
"""


def _indent(code: str, spaces: int = 4) -> str:
    pad = " " * spaces
    return "\n".join(pad + line if line.strip() else line for line in code.splitlines())


def _load_policies():
    # Permite rodar a partir do root: python demos/06-nl-to-python/generate.py ...
    here = Path(__file__).resolve().parent
    sys.path.insert(0, str(here))
    from policies import validate_code  # noqa: WPS433 (import local controlado)

    return validate_code


def _offline_steps(task: str, out_dir: Path) -> str:
    steps: list[str] = []

    if re.search(r"padroniz|normaliz|snake", task, re.I):
        steps.append("df.columns = [c.strip().lower().replace(' ', '_') for c in df.columns]")

    if re.search(r"nul|missing", task, re.I) and re.search(r"valor", task, re.I):
        steps.append("df['valor'] = pd.to_numeric(df['valor'], errors='coerce').fillna(0)")

    if re.search(r"coluna\s+mes|m[eê]s\s+a\s+partir", task, re.I):
        steps.append("df['data'] = pd.to_datetime(df['data'], errors='coerce')")
        steps.append("df['mes'] = df['data'].dt.to_period('M').astype(str)")

    if re.search(r"agreg|group|som|soma", task, re.I) and re.search(r"mes", task, re.I):
        steps.append("resumo = df.groupby('mes', as_index=False)['valor'].sum().sort_values('mes')")

    if re.search(r"salv|export", task, re.I) and re.search(r"resumo", task, re.I):
        steps.append(f"resumo.to_csv(r'{(out_dir / 'resumo.csv')}', index=False)")

    if re.search(r"gr[aá]fico|plot|linha", task, re.I):
        steps.append(
            "plt.figure()\n"
            "plt.plot(resumo['mes'], resumo['valor'])\n"
            "plt.xticks(rotation=45, ha='right')\n"
            "plt.title('Valor por mês')\n"
            "plt.tight_layout()"
        )
        steps.append(f"plt.savefig(r'{(out_dir / 'plot.png')}', dpi=160)")

    if not steps:
        steps = [
            "df.columns = [c.strip().lower().replace(' ', '_') for c in df.columns]",
            "df['valor'] = pd.to_numeric(df['valor'], errors='coerce').fillna(0)",
            "df['data'] = pd.to_datetime(df['data'], errors='coerce')",
            "df['mes'] = df['data'].dt.to_period('M').astype(str)",
            "resumo = df.groupby('mes', as_index=False)['valor'].sum().sort_values('mes')",
            f"resumo.to_csv(r'{(out_dir / 'resumo.csv')}', index=False)",
            "plt.figure()\n"
            "plt.plot(resumo['mes'], resumo['valor'])\n"
            "plt.xticks(rotation=45, ha='right')\n"
            "plt.title('Valor por mês')\n"
            "plt.tight_layout()",
            f"plt.savefig(r'{(out_dir / 'plot.png')}', dpi=160)",
        ]

    return _indent("\n".join(steps), 4)


def _llm_steps(task: str) -> str:
    prompt = f"""Você é um engenheiro de dados. Transforme a tarefa abaixo em passos de código Python (pandas + matplotlib)
em formato de bloco, SEM imports e SEM definições de função. Use df como DataFrame de entrada e crie a variável resumo
quando fizer agregação. Não use open/eval/exec/os/subprocess/requests.

TAREFA:
{task}
"""
    return llm_generate(prompt).text.strip()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True, help="Arquivo .md com a tarefa em linguagem natural")
    ap.add_argument("--data", required=True, help="CSV de entrada")
    ap.add_argument("--out", required=True, help="Diretório de saída")
    args = ap.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    task = Path(args.task).read_text(encoding="utf-8")

    validate_code = _load_policies()

    steps = _offline_steps(task, out_dir)
    llm_steps = _llm_steps(task)
    if llm_steps:
        llm_steps = llm_steps.strip().strip("`")
        steps = _indent(llm_steps, 4)

    code = BASE_TEMPLATE.format(DATA_PATH=args.data, STEPS=steps)

    result = validate_code(code)
    if not result.ok:
        reasons = "\n- ".join(result.reasons)
        raise SystemExit(f"Código gerado violou policies:\n- {reasons}")

    out_file = out_dir / "generated_task.py"
    out_file.write_text(code, encoding="utf-8")

    import runpy  # stdlib

    runpy.run_path(str(out_file), run_name="__main__")
    print(f"OK: gerado e executado: {out_file}")


if __name__ == "__main__":
    main()
