# ITcredibl Enterprise SDK and Demo

## 🚀 What is ITcredibl?
ITcredibl is an enterprise AI gateway that lets you connect to 7+ leading AI providers (OpenAI, Anthropic, Google, and more) through a single, unified API. It helps you:
- Save 40-60% on AI costs with smart routing and automatic failover.
- Ensure enterprise-grade security and compliance (SOC2, HIPAA, GDPR).
- Scale from startup to millions of requests with 99.99% uptime.
- Collaborate with your team using role-based access and shared configs.
- Monitor and optimize usage, cost, and performance with real-time analytics.

## 🌟 Why ITcredibl?
Traditional AI integration is complex, expensive, and risky:
- Vendor lock-in to a single provider.
- Manual cost management and failover.
- Security and compliance headaches.
- Limited visibility and control.

**ITcredibl solves these problems:**
- One API, many providers: Switch instantly, avoid lock-in.
- Smart routing: Always use the best model for your needs and budget.
- Enterprise security: Compliance and audit trails built-in.
- Developer-first: SDKs, docs, and code examples for rapid onboarding.

## 🛠️ Example Use Cases
- Multi-provider chatbots with automatic fallback.
- Cost-optimized document analysis and summarization.
- Secure, compliant AI for healthcare and finance.
- Real-time analytics for AI usage and spend.

## 🏗️ Architecture Overview
```
[Your App] → [ITcredibl API Gateway] → [OpenAI | Anthropic | Google | ...]
```
- ITcredibl handles routing, failover, security, and analytics.

## 📦 Repo Structure
- `python_sdk`: Streaming, retries, parallel load, advanced routing demos.
- `ts_sdk`: TypeScript SDK for enterprise integration and local testing.

## ⚡ Quick Start
### Prerequisites
- Set `ITCREDIBL_API_KEY` in your shell
- Optional: `ITCREDIBL_API_URL`

### Python
```powershell
cd python_sdk
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:ITCREDIBL_API_KEY="your_key"
python -m examples.cli_demo
python -m examples.stream_demo
ITCREDIBL_STRESS_N=100 python -m examples.stress_test
```

### TypeScript
```powershell
cd ts_sdk
npm install
npm run example
```

## 🤖 CI and Automation
- Makefile for setup, build, test, demo
- GitHub Actions for both SDKs

## 📚 Learn More
- [ai-insight.itcredibl.com](https://ai-insight.itcredibl.com) — Platform features, docs, and competitive analysis
- Explore the demo suite for hands-on examples

## 💬 Questions?
Open an issue or contact us at [itcredibl.com](https://itcredibl.com) for support and partnership opportunities.


