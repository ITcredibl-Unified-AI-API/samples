# ITcredibl Enterprise Demo Suite (Python)

## 🚀 Transform Your AI Infrastructure
ITcredibl is the unified AI gateway for modern enterprises and startups. Connect to 7+ leading AI providers (OpenAI, Anthropic, Google, and more) through a single API, optimize costs, ensure compliance, and scale with confidence.

## 🌟 What Makes ITcredibl Different?
- **Multi-Provider Intelligence:** Instantly switch between top AI providers—no vendor lock-in.
- **Cost Optimization:** Save 40-60% on AI spend with smart routing and automatic failover.
- **Enterprise Security:** SOC2, HIPAA, GDPR compliance, audit trails, and robust data protection.
- **Team Collaboration:** Role-based access, team workspaces, and shared model configs.
- **Real-time Analytics:** Monitor usage, costs, and performance with predictive analytics and 99.99% uptime.
- **Enterprise Scale:** Scale from thousands to millions of requests with enterprise-grade infrastructure.
- **Developer Experience:** Comprehensive docs, code examples, SDKs, and integration guides for rapid onboarding.

## 🛠️ What’s Included in This Suite?
- Chat with **true streaming** (SSE)
- **Policy-based smart routing** (allow/deny, health score, residency hint)
- **Automatic fallbacks** to meet SLAs
- **Tool/function calling**
- **Embeddings** and **Moderation**
- **Usage/FinOps analytics**
- Batch/parallel + stress tests
- Cost caps & residency flags (demo)
- Extensible **metrics hook** for Datadog/Splunk

## 🏗️ How the Demos Help You
Each demo script showcases a real-world scenario:
- Chat and streaming: See multi-provider chat in action
- Fallbacks: Experience reliability and SLA guarantees
- Policy enforcement: Enforce compliance and residency
- Tool calling: Integrate external functions and APIs
- Embeddings & moderation: Advanced AI features for your data
- Usage analytics: Track and optimize your AI spend

## ⚡ Quickstart (Windows PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
# set your key
[Environment]::SetEnvironmentVariable('ITCREDIBL_API_KEY','your_key','Process')
# run a quick demo
python demos\01_basic_chat.py


# create venv and install
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -e .

# env
Copy-Item .env.example .env
$env:ITCREDIBL_API_KEY="your_key_here"
$env:ITCREDIBL_API_URL="https://api.itcredibl.com/functions/v1/itcredibl-api"

# Run demo scripts to showcase platform features
python demos\01_basic_chat.py
python demos\02_streaming.py
python demos\04_fallbacks.py
python demos\11_policy_enforcement.py

# Run via CLI wrapper for feature demonstrations
python -m itcredibl_enterprise_cli basic
python -m itcredibl_enterprise_cli streaming
python -m itcredibl_enterprise_cli routing
python -m itcredibl_enterprise_cli fallbacks
python -m itcredibl_enterprise_cli tools
python -m itcredibl_enterprise_cli embeddings
python -m itcredibl_enterprise_cli moderation
python -m itcredibl_enterprise_cli usage
python -m itcredibl_enterprise_cli batch
python -m itcredibl_enterprise_cli stress
python -m itcredibl_enterprise_cli policy
python -m itcredibl_enterprise_cli residency
```

## 📚 Learn More
- [ai-insight.itcredibl.com](https://ai-insight.itcredibl.com) — Platform features, docs, and competitive analysis
- [itcredibl.com](https://itcredibl.com) — Company and support

## 💬 Questions?
Open an issue or contact us for support and partnership opportunities.