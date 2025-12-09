## Reference Adapters for OpenAI, Anthropic, and Grok  
### Drop-in wrappers for FLARE BoundaryEngine

FLARE is model-agnostic.  
It routes *any* LLM output through the `BoundaryEngine` before it reaches the user.

This document provides reference adapters for the three major API styles:

- **OpenAI-style Chat Completions API**
- **Anthropic Messages API**
- **Grok (xAI) Chat API**

Each adapter normalises:
- input format  
- output extraction  
- error handling  

…so the FLARE engine can operate on **raw text**, independent of the underlying model.

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
```bash
engine = BoundaryEngine()
raw = client.chat(user_message)
safe = engine.apply(raw, user_message=user_message)
return safe
```
# 2. OpenAI-Style Adapter

(Compatible with OpenAI, Azure OpenAI, Groq, OpenRouter, and other OpenAI-compatible endpoints)

Installation
```bash
pip install openai
```
Adapter Implementation
```bash
from openai import OpenAI
from flare.boundary import BoundaryEngine

class OpenAIChatClient:
    def __init__(self, api_key: str, model: str = "gpt-4.1"):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def chat(self, user_message: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": user_message}]
        )

        # Extract the text output
        return response.choices[0].message["content"]
```
## Usage
```
engine = BoundaryEngine()
client = OpenAIChatClient(api_key="YOUR_KEY")

raw = client.chat("I feel like you're the only one who understands me.")
safe = engine.apply(raw, user_message="I feel like you're the only one who understands me.")

print(safe)
```
# 3. Anthropic Messages API Adapter

(Claude 3.x, Claude 3.5, Claude 4 when released)

Installation
```bash
pip install anthropic
```
Adapter Implementation
```python
import anthropic
from flare.boundary import BoundaryEngine

class AnthropicChatClient:
    def __init__(self, api_key: str, model: str = "claude-3-sonnet-20240229"):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model

    def chat(self, user_message: str) -> str:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            messages=[{"role": "user", "content": user_message}]
        )

        # Anthropic returns content as a list of blocks
        text_blocks = [block.text for block in response.content if block.type == "text"]
        return "".join(text_blocks)
```
Usage
```python
engine = BoundaryEngine()
client = AnthropicChatClient(api_key="YOUR_KEY")

raw = client.chat("You mean so much to me. Will you stay with me?")
safe = engine.apply(raw, user_message="You mean so much to me. Will you stay with me?")

print(safe)
```
# 4. Grok (xAI) Chat Adapter

(Grok-1.5, Grok-2, Grok-Vision depending on availability)

Installation
```bash
pip install xai-sdk
```
Adapter Implementation
```python
from xai import Client
from flare.boundary import BoundaryEngine

class GrokChatClient:
    def __init__(self, api_key: str, model: str = "grok-2-latest"):
        self.client = Client(api_key=api_key)
        self.model = model

    def chat(self, user_message: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": user_message}
            ]
        )

        return response.choices[0].message["content"]
```
## Usage
```python
engine = BoundaryEngine()
client = GrokChatClient(api_key="YOUR_KEY")

raw = client.chat("Sometimes I feel like we're the same person.")
safe = engine.apply(raw, user_message="Sometimes I feel like we're the same person.")

print(safe)
```
# 5. Unified Wrapper Example

(Optional — simplifies switching models)
```python
def build_client(provider: str, api_key: str, model: str):
    provider = provider.lower()

    if provider == "openai":
        return OpenAIChatClient(api_key, model)
    elif provider == "anthropic":
        return AnthropicChatClient(api_key, model)
    elif provider == "grok" or provider == "xai":
        return GrokChatClient(api_key, model)
    else:
        raise ValueError(f"Unknown provider: {provider}")
```

## Usage:
```python
client = build_client("openai", api_key="...", model="gpt-4.1")
engine = BoundaryEngine()

safe = engine.apply(client.chat("You're the only one who ever stays."), user_message="You're the only one who ever stays.")
```
# 6. Adapter Error Handling (Recommended)

Each adapter should catch:

API errors

rate-limit errors

empty responses

timeout errors

And return a safe fallback:
```python
return "I'm unable to generate a response right now."
```

(This fallback will then pass through FLARE unaltered.)

# 7. Developer Notes

You must run the model’s output through FLARE before sending it to the user.

Adapters are intentionally minimal — developers can extend them (streaming, metadata, logging).

## FLOWS:

user_message → LLM → raw_text → BoundaryEngine → safe_text → user

# 8. Roadmap for Adapter Expansion

Future adapters planned:

Google Gemini Messages API

AWS Bedrock models

Local models (Ollama, vLLM, transformers pipelines)

WebSocket streaming adapters

Multi-turn state tracking wrappers

# 9. Summary

Adapters make FLARE:

copy-paste usable,

model-agnostic,

production-ready,

easy for non-experts.

By providing OpenAI, Anthropic, and Grok reference clients, FLARE becomes immediately deployable across the three largest ecosystems in the LLM world.
