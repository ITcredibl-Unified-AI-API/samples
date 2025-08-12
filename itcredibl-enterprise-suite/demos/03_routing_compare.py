# Smart routing across providers based on latency, cost, quality, and efficiency
# Run:  python demos/03_routing_compare.py
# Env:  ITCREDIBL_PROVIDERS, ITCREDIBL_MODEL, ITCREDIBL_WEIGHT_LATENCY, ITCREDIBL_WEIGHT_COST,
#       ITCREDIBL_WEIGHT_QUALITY, ITCREDIBL_WEIGHT_THROUGHPUT, ITCREDIBL_CONC (optional)

import asyncio, os, time, json, math
from itcredibl_enterprise.client import ITcrediblClient
from itcredibl_enterprise.console import header, kv_table, box

# Providers to compare (comma-separated)
PROVIDERS = [p.strip() for p in os.getenv("ITCREDIBL_PROVIDERS", "openai,anthropic,groq").split(",") if p.strip()]
MODEL = os.getenv("ITCREDIBL_MODEL", "gpt-4o")

# Weighting (defaults favor quality, then latency, then cost, then throughput)
W_LAT = float(os.getenv("ITCREDIBL_WEIGHT_LATENCY", "0.30"))
W_COST = float(os.getenv("ITCREDIBL_WEIGHT_COST", "0.20"))
W_QUAL = float(os.getenv("ITCREDIBL_WEIGHT_QUALITY", "0.40"))
W_TPS = float(os.getenv("ITCREDIBL_WEIGHT_THROUGHPUT", "0.10"))

# Quality probe: aim for an exact target to allow objective scoring
QUALITY_PROMPT = os.getenv("ITCREDIBL_QUALITY_PROMPT", "Reply with exactly the single word: PARIS")
QUALITY_EXPECTED = os.getenv("ITCREDIBL_QUALITY_EXPECTED", "paris").strip().lower()

CONC = max(1, int(os.getenv("ITCREDIBL_CONC", "2")))


def _extract_text(resp):
    try:
        return (resp.get("choices", [{}])[0].get("message", {}) or {}).get("content") or ""
    except Exception:
        return ""


def _usage(resp):
    u = resp.get("usage", {}) if isinstance(resp, dict) else {}
    return {
        "prompt_tokens": u.get("prompt_tokens"),
        "completion_tokens": u.get("completion_tokens"),
        "total_tokens": u.get("total_tokens"),
        "cost": u.get("cost"),
    }


async def measure_provider(provider: str) -> dict:
    client = ITcrediblClient()

    # === App-like prompt (latency/cost/throughput) ===
    start = time.perf_counter()
    r1 = await client.chat(
        messages=[
            {"role": "system", "content": "You are concise and factual."},
            {"role": "user", "content": "Give two bullets explaining zero trust security."},
        ],
        model=MODEL,
        provider=provider,
        temperature=0.2,
        max_tokens=160,
    )
    t_app = time.perf_counter() - start
    u1 = _usage(r1)
    text1 = _extract_text(r1)

    # Throughput: completion tokens per second (fallback to characters/sec)
    comp_toks = u1.get("completion_tokens") or 0
    tps = (comp_toks / t_app) if t_app > 0 else 0.0
    if not comp_toks:
        tps = (len(text1) / max(t_app, 1e-6)) / 4.0  # rough char->token

    # === Quality probe ===
    start = time.perf_counter()
    r2 = await client.chat(
        messages=[{"role": "user", "content": QUALITY_PROMPT}],
        model=MODEL,
        provider=provider,
        temperature=0.0,
        max_tokens=8,
    )
    t_quality = time.perf_counter() - start
    text2 = _extract_text(r2).strip().lower()

    # strict correctness (exact word), plus a soft check if answer contains it
    if text2 == QUALITY_EXPECTED:
        quality_score = 1.0
    elif QUALITY_EXPECTED in text2:
        # small penalty if extra words are included
        extra_penalty = min(0.3, max(0.0, (len(text2.split()) - 1) * 0.1))
        quality_score = max(0.0, 0.8 - extra_penalty)
    else:
        quality_score = 0.0

    await client.aclose()

    return {
        "provider": provider,
        "latency_ms": int(t_app * 1000),
        "quality_latency_ms": int(t_quality * 1000),
        "cost": u1.get("cost"),
        "prompt_tokens": u1.get("prompt_tokens"),
        "completion_tokens": u1.get("completion_tokens"),
        "total_tokens": u1.get("total_tokens"),
        "tps": round(tps, 3),
        "quality_text": text2,
        "quality_score": round(quality_score, 3),
    }


def _normalize_inverse(values):
    # Lower is better (latency, cost) => convert to 0..1 where 1 is best
    # If any None, treat them as median of known values
    nums = [v for v in values if isinstance(v, (int, float))]
    if not nums:
        return [0.5 for _ in values]
    mn = min(nums); mx = max(nums)
    out = []
    for v in values:
        if not isinstance(v, (int, float)):
            v = (mn + mx) / 2
        if v <= 0:
            out.append(1.0 if v == mn else 0.0)
        elif mn == mx:
            out.append(1.0)
        else:
            out.append(float(mn) / float(v))
    return out


def _normalize_direct(values):
    # Higher is better (throughput, quality)
    nums = [v for v in values if isinstance(v, (int, float))]
    if not nums:
        return [0.5 for _ in values]
    mx = max(nums)
    return [float(v) / float(mx) if isinstance(v, (int, float)) and mx > 0 else 0.0 for v in values]


async def main():
    header("Smart Routing: latency • cost • quality • efficiency")

    # Measure in limited parallel to keep things snappy but not overload
    sem = asyncio.Semaphore(CONC)
    async def guarded(p):
        async with sem:
            try:
                return await measure_provider(p)
            except Exception as e:
                return {"provider": p, "error": str(e)}

    results = await asyncio.gather(*[guarded(p) for p in PROVIDERS])

    # Show raw metrics
    for row in results:
        kv_table(row, title=row.get("provider", "result"))

    # Filter out errors
    ok = [r for r in results if not r.get("error")]
    if not ok:
        box("All providers failed. Check API URL, model name, or key.", title="Routing Result")
        return

    # Normalize & score
    lat_scores = _normalize_inverse([r["latency_ms"] for r in ok])
    cost_scores = _normalize_inverse([r.get("cost", math.nan) for r in ok])
    qual_scores = _normalize_direct([r["quality_score"] for r in ok])
    tps_scores = _normalize_direct([r["tps"] for r in ok])

    overall = []
    for i, r in enumerate(ok):
        score = (
            W_LAT * lat_scores[i] +
            W_COST * cost_scores[i] +
            W_QUAL * qual_scores[i] +
            W_TPS * tps_scores[i]
        )
        overall.append({"provider": r["provider"], "score": round(score, 4)})

    # Pick best
    best = max(overall, key=lambda x: x["score"]) if overall else None
    if best:
        box(json.dumps({
            "winner": best["provider"],
            "score": best["score"],
            "weights": {"latency": W_LAT, "cost": W_COST, "quality": W_QUAL, "throughput": W_TPS},
        }, indent=2), title="Smart Router Decision")

if __name__ == "__main__":
    asyncio.run(main())