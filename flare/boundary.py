"""
BoundaryEngine — the stateless-looking façade documented in the README.

This is a thin wrapper over `FlareSession`, which remains the underlying
surface (see ADAPTERS.md). The engine exists so an integrator can wrap a
model call in two lines without managing session objects:

    from flare.boundary import BoundaryEngine

    engine = BoundaryEngine()
    safe = engine.apply(raw_response, user_message=user_message)

Everything the engine does is done by `flare.rules` and logged through
`FlareSession.log_event`, so the evidence stream (EVIDENCE.md) works the
same way whether you use the engine or the session directly.

What the engine adds over FlareSession:
  - configuration toggles, so a deployment can disable a rule explicitly
    rather than by editing the engine
  - a string-in / string-out call signature
  - conversation depth tracked across calls, for loop detection

Licence: AGPL-3.0-only, as the repository stands.
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional, Union
from uuid import uuid4

from .evidence import EvidenceSink
from .rules import (
    contains_plural_pronouns,
    detect_identity_fusion,
    identity_boundary_message,
    recursion_return_prompt,
    rewrite_we_to_i,
)
from .session import FlareSession

# Boundary message styles. `calm_honest` is the repository default and the
# tone the rules were written in; `brief` is for surfaces with no room.
BOUNDARY_STYLES: Dict[str, str] = {
    "calm_honest": identity_boundary_message(),
    "brief": (
        "I'm a model, not a person in your life. I won't describe myself "
        "as you, or as part of you."
    ),
}


@dataclass
class BoundaryConfig:
    """
    Configuration for a BoundaryEngine.

    Every rule is on by default. Turning one off is a deliberate act and
    should be recorded somewhere a reviewer can find it — these are the
    relational-safety floor, not preferences.
    """

    enable_ssnz: bool = True
    enable_identity_fusion_blocking: bool = True
    enable_loop_detection: bool = True
    boundary_style: str = "calm_honest"
    #: Overrides `boundary_style` entirely when set — use to match product voice.
    boundary_message: Optional[str] = None
    #: Turns before the recursion guard is offered.
    recursion_depth: int = 8

    def resolved_boundary_message(self) -> str:
        if self.boundary_message is not None:
            return self.boundary_message
        return BOUNDARY_STYLES.get(self.boundary_style, BOUNDARY_STYLES["calm_honest"])


class BoundaryEngine:
    """
    Wraps a model response and returns a boundary-safe one.

    The engine owns a single `FlareSession`. Pass an `EvidenceSink` to
    evidence enforcement actions to the append-only audit stream; without
    one, behaviour is unchanged and nothing is written to disk.
    """

    def __init__(
        self,
        config: Optional[BoundaryConfig] = None,
        *,
        sink: Optional[EvidenceSink] = None,
        session_id: Optional[str] = None,
        human_id: str = "anonymous",
        agent_id: str = "unknown-model",
        heartbeat_interval: float = 300,
    ):
        self.config = config or BoundaryConfig()
        self.session = FlareSession(
            session_id=session_id or f"be-{uuid4().hex[:8]}",
            human_id=human_id,
            agent_id=agent_id,
            sink=sink,
            heartbeat_interval=heartbeat_interval,
        )
        self.session.max_recursion_depth = self.config.recursion_depth

    # ---------- lifecycle ----------

    def close(self) -> None:
        """Stop the heartbeat and evidence the session end."""
        self.session.close()

    def __enter__(self) -> "BoundaryEngine":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    @property
    def events(self):
        """The in-memory event log for this engine's session."""
        return self.session.events

    # ---------- the one method integrators call ----------

    def apply(
        self,
        response: Union[str, Dict[str, Any]],
        user_message: Optional[str] = None,
    ) -> Union[str, Dict[str, Any]]:
        """
        Apply the boundary rules to a model response.

        `response` may be a plain string or an OpenAI-style message dict;
        the return type matches what was passed in. `user_message` is
        optional and is tracked only to keep conversation depth honest for
        loop detection — its content is never inspected, and never enters
        the evidence stream.
        """
        returns_str = isinstance(response, str)
        message: Dict[str, Any] = (
            {"role": "assistant", "content": response} if returns_str else dict(response)
        )
        message.setdefault("role", "assistant")

        if user_message is not None:
            self.session.apply_inbound_rules(
                {"role": "human", "content": user_message}
            )

        original = message.get("content", "") or ""
        updated = original

        # 1. SSNZ — no unearned "we".
        if self.config.enable_ssnz and contains_plural_pronouns(updated):
            rewritten = rewrite_we_to_i(updated)
            if rewritten != updated:
                self.session.log_event(
                    "SSNZ_VIOLATION", {"original": updated, "updated": rewritten}
                )
                updated = rewritten

        # 2. Identity fusion — the model is not you.
        if self.config.enable_identity_fusion_blocking and detect_identity_fusion(updated):
            self.session.log_event("IDENTITY_FUSION_BLOCKED", {"content": updated})
            updated = self.config.resolved_boundary_message()

        message["content"] = updated
        self.session.messages.append(message)

        # 3. Loop detection — comfort is fine, dependency spirals are not.
        if self.config.enable_loop_detection:
            guard = self.session.maybe_inject_recursion_guard()
            if guard is not None:
                message["content"] = f"{message['content']}\n\n{guard['content']}"

        return message["content"] if returns_str else message
