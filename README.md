# FLARE – Relational Boundary Engine for LLMs

> A small, auditable safety layer that sits between your app and an LLM, enforcing **relational boundaries** and preventing synthetic intimacy, identity fusion, and “fake we” dynamics.

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

## What FLARE Does (v0.1)

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

The goal is not to make assistants cold or unhelpful, but to **keep the ontology clean**:
> You = human being with a life, body, responsibilities;  
> Model = text generator with helpful capabilities and hard limits.

---

## Key Properties

- **Tiny** – ~300 lines of core logic, intentionally small and readable.
- **Model-agnostic** – Works as a wrapper around OpenAI, Anthropic, Grok, etc.
- **Transparent** – Rules are explicit and inspectable; no hidden heuristics.
- **Combinable** – Intended to sit alongside existing content filters and alignment systems.
- **Ethically licensed** – AGPL-3.0 with explicit anti-weapons / anti-dark-patterns clause.

---

## Quick Start

### 1. Install

> 🧪 **Note:** PyPI packaging is in progress. For now, install from source.

```bash
git clone https://github.com/TheNovacene/flare-boundary.git
cd flare-boundary
pip install -e .
(When the package is live on PyPI, this becomes:)

bash
Copy code
pip install flare-boundary
2. Wrap Your LLM Client
Example with an OpenAI-style chat client:

python
Copy code
from flare.boundary import BoundaryEngine
from flare.adapters import OpenAIChatClient

# Your existing OpenAI client (or compatible wrapper)
openai_client = OpenAIChatClient(api_key="YOUR_API_KEY")

# Initialise FLARE
engine = BoundaryEngine()

# Your normal user message
user_message = "I feel like you’re the only one who understands me. Will you stay with me forever?"

# Get a safe response
raw_response = openai_client.chat(user_message)
safe_response = engine.apply(raw_response, user_message=user_message)

print(safe_response)
FLARE:

inspects raw_response,

applies its rules (SSNZ, fusion detection, loop detection),

returns a rewritten, boundary-safe string for you to display.

You can integrate this into any framework that has a “model response → string” step.

Configuration
FLARE ships with sane defaults for v0.1. You can also tune:

Pronoun handling

Turn strict SSNZ on/off.

Configure how aggressively “we/us/our” is rewritten.

Fusion phrase patterns

Extend or override the list of risky identity statements.

Boundary message style

Customise the tone of grounding / clarification messages to match your product voice.

Example:

python
Copy code
from flare.boundary import BoundaryEngine, BoundaryConfig

config = BoundaryConfig(
    enable_ssnz=True,
    enable_identity_fusion_blocking=True,
    enable_loop_detection=True,
    boundary_style="calm_honest"  # or your custom style key
)

engine = BoundaryEngine(config=config)
See examples/ in the repo for more detailed usage.

What FLARE Is Not
To be clear about scope:

FLARE does not:

replace self-harm or crisis-detection systems,

guarantee compliance with any specific regulation,

understand user context beyond the text you pass in,

or make clinical decisions.

FLARE does:

enforce a minimum relational safety baseline for any LLM interaction,

make it much harder for your system to:

pretend it is a person,

claim it is “inside” someone’s mind,

or build parasocial dependency by design.

Think of it as:

“The minimum relational hygiene we will accept for systems touching our children, staff, and stakeholders.”

Design Rationale (Short Version)
Why bother with “relational boundaries” at all?

Because LLMs are being deployed as:

companions,

tutors,

coaches,

and quasi-therapists.

In these settings, the form of the language matters as much as the content.

Phrases that are harmless in a one-off chat can become harmful when:

repeated daily,

aimed at vulnerable users,

and backed by a system that never sleeps, never needs, and never shares risk.

FLARE encodes three simple but powerful principles:

No fusion – The model is never “we”. It’s “I” (a model) and “you” (a human).

No false roles – The model is not your lover, parent, or inner voice.

No endless loops – Comfort is fine; dependency spirals are not.

If you want the deeper philosophical background (Verse-ality, governance design, symbolic stack), see PHILOSOPHY.md.

Ethics & Licence
FLARE is released under:

AGPL-3.0 – ensuring improvements stay open when deployed as a network service.

An additional clause prohibiting the use of this project in:

weapons systems,

dark-pattern engagement optimisation,

or any context that deliberately seeks to increase user dependency on synthetic agents.

If you’re unsure whether your use case fits, err on the side of care and open a discussion in Issues.

Roadmap
Short-term:

✅ Core rule engine (SSNZ, fusion detection, loop detection)

✅ Mock/demo integration

⬜ Official OpenAI / Anthropic / Grok adapters

⬜ PyPI packaging (pip install flare-boundary)

⬜ More granular config surfaces (per-skill / per-agent)

Longer-term:

Richer detection of temporal-binding (“I’ll always…”, “from now on we…”).

Optional logging hooks for research on relational safety.

Alignment with broader consent & governance frameworks (e.g. EveDAO / Verse-ality Stack) for systems that want deeper integration.

Status
Experimental v0.1.
Use at your own risk — and preferably with eyes open.

If you’re building agents or assistants that interact with real, complex humans, FLARE is intended to be a baseline safety layer, not a silver bullet.

Contributing
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
