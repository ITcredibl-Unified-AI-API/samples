# @itcredibl/sdk (TypeScript)

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