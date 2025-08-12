import asyncio, os
from itcredibl_enterprise.client import ITcrediblClient
from itcredibl_enterprise.console import header, kv_table, box
from itcredibl_enterprise.policies import RoutingPolicy
from itcredibl_enterprise.health import ProviderHealth

MODEL = os.getenv("ITCREDIBL_MODEL", "gpt-4o")
FALLBACKS = [p.strip() for p in os.getenv("ITCREDIBL_FALLBACKS", "openai,anthropic,groq").split(",") if p.strip()]

async def main():
    header("Fallbacks & SLA Protection")

    # pick a preferred starting provider based on simple health signal
    chosen = RoutingPolicy(allow=FALLBACKS).pick(FALLBACKS, ProviderHealth())
    order = [chosen] + [p for p in FALLBACKS if p != chosen]

    last_error = None
    for provider in order:
        c = ITcrediblClient()
        try:
            r = await c.chat(
                messages=[{"role":"user","content":"One sentence: why fallbacks protect SLAs."}],
                model=MODEL,
                provider=provider,
                temperature=0.0,
            )
            text = (r.get("choices", [{}])[0].get("message", {}) or {}).get("content") or ""
            usage = r.get("usage", {})
            kv_table({"chosen": provider, "cost": usage.get("cost"), "total_tokens": usage.get("total_tokens")}, title="Winner")
            box(text.strip(), title="Assistant Output")
            await c.aclose()
            return
        except Exception as e:
            last_error = e
            kv_table({"provider": provider, "ok": False, "error": str(e)}, title=f"Failed: {provider}")
        finally:
            await c.aclose()

    box(f"All providers failed. Last error: {last_error}", title="Failure")

if __name__ == "__main__":
    asyncio.run(main())