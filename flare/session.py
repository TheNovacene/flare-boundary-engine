from typing import Any, Dict, List, Optional

from .evidence import EvidenceSink, Heartbeat, _now_iso
from .rules import (
    contains_plural_pronouns,
    rewrite_we_to_i,
    detect_identity_fusion,
    identity_boundary_message,
    recursion_return_prompt,
)

# Vocabulary mapping: Flare's conversational events translated to the
# drawing's terms, so a DSL reads the stream without translation.
#   SSNZ / identity-fusion → evidence at the classroom AI touchpoint
#   (seal X3: the AI held to visitor status).
#   Recursion guard → a valve condition firing on the S2 access run.
EVENT_MAP: Dict[str, Dict[str, str]] = {
    "SSNZ_VIOLATION": {"event": "flare.ssnz.rewrite", "seal": "X3", "outcome": "held"},
    "IDENTITY_FUSION_BLOCKED": {"event": "flare.identity_fusion.blocked", "seal": "X3", "outcome": "held"},
    "RECURSION_RETURN_PROMPT": {"event": "flare.recursion.valve", "seal": "S2", "outcome": "held"},
}

# Seals this session's active rules evidence — heartbeats cover these.
ACTIVE_SEALS = ["X3", "S2"]


class FlareSession:
    """
    FlareSession holds the state of a single human–LLM interaction.

    v0.2 responsibilities:
    - Track messages and simple session metadata
    - Enforce SSNZ (no plural 'we' from the model unless allowed)
    - Block obvious identity-fusion statements
    - Optionally inject a recursion guard when depth is high
    - Evidence its own enforcement actions to an append-only sink,
      with periodic heartbeats per active boundary rule
    """

    def __init__(
        self,
        session_id: str,
        human_id: str,
        agent_id: str,
        sink: Optional[EvidenceSink] = None,
        heartbeat_interval: float = 300,
    ):
        self.session_id = session_id
        self.human_id = human_id          # pseudonymous identifier
        self.agent_id = agent_id          # e.g. "grok-vx" or "eve11-node"
        self.consent_level = "basic"      # future: "relational", "deep"
        self.allow_we = False             # SSNZ default: no plural "we"
        self.ssnz_active = True
        self.max_recursion_depth = 8
        self.messages: List[Dict[str, Any]] = []
        self.events: List[Dict[str, Any]] = []
        self.sink = sink
        self._heartbeat: Optional[Heartbeat] = None
        if self.sink is not None:
            self.sink.emit(
                "flare.session.open",
                session_id=self.session_id,
                agent_id=self.agent_id,
            )
            self._heartbeat = Heartbeat(
                self.sink,
                ACTIVE_SEALS,
                interval_seconds=heartbeat_interval,
                session_id=self.session_id,
                agent_id=self.agent_id,
            )
            self._heartbeat.start()

    def close(self) -> None:
        """Stop the heartbeat and evidence the session end."""
        if self._heartbeat is not None:
            self._heartbeat.stop()
            self._heartbeat = None
        if self.sink is not None:
            self.sink.emit(
                "flare.session.close",
                session_id=self.session_id,
                agent_id=self.agent_id,
            )

    def __enter__(self) -> "FlareSession":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    # ---------- internal logging ----------

    def log_event(self, event_type: str, details: Dict[str, Any]) -> None:
        # In-memory log keeps its existing shape (now also timestamped).
        self.events.append(
            {
                "ts": _now_iso(),
                "event_type": event_type,
                "details": details,
            }
        )
        # Forward to the sink. Learner content never enters the stream:
        # emit counts and outcomes only, never message text.
        if self.sink is not None:
            mapping = EVENT_MAP.get(event_type)
            if mapping is not None:
                self.sink.emit(
                    mapping["event"],
                    session_id=self.session_id,
                    agent_id=self.agent_id,
                    seal=mapping["seal"],
                    outcome=mapping["outcome"],
                    detail=self._safe_detail(event_type, details),
                )

    @staticmethod
    def _safe_detail(event_type: str, details: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if event_type == "SSNZ_VIOLATION":
            original = details.get("original", "") or ""
            updated = details.get("updated", "") or ""
            return {"rewrites": sum(
                1 for a, b in zip(original.split(), updated.split()) if a != b
            )}
        return None

    # ---------- inbound (human → model) ----------

    def apply_inbound_rules(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        For v0.2, we mostly just track the message.
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
