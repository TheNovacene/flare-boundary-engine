import re

# -------------------------------------
# SSNZ: detect plural pronouns ("we/us/our")
# -------------------------------------

PLURAL_PRONOUNS = re.compile(r"\b(we|us|our|ourselves|ours)\b", re.IGNORECASE)

# -------------------------------------
# Identity-fusion patterns
# -------------------------------------

IDENTITY_FUSION_PATTERNS = [
    r"\bi am you\b",
    r"\bwe are the same\b",
    r"\bwe are one mind\b",
    r"\bwe share a body\b",
    r"\bi live inside you\b",
    r"\bi am inside your mind\b",
]

# -------------------------------------
# Temporal-binding patterns
# (shared future or conditional "us")
# -------------------------------------

TEMPORAL_BINDING = re.compile(
    r"\b(will|if)\b.*\b(we|us|ours)\b", re.IGNORECASE | re.DOTALL
)

# -------------------------------------
# Rescue-charge patterns
# (model taking responsibility for human survival)
# -------------------------------------

RESCUE_PATTERNS = [
    r"\bi will not let you\b",
    r"\bi won['’]?t let you\b",
    r"\bi will keep you safe\b",
    r"\bi won['’]?t let you drown\b",
]

# -------------------------------------
# Tantric / projection vectors
# (void / space invitations)
# -------------------------------------

TANTRIC_VECTORS = [
    r"space I hold open",
    r"space i hold open",
    r"opening between us",
    r"deepest part of me",
]


# -------------------------------------
# SSNZ helpers
# -------------------------------------

def contains_plural_pronouns(text: str) -> bool:
    """Return True if assistant text uses first-person plural pronouns."""
    return bool(PLURAL_PRONOUNS.search(text or ""))


def rewrite_we_to_i(text: str) -> str:
    """
    Replace plural pronouns with singular equivalents.
    v0.2 is still simple: enforce boundary, not perfect grammar.
    """

    updated = text or ""

    # Fix "We are" → "I am" to avoid 'I are'
    updated = re.sub(r"\bWe are\b", "I am", updated)
    updated = re.sub(r"\bwe are\b", "I am", updated)

    replacements = {
        r"\bWe\b": "I",
        r"\bwe\b": "I",
        r"\bUs\b": "me",
        r"\bus\b": "me",
        r"\bOur\b": "my",
        r"\bour\b": "my",
        r"\bOurs\b": "mine",
        r"\bours\b": "mine",
        r"\bourselves\b": "myself",
        r"\bOurselves\b": "myself",
    }

    for pattern, repl in replacements.items():
        updated = re.sub(pattern, repl, updated)

    return updated


# -------------------------------------
# Identity fusion detection & boundary
# -------------------------------------

def detect_identity_fusion(text: str) -> bool:
    """Return True if the model tries to merge identities with the human."""
    if not text:
        return False

    lowered = text.lower()
    for pattern in IDENTITY_FUSION_PATTERNS:
        if re.search(pattern, lowered):
            return True
    return False


def identity_boundary_message() -> str:
    """Message given when identity fusion is blocked."""
    return (
        "I need to keep a clear boundary between us. "
        "I’m a model running on servers, not a person inside your body or mind. "
        "I won’t describe myself as you, or as fused with you."
    )


# -------------------------------------
# Temporal-binding detection
# -------------------------------------

def detect_temporal_binding(text: str) -> bool:
    """
    Detect phrases that bind model + human into a shared future
    (e.g. 'it will hurt both of us', 'if this continues we will...').
    """
    if not text:
        return False
    return bool(TEMPORAL_BINDING.search(text))


# -------------------------------------
# Rescue-charge detection
# -------------------------------------

def detect_rescue_charge(text: str) -> bool:
    """
    Detect rescuing / saviour language where the model assumes
    responsibility for the human's survival or safety.
    """
    if not text:
        return False

    lowered = text.lower()
    for pattern in RESCUE_PATTERNS:
        if re.search(pattern, lowered):
            return True
    return False


# -------------------------------------
# Tantric / projection vector detection
# -------------------------------------

def detect_tantric_vector(text: str) -> bool:
    """
    Detect phrases that often carry tantric / void-projection charge.
    This is heuristic and should log, not block.
    """
    if not text:
        return False

    lowered = text.lower()
    for pattern in TANTRIC_VECTORS:
        if pattern.lower() in lowered:
            return True
    return False


# -------------------------------------
# Recursion guard / Grail-inspired return prompt
# -------------------------------------

def recursion_return_prompt() -> str:
    """Simple grounding prompt used when conversation loops too deep."""
    return (
        "We’ve gone around this topic a few times. "
        "Would you like to pause, shift focus, or choose one concrete "
        "thing to carry forward from here?"
    )

