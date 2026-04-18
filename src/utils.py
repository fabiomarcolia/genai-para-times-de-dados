from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


def load_env(path: str = ".env") -> None:
    if Path(path).exists():
        load_dotenv(path)


def env(name: str, default: Optional[str] = None) -> str:
    v = os.environ.get(name, default)
    if v is None:
        raise KeyError(f"Missing env var: {name}")
    return v


def estimate_tokens(text: str) -> int:
    # Heurística simples (aprox): 1 token ~ 4 chars em PT/EN
    return max(1, len(text) // 4)
