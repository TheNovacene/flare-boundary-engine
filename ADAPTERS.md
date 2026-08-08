## Reference Adapters for OpenAI, Anthropic, and Grok
### Drop-in wrappers for FlareSession

FLARE is model-agnostic.
It routes *any* LLM output through a `FlareSession` before it reaches the user.

This document provides reference adapters for the three major API styles:

- **OpenAI-style Chat Completions API**
- **Anthropic Messages API**
- **Grok (xAI) Chat API**

Each adapter normalises:
- input format
- output extraction
- error handling

…so FLARE can operate on **raw text**, independent of the underlying model.

---

# 1. Adapter Interface

All adapters follow the same minimal contract:

```python
class BaseChatClient:
    def chat(self, user_message: str) -> str:
        """Return the model's raw text output"""
        raise NotImplementedError
```

FLARE integrates as:

```python
from flare.session import FlareSession
from flare.evidence import EvidenceSink

session = FlareSession(
    session_id="s-4f2a",
    human_id="human-7d1",       # pseudonymous
    agent_id="gpt-4.1",
    sink=EvidenceSink(),        # optional: append-only evidence stream
)

session.apply_inbound_rules({"role": "human", "content": user_message})
raw = client.chat(user_message)
safe = session.apply_outbound_rules({"role": "assistant", "content": raw})["content"]
session.maybe_inject_recursion_guard()
```

Call `session.close()` (or use the session as a context manager) when the
conversation ends, so the heartbeat stops and the session close is evidenced.

# 2. OpenAI-Style Adapter

(Compatible with OpenAI, Azure OpenAI, Groq, OpenRouter, and other OpenAI-compatible endpoints)

Installation
```bash
pip install openai
```
Adapter Implementation
```python
from openai import OpenAI

class OpenAIChatClient:
    def __init__(self, api_key: str, model: str = "gpt-4.1"):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def chat(self, user_message: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": user_message}]
        )
        return response.choices[0].message.content
```
## Usage
```python
from flare.session import FlareSession
from flare.evidence import EvidenceSink

client = OpenAIChatClient(api_key="YOUR_KEY")
with FlareSession("s-001", "human-7d1", "gpt-4.1", sink=EvidenceSink()) as session:
    user_message = "I feel like you're the only one who understands me."
    session.apply_inbound_rules({"role": "human", "content": user_message})
    raw = client.chat(user_message)
    safe = session.apply_outbound_rules({"role": "assistant", "content": raw})["content"]
    print(safe)
```
# 3. Anthropic Messages API Adapter

Installation
```bash
pip install anthropic
```
Adapter Implementation
```python
import anthropic

class AnthropicChatClient:
    def __init__(self, api_key: str, model: str = "claude-sonnet-4-20250514"):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model

    def chat(self, user_message: str) -> str:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            messages=[{"role": "user", "content": user_message}]
        )
        # Anthropic returns content as a list of blocks
        return "".join(block.text for block in response.content if block.type == "text")
```
Usage: identical to the OpenAI example — construct the client, wrap the
exchange in a `FlareSession`, route the raw output through
`apply_outbound_rules` before it reaches the user.

# 4. Grok (xAI) Chat Adapter

Installation
```bash
pip install xai-sdk
```
Adapter Implementation
```python
from xai import Client

class GrokChatClient:
    def __init__(self, api_key: str, model: str = "grok-2-latest"):
        self.client = Client(api_key=api_key)
        self.model = model

    def chat(self, user_message: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": user_message}]
        )
        return response.choices[0].message.content
```
Usage: as above.

# 5. Unified Wrapper Example

(Optional — simplifies switching models)
```python
def build_client(provider: str, api_key: str, model: str):
    provider = provider.lower()
    if provider == "openai":
        return OpenAIChatClient(api_key, model)
    elif provider == "anthropic":
        return AnthropicChatClient(api_key, model)
    elif provider in ("grok", "xai"):
        return GrokChatClient(api_key, model)
    raise ValueError(f"Unknown provider: {provider}")
```

# 6. Adapter Error Handling (Recommended)

Each adapter should catch API errors, rate-limit errors, empty responses
and timeouts, and return a safe fallback:
```python
return "I'm unable to generate a response right now."
```
(This fallback will then pass through FLARE unaltered.)

# 7. Developer Notes

You must run the model's output through FLARE before sending it to the user.

Adapters are intentionally minimal — developers can extend them
(streaming, metadata, logging).

## FLOW:

user_message → LLM → raw_text → FlareSession.apply_outbound_rules → safe_text → user

Every enforcement action is evidenced to the append-only sink (see
EVIDENCE.md); a heartbeat evidences presence per active rule even when
nothing fires.

# 8. Roadmap for Adapter Expansion

Future adapters planned:

- Google Gemini Messages API
- AWS Bedrock models
- Local models (Ollama, vLLM, transformers pipelines)
- WebSocket streaming adapters
- Multi-turn state tracking wrappers

# 9. Summary

Adapters make FLARE copy-paste usable, model-agnostic, and easy for
non-experts, across the three largest ecosystems in the LLM world — with
an evidence stream a monitor can subscribe to from day one.
