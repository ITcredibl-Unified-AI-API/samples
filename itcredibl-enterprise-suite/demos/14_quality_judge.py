import asyncio
import json
import os

from itcredibl_enterprise.client import ITcrediblClient
from itcredibl_enterprise.console import box, header, kv_table
from itcredibl_enterprise.judge import build_messages

TASK = "List 3 benefits of zero trust in enterprises."
MODEL = os.getenv("ITCREDIBL_MODEL", "gpt-4o")
JUDGE_MODEL = os.getenv("ITCREDIBL_JUDGE_MODEL", MODEL)
PROVIDERS = [
    p.strip()
    for p in os.getenv("ITCREDIBL_PROVIDERS", "openai,anthropic").split(",")
    if p.strip()
]


async def ask(c, provider):
    r = await c.chat(
        [{"role": "user", "content": TASK}],
        model=MODEL,
        provider=provider,
        temperature=0.2,
    )
    return (r.get("choices", [{}])[0].get("message", {}) or {}).get("content", "")


async def judge(c, answer: str):
    r = await c.chat(build_messages(TASK, answer), model=JUDGE_MODEL, temperature=0.0)
    txt = (r.get("choices", [{}])[0].get("message", {}) or {}).get("content", "")
    try:
        obj = json.loads(txt)
        return float(obj.get("score", 0.0)), obj.get("rationale", "")
    except Exception:
        return (1.0 if "-" in answer else 0.6), "heuristic"


async def main():
    header("Judge Model Quality Scoring")
    c = ITcrediblClient()
    results = []
    for p in PROVIDERS:
        ans = await ask(c, p)
        score, why = await judge(c, ans)
        results.append({"provider": p, "score": round(score, 3), "why": why})
    for r in results:
        kv_table(r, title=r["provider"])
    best = max(results, key=lambda x: x["score"])
    box(
        json.dumps({"winner": best["provider"], "score": best["score"]}, indent=2),
        title="Judge Decision",
    )
    await c.aclose()


if __name__ == "__main__":
    asyncio.run(main())
