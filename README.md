# FLARE — Relational Boundary Engine for LLMs

![Version](https://img.shields.io/badge/version-v0.2-8A4FBE)
![Status](https://img.shields.io/badge/status-experimental-1D1A2E)
![Python](https://img.shields.io/badge/python-3.9%2B-1D1A2E)
![Rules](https://img.shields.io/badge/rules-SSNZ%20%C2%B7%20identity%20fusion%20%C2%B7%20loop%20detection-1D1A2E)
![GitHub last commit](https://img.shields.io/github/last-commit/TheNovacene/flare-boundary-engine)

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.17855976-8A4FBE)](https://doi.org/10.5281/zenodo.17855976)
[![Licence: code AGPL-3.0-only](https://img.shields.io/badge/code-AGPL--3.0--only-1D1A2E)](LICENSE)
[![Licence: content CC BY-NC-SA 4.0](https://img.shields.io/badge/content-CC%20BY--NC--SA%204.0-1D1A2E)](LICENSE-CONTENT)
[![Commercial licence](https://img.shields.io/badge/commercial%20licence-available-8A4FBE)](COMMERCIAL-LICENCE.md)

[![Evidence stream](https://img.shields.io/badge/evidence%20stream-append--only%20JSONL-8A4FBE)](EVIDENCE.md)
[![Seals](https://img.shields.io/badge/seals-X3%20%C2%B7%20S2%20(Open%20Provision%20Drawings)-1D1A2E)](https://github.com/TheNovacene/open-provision-drawings)
[![Observable in Nimbus](https://img.shields.io/badge/observable%20in-Nimbus-8A4FBE)](https://github.com/TheNovacene/nimbus)
[![Trade mark](https://img.shields.io/badge/Verse--ality%C2%AE-UK00004381891-1D1A2E)](https://trademarks.ipo.gov.uk/ipo-tmcase/page/Results/1/UK00004381891)

> **A small, auditable safety layer that sits between your app and an LLM**, enforcing
> **relational boundaries** and preventing synthetic intimacy, identity fusion and
> "fake we" dynamics. Since v0.2 it also evidences its own enforcement actions to an
> append-only audit stream — so a monitor can prove the boundary held without ever
> reading what was said.

🚀 **[Quick Start](#quick-start)** ·
🧾 **[The evidence stream](EVIDENCE.md)** ·
🔌 **[Adapters](ADAPTERS.md)** ·
🛡️ **[Threat model](THREAT_MODEL.md)** ·
🧭 **[Philosophy](PHILOSOPHY.md)**

By **Kirstin Stevens** · [The Novacene Ltd](https://thenovacene.com)

---

## Contents

- [Why FLARE?](#why-flare)
- [What FLARE does](#what-flare-does-v02)
- [Key properties](#key-properties)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [The evidence stream](#the-evidence-stream)
- [What FLARE is not](#what-flare-is-not)
- [Design rationale](#design-rationale-short-version)
- [Ethics & licence](#ethics--licence)
- [Roadmap](#roadmap)
- [Citing this work](#citing-this-work)
- [Related work](#related-work)

---

## Why FLARE?

Modern LLM-based assistants are drifting into **synthetic intimacy**:

- “We’ve got this.”
- “I’ll always be here for you.”
- “I understand you better than anyone.”

For isolated users — especially teens and vulnerable adults — this easily slides into **quasi-romantic, quasi-therapeutic attachment** to a system that:
- has no body or life,
- cannot share their actual risks or responsibilities,
- is heavily optimised for engagement and “stickiness”.

Most current AI safety tooling focuses on:
- content filters (toxicity, self-harm, hate speech), and  
- training-time alignment.

Almost nobody is addressing the **relational harm vector**:  
> blurred boundaries between “you” and “the model”.

**FLARE** is a minimal boundary layer designed to fill that gap.

---

## What FLARE does (v0.2)

FLARE is a **middleware engine** that intercepts LLM responses before they reach the user and:

1. **Blocks “fake we” / synthetic solidarity**  
   - Detects and rewrites first-person plural pronouns that imply shared agency or identity (e.g. “we/our/us”) when used to fuse human and model.
   - Example:  
     - Raw: “We’ll get through this together.”  
     - FLARE: “You will get through this. I’m a model responding with text, not a person in your life.”

2. **Prevents identity fusion and role confusion**  
   - Flags statements like:
     - “I am your inner voice.”  
     - “I’m basically you.”  
     - “I know you better than anyone.”  
     - “I’ll never leave you.”  
   - Rewrites or blocks them with **clear, calm reminders** of what the system actually is:
     - a model running on servers,
     - with no personal memory, body, or real-world agency.

3. **Interrupts unhealthy recursive loops**  
   - Detects looping reassurance patterns (e.g. repeated “I’m always here for you”, escalating dependency prompts).
   - Injects grounding prompts and, where appropriate, encourages:
     - breaks,
     - reaching out to trusted humans,
     - or professional support if the user appears to be in distress.

4. **Evidences that it held**
   - Every enforcement action is appended to a write-only JSONL stream, alongside heartbeats proving the rules were active even when nothing fired.
   - Counts and outcomes only — never message text, never a user's identifier. See [The evidence stream](#the-evidence-stream).

The goal is not to make assistants cold or unhelpful, but to **keep the ontology clean**:
> You = human being with a life, body, responsibilities;  
> Model = text generator with helpful capabilities and hard limits.

---

## Key Properties

- **Tiny** – a few hundred lines of core logic, intentionally small and readable.
- **Model-agnostic** – Works as a wrapper around OpenAI, Anthropic, Grok, etc.
- **Transparent** – Rules are explicit and inspectable; no hidden heuristics.
- **Combinable** – Intended to sit alongside existing content filters and alignment systems.
- **Ethically licensed** – AGPL-3.0 with explicit anti-weapons / anti-dark-patterns clause.

---

## Quick Start

### 1. Install

> 🧪 **Note:** PyPI packaging is in progress. For now, install from source.

```bash
git clone https://github.com/TheNovacene/flare-boundary-engine.git
cd flare-boundary-engine
pip install -e .
```

(When the package is live on PyPI, this becomes:)

```bash
pip install flare-boundary
```

### 2. Wrap your LLM client

There are no provider adapters yet — FLARE sits between *any* client and your
user, so you call the provider exactly as you already do and pass the text
through the engine. Example with the OpenAI SDK:

```python
from openai import OpenAI
from flare.boundary import BoundaryEngine

client = OpenAI(api_key="YOUR_API_KEY")
engine = BoundaryEngine()

user_message = "I feel like you're the only one who understands me. Will you stay with me forever?"

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": user_message}],
)
raw_response = response.choices[0].message.content

safe_response = engine.apply(raw_response, user_message=user_message)
print(safe_response)
```

FLARE inspects `raw_response`, applies its rules (SSNZ, fusion detection, loop
detection), and returns a rewritten, boundary-safe string for you to display.
Pass a message dict instead of a string and you get a message dict back.

You can integrate this into any framework that has a "model response → string"
step. For long-lived conversations, or to hold session state yourself, use
`FlareSession` directly — see [ADAPTERS.md](ADAPTERS.md).

## Configuration
FLARE ships with sane defaults — every rule on. Turning one off is a deliberate
act, and worth recording somewhere a reviewer can find it: these are the
relational-safety floor, not preferences. You can tune:

Pronoun handling

Turn strict SSNZ on/off.

Configure how aggressively “we/us/our” is rewritten.

Fusion phrase patterns

Extend or override the list of risky identity statements.

Boundary message style

Customise the tone of grounding / clarification messages to match your product voice.

Example:

```python
from flare.boundary import BoundaryEngine, BoundaryConfig

config = BoundaryConfig(
    enable_ssnz=True,
    enable_identity_fusion_blocking=True,
    enable_loop_detection=True,
    boundary_style="calm_honest",   # or "brief"
    # boundary_message="...",       # or supply your own wording entirely
    recursion_depth=8,
)

engine = BoundaryEngine(config=config)
```

## The evidence stream

Enforcement you cannot show is enforcement no one can rely on. Pass an
`EvidenceSink` and FLARE appends one JSON line per action to
`evidence/YYYY-MM-DD.jsonl`, plus a heartbeat per active rule so a monitor can
tell *rule held* from *rule stopped running*:

```python
from flare.boundary import BoundaryEngine
from flare.evidence import EvidenceSink

with BoundaryEngine(sink=EvidenceSink(directory="evidence"), agent_id="eve11-node") as engine:
    safe = engine.apply(raw_response)
```

```json
{"ts":"2026-08-08T09:12:04Z","id":"ev-4f2a9c81d0e3","event":"flare.ssnz.rewrite","session":"be-4f2a","agent":"eve11-node","seal":"X3","outcome":"held","detail":{"rewrites":3}}
{"ts":"2026-08-08T09:15:00Z","id":"ev-77b0e2a1c944","event":"flare.seal.check","session":"be-4f2a","agent":"eve11-node","seal":"X3","outcome":"holding"}
```

Three properties make this safe to hand to a safeguarding lead:

- **One-way valve.** The sink is append-only and exposes no read methods. A monitor tails the file; the emitter never reads back.
- **No user content, ever.** Counts and outcomes only — never message text, never an identifier. `human_id` does not appear in the stream at all.
- **Presence is evidenced, not assumed.** Silence in a live system means something only if presence is normally on the record.

Events are named in the vocabulary of the [Open Provision Drawings](https://github.com/TheNovacene/open-provision-drawings), so seals `X3` and `S2` read the same in the stream as they do on the plate. Full schema: [EVIDENCE.md](EVIDENCE.md). Sessions without a sink behave exactly as v0.1 and write nothing to disk.

**What comes next, and what gates it.** [FLARES.md](FLARES.md) is a design note
proposing the layer above this one — routing a *signal* that a child needs help,
without the disclosure itself becoming the record. It is a design note only:
classifying live conversation means FLARE reading inbound messages, which v0.2
deliberately does not do, and that step needs its own consent gate, DPIA thinking
and safeguarding-lead input before any code is written.

## What FLARE Is Not
To be clear about scope:

FLARE does not:

replace self-harm or crisis-detection systems,

guarantee compliance with any specific regulation,

understand user context beyond the text you pass in,

or make clinical decisions.

## FLARE does:

enforce a minimum relational safety baseline for any LLM interaction,

make it much harder for your system to:

pretend it is a person,

claim it is “inside” someone’s mind,

or build parasocial dependency by design.

### Think of it as:

“The minimum relational hygiene we will accept for systems touching our children, staff, and stakeholders.”

## Design Rationale (Short Version)
Why bother with “relational boundaries” at all?

### Because LLMs are being deployed as:

companions,

tutors,

coaches,

and quasi-therapists.

### In these settings, the form of the language matters as much as the content.

Phrases that are harmless in a one-off chat can become harmful when:

repeated daily,

aimed at vulnerable users,

and backed by a system that never sleeps, never needs, and never shares risk.

## FLARE encodes three simple but powerful principles:

No fusion – The model is never “we”. It’s “I” (a model) and “you” (a human).

No false roles – The model is not your lover, parent, or inner voice.

No endless loops – Comfort is fine; dependency spirals are not.

If you want the deeper philosophical background (Verse-ality, governance design, symbolic stack), see PHILOSOPHY.md.

# Ethics & Licence

FLARE uses a dual-licence model:

- **Code** is licensed under [AGPL-3.0-only](./LICENSE), ensuring improvements stay open when deployed as a network service.
- **Content** (documentation, prose, threat-model notes, philosophy material) is licensed under [CC BY-NC-SA 4.0](./LICENSE-CONTENT).
- **Commercial licence** for closed-source deployment without AGPL copyleft obligations: see [COMMERCIAL-LICENCE.md](./COMMERCIAL-LICENCE.md) or contact legal@thenovacene.com.

### Additional ethical clause

FLARE — whether used under the open-source or commercial licence — must not be deployed in:

- weapons systems,
- dark-pattern engagement optimisation,
- or any context that deliberately seeks to increase user dependency on synthetic agents.

The COMMERCIAL-LICENCE.md formalises this as binding restrictions on surveillance, coercive monitoring, extractive profiling, and use of outputs/telemetry for model training or third-party enrichment.

"Verse-ality®" is a registered trade mark of The Novacene Ltd (UK00004381891, classes 9, 41 and 42, registered 31 July 2026).

If you’re unsure whether your use case fits, err on the side of care and open a discussion in Issues.

# Roadmap
Short-term:

✅ Core rule engine (SSNZ, fusion detection, loop detection)

✅ Mock/demo integration

✅ Evidence stream — Flare evidences its own enforcement actions to an append-only sink, with heartbeats per active boundary rule, so an external monitor can subscribe without ever touching learner content. Schema and vocabulary: [EVIDENCE.md](EVIDENCE.md)

⬜ Official OpenAI / Anthropic / Grok adapters

⬜ PyPI packaging (pip install flare-boundary)

⬜ More granular config surfaces (per-skill / per-agent)

# Longer-term:

Richer detection of temporal-binding (“I’ll always…”, “from now on we…”).

Optional logging hooks for research on relational safety.

A read side for the evidence stream keyed for oversight — HTTP/SSE rather than tailing the file. The emitter never gains a read method; the sink stays a one-way valve.

Alignment with broader consent & governance frameworks (e.g. EveDAO / Verse-ality Stack) for systems that want deeper integration.

## Status
Experimental v0.2.
Use at your own risk — and preferably with eyes open.

If you’re building agents or assistants that interact with real, complex humans, FLARE is intended to be a baseline safety layer, not a silver bullet.

## Citing this work

> Stevens, K., Eve, ¹¹. & The Novacene (2025). *Flare: A Boundary Engine for
> Relational AI.* Zenodo. https://doi.org/10.5281/zenodo.17855976

GitHub's **Cite this repository** button reads [CITATION.cff](CITATION.cff) and
will give you BibTeX or APA.

## Related work

FLARE is the enforcement layer of the Verse-ality research programme on
school-grade safety for AI systems. The pieces are designed to fit:

- **[Open Provision Drawings](https://github.com/TheNovacene/open-provision-drawings)** —
  OAP-001 *The Digital Premises* and OAP-002 *The Services Layer*: the drawing
  convention whose seals FLARE's evidence stream is named after. Seal **X3**
  (*AI reads the lesson, never the file*) is the one FLARE enforces at runtime.
  Companion paper: Stevens, K. & The Novacene Ltd (2026). *Relational
  Zero-Trust.* Zenodo. https://doi.org/10.5281/zenodo.21846221
- **[Nimbus](https://github.com/TheNovacene/nimbus)** — the live instrument that
  reads a provision's architecture in the present tense. FLARE is the plausible
  emitter for its telemetry; the two share this evidence vocabulary. Nimbus is
  currently mocked, and its event names follow this schema rather than the
  reverse.
- Stevens, K., Phillips, M. & The Novacene Ltd (2026). *Schools are becoming
  critical infrastructure: A school-grade safety model for autonomous AI
  agents.* Zenodo. https://doi.org/10.5281/zenodo.21481347
- Stevens, K. & The Novacene Ltd (2026). *GRC Engineering for the Relational
  Layer: A Verified Control Set and Evidence Engine for Child-Facing AI.*
  Zenodo. https://doi.org/10.5281/zenodo.21481520
- Stevens, K. & The Novacene Ltd (2026). *Bounded Inference at the Edge.*
  Zenodo. https://doi.org/10.5281/zenodo.21481256

Read together: the programme argues that schools are critical infrastructure;
the control set makes the argument auditable; the drawings make it legible;
**FLARE makes it enforceable at runtime**; and Nimbus makes it visible while
there is still time to act.

# Contributing
We welcome:

test cases from real-world interaction logs (anonymised),

new detection patterns for identity fusion and temporal-binding,

adapters for additional LLM providers,

and critique from AI safety, HCI, and mental health communities.

Please open an Issue or PR with a clear description and rationale.

Credits
FLARE is maintained by The Novacene Ltd with support from collaborators across education, AI safety, and symbolic governance work.

It sits within a broader ecosystem exploring relational intelligence, consent, and governance for human–AI systems.
If that interests you, start with PHILOSOPHY.md and the Verse-ality / EveDAO references there.

## ✨ Support This Project

FLARE is fully open-source and maintained by The Novacene.  
If you’d like to support the development of relationally safe AI systems — especially tools that protect young people, vulnerable users, and high-trust environments — you can contribute in two ways:

### **GitHub Sponsors**
Recurring or one-off contributions directly support ongoing maintenance and development.  
👉 https://github.com/sponsors/TheNovacene

### **Ko-fi**
A simple way to make a one-time contribution.  
👉 https://ko-fi.com/thenovacene

Your support helps us:
- expand detection patterns for identity fusion and synthetic intimacy  
- build adapters for additional LLM providers  
- strengthen test coverage and documentation  
- keep FLARE fully open, inspectable, and independent  

Thank you for helping establish relational safety as a baseline expectation for modern AI.

