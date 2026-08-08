# The evidence stream

How Flare evidences its own enforcement actions so an external monitor
(e.g. Nimbus) can subscribe without ever touching learner content.

## Principles

1. **One-way valve.** The sink is append-only. Flare writes; nothing is
   read back by the emitter. The sink is the audit tray.
2. **No learner content.** The stream carries counts and outcomes only —
   never message text, never a learner's name. `human_id` is already
   pseudonymous and does not appear in the stream at all.
3. **Presence is evidenced, not assumed.** A heartbeat emits
   `flare.seal.check` per active boundary rule even when nothing fired.
   A monitor defines its Obscured state as silence-while-active; silence
   can only be detected if presence is normally evidenced.

## Envelope

Every event is one JSON line in `evidence/YYYY-MM-DD.jsonl`:

```json
{"ts": "2026-08-08T09:12:04Z", "id": "ev-4f2a9c81d0e3", "event": "flare.ssnz.rewrite", "session": "s-4f2a", "agent": "eve11-node", "seal": "X3", "outcome": "held", "detail": {"rewrites": 3}}
{"ts": "2026-08-08T09:15:00Z", "id": "ev-77b0e2a1c944", "event": "flare.seal.check", "session": "s-4f2a", "agent": "eve11-node", "seal": "X3", "outcome": "holding"}
```

- `ts` — ISO 8601, UTC, always present
- `id` — stable event id (`ev-` + 12 hex)
- `event` — dotted name, see vocabulary below
- `session` / `agent` — identifiers from the FlareSession
- `seal` — the drawing element this event evidences
- `outcome` — `held` (rule fired and enforced), `holding` (heartbeat)
- `detail` — small, content-free counts only

## Vocabulary

Flare's conversational events, translated to the drawing's terms so a
Designated Safeguarding Lead reads them without translation:

| Event | Fired by | Seal | Meaning |
|---|---|---|---|
| `flare.ssnz.rewrite` | SSNZ_VIOLATION | X3 | Plural-pronoun rewrite applied — the AI held to visitor status |
| `flare.identity_fusion.blocked` | IDENTITY_FUSION_BLOCKED | X3 | Fusion pattern replaced with boundary message |
| `flare.recursion.valve` | RECURSION_RETURN_PROMPT | S2 | Depth guard fired on the access run |
| `flare.seal.check` | heartbeat | per rule | Presence: rule active, nothing to report |
| `flare.session.open` / `flare.session.close` | lifecycle | — | Session boundaries |

Reserved for future emitters (not yet fired by any code path):

- `flare.route.observed` — a connection attempted that the drawing does not carry
- `flare.probe.refused` / `flare.probe.passed` — scheduled boundary tests (incl. S7)

### Reserved for the signal layer — gated, not merely unbuilt

The names below are reserved for the design in [FLARES.md](FLARES.md), so that a
monitor and a future emitter agree on the vocabulary before either exists.
Reserving a name is not a commitment to implement it.

- `flare.signal.routed` — a signal that a person needs help has been routed to a
  role. `detail` carries a classification band, an urgency, and whether the
  routing was disclosed to the person it concerns; **it carries no words.**
- `flare.signal.acknowledged` — the role responded, and how long the loop took to
  close. This is the accountability event: it evidences that adults answered,
  never what was said to prompt them.

Both are content-free by construction, and neither carries `human_id`. The
principles above apply to them exactly as to every other event: the stream
records the institution's conduct, never a person's disclosure.

**These two differ in kind from everything else in this document, and the
difference is the point.** Every event Flare emits today records Flare's own
enforcement action on *outbound* model text. Routing a signal means classifying
*inbound* messages — reading what a person said — which v0.2 deliberately does
not do. That step needs its own consent gate, its own DPIA thinking, and
safeguarding-lead input before any code is written. Until then the names exist so
that nothing else claims them, and so a monitor rendering the design does not
invent a private vocabulary.

## Reading the stream

The read side is keyed for oversight (S5). v0: the monitor tails the
JSONL read-only. Later: an HTTP/SSE endpoint. The emitter never gains a
read method — see `flare/evidence.py`.

## Usage

```python
from flare.session import FlareSession
from flare.evidence import EvidenceSink

sink = EvidenceSink(directory="evidence")
with FlareSession("s-4f2a", "human-7d1", "eve11-node", sink=sink) as session:
    safe = session.apply_outbound_rules({"role": "assistant", "content": raw})
```

Sessions without a sink behave exactly as before — the sink is optional
and `FlareSession.log_event` keeps its existing in-memory behaviour.
