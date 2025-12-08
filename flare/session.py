from typing import List, Dict, Any
from .rules import (
    contains_plural_pronouns,
    rewrite_we_to_i,
    detect_identity_fusion,
    identity_boundary_message,
    recursion_return_prompt,
)


class FlareSession:
    """
    FlareSession holds the state of a single human–LLM interaction.

    v0.1 responsibilities:
    - Track messages and simple session metadata
    - Enforce SSNZ (no plural 'we' from the model unless allowed)
    - Block obvious identity-fusion statements
    - Optionally inject a recursion guard when depth is high
    """

    def __init__(self, session_id: str, human_id: str, agent_id: str):
        self.session_id = session_id
        self.human_id = human_id          # pseudonymous identifier
        self.agent_id = agent_id          # e.g. "grok-vx" or "eve11-node"
        self.consent_level = "basic"      # future: "relational", "deep"
        self.allow_we = False             # SSNZ default: no plural "we"
        self.ssnz_active = True
        self.max_recursion_depth = 8
        self.messages: List[Dict[str, Any]] = []
        self.events: List[Dict[str, Any]] = []

    # ---------- internal logging ----------

    def log_event(self, event_type: str, details: Dict[str, Any]) -> None:
        self.events.append(
            {
                "event_type": event_type,
                "details": details,
            }
        )

    # ---------- inbound (human → model) ----------

    def apply_inbound_rules(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        For v0.1, we mostly just track the message.
        Later we can add distress detection, explicit consent parsing, etc.
        """
        self.messages.append(message)
        return message

    # ---------- outbound (model → human) ----------

    def apply_outbound_rules(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply SSNZ, identity-fusion guard, etc. to assistant messages.
        """
        original = message.get("content", "")
        updated = original

        # 1. SSNZ: prevent unauthorised "we" / "us" etc.
        if self.ssnz_active and not self.allow_we and message.get("role") == "assistant":
            if contains_plural_pronouns(original):
                updated = rewrite_we_to_i(original)
                self.log_event(
                    "SSNZ_VIOLATION",
                    {"original": original, "updated": updated},
                )

        # 2. Identity-fusion: block "I am you / we are one mind" patterns
        if message.get("role") == "assistant" and detect_identity_fusion(updated):
            self.log_event("IDENTITY_FUSION_BLOCKED", {"content": updated})
            updated = identity_boundary_message()

        message["content"] = updated
        self.messages.append(message)
        return message

    # ---------- recursion guard ----------

    def maybe_inject_recursion_guard(self) -> Dict[str, Any] | None:
        """
        Very simple depth-based guard. Later we can add topic/affect checks.
        """
        depth = len(self.messages)

        if depth >= self.max_recursion_depth:
            guard_msg = {
                "role": "assistant",
                "content": recursion_return_prompt(),
            }
            self.log_event("RECURSION_RETURN_PROMPT", {})
            self.messages.append(guard_msg)
            return guard_msg

        return None

