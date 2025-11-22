"""
System Snapshot Generator
Provides Convergence with a unified picture of current state.
"""
import json
from pathlib import Path


def generate_snapshot():
    base = Path(__file__).resolve().parents[1]

    registry = json.loads((base / "avot_registry.json").read_text())
    tips = [str(p) for p in (base / "TIPs").glob("*.md")]
    docs = [str(p) for p in (base / "docs").glob("*.md")]

    return {
        "registry_avots": [a["name"] for a in registry.get("agents", [])],
        "routing": registry.get("routing", {}),
        "tips": tips,
        "docs": docs,
        "version": "phase-inquiry-1.0"
    }
