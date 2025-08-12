import asyncio
import os

from itcredibl_enterprise.client import ITCError, ITcrediblClient
from itcredibl_enterprise.console import box, header, kv_table

MODEL = os.getenv("ITCREDIBL_MODEL", "gpt-4o")
BASE_URL = os.getenv(
    "ITCREDIBL_API_URL", "https://api.itcredibl.com/functions/v1/itcredibl-api"
)
N = int(os.getenv("ITCREDIBL_USAGE_SAMPLES", "3"))


async def sample_call(i, client):
    r = await client.chat(
        messages=[{"role": "user", "content": f"Return just the number {i}"}],
        model=MODEL,
        temperature=0.0,
        max_tokens=8,
    )
    return r.get("usage", {})


async def main():
    header("Usage & Analytics")
    c = ITcrediblClient(base_url=BASE_URL)

    # Try gateway-native usage endpoint first
    try:
        u = await c.usage()
        txt = str(u)
        box(
            (txt[:1200] + "…") if len(txt) > 1200 else txt,
            title="Gateway Usage Response",
        )
        await c.aclose()
        return
    except ITCError:
        pass

    # Client-side aggregation fallback
    usages = []
    for i in range(1, N + 1):
        try:
            u = await sample_call(i, c)
            usages.append(u)
        except Exception:
            usages.append({})
    await c.aclose()

    total_prompt = sum(int(u.get("prompt_tokens") or 0) for u in usages)
    total_completion = sum(int(u.get("completion_tokens") or 0) for u in usages)
    total_tokens = sum(
        int(
            u.get("total_tokens")
            or ((u.get("prompt_tokens") or 0) + (u.get("completion_tokens") or 0))
        )
        for u in usages
    )
    total_cost = sum(float(u.get("cost") or 0.0) for u in usages)

    kv_table(
        {
            "samples": len(usages),
            "prompt_tokens": total_prompt,
            "completion_tokens": total_completion,
            "total_tokens": total_tokens,
            "est_cost_usd": round(total_cost, 6),
        },
        title="Aggregated Usage (client-side)",
    )


if __name__ == "__main__":
    asyncio.run(main())
