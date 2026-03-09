---
name: openclaw-installer
description: "OpenClaw 一键安装配置助手。当用户提到安装 OpenClaw、配置 OpenClaw、设置 OpenClaw、openclaw install、openclaw setup，或者想要搭建 AI 编程助手/AI 代码编辑器环境时触发此技能。自动完成环境检查、安装、配置和验证全流程。用户是技术小白，只需提供 API Key 即可。"
---

# OpenClaw 安装助手

自动完成 OpenClaw 的安装和配置，用户只需提供 API Key。

## 流程

按以下步骤顺序执行，每步完成后再进行下一步。全程使用中文与用户交流。

### 第 1 步：获取 API Key

- 检查环境变量 `GPTPROTO_API_KEY` 是否已存在
- 若已有，直接使用；若没有，询问用户提供
- API Key 格式示例：`sk-xxxxxxxx`

### 第 2 步：环境检查

检查 Node.js 版本：

```bash
node --version
```

- 要求 Node.js >= 22，若版本不足或未安装，自动安装/升级：
  - macOS: `brew install node@22` 或使用 nvm
  - Linux: 使用 nvm 或 NodeSource 安装

检查 OpenClaw 是否已安装：

```bash
which openclaw 2>/dev/null || npm list -g openclaw 2>/dev/null
```

- 若已安装，询问用户是否卸载重装
- **卸载前必须先 `cd ~`**，否则会报错 `ENOENT: uv_cwd`：

```bash
cd ~ && npm uninstall -g openclaw
```

### 第 3 步：安装 OpenClaw

根据平台选择安装方式：

**macOS/Linux（推荐）：**
```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

**Windows：**
```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

**备选方案（npm，使用国内镜像）：**
```bash
npm install -g openclaw@latest --registry=https://registry.npmmirror.com
```

安装后验证：
```bash
openclaw --version
```

### 第 4 步：配置

跳过 OpenClaw 自带的配置向导，直接手动写入配置文件。

1. 读取 `references/config-template.json` 获取配置模板
2. 将模板中所有 `<GPTPROTO_API_KEY>` 替换为用户实际的 API Key
3. 确保目录存在并写入配置：

```bash
mkdir -p ~/.openclaw
```

将替换后的 JSON 写入 `~/.openclaw/openclaw.json`。

配置要点：
- GPT Proto 兼容模式，Base URL: `https://gptproto.com/v1`
- 包含两个 provider：`gptproto`（Anthropic 协议）和 `gptproto-openai`（OpenAI 协议）
- 默认主模型：`gptproto-openai/gpt-5.4`
- 可用模型：Claude Opus 4.6、GLM-5、GPT-4o、GPT-5.4

### 第 5 步：安全加固

修复配置文件和目录权限，避免安全审计告警：

```bash
chmod 600 ~/.openclaw/openclaw.json
chmod 700 ~/.openclaw
```

### 第 6 步：启动网关

**必须先启动网关，Dashboard 才能访问。** 使用 `--force` 确保端口不被占用：

```bash
openclaw gateway run --force 2>&1 &
sleep 5
openclaw health
```

- 等待看到 `[gateway] listening on ws://127.0.0.1:18789` 表示启动成功
- 网关启动后会自动生成 auth token 并写入配置文件

### 第 7 步：打开 Dashboard

```bash
openclaw dashboard
```

- 该命令会输出带 token 的完整 URL 并自动在浏览器中打开
- URL 格式为：`http://127.0.0.1:18789/#token=<自动生成的TOKEN>`

## 完成输出

安装完成后，向用户展示：
- 安装结果（成功/失败）
- 配置文件路径：`~/.openclaw/openclaw.json`
- Dashboard 地址（`openclaw dashboard` 输出的完整带 token 的 URL）
- 可用模型列表

## 参考

- OpenClaw 官方文档：https://docs.openclaw.ai/start/getting-started
- OpenClaw GitHub：https://github.com/openclaw/openclaw
