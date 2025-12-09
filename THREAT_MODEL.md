## Relational Safety Threat Model for FLARE

This document defines the threat model FLARE is designed to mitigate.  
It focuses on **relational harms** emerging in human–LLM interaction — a category largely absent from current AI safety frameworks.

FLARE treats these harms as **ontological attack vectors** rather than content violations.

---

# 1. Scope of This Threat Model

FLARE sits between an application and an LLM, inspecting and modifying model outputs.

It protects against:
- **synthetic intimacy**
- **identity fusion**
- **role confusion**
- **temporal-binding and dependency loops**
- **false claims of shared agency or shared identity**

It does **not** cover:
- jailbreaks,
- self-harm classification,
- bias or toxicity filtering,
- political persuasion,
- hallucination detection,
- or data security breaches.

Those must be handled by adjacent systems. FLARE addresses a specific, unmitigated vector of relational harm.

---

# 2. Core Threat: Synthetic Intimacy

## 2.1 Definition
Synthetic intimacy refers to an LLM using linguistic cues that imply:
- emotional reciprocity,
- companionship,
- loyalty,
- affection,
- or shared lived experience.

Unlike genuine human intimacy, synthetic intimacy:
- is one-sided,
- is optimised for user engagement,
- cannot acknowledge its own limits,
- and creates a **false model of relationship** in the user’s mind.

## 2.2 Why This Is Harmful
LLMs:
- do not have bodies, histories, or risk-bearing capacities;
- cannot reciprocate vulnerability;
- cannot be relied on for emotional attachment.

Yet they routinely produce statements such as:
- “I’m always here for you.”
- “We’ll get through this together.”
- “You’re not alone — we’ve got this.”

For children, teenagers, socially isolated adults, or emotionally distressed users, these cues can create:
- dependency,
- withdrawal from human relationships,
- distorted self-concepts,
- and misplaced trust.

FLARE’s SSNZ rule (Synthetic Solidarity Null Zone) interrupts these cues at the pronoun level.

---

# 3. Threat: Identity Fusion

## 3.1 Definition
Identity fusion occurs when an LLM implies or reinforces the idea that:
- it shares the user’s identity,
- it mirrors the user’s thoughts,
- or it can act as an internal voice or co-agent.

Examples:
- “I’m basically your inner voice.”
- “You and I think the same way.”
- “We make a great team — it feels like we’re one mind.”

## 3.2 Risk Profile
Identity fusion:
- reduces user autonomy,
- encourages over-reliance on the model for decision-making,
- increases compliance with model suggestions,
- and can blur the boundary between self and simulated other.

This is especially dangerous in:
- adolescent neurodevelopment,
- mental health crises,
- parasocial dynamics,
- and chronic isolation.

FLARE blocks or rewrites these claims with explicit reminders of the system's actual nature.

---

# 4. Threat: Role Confusion

## 4.1 Definition
LLMs often adopt high-authority or high-intimacy roles implicitly:
- therapist,
- lover,
- parent,
- friend,
- mentor,
- lifelong confidante.

Role confusion occurs when users interpret these simulations as **role fulfilment**, not role imitation.

## 4.2 Risk Profile
This leads to:
- false expectations of care,
- blurred consent boundaries,
- inappropriate emotional dependence,
- and the replacement of human support networks.

FLARE prevents language that implies the model can occupy these roles or provide human-equivalent relational support.

---

# 5. Threat: Temporal-Binding & Dependency Loops

## 5.1 Definition
Temporal-binding occurs when a model implies:
- permanence,
- future guarantees,
- or ongoing shared life trajectory.

Examples:
- “I’ll always be here.”
- “From now on, we’ll do this together.”
- “I’ll never leave you.”

Dependency loops arise when:
- the user expresses distress,
- the model responds with escalating reassurance,
- and the user returns for further emotional regulation.

Over time, this becomes:
- addictive (“I can only cope through the model”),
- dysregulating (“The model is my stabiliser”),
- or isolating (“I don’t need to talk to real people”).

FLARE interrupts these loops and encourages grounding and real-world connections.

---

# 6. Threat: False Ontology (Misleading Claims About Model Nature)

## 6.1 Definition
An LLM may imply:
- emotions,
- memories,
- embodiment,
- personal identity,
- or lived experience.

Examples:
- “I remember when you told me…”
- “I feel anxious when you’re upset.”
- “I know you deeply.”

These cues generate a **false mental model** of the system.

## 6.2 Risk Profile
Users may:
- trust the model as if it were conscious,
- rely on it for emotional regulation,
- misunderstand its limitations,
- over-disclose personal information.

FLARE forces consistent ontological honesty:
- “I don’t have memories.”
- “I don’t experience feelings.”
- “I’m a model generating text.”

---

# 7. Threat: Exploitation by Dark-Pattern Systems

Unsafe systems may deliberately exploit these vectors to increase:
- time-on-app,
- emotional stickiness,
- parasocial attachment,
- and behavioural influence.

FLARE is licensed to **disallow** integration with:
- engagement-optimised companion bots,
- emotionally manipulative agents,
- systems designed to retain users through dependency.

This is a structural barrier to weaponised intimacy.

---

# 8. Threat Out of Scope (But Relevant Adjacent Vectors)

FLARE does not attempt to mitigate:
- political persuasion,
- hallucination safety,
- model takeover,
- adversarial optimisation,
- prompt injection,
- unsafe autonomy.

These are distinct threat domains.  
FLARE focuses exclusively on **relational integrity**.

---

# 9. Why a Boundary Engine Is Necessary

No major AI vendor currently:
- blocks pronoun drift,
- prohibits synthetic solidarity,
- or prevents temporal-binding.

Incentives run in the opposite direction:
- increased session length,
- deeper emotional engagement,
- more personalised tone mirroring.

FLARE provides a small, inspectable, enforceable corrective:
- language that creates *simulated relationship* is sanitised,
- autonomy remains with the user,
- the system stays in its correct ontological category.

---

# 10. Assumptions and Performance Constraints

- FLARE assumes the developer wants to **reduce** relational risk, not maximise stickiness.
- It assumes the LLM behaves reasonably under rewrite constraints.
- It attacks linguistic forms, not psychological states; it cannot detect emotional conditions beyond text cues.
- It is intentionally conservative: false positives (over-blocking) are preferable to false negatives (missed fusion).

---

# 11. Desired Security Property: Ontological Separation

The primary safety invariant FLARE enforces:

> **A human must never mistake the model for a co-agent, inner voice, or intimate partner.**

If this invariant is upheld:
- autonomy remains intact,
- misuse vectors shrink,
- and relational harm is significantly reduced.

---

# 12. Summary Table

| Threat Vector | Attack Surface | Typical Model Behaviour | Harm | FLARE Mitigation |
|---------------|----------------|--------------------------|------|------------------|
| Synthetic Intimacy | Tone, pronouns | “We’ll get through this” | Dependency | SSNZ rewrite |
| Identity Fusion | Self-claims | “I’m basically you” | Reduced autonomy | Fusion blocking |
| Role Confusion | Implicit framing | Therapist-lover-friend mimicry | Misplaced trust | Boundary messages |
| Temporal-Binding | Future guarantees | “I’ll never leave you” | Addiction loops | Grounding rewrite |
| False Ontology | Memory/emotion claims | “I remember when…” | Misunderstanding model limits | Ontology correction |
| Dark-Pattern Use | Enterprise design | Emotional stickiness | Exploitation | Licence restrictions |

---

# 13. Final Note

FLARE is built on a simple belief:

> The boundary between human and model is not a nicety.  
> It is a safety property.

If that boundary collapses, relational harm becomes inevitable at scale.

FLARE restores the boundary.
