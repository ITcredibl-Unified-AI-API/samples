import asyncio, os
from itcredibl_enterprise.client import ITcrediblClient
from itcredibl_enterprise.console import header, kv_table

MODEL = os.getenv("ITCREDIBL_MODEL", "gpt-4o")

async def one(i):
    c = ITcrediblClient()
    try:
        r = await c.chat([{"role":"user","content": f"Say hi #{i}"}], model=MODEL, temperature=0)
        return (r.get("choices", [{}])[0].get("message", {}) or {}).get("content", "").strip()
    finally:
        await c.aclose()

async def main():
    header("Batch & Parallel")
    outs = await asyncio.gather(*[one(i) for i in range(1, 6)])
    kv_table({"responses": len(outs)}, title="Batch Summary")

if __name__ == "__main__":
    asyncio.run(main())