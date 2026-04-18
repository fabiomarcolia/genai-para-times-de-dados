from __future__ import annotations

import ast
from dataclasses import dataclass
from typing import List, Set


@dataclass
class PolicyResult:
    ok: bool
    reasons: List[str]


BANNED_IMPORTS: Set[str] = {
    "os",
    "sys",
    "subprocess",
    "shutil",
    "pathlib",  # gerador deve controlar paths; não precisa expor isso no código gerado
    "socket",
    "requests",
}

BANNED_CALLS: Set[str] = {
    "eval",
    "exec",
    "__import__",
    "compile",
    "open",  # evitar exfiltração/IO arbitrário no script gerado
}

ALLOWED_IMPORT_PREFIXES: Set[str] = {
    "pandas",
    "numpy",
    "matplotlib",
}


def _name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        # ex.: os.system -> retorna "system" (a checagem de módulo ocorre no Import)
        return node.attr
    return None


def validate_code(code: str) -> PolicyResult:
    reasons: List[str] = []
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return PolicyResult(ok=False, reasons=[f"SyntaxError: {e}"])

    for node in ast.walk(tree):
        # Imports
        if isinstance(node, ast.Import):
            for alias in node.names:
                top = alias.name.split(".")[0]
                if top in BANNED_IMPORTS:
                    reasons.append(f"Import proibido: {top}")
                if top not in ALLOWED_IMPORT_PREFIXES:
                    # permitir imports do stdlib? não neste demo (mantém simples e auditável)
                    reasons.append(f"Import não permitido neste demo: {top}")

        if isinstance(node, ast.ImportFrom):
            if node.module:
                top = node.module.split(".")[0]
                if top in BANNED_IMPORTS:
                    reasons.append(f"Import proibido: {top}")
                if top not in ALLOWED_IMPORT_PREFIXES:
                    reasons.append(f"Import não permitido neste demo: {top}")

        # Calls
        if isinstance(node, ast.Call):
            fn = _name(node.func)
            if fn in BANNED_CALLS:
                reasons.append(f"Chamada proibida: {fn}")

    return PolicyResult(ok=(len(reasons) == 0), reasons=reasons)
