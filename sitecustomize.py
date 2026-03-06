"""Project-level Python startup hooks.

This module is auto-imported by Python when present on sys.path. It sets
safe environment defaults early to avoid known macOS hangs in heavy ML
dependencies and to silence third-party Pydantic plugin warnings.
"""

import os
import sys

# Avoid third-party Pydantic plugin import warnings (e.g., logfire) unless user opts in
os.environ.setdefault("PYDANTIC_DISABLE_PLUGINS", "1")

_SAFE_ENV_DEFAULTS = {
    "TRANSFORMERS_NO_TF": "1",
    "TOKENIZERS_PARALLELISM": "false",
    "OMP_NUM_THREADS": "1",
    "MKL_NUM_THREADS": "1",
    "OPENBLAS_NUM_THREADS": "1",
    "VECLIB_MAXIMUM_THREADS": "1",
}

if "--no-safe-env" not in sys.argv:
    for key, value in _SAFE_ENV_DEFAULTS.items():
        os.environ.setdefault(key, value)
