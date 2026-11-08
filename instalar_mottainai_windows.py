
    
  
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Baixa o instalador ativador.cmd e o salva na pasta Downloads do Windows.

IMPORTANTE:
- O arquivo esperado é um script Windows Batch (.cmd), não um script Bash (.sh).
- Este programa apenas baixa, valida e move o arquivo.
- O arquivo .cmd NÃO é executado automaticamente.
- Baixar o arquivo não significa que o programa foi instalado.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Optional

URL = (
    "https://raw.githubusercontent.com/"
    "josuejuca/ativador-windows/main/ativador.cmd"
)
FILENAME = "ativador.cmd"
CURL_TIMEOUT_SECONDS = 300


def log(message: str = "") -> None:
    print(message, flush=True)


def section(title: str) -> None:
    log()
    log("=" * 72)
    log(title)
    log("=" * 72)


def format_bytes(size: int) -> str:
    if size < 1024:
        return f"{size} bytes"
    if size < 1024 * 1024:
        return f"{size} bytes ({size / 1024:.2f} KiB)"
    return f"{size} bytes ({size / (1024 * 1024):.2f} MiB)"


def get_downloads_dir(override: Optional[str]) -> Path:
    if override:
        return Path(override).expanduser()

    # USERPROFILE/Downloads é o caminho padrão do Windows.
    profile = os.environ.get("USERPROFILE")
    if profile:
        return Path(profile) / "Downloads"

    return Path.home() / "Downloads"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def inspect_cmd_file(path: Path) -> tuple[bool, str, str]:
    """
    Verifica se o download parece ser um arquivo Batch válido.

    Não existe uma assinatura obrigatória para arquivos .cmd. Por isso,
    a validação verifica se o conteúdo é texto, rejeita HTML e procura
    comandos/sintaxe comuns do Windows Batch.
    """
    data = path.read_bytes()

    if not data:
        return False, "arquivo vazio", ""

    if b"\x00" in data:
        return False, "conteúdo binário ou incompatível com um script .cmd", ""

    text = data.decode("utf-8-sig", errors="replace")
    stripped = text.lstrip()
    first_line = next(
        (line.strip() for line in text.splitlines() if line.strip()),
        "",
    )

    lowered = stripped.lower()

    if (
        lowered.startswith("<!doctype html")
        or lowered.startswith("<html")
        or "<html" in lowered[:4096]
    ):
        return False, "página HTML recebida no lugar do arquivo .cmd", first_line

    # Comandos e construções comuns de arquivos Batch.
    batch_patterns = (
        r"(?im)^\s*@?echo\b",
        r"(?im)^\s*@?set(?:local)?\b",
        r"(?im)^\s*@?if\b",
        r"(?im)^\s*@?for\b",
        r"(?im)^\s*@?call\b",
        r"(?im)^\s*@?goto\b",
        r"(?im)^\s*@?exit(?:\s+/b)?\b",
        r"(?im)^\s*@?start\b",
        r"(?im)^\s*@?rem\b",
        r"(?im)^\s*::",
        r"(?im)^\s*@?title\b",
        r"(?im)^\s*@?chcp\b",
    )

    if not any(re.search(pattern, text) for pattern in batch_patterns):
        return (
            False,
            "o conteúdo é texto, mas não foi possível reconhecer comandos Batch",
            first_line,
        )