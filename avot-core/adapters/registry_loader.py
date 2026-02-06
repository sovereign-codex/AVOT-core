from typing import Dict, Any
import yaml
from pathlib import Path


class RegistryReadError(Exception):
    """Raised when the registry cannot be read safely."""
    pass


class RegistryLoader:
    """
    Read-only adapter for the AVOT registry.

    This loader:
    - reads the registry from disk
    - returns immutable snapshots
    - performs no mutation
    - performs no interpretation

    It is intentionally simple.
    """

    def __init__(self, registry_path: str):
        self.registry_path = Path(registry_path)

        if not self.registry_path.exists():
            raise RegistryReadError(
                f"Registry file not found at {self.registry_path}"
            )

    def load_registry(self) -> Dict[str, Any]:
        """
        Load the full registry as a snapshot.
        """
        try:
            with self.registry_path.open("r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            raise RegistryReadError(f"Failed to read registry: {e}")

    def get_avot_entry(self, avot_id: str) -> Dict[str, Any]:
        """
        Retrieve a single AVOT's registry entry.

        Returns an empty dict if the AVOT is not registered.
        """
        registry = self.load_registry()
        avots = registry.get("avot_registry", {}).get("avots", {})

        return avots.get(avot_id, {}).copy()

    def registry_metadata(self) -> Dict[str, Any]:
        """
        Return top-level registry metadata (non-AVOT).
        """
        registry = self.load_registry()
        meta = registry.get("avot_registry", {}).copy()
        meta.pop("avots", None)
        return meta