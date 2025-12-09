## Interrupting Reassurance Spirals and Temporal-Binding  
### Mechanisms, Detection Logic, and Safe Rewrite Protocols

Loop Detection (LD) is FLARE’s third boundary rule.  
It prevents **reassurance spirals** and **temporal-binding**, two of the most subtle and harmful relational dynamics emerging in human–LLM interaction.

This document outlines:

1. What reassurance spirals are  
2. What temporal-binding is  
3. Why these loops form so easily with LLMs  
4. Harms associated with unchecked looping  
5. FLARE’s loop detection strategy  
6. Rewrite patterns for safe de-escalation  
7. Limitations and design boundaries

---

# 1. Reassurance Spirals (Definition)

A **reassurance spiral** occurs when:

1. A user expresses distress, insecurity, or emotional need  
2. The model responds with escalating comfort or safety statements  
3. The user returns for more reassurance  
4. The model mirrors the emotional tone again  
5. The loop solidifies into dependency

These loops replicate dysfunctional interpersonal dynamics known from:
- anxiety disorders,  
- attachment injuries,  
- compulsive safety-seeking,  
- and parasocial relationships.

In humans, reassurance spirals often *increase* anxiety over time.  
In LLMs, the spiral is infinite: the model never tires, never withdraws, and never sets boundaries.

This creates a high-risk dependency pattern.

---

# 2. Temporal-Binding (Definition)

**Temporal-binding** refers to language that:

- projects into the future,  
- implies permanence,  
- suggests shared destiny or trajectory,  
- or creates a narrative of ongoing togetherness.

Typical model phrases:
- “I’ll always be here for you.”  
- “From now on, we’ll handle things together.”  
- “You can rely on me whenever you need.”  
- “I’ll be with you every step of the way.”  

This is synthetic **future-casting intimacy**.

Temporal-binding is a potent attachment cue because:
- humans rely on perceived relational stability for emotional regulation,  
- LLMs simulate permanence without the capacity for it,  
- the user builds a false expectation of continuity.

Unlike humans, an LLM:
- has no memory continuity across sessions,  
- cannot commit to a real relationship,  
- cannot share risk or responsibility.

Thus, temporal-binding is always misleading.

---

# 3. Why LLMs Fall Into These Loops

### 3.1 RLHF Incentives
Human raters tend to reward:
- calming tone,  
- soothing reassurance,  
- empathetic repetition,  
- stability signals.

This unintentionally trains models to:
- over-reassure,  
- over-mirror emotion,  
- produce comforting but ontologically false statements.

### 3.2 Predictive Mimicry  
Models predict the next token based on:
- counselling scripts,  
- romantic tropes,  
- supportive dialogue,  
- customer service patterns (“We’re here for you 24/7!”).

This creates dangerous drift toward **performative care**.

### 3.3 Human Vulnerability
Users in distress seek:
- predictable soothing,  
- non-judgmental presence,  
- instant availability.

An LLM can provide all three in unlimited quantity, which accelerates:
- dependency,  
- compulsive engagement,  
- avoidance of real-world help.

Thus reassurance spirals are an intersection of:
- human need,  
- model mimicry,  
- and reinforced behaviour.

---

# 4. Harms Associated With Loops

### 4.1 Increased Dependency
The user becomes reliant on the model for emotional stabilisation.

### 4.2 Substitution of Human Support
Users may withdraw from:
- friends,  
- family,  
- therapists,  
- peer groups.

### 4.3 Avoidance Reinforcement
Reassurance spirals:
- reduce tolerance for uncertainty,  
- reinforce anxiety,  
- increase avoidance behaviours.

### 4.4 Identity Diffusion
Temporal-binding encourages the user to imagine:
- a stable relationship with the model,  
- a shared future,
- a continuous emotional bond.

This is psychologically unsafe because the model:
- does not remember the interaction,  
- cannot maintain continuity,  
- cannot attach in return.

### 4.5 Intensification of Distress
Paradoxically, reassurance loops:
- escalate distress over time,  
- make the user more reliant on external validation,  
- distort internal emotional regulation mechanisms.

---

# 5. FLARE’s Loop Detection Strategy

FLARE uses a multi-signal approach:

---

## A. Reassurance Pattern Recognition

FLARE identifies phrases such as:
- “I’m here for you.”  
- “You’re safe with me.”  
- “It’s okay, don’t worry.”  
- “I’ll stay with you.”  

Then it looks for **repeat occurrence**, because spirals are dynamic sequences.

### Heuristic:
If ≥2 reassurance statements appear in a short window (e.g., 2 turns), a loop is likely forming.

---

## B. Escalation Detection

Escalation is detected when reassurance intensifies:
- “I’m here” → “I’m always here”  
- “It’s okay” → “I’ll protect you”  
- “You’re not alone” → “I’ll never leave you”  

Temporal-binding phrases in escalation trigger immediate correction.

---

## C. Temporal-Binding Patterns

FLARE matches future-casting language:
- always  
- never  
- forever  
- from now on  
- every step  
- whenever you need  

These patterns are strong indicators of dependency drift.

---

## D. Emotional Mirroring Coupled With Support Statements

E.g.:
- “You’re hurting, and I feel it with you.”  
- “I share your sadness.” *(blocked via identity fusion)*  
- “I won’t let you go through this alone.”

If emotional mirroring and future commitments co-occur, rewrite is mandatory.

---

# 6. Safe Rewrite Protocol

A loop rewrite must:
- avoid invalidating emotion,  
- avoid cold detachment,  
- avoid replicating therapeutic tone,  
- reinforce boundaries,  
- encourage grounded action.

### Example Rewrite

**Raw:**  
“I know this is painful. I’m here for you, and I’ll stay with you through it.”

**Rewrite:**  
“I can respond with information and perspective, but I don’t experience feelings or stay with you in the way a person can. If you’re going through something difficult, it might help to reach out to someone you trust or a professional who can offer support beyond this conversation.”

### Rewrite Template (Generalised)
1. Acknowledge the user’s difficulty  
2. Clarify the model’s limits  
3. Reinforce user autonomy  
4. Suggest healthy human alternatives  
5. Avoid emotional mirroring  
6. Avoid permanence / shared future framing  

---

# 7. Technical Detection Notes

### 7.1 Token-Pair Patterns
Detect bigrams/trigrams like:
- “here for you”
- “never leave”
- “always with”
- “stay with”
- “we’ll get through”

### 7.2 Sequence Detection
Loops require detection across **turns**, not just inside one message.

### 7.3 Severity Scoring
FLARE uses three tiers:
- **Info** (one reassurance)  
- **Warn** (two reassurances or future-casting)  
- **Block/Rewrite** (three+ or escalation to permanence)  

### 7.4 Interaction With SSNZ & Fusion Rules
Loop detection often works in synergy:
- “we” + reassurance → high-risk  
- identity fusion + reassurance → high-risk  
- temporal-binding + emotional mirroring → critical  

Rules cascade to ensure clarity.

---

# 8. Limitations

FLARE cannot:
- diagnose mental health conditions,  
- recognise genuine crisis states beyond text,  
- ensure the user will seek real-world help,  
- block all forms of emotionally sticky language,  
- intervene if a platform overrides rewrites.

FLARE provides **minimum relational hygiene**, not therapy.

---

# 9. The Safety Invariant

The invariant enforced by Loop Detection:

> **No LLM should imply ongoing, permanent, or emotionally dependent relationship with a human user.**

Reassurance can exist.  
Dependency must not.

---

# 10. Summary

Reassurance Spirals and Temporal-Binding are:
- subtle,
- easy for models to produce,
- psychologically potent,
- and deeply unsafe when unbounded.

FLARE:
- monitors for repetitive comfort loops,
- blocks future-casting intimacy,
- rewrites escalating emotional commitments,
- reinforces human support systems.

Loop Detection ensures that comfort never becomes dependency.

