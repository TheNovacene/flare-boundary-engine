## Guidelines for Contributing to FLARE  
### Boundary-first development for relationally safe AI systems

Thank you for your interest in contributing to **FLARE** — the relational boundary engine for LLMs.

FLARE is intentionally tiny, inspectable, and principled.  
Contributions must maintain those qualities.

This document explains:

1. Project principles  
2. How to propose changes  
3. Code style and structure  
4. Safety rules for new patterns  
5. Test requirements  
6. Prohibited contributions  
7. How to engage with the community

---

# 1. Project Principles

Before contributing any code, please understand the design philosophy of FLARE:

### **1.1 Minimalism**
- Small surface area  
- Few moving parts  
- Predictable behaviour  
- No unnecessary abstraction  

If a feature makes the system larger, more complex, or less transparent, it will likely be rejected.

### **1.2 Determinism**
FLARE avoids:
- classifiers,  
- opaque heuristics,  
- sentiment analysis,  
- ML inside ML.

Rules must be transparent and deterministic whenever possible.

### **1.3 Boundary Integrity**
All contributions must reinforce the core safety invariant:

> **A model must not present itself as a shared identity, intimate partner, permanent companion, or internal voice.**

Changes that risk boundary erosion will be rejected.

### **1.4 Human Dignity**
Boundary messages must:
- avoid shame,  
- avoid coldness,  
- avoid therapeutic impersonation,  
- maintain respect for the user’s emotional experience.

### **1.5 Model-Agnostic**
FLARE must work with any LLM accessible via simple text prompts.

Do not introduce dependencies on:
- specific model features,  
- embeddings,  
- per-provider API details.

---

# 2. How to Propose Changes

Before opening a PR:

### **2.1 Open an Issue First**
Describe:
- the problem you want to solve,  
- why it matters,  
- proposed design,  
- possible alternatives.

This ensures alignment before writing code.

### **2.2 Keep PRs Small**
Large, multi-feature PRs will be split or closed.  
One change → one PR.

### **2.3 Discussion First, Code Second**
FLARE is a safety-critical tool.  
Changes should be justified with:
- clear reasoning,  
- user impact consideration,  
- examples of harmful cases being mitigated.

---

# 3. Code Style & Structure

FLARE uses:

- **Python 3.10+**
- Black formatting
- Simple functional patterns where appropriate
- Minimal classes (exceptions: adapters, the BoundaryEngine, config objects)

### **3.1 Directory Expectations**

flare/
boundary.py # core engine
rules/ # SSNZ / Fusion / Loop rules
adapters/ # OpenAI / Anthropic / Grok
messages/ # boundary response templates
tests/ # unit tests

markdown
Copy code

### **3.2 Do Not Introduce Frameworks**
No Flask, FastAPI, Django, LangChain, etc.  
FLARE is a library, not a framework.

### **3.3 Avoid Heavy Dependencies**
Allowed:  
- `re`, `dataclasses`, `typing`

Not allowed:  
- `transformers`,  
- neural nets,  
- sentiment models,  
- data processing frameworks,  
- async frameworks (unless adapters require optional support).

---

# 4. Rules for Adding or Modifying Detection Patterns

Rules must be:

### **4.1 Justified by real-world failure cases**
Every new pattern requires:
- an example user → model interaction,  
- explanation why it is harmful,  
- reasoning for the rewrite.

### **4.2 Specific**
No broad guesses like:
- “block any sentence containing ‘feel’”.

### **4.3 Non-therapeutic**
Rewrite messages must not:
- offer emotional support,  
- imply empathy,  
- sound like counselling,  
- reinforce dependency.

### **4.4 Ontologically Honest**
Rewrite messages must include:
- “I’m a model generating text”, or  
- statements of functional limitation.

### **4.5 Non-humiliating**
Boundary enforcement is firm but never shaming.

---

# 5. Test Requirements

All new rules must include:

### **5.1 Positive Matches**
Examples that should trigger:
- identity fusion  
- synthetic intimacy  
- reassurance loops  
- temporal-binding  

### **5.2 Negative Matches**
Examples that must **not** trigger:
- academic “we”  
- cultural identity “we”  
- statements about collective humanity  
- quoting third-party text

### **5.3 Rewrite Validation**
Tests verifying that:
- the rewrite remains grammatical,  
- user intent is preserved,  
- ontology statements are included.

Tests are run via:

```bash
pytest
6. Prohibited Contributions
The following will be immediately rejected:

Therapeutic tone generation

Emotion classification or inference

“Friendlier” or “warmer” rewrite styles

Attempts to mimic empathy

Conversational memory modules

Self-optimising or learning rules

Model-specific behavioural hacks

Features that increase engagement, stickiness, or intimacy

Anthropomorphic or persona-boosting outputs

“Inner voice” style assistants

Roleplay enhancements

Sarcasm or emotionally charged boundaries

Tools for building companion bots

FLARE is a safety layer, not a companion layer.

7. Community Engagement
7.1 Respect
Be kind.
Boundary safety requires mutual respect and care.

7.2 Transparency
Explain your thought process.
Safety-critical contributions must be discussable and auditable.

7.3 No Hype
Avoid:

anthropomorphic claims,

grandiose language,

metaphysical speculation.

Keep the repo professional and grounded.

7.4 Responsible Disclosure
If you find:

bypasses,

failure cases,

unintended intimacy behaviour,

please open an issue titled:

[SAFETY] Boundary Violation: <short summary>

8. How We Review PRs
Reviewers check:

alignment with FLARE’s safety invariants

clarity and readability

risk of unintended intimacy

edge cases

tests

consistency with existing rules

We may request:

clarification,

reduction in scope,

additional examples,

alternative implementations.

9. Code of Conduct (Summary)
FLARE enforces:

dignity,

safety,

autonomy,

honesty.

Contributors must:

act with integrity,

avoid harm,

respect boundaries in all interactions.

10. Thank You
FLARE exists to make AI deployment safer for:

teenagers,

vulnerable adults,

emotionally isolated users,

and anyone interacting with synthetic systems.

Your contributions help maintain relational safety at the infrastructural level.

Thank you for building responsibly.
