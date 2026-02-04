from typing import Any, Dict, Optional
from datetime import datetime


class AvotRefusal(Exception):
    """
    Raised when an AVOT refuses an action.
    Refusal is a valid outcome, not an error state.
    """

    def __init__(self, reason: str, reference: str, next_step: str):
        self.reason = reason
        self.reference = reference
        self.next_step = next_step
        super().__init__(reason)


class AvotBase:
    """
    Canonical AVOT base class.

    This class provides:
    - identity awareness
    - lifecycle awareness
    - action classification
    - permission checking
    - dignified refusal
    - signal emission

    It does NOT provide:
    - domain logic
    - enforcement of other AVOTs
    - automation
    """

    # --- Construction ---

    def __init__(
        self,
        avot_id: str,
        header: Dict[str, Any],
        registry_entry: Dict[str, Any],
    ):
        self.avot_id = avot_id
        self.header = header
        self.registry_entry = registry_entry

    # --- Identity & State ---

    def identify(self) -> Dict[str, Any]:
        return {
            "avot_id": self.avot_id,
            "purpose": self.header.get("purpose"),
            "steward": self.header.get("steward"),
            "header_ref": self.header.get("id"),
        }

    def state(self) -> Dict[str, Any]:
        return {
            "lifecycle_state": self.registry_entry.get("lifecycle_state"),
            "maturity": self.registry_entry.get("maturity"),
            "binding": self.registry_entry.get("binding", False),
        }

    # --- Action Classification ---

    def classify_action(self, intent: str) -> str:
        """
        Map an intent string to a canonical action type.
        Override if needed, but do not collapse categories.
        """
        intent = intent.lower()

        if intent in {"think", "analyze", "reason"}:
            return "think"
        if intent in {"say", "respond", "communicate"}:
            return "communicate"
        if intent in {"run", "execute", "perform"}:
            return "execute"
        if intent in {"bind", "write", "commit"}:
            return "bind"
        if intent in {"propose", "suggest", "request"}:
            return "propose"

        return "communicate"

    # --- Permission Evaluation ---

    def can_attempt(self, action_type: str) -> bool:
        lifecycle = self.registry_entry.get("lifecycle_state")
        binding_allowed = self.registry_entry.get("binding", False)

        if lifecycle in {"S6", "S7", "S8", "S9"}:
            return False

        if action_type == "bind" and not binding_allowed:
            return False

        return True

    # --- Refusal ---

    def refuse(
        self,
        reason: str,
        reference: str,
        next_step: str = "wait",
    ) -> None:
        raise AvotRefusal(
            reason=reason,
            reference=reference,
            next_step=next_step,
        )

    # --- Signals ---

    def emit_signal(
        self,
        signal_type: str,
        payload: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Emit a non-binding signal.
        This implementation simply returns the signal object.
        Adapters may persist or forward it.
        """
        return {
            "avot_id": self.avot_id,
            "signal_type": signal_type,
            "payload": payload or {},
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }

    # --- Guarded Attempt Helper ---

    def attempt(self, intent: str, action_callable):
        """
        Optional helper to wrap action attempts with classification and permission checks.
        """
        action_type = self.classify_action(intent)

        if not self.can_attempt(action_type):
            self.refuse(
                reason=f"Action '{action_type}' not permitted in current state",
                reference=f"lifecycle={self.registry_entry.get('lifecycle_state')}",
                next_step="propose",
            )

        return action_callable()