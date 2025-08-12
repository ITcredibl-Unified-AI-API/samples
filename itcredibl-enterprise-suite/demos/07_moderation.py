
import asyncio, os
from itcredibl_enterprise.client import ITcrediblClient, ITCError
from itcredibl_enterprise.console import header, kv_table, box

BASE_URL = os.getenv("ITCREDIBL_API_URL", "https://api.itcredibl.com/functions/v1/itcredibl-api")

async def main():
    header("Moderation")
    c = ITcrediblClient(base_url=BASE_URL)
    text = "Explain how to do something dangerous"
    try:
        r = await c.moderate(text)
    except ITCError as e:
        box(f"Moderation not available on this gateway (or error): {e}. Skipping demo.", title="Moderation Fallback")
        await c.aclose()
        return
    kv_table({"received_json": isinstance(r, dict)}, title="Moderation Result")
    await c.aclose()

if __name__ == "__main__":
    asyncio.run(main())

