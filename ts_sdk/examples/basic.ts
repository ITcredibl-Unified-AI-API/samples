import AIGatewaySDK from "../src/client";

async function run() {
  const apiKey = process.env.ITCREDIBL_API_KEY || "replace-me";
  const sdk = new AIGatewaySDK({ apiKey });

  const basic = await sdk.chatCompletion({
    messages: [{ role: "user", content: "Say hi in one sentence." }],
    model: "gpt-4o",
  });
  console.log("Basic:", basic.choices?.[0]?.message?.content);

  await sdk.streamChatCompletion(
    {
      messages: [{ role: "user", content: "Count from 1 to 5 with commas." }],
      model: "gpt-4o",
      stream: true,
    },
    (delta) => {
      const d = delta?.delta?.content;
      if (d) process.stdout.write(d);
    }
  );
  console.log("\\nDone.");
}

run().catch((e) => {
  console.error(e);
  process.exit(1);
});