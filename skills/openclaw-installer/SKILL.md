---
name: openclaw-installer
description: "OpenClaw one-click installation and configuration assistant. Triggered when the user mentions installing OpenClaw, configuring OpenClaw, setting up OpenClaw, openclaw install, openclaw setup, or wants to set up an AI programming assistant / AI code editor environment. Automatically completes the full workflow of environment checks, installation, configuration, and verification. The user is a non-technical beginner who only needs to provide an API Key."
---

# OpenClaw Installation Assistant

Automatically complete the installation and configuration of OpenClaw. The user only needs to provide an API Key.

## Workflow

Execute the following steps in order. Proceed to the next step only after the current one is complete. Communicate with the user in English throughout.

### Step 1: Obtain API Key

- Check whether the environment variable `GPTPROTO_API_KEY` already exists
- If it exists, use it directly; if not, ask the user to provide it
- API Key format example: `sk-xxxxxxxx`

### Step 2: Environment Check

Check the Node.js version:

```bash
node --version
```

- Requires Node.js >= 22. If the version is insufficient or not installed, automatically install/upgrade:
  - macOS: `brew install node@22` or use nvm
  - Linux: Use nvm or NodeSource to install

Check whether OpenClaw is already installed:

```bash
which openclaw 2>/dev/null || npm list -g openclaw 2>/dev/null
```

- If already installed, ask the user whether to uninstall and reinstall
- **Must `cd ~` before uninstalling**, otherwise it will throw `ENOENT: uv_cwd` error:

```bash
cd ~ && npm uninstall -g openclaw
```

### Step 3: Install OpenClaw

Choose the installation method based on the platform:

**macOS/Linux (Recommended):**
```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

**Windows:**
```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

**Alternative (npm, using China mirror):**
```bash
npm install -g openclaw@latest --registry=https://registry.npmmirror.com
```

Verify after installation:
```bash
openclaw --version
```

### Step 4: Configuration

Skip OpenClaw's built-in configuration wizard and write the config file manually.

1. Read `references/config-template.json` to get the configuration template
2. Replace all `<GPTPROTO_API_KEY>` in the template with the user's actual API Key
3. Ensure the directory exists and write the configuration:

```bash
mkdir -p ~/.openclaw
```

Write the processed JSON to `~/.openclaw/openclaw.json`.

Configuration details:
- GPT Proto compatibility mode, Base URL: `https://gptproto.com/v1`
- Includes two providers: `gptproto` (Anthropic protocol) and `gptproto-openai` (OpenAI protocol)
- Default primary model: `gptproto-openai/gpt-5.4`
- Available models: Claude Opus 4.6, GLM-5, GPT-4o, GPT-5.4

### Step 5: Security Hardening

Fix configuration file and directory permissions to avoid security audit warnings:

```bash
chmod 600 ~/.openclaw/openclaw.json
chmod 700 ~/.openclaw
```

### Step 6: Start the Gateway

**The gateway must be started first before the Dashboard can be accessed.** Use `--force` to ensure the port is not occupied:

```bash
openclaw gateway run --force 2>&1 &
sleep 5
openclaw health
```

- Wait until you see `[gateway] listening on ws://127.0.0.1:18789` to confirm a successful start
- After the gateway starts, it will automatically generate an auth token and write it to the config file

### Step 7: Open the Dashboard

```bash
openclaw dashboard
```

- This command outputs the full URL with the token and automatically opens it in the browser
- URL format: `http://127.0.0.1:18789/#token=<AUTO_GENERATED_TOKEN>`

## Completion Output

After installation is complete, present the following to the user:
- Installation result (success/failure)
- Config file path: `~/.openclaw/openclaw.json`
- Dashboard URL (the full token-bearing URL output by `openclaw dashboard`)
- List of available models

## References

- OpenClaw official documentation: https://docs.openclaw.ai/start/getting-started
- OpenClaw GitHub: https://github.com/openclaw/openclaw
