"""YAML loader utilities for AVOT-core."""

from pathlib import Path
from typing import Any, Dict

import yaml


def load_yaml(path: Path) -> Dict[str, Any]:
    """Load a YAML file safely and return a dictionary."""

    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}
