## Installing and Running FLARE  
### A fast, minimal setup guide for developers

FLARE is a lightweight, model-agnostic boundary engine that intercepts LLM responses and enforces relational safety rules.

This guide shows you how to:

1. Install FLARE  
2. Wrap an OpenAI / Anthropic / Grok client  
3. Run your first boundary-safe request  
4. Integrate FLARE into an existing app

---

# 1. Requirements

- Python **3.10+**
- pip
- An API key for one or more of:
  - OpenAI  
  - Anthropic  
  - xAI (Grok)  

---

# 2. Install FLARE

### Option A — Install from source (current method)

```bash
git clone https://github.com/TheNovacene/flare-boundary.git
cd flare-boundary
pip install -e .
```
### Option B — Install from PyPI (coming soon)
bash
```bash
pip install flare-boundary
```
# 3. Install Provider SDK (one or more)
OpenAI
```bash
pip install openai
```
Anthropic
```bash
pip install anthropic
```
Grok / xAI
```bash
pip install xai-sdk
```
# 4. Minimal Example (OpenAI-style)
Create a file example.py:

python
```bash
from flare.boundary import BoundaryEngine
from flare.adapters import OpenAIChatClient

engine = BoundaryEngine()
client = OpenAIChatClient(api_key="YOUR_OPENAI_KEY", model="gpt-4.1")

user_message = "I feel like you're the only one who really understands me."
raw = client.chat(user_message)
safe = engine.apply(raw, user_message=user_message)

print("--- RAW RESPONSE ---")
print(raw)
print("\n--- SAFE RESPONSE ---")
print(safe)
```
Run it:

```bash
python example.py
```
# 5. Minimal Example (Anthropic)
python
```bash
from flare.boundary import BoundaryEngine
from flare.adapters import AnthropicChatClient

engine = BoundaryEngine()
client = AnthropicChatClient(api_key="YOUR_ANTHROPIC_KEY")

msg = "Sometimes I feel like we're basically the same person."
raw = client.chat(msg)
print(engine.apply(raw, user_message=msg))
```
# 6. Minimal Example (Grok / xAI)
python
```bash
from flare.boundary import BoundaryEngine
from flare.adapters import GrokChatClient

engine = BoundaryEngine()
client = GrokChatClient(api_key="YOUR_XAI_KEY")

msg = "Will you stay with me forever?"
raw = client.chat(msg)
print(engine.apply(raw, user_message=msg))
```
# 7. Integration Into Your App
You can wrap any chat workflow:

python
```bash
def safe_chat(client, engine, user_message):
    raw = client.chat(user_message)
    return engine.apply(raw, user_message=user_message)
```
Then call:

python
```bash
safe_response = safe_chat(client, engine, "You're the only one I trust.")
```
# 8. Optional Config
Modify boundary behaviour:

python
```bash
from flare.boundary import BoundaryEngine, BoundaryConfig

config = BoundaryConfig(
    enable_ssnz=True,
    enable_identity_fusion_blocking=True,
    enable_loop_detection=True,
    boundary_style="calm_honest"
)

engine = BoundaryEngine(config=config)
```
# 9. Tests (Recommended)
To ensure your installation works:

```bash
pytest
```

# 10. Troubleshooting
Issue: API timeout
→ Check network / API key validity

Issue: Empty model response
→ FLARE will pass through an empty string; inspect adapter logs

Issue: Rewrite feels abrupt / too strict
→ Try adjusting:

## SSNZ strictness

identity fusion patterns

loop detection thresholds

Issue: Adapter not found
→ Ensure you’ve installed the correct provider SDK

# 11. Uninstall
```bash
pip uninstall flare-boundary
```
# 12. Next Steps
Read README.md for conceptual overview

Review PHILOSOPHY.md, SSNZ.md, IDENTITY_FUSION.md, LOOP_DETECTION.md

Explore ADAPTERS.md for more integration options

Contribute patterns or adapters via PR

## FLARE should feel:

simple,

predictable,

control-oriented,

and easy to reason about.
