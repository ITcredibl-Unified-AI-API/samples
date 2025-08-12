import os, asyncio
from itcredibl.itcredibl_client import ITcrediblClient

async def main():
    client = ITcrediblClient()
    print("\nStreaming demo\n")
    async for chunk in client.chat_stream(
        messages=[{"role":"user","content":"Give me a 1 paragraph summary of Kubernetes."}],
        provider=os.getenv("ITCREDIBL_PROVIDER","openai"),
        model=os.getenv("ITCREDIBL_MODEL","gpt-4o"),
        temperature=0.2,
    ):
        delta = chunk.get("choices", [{}])[0].get("delta", {}).get("content")
        if delta:
            print(delta, end="", flush=True)

if __name__ == "__main__":
    asyncio.run(main())