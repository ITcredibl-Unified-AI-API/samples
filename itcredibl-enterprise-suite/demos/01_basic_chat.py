import asyncio, os
from itcredibl_enterprise.client import ITcrediblClient
from itcredibl_enterprise.console import header, box

MODEL = os.getenv("ITCREDIBL_MODEL", "gpt-4o-mini")

async def main():
    header("Basic Chat")
    client = ITcrediblClient()
    r = await client.chat([
        {"role": "system", "content": "You are concise."},
        {"role": "user", "content": "Say hello in one sentence."}
    ], model=MODEL, temperature=0.2)
    await client.aclose()
    text = r.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
    box(text, title="Assistant")

if __name__ == "__main__":
    asyncio.run(main())