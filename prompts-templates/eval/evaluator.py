from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

from src.utils import load_env, estimate_tokens


@dataclass
class EvalResult:
    id: str
    ok: bool
    reason: str
    latency_ms: int
    tokens_est: int


def simple_checks(answer: str, expected_contains: List[str], must_cite: bool) -> Tuple[bool, str]:
    a = answer.lower()
    missing = [t for t in expected_contains if t.lower() not in a]
    if missing:
        return False, f"missing_terms={missing}"
    if must_cite and "[fonte:" not in a:
        return False, "missing_citations"
    return True, "ok"


def run_eval(run_fn, dataset_path: str) -> List[EvalResult]:
    results: List[EvalResult] = []
    with open(dataset_path, "r", encoding="utf-8") as f:
        for line in f:
            item = json.loads(line)
            t0 = time.time()
            answer = run_fn(item["question"])
            latency_ms = int((time.time() - t0) * 1000)
            tokens_est = estimate_tokens(answer)
            ok, reason = simple_checks(
                answer,
                item.get("expected_contains", []),
                bool(item.get("must_cite", False)),
            )
            results.append(EvalResult(item["id"], ok, reason, latency_ms, tokens_est))
    return results


if __name__ == "__main__":
    load_env()
    # Exemplo de uso (substitua run_fn por sua função real)
    def run_fn(q: str) -> str:
        return f"Resposta dummy para: {q} [fonte:1]"

    dataset = os.environ.get("EVAL_DATASET", "templates/eval/eval_dataset_template.jsonl")
    res = run_eval(run_fn, dataset)
    passed = sum(1 for r in res if r.ok)
    print(f"passed={passed}/{len(res)}")
    for r in res:
        print(r)
