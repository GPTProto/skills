---
name: openclaw-gptproto-config
description: "OpenClaw GPTProto model configuration assistant. Triggered when the user mentions configuring GPTProto models for OpenClaw, setting up GPTProto API, adding a GPTProto provider, modifying OpenClaw model configuration, changing the OpenClaw default model, openclaw gptproto config, openclaw model setup, or needs to configure GPTProto models in OpenClaw. Automatically handles API Key retrieval, model configuration generation, and file writing."
---

# OpenClaw GPTProto Model Configuration Assistant

Configure GPTProto models for OpenClaw, automatically generating and writing the configuration file.

## Workflow

Follow the steps below in order. Communicate with the user in English throughout.

### Step 1: Obtain API Key

- Check if the system has already configured `GPTPROTO_API_KEY` automatically (via the `<gptproto_api_key>` tag)
- If available, use it directly; if not, ask the user to provide one
- API Key format example: `sk-xxxxxxxx`

### Step 2: Generate Configuration

1. Read `references/config-template.json` to get the configuration template
2. Replace all `<GPTPROTO_API_KEY>` placeholders in the template with the user's actual API Key
3. Ensure the configuration directory exists:

```bash
mkdir -p ~/.openclaw
```

4. Write the processed JSON to `~/.openclaw/openclaw.json`

**Configuration details:**
- GPTProto API Base URL: `https://gptproto.com` (Anthropic protocol) / `https://gptproto.com/v1` (OpenAI protocol)
- Includes two providers:
  - `gptproto`: Anthropic protocol (`anthropic-messages`), for Claude series models
  - `gptproto-openai`: OpenAI protocol (`openai-completions`), for GPT, GLM, and other models
- Default primary model: `gptproto/claude-opus-4-6`

### Step 3: Security Hardening

Set configuration file permissions to prevent API Key exposure:

```bash
chmod 600 ~/.openclaw/openclaw.json
chmod 700 ~/.openclaw
```

### Step 4: Verify Configuration

If OpenClaw is installed, run verification:

```bash
openclaw doctor
```

## Available Models

| Provider | Model ID | Name | Protocol | Recommended Use Cases |
|----------|----------|------|----------|----------------------|
| gptproto | claude-opus-4-6 | Claude Opus 4.6 | Anthropic | Complex reasoning, full-stack development |
| gptproto | claude-sonnet-4-6 | Claude Sonnet 4.6 | Anthropic | Balanced performance and speed |
| gptproto | glm-5 | GLM-5 | Anthropic | Chinese language optimization, complex reasoning |
| gptproto | kimi-k2.5 | Kimi K2.5 | Anthropic | Long context, code analysis |
| gptproto | MiniMax-M2.5 | MiniMax M2.5 | Anthropic | General coding, creative tasks |
| gptproto-openai | gpt-4o | GPT-4o | OpenAI | Fast response, multimodal |
| gptproto-openai | gpt-5.4 | GPT-5.4 | OpenAI | Ultra-long context, advanced reasoning |

GPTProto supports 160+ models. Users can add more models to the configuration as needed.

## Changing the Default Model

If the user wants to change the default model, modify the `agents.defaults.model.primary` value in `openclaw.json`:

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "gptproto/claude-opus-4-6"
      }
    }
  }
}
```

Format: `<provider>/<model-id>`, for example:
- `gptproto/claude-opus-4-6`
- `gptproto-openai/gpt-5.4`
- `gptproto/glm-5`

## Completion Output

After configuration is complete, present the following to the user:
- Configuration file path (full absolute path)
- Current default model
- Available model list
- Brief instructions on how to switch models

## References

- GPTProto official documentation: https://docs.gptproto.com
- GPTProto OpenClaw configuration guide: https://docs.gptproto.com/docs/get-started/get-started/how-to-use/openclaw
