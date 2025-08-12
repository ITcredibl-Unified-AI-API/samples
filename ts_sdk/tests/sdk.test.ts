import { AIGatewaySDK } from "../src/client";

test("constructs SDK", () => {
  const sdk = new AIGatewaySDK({ apiKey: "test" });
  expect(sdk).toBeDefined();
});