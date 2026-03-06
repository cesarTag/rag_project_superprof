from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator


def safe_import(module_name: str, install_hint: str):
    try:
        return __import__(module_name, fromlist=["*"])
    except Exception as exc:  # pragma: no cover - intentionally broad for optional deps
        raise ImportError(
            f"Missing dependency for '{module_name}'. Install {install_hint} to enable this option."
        ) from exc


def find_pdfs(input_dir: str | Path, recursive: bool) -> list[Path]:
    base = Path(input_dir)
    if not base.exists():
        raise FileNotFoundError(f"Input directory not found: {base}")
    patterns = ["*.pdf", "*.PDF"]
    paths: list[Path] = []
    for pattern in patterns:
        if recursive:
            paths.extend(base.rglob(pattern))
        else:
            paths.extend(base.glob(pattern))
    return sorted(set(paths))


def ensure_parent(path: str | Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def write_jsonl(path: str | Path, records: Iterable[Dict[str, Any]]) -> None:
    path = ensure_parent(path)
    with path.open("w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


def read_jsonl(path: str | Path) -> list[Dict[str, Any]]:
    path = Path(path)
    records: list[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            records.append(json.loads(line))
    return records


def iter_jsonl(path: str | Path) -> Iterator[Dict[str, Any]]:
    path = Path(path)
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)

