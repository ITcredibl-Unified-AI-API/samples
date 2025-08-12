import asyncio, os, time, statistics
from itcredibl.itcredibl_client import ITcrediblClient

N = int(os.getenv("ITCREDIBL_STRESS_N", "50"))

async def worker(i: int, client: ITcrediblClient):
    start = time.perf_counter()
    r = await client.chat_async(
        messages=[{"role":"user","content": f"Return the number {i}"}],
        provider=os.getenv("ITCREDIBL_PROVIDER", "openai"),
        model=os.getenv("ITCREDIBL_MODEL", "gpt-4o-mini"),
        temperature=0.0,
    )
    latency = time.perf_counter() - start
    return latency, r.get("choices", [{}])[0].get("message", {}).get("content","")

async def main():
    client = ITcrediblClient()
    tasks = [worker(i, client) for i in range(N)]
    results = await asyncio.gather(*tasks)
    lats = [lat for lat,_ in results]
    print(f"Completed {N} calls")
    print(f"p50 {statistics.median(lats):.3f}s, max {max(lats):.3f}s, avg {statistics.mean(lats):.3f}s")

if __name__ == "__main__":
    asyncio.run(main())