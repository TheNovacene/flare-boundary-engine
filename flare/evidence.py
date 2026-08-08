"""
Evidence sink and heartbeat for Flare.

The sink is a one-way valve: Flare appends events, nothing is read back.
Each event is a single JSON line in evidence/YYYY-MM-DD.jsonl — timestamped
(ISO 8601, UTC), carrying a stable event id, session and agent identifiers,
and the seal the event evidences. Learner content never enters the stream:
Flare evidences its own enforcement actions only (counts, outcomes), never
what was said.

A monitor (e.g. Nimbus) subscribes read-only by tailing the JSONL; a later
version may add an HTTP/SSE read side keyed for oversight.

Licence: AGPL-3.0-only, as the repository stands.
"""

import json
import os
import threading
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class EvidenceSink:
    """
    Append-only JSONL sink. Write-only by design: this class exposes no
    read methods, honouring the one-way valve ("data in, nothing back").
    """

    def __init__(self, directory: str = "evidence"):
        self.directory = directory
        self._lock = threading.Lock()

    def emit(
        self,
        event: str,
        *,
        session_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        seal: Optional[str] = None,
        outcome: Optional[str] = None,
        detail: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Append one event line. Returns the envelope that was written."""
        envelope: Dict[str, Any] = {
            "ts": _now_iso(),
            "id": f"ev-{uuid.uuid4().hex[:12]}",
            "event": event,
        }
        if session_id:
            envelope["session"] = session_id
        if agent_id:
            envelope["agent"] = agent_id
        if seal:
            envelope["seal"] = seal
        if outcome:
            envelope["outcome"] = outcome
        if detail:
            envelope["detail"] = detail

        line = json.dumps(envelope, ensure_ascii=False)
        with self._lock:
            os.makedirs(self.directory, exist_ok=True)
            path = os.path.join(
                self.directory,
                datetime.now(timezone.utc).strftime("%Y-%m-%d") + ".jsonl",
            )
            with open(path, "a", encoding="utf-8") as f:
                f.write(line + "\n")
        return envelope


class Heartbeat:
    """
    Periodic presence signal: one `flare.seal.check` per active boundary
    rule, emitted even when nothing fired. Silence-while-active can only
    be detected if presence is normally evidenced.
    """

    def __init__(
        self,
        sink: EvidenceSink,
        seals: List[str],
        *,
        interval_seconds: float = 300,
        session_id: Optional[str] = None,
        agent_id: Optional[str] = None,
    ):
        self.sink = sink
        self.seals = list(seals)
        self.interval_seconds = interval_seconds
        self.session_id = session_id
        self.agent_id = agent_id
        self._stop = threading.Event()
        self._thread: Optional[threading.Thread] = None

    def _beat_once(self) -> None:
        for seal in self.seals:
            self.sink.emit(
                "flare.seal.check",
                session_id=self.session_id,
                agent_id=self.agent_id,
                seal=seal,
                outcome="holding",
            )

    def _run(self) -> None:
        self._beat_once()  # evidence presence immediately on start
        while not self._stop.wait(self.interval_seconds):
            self._beat_once()

    def start(self) -> None:
        if self._thread is not None:
            return
        self._thread = threading.Thread(target=self._run, daemon=True, name="flare-heartbeat")
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        if self._thread is not None:
            self._thread.join(timeout=self.interval_seconds + 1)
            self._thread = None
