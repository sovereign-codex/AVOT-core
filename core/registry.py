"""Registry utilities for AVOT-Core."""
import json
from pathlib import Path

# Registry lives at project root alongside ``avot_engine.py``
REGISTRY_PATH = Path(__file__).resolve().parent.parent / "avot_registry.json"


def load_registry():
    """Load and return the AVOT registry JSON as a dictionary."""
    with REGISTRY_PATH.open() as f:
        return json.load(f)


__all__ = ["load_registry", "REGISTRY_PATH"]
