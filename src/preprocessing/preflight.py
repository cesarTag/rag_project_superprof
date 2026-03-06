from __future__ import annotations

import os
import subprocess
import sys
from typing import Dict


SAFE_ENV_DEFAULTS: Dict[str, str] = {
    "TRANSFORMERS_NO_TF": "1",
    "TOKENIZERS_PARALLELISM": "false",
    "OMP_NUM_THREADS": "1",
    "MKL_NUM_THREADS": "1",
    "OPENBLAS_NUM_THREADS": "1",
    "VECLIB_MAXIMUM_THREADS": "1",
}


def check_torch_health(timeout_seconds: int = 5) -> None:
    env = os.environ.copy()
    for key, value in SAFE_ENV_DEFAULTS.items():
        env.setdefault(key, value)
    env.setdefault("PYDANTIC_DISABLE_PLUGINS", "1")

    cmd = [
        sys.executable,
        "-c",
        "import torch; print(torch.__version__)",
    ]
    try:
        subprocess.run(cmd, check=True, env=env, timeout=timeout_seconds)
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(
            "Torch import timed out. This can indicate a broken or incompatible torch install. "
            "Try using a fresh virtualenv and reinstall pinned requirements, or downgrade torch."
        ) from exc
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(
            "Torch failed to import in a subprocess. This can indicate a broken or incompatible torch install. "
            "Try using a fresh virtualenv and reinstall pinned requirements, or downgrade torch."
        ) from exc

