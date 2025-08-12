# ITcredibl Enterprise Python SDK Demo

---

## 🚀 Transform Your AI Projects with ITcredibl
ITcredibl is the unified AI gateway for modern enterprises and startups. Connect to 7+ leading AI providers (OpenAI, Anthropic, Google, and more) through a single API, optimize costs, ensure compliance, and scale with confidence.

### Why Choose ITcredibl?
- **Multi-Provider Intelligence:** Instantly switch between top AI providers—no vendor lock-in.
- **Cost Optimization:** Save 40-60% on AI spend with smart routing and automatic failover.
- **Enterprise Security:** SOC2, HIPAA, GDPR compliance, audit trails, and robust data protection.
- **Team Collaboration:** Role-based access, team workspaces, and shared model configs.
- **Real-time Analytics:** Monitor usage, costs, and performance with predictive analytics and 99.99% uptime.
- **Enterprise Scale:** Scale from thousands to millions of requests with enterprise-grade infrastructure.
- **Developer Experience:** Comprehensive docs, code examples, SDKs, and integration guides for rapid onboarding.

---

## Quick start
```bash
python -m venv .venv && . .venv/Scripts/activate  # Windows PowerShell
pip install -r requirements.txt
setx ITCREDIBL_API_KEY "your_key"
python -m examples.cli_demo
python -m examples.stream_demo
ITCREDIBL_STRESS_N=100 python -m examples.stress_test
```