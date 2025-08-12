
import asyncio, os
from itcredibl_enterprise.client import ITcrediblClient, ITCError
from itcredibl_enterprise.console import header, kv_table, box

MODEL = os.getenv("ITCREDIBL_EMBED_MODEL", "text-embedding-3-small")
BASE_URL = os.getenv("ITCREDIBL_API_URL", "https://api.itcredibl.com/functions/v1/itcredibl-api")

async def main():
    header("Embeddings")
    c = ITcrediblClient(base_url=BASE_URL)
    data = ["hello world", "itcredibl gateway"]
    try:
        r = await c.embeddings(data, model=MODEL)
    except ITCError as e:
        box(f"Embeddings not available on this gateway (or error): {e}. Skipping demo.", title="Embeddings Fallback")
        await c.aclose()
        return
    vecs = r.get("data", [])
    dim = 0
    if vecs:
        first = vecs[0].get("embedding") or []
        dim = len(first) if isinstance(first, list) else 0
    kv_table({"inputs": len(data), "vectors": len(vecs), "dimension": dim}, title="Embedding Summary")
    await c.aclose()

if __name__ == "__main__":
    asyncio.run(main())