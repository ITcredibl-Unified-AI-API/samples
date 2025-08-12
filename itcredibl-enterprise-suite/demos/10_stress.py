import asyncio
import os
import time

from itcredibl_enterprise.client import ITcrediblClient
from itcredibl_enterprise.console import header, kv_table

MODEL = os.getenv("ITCREDIBL_MODEL", "gpt-4o")
TOTAL = int(os.getenv("ITCREDIBL_STRESS_TOTAL", "50"))
CONC = int(os.getenv("ITCREDIBL_STRESS_CONC", "10"))


async def worker(i, sem):
    async with sem:
        c = ITcrediblClient()
        try:
            await c.chat(
                [{"role": "user", "content": f"OK #{i}"}], model=MODEL, temperature=0
            )
        finally:
            await c.aclose()


async def main():
    header("Stress Test")
    sem = asyncio.Semaphore(CONC)
    t0 = time.perf_counter()
    await asyncio.gather(*[worker(i, sem) for i in range(1, TOTAL + 1)])
    ms = int((time.perf_counter() - t0) * 1000)
    kv_table(
        {"total": TOTAL, "concurrency": CONC, "elapsed_ms": ms}, title="Stress Summary"
    )


if __name__ == "__main__":
    asyncio.run(main())
