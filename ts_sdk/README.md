# @itcredibl/sdk (TypeScript)

---

## 🚀 Transform Your AI Apps with ITcredibl
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

## Install
```bash
npm install @itcredibl/sdk
```

## Quick start
```ts
import AIGatewaySDK from "@itcredibl/sdk";

const sdk = new AIGatewaySDK({ apiKey: process.env.ITCREDIBL_API_KEY! });

const res = await sdk.chatCompletion({
  model: "gpt-4o",
  messages: [{ role: "user", content: "Hello" }]
});

console.log(res.choices[0].message.content);
```

## Run the example
```bash
npm run example
```