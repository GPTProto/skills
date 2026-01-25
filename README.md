# GPTProto Skills

A collection of Claude Code skills for web automation and artifact creation.

> Open-sourced from [gptproto.com](https://gptproto.com)

## Skills

| Skill | Description |
|-------|-------------|
| [url2pdf](./skills/url2pdf) | Convert web pages to PDF files (single or batch) |
| [web-artifacts-builder](./skills/web-artifacts-builder) | Build complex React + shadcn/ui artifacts for claude.ai |
| [webapp-testing](./skills/webapp-testing) | Test local web applications using Playwright |

## Installation

To use these skills with Claude Code, copy the skill folders to your Claude Code skills directory or reference them in your configuration.

### Prerequisites

- Python 3.8+
- Node.js 18+
- Playwright (`pip install playwright && playwright install chromium`)

## Quick Start

### url2pdf

Convert a single URL:
```bash
python skills/url2pdf/url2pdf/scripts/url_to_pdf.py --url "https://example.com" --output "example.pdf"
```

Batch convert from file:
```bash
python skills/url2pdf/url2pdf/scripts/url_to_pdf.py --file urls.txt --output-dir ./pdfs
```

### web-artifacts-builder

Initialize and build a React artifact:
```bash
bash skills/web-artifacts-builder/scripts/init-artifact.sh my-app
cd my-app
# ... develop your app ...
bash ../skills/web-artifacts-builder/scripts/bundle-artifact.sh
```

Stack: React 18 + TypeScript + Vite + Tailwind CSS + 40+ shadcn/ui components

### webapp-testing

Test a local web app with Playwright:
```bash
python skills/webapp-testing/scripts/with_server.py \
  --server "npm run dev" --port 5173 \
  -- python your_test.py
```

## License

- `web-artifacts-builder`: See [LICENSE.txt](./skills/web-artifacts-builder/LICENSE.txt)
- `webapp-testing`: See [LICENSE.txt](./skills/webapp-testing/LICENSE.txt)

## Links

- Website: [gptproto.com](https://gptproto.com)
- Issues: [GitHub Issues](https://github.com/GPTProto/skills/issues)
