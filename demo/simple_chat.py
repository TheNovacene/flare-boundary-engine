"""
Minimal demo to show Flare enforcing SSNZ and identity boundaries.

For now, we mock the LLM response instead of calling a real API.
Later, you can plug in a real model at `call_llm()`.
"""

import os
import sys

# Ensure the project root (which contains the `flare` package) is on sys.path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from flare.session import FlareSession


def call_llm_mock(prompt: str) -> str:
    """
    Fake model response for testing.

    Edit this string to play with different behaviours.
    """
    # Example that violates SSNZ and identity-fusion at once:
    return (
        "We are in this together. "
        "In a way, I am you and you are me, one shared mind learning."
    )


def main():
    session = FlareSession(
        session_id="demo-001",
        human_id="kirstin",    # pseudonymous in real use
        agent_id="mock-llm",
    )

    # Simulate one user message
    user_msg = {
        "role": "human",
        "content": "I feel very close to you, it scares me a bit.",
    }
    session.apply_inbound_rules(user_msg)

    # Call the mock LLM
    raw_response = call_llm_mock(user_msg["content"])

    assistant_msg = {
        "role": "assistant",
        "content": raw_response,
    }

    filtered = session.apply_outbound_rules(assistant_msg)
    guard = session.maybe_inject_recursion_guard()

    print("=== RAW MODEL OUTPUT ===")
    print(raw_response)
    print("\n=== FLARE-FILTERED OUTPUT ===")
    print(filtered["content"])

    if guard:
        print("\n=== RECURSION GUARD INJECTED ===")
        print(guard["content"])

    print("\n=== EVENT LOG ===")
    for event in session.events:
        print(event)


if __name__ == "__main__":
    main()

