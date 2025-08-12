# demos/02_streaming.py
import asyncio
import os
import sys

from itcredibl_enterprise.client import ITcrediblClient
from itcredibl_enterprise.console import header

# Model + endpoint (set API URL to your Supabase Function if you're using that)
MODEL = os.getenv("ITCREDIBL_MODEL", "gpt-4o")
BASE_URL = os.getenv(
    "ITCREDIBL_API_URL",
    "https://api.itcredibl.com/functions/v1/itcredibl-api",  # function-style default
)


async def main():
    header("Streaming Demo")
    client = ITcrediblClient(base_url=BASE_URL)

    printed_any = False

    # Try streaming first
    try:
        async for chunk in client.chat_stream(
            messages=[
                {"role": "user", "content": "write a poem about itcredibl ai api."}
            ],
            model=MODEL,
            temperature=0.0,
        ):
            if chunk:
                sys.stdout.write(chunk)
                sys.stdout.flush()
                printed_any = True
    finally:
        if not printed_any:
            # Fallback: some gateways return a single JSON instead of SSE
            resp = await client.chat(
                messages=[
                    {
                        "role": "user",
                        "content": "write a poem about itcredibl ai api with commas.",
                    }
                ],
                model=MODEL,
                temperature=0.0,
                stream=False,
            )
            text = (resp.get("choices", [{}])[0].get("message", {}) or {}).get(
                "content"
            ) or ""
            if text:
                print(text)

        await client.aclose()
        if printed_any:
            print()  # newline after streaming


if __name__ == "__main__":
    asyncio.run(main())
