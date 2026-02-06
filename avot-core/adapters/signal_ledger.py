from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime
import yaml
import uuid


class SignalLedgerError(Exception):
    """Raised when the signal ledger cannot be read or written safely."""
    pass


class SignalLedger:
    """
    Read / append-only adapter for the Signal Ledger.

    This adapter:
    - reads the ledger as truth
    - appends new signals
    - never mutates or deletes existing signals
    - performs no interpretation
    """

    def __init__(self, ledger_path: str):
        self.ledger_path = Path(ledger_path)

        if not self.ledger_path.exists():
            raise SignalLedgerError(
                f"Signal ledger not found at {self.ledger_path}"
            )

    # --- Internal helpers ---

    def _load(self) -> Dict[str, Any]:
        try:
            with self.ledger_path.open("r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            raise SignalLedgerError(f"Failed to read signal ledger: {e}")

    def _write(self, data: Dict[str, Any]) -> None:
        try:
            with self.ledger_path.open("w", encoding="utf-8") as f:
                yaml.safe_dump(data, f, sort_keys=False)
        except Exception as e:
            raise SignalLedgerError(f"Failed to write signal ledger: {e}")

    # --- Public API ---

    def read_signals(self) -> List[Dict[str, Any]]:
        ledger = self._load()
        return ledger.get("signal_ledger", {}).get("signals", [])

    def append_signal(
        self,
        avot_id: str,
        signal_type: str,
        description: str,
        severity: str = "low",
        context: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Append a new signal emitted by an AVOT.

        This method:
        - generates a unique signal_id
        - timestamps the observation
        - appends without altering existing entries
        """

        ledger = self._load()

        if "signal_ledger" not in ledger:
            raise SignalLedgerError("Invalid signal ledger structure")

        signal = {
            "signal_id": f"SIG-{uuid.uuid4()}",
            "avot_id": avot_id,
            "signal_type": signal_type,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "severity": severity,
            "description": description,
            "context": context or {},
            "metadata": metadata or {},
        }

        ledger["signal_ledger"].setdefault("signals", []).append(signal)
        self._write(ledger)

        return signal
