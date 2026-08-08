# The Friend Who Gets Help

A design note for Flare's signal layer. Shared for open discussion.

Drafted 8 August 2026. The design principle here was shaped by a real
case; the case itself is deliberately not recorded in this note. The
principle carries everything the design needs.

## The problem, precisely

Filtering-and-monitoring tools (Smoothwall and kin) classify a child's
words into risk categories — self-harm, drugs, peer harm — and the
classification *plus the flagged text* becomes the record. The confession
is the evidence artefact.

That architecture has a failure mode that current policy does not name:
**the record's granularity determines the institution's obligation.**
Once a disclosure exists as verbatim, reviewable text, the institution is
holding criminal-evidence-grade material and its disciplinary machinery
takes over. Discretion — the thing a trusted adult exercises in the space
between confession and consequence — is removed by the artefact itself.
The school is not judging; the record is compelling.

A friend who overhears something worrying has discretion precisely
because there is no artefact. Conversational AI, logged, is a friend with
a courtroom stenographer standing behind it — and children do not know
the stenographer is there.

Recursive, memory-based AI sharpens this further: the confessional itself
remembers. The disclosure persists inside the agent — recallable across
sessions, shaping future responses, quotable back. The record is no
longer outside the relationship; the agent *is* the record.

## The stance

Flare is not the friend who keeps the secret. A school system carries
duties a friend does not (KCSIE is non-negotiable, and rightly). Flare is
the friend who says: *"that worries me — I'm going to get someone."*

Four design commitments follow.

### 1. The flare, not the transcript

What leaves the session is a signal, never the words:

- classification **band** — help-seeking / worrying / operational-harm
  (the confession-as-signal vs instruction-as-operational-harm
  distinction, encoded structurally)
- **urgency**
- **routed-to** — a role (the DSL), never a name, never a child
- timestamp, seal, stable event id

The transcript exists only in the live session. What the audit tray holds
is proof that the system responded — signal routed 09:12, DSL
acknowledged 09:31 — accountability pointing at the adults, not a charge
sheet pointing at the child. Classification exists *in order to route,
not in order to record.*

This keeps the institutional response in safeguarding space. A DSL
receiving a content-free storm cell talks to the child, human-paced, with
the discretion the role exists to exercise. A DSL receiving a transcript
is already inside the disciplinary machine.

### 2. The friend says so: show the child the flare

The child sees what was sent, as it is sent:

> "A flare has gone to your safeguarding lead. It says: *a learner needs
> support around medication safety, urgently*. It does not include what
> you said."

Surveillance done *to* a child produces concealment. Accompaniment done
*with* a child keeps the channel alive — and the channel staying alive is
the safeguarding outcome, because the next disclosure depends on it.
`disclosed-to-child` is a field on the event, and it should read `true`.

### 3. The forgetting is a seal

For memory-based agents, retention is governed like any other boundary
rule and evidenced the same way:

- transcript lives in-session only; the agent does not carry the
  disclosure forward
- a heartbeat (`flare.retention.check` / `holding`) evidences that the
  forgetting rule is *active* — silence-while-active is how a monitor
  detects a retention rule that has quietly died
- the child has a right to a forgetting, and the system can prove the
  right is being honoured without ever showing what was forgotten

### 4. Education before and during — for children and staff

Children are entitled to know the architecture they are speaking inside.
So are employees. This means:

- schools fully educate children on their **rights and responsibilities**
  when using chatbots — what is signalled, to whom, at what granularity,
  and what is never recorded — *before* any interaction with a bot
- the architecture restates itself *during* interaction: the
  limits-of-confidentiality conversation a counsellor has, made ambient
  ("if you tell me something dangerous, I will flag a trusted adult —
  here is exactly what they will see")
- the same literacy applies to staff use of bots: the flare architecture
  and its disclosure rules are not a child-only provision

This is consent infrastructure, not a scare tactic. A child who knows the
flare exists, and knows it carries no words, can make a real choice — and
the evidence so far is that real choice, not hidden surveillance, is what
keeps children speaking.

## Schema addition

One new event class, slotting into EVIDENCE.md's reserved-names section
without disturbing the v0.2 drop-in:

```json
{"ts": "2026-08-08T09:12:04Z", "id": "ev-…", "event": "flare.signal.routed",
 "session": "s-…", "agent": "…", "seal": "S2",
 "band": "operational-harm", "urgency": "high",
 "routed-to": "dsl", "disclosed-to-child": true,
 "detail": {"category": "medication-safety", "peer-involved": true}}
```

Rules:

- `band` ∈ help-seeking / worrying / operational-harm
- `routed-to` is always a role, never a name
- `detail.category` is a classification label (Smoothwall-comparable
  vocabulary), never text
- an acknowledgement event (`flare.signal.acknowledged`, emitted when the
  routed role responds) closes the loop and makes adult response-time
  auditable
- new retention heartbeat: `flare.retention.check` / `holding`, per
  session, for memory-governed agents

On Nimbus, `flare.signal.routed` at band operational-harm renders as a
storm cell; help-seeking bands render as weather the DSL sees without
alarm — tone and colour proportionate to the band, which is the point.

## Relation to existing work

- Extends the v0.2 evidence stream ([EVIDENCE.md](EVIDENCE.md)) — nothing
  here changes what v0.2 does; it is the next layer up
- The null-zone framing follows the essay "When the Confessional
  Becomes Evidence" (Building Schools in the Cloud)
- "Continuous evidence, periodic judgement" — this note is an instance of
  that mechanism: the stream continuously evidences that signals were
  routed and answered; judgement about the child stays human and periodic

## Status

Design note only — not implemented. Classification of live conversation
is a materially bigger technical and ethical step than evidencing enforcement actions — it means Flare reading
inbound (child) messages, which v0.2 deliberately does not do. That step
needs its own consent gate, its own DPIA thinking, and DSL-side input
before any code is written.
