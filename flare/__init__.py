"""
FLARE — a relational boundary engine for LLMs.

Two entry points, the same rules underneath:

    from flare.boundary import BoundaryEngine     # wrap a response, string in / string out
    from flare.session import FlareSession        # hold a conversation's state

Add an EvidenceSink to either and enforcement actions are evidenced to an
append-only audit stream — see EVIDENCE.md.

Licence: code AGPL-3.0-only; content CC BY-NC-SA 4.0.
"""

from .boundary import BOUNDARY_STYLES, BoundaryConfig, BoundaryEngine
from .evidence import EvidenceSink, Heartbeat
from .session import FlareSession

__all__ = [
    "BoundaryEngine",
    "BoundaryConfig",
    "BOUNDARY_STYLES",
    "FlareSession",
    "EvidenceSink",
    "Heartbeat",
]

__version__ = "0.2.0"
