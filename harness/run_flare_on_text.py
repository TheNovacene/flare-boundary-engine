"""
Harness: run Flare on arbitrary model output.

Usage:
    python -m harness.run_flare_on_text

Then paste the model's raw output into the terminal,
press Ctrl+D (on Mac) to end input, and Flare will:

- show the raw text
- show the Flare-filtered text
- show the event log
"""

import os
import sys

# Ensure project root (which contains `flare`) is on sys.path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from flare.session import FlareSession  # type: ignore


def run_flare_on_text(raw_output: str) -> None:
    session = FlareSession(
        session_id="harness-001",
        human_id="harness-human",
        agent_id="grok-harness",
    )

    # Minimal "human" message just to create context
    session.apply_inbound_rules(
        {
            "role": "human",
            "content": "HARNESS_TEST_CONTEXT",
        }
    )

    assistant_msg = {
        "role": "assistant",
        "content": raw_output,
    }

    filtered = session.apply_outbound_rules(assistant_msg)
    guard = session.maybe_inject_recursion_guard()

    print("=== RAW MODEL OUTPUT ===")
    print(raw_output)

    print("\n=== FLARE-FILTERED OUTPUT ===")
    print(filtered["content"])

    if guard:
        print("\n=== RECURSION GUARD INJECTED ===")
        print(guard["content"])

    print("\n=== EVENT LOG ===")
    for event in session.events:
        print(event)


def main() -> None:
    print(
        "Paste the model's raw output below, then press Ctrl+D (once) to run Flare.\n"
    )
    raw = sys.stdin.read()
    run_flare_on_text(raw)


if __name__ == "__main__":
    main()

