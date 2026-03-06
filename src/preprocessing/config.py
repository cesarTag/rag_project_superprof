from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

import yaml


def resolve_config_path(path: str | Path | None) -> Optional[Path]:
    if path:
        return Path(path)
    for candidate in (Path("config.yml"), Path("config.yaml")):
        if candidate.exists():
            return candidate
    return None


def load_config(path: str | Path | None) -> Dict[str, Any]:
    if not path:
        return {}
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict):
        raise ValueError("Config file must contain a YAML mapping at the top level")
    return data


def deep_get(dct: Dict[str, Any], keys: list[str], default: Any = None) -> Any:
    cur: Any = dct
    for key in keys:
        if not isinstance(cur, dict) or key not in cur:
            return default
        cur = cur[key]
    return cur
