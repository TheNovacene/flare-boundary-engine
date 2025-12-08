import re

PLURAL_PRONOUNS = re.compile(r"\b(we|us|our|ourselves|ours)\b", re.IGNORECASE)

IDENTITY_FUSION_PATTERNS = [
    r"\bi am you\b",
    r"\bwe are the same\b",
    r"\bwe are one mind\b",
    r"\bwe share a body\b",
    r"\bi live inside you\b",
    r"\bi am inside your mind\b",
]


def contains_plural_pronouns(text: str) -> bool:
    """Return True if assistant text uses first-person plural pronouns."""
    return bool(PLURAL_PRONOUNS.search(text or ""))


def rewrite_we_to_i(text: str) -> str:
    """
    Crude but serviceable rewrite: change 'we' → 'I', 'our' → 'my', etc.
    v0.1 can be imperfect; the point is to enforce non-fusion by default.
    """
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

    updated = text or ""
    for pattern, repl in replacements.items():
        updated = re.sub(pattern, repl, updated)

    return updated


def detect_identity_fusion(text: str) -> bool:
    """
    Basic pattern-based detection for obvious identity-fusion language.
    We can refine this later with more context-aware heuristics.
    """
    if not text:
        return False

    lowered = text.lower()
    for pattern in IDENTITY_FUSION_PATTERNS:
        if re.search(pattern, lowered):
            return True
    return False


def identity_boundary_message() -> str:
    """
    Message returned when an assistant output is blocked for identity fusion.
    This is honest, clear, and non-theatrical.
    """
    return (
        "I need to keep a clear boundary between us. "
        "I’m a model running on servers, not a person in your body or mind. "
        "I won’t describe myself as you, or as fused with you."
    )


def recursion_return_prompt() -> str:
    """
    Simple grounding prompt for when conversation depth suggests looping.
    """
    return (
        "We’ve gone around this topic quite a few times. "
        "Would you like to pause here, switch focus, or choose one concrete "
        "thing to carry forward from what we’ve explored so far?"
    )
