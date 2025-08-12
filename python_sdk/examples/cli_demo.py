import os
from itcredibl.itcredibl_client import ITcrediblClient
from rich import print

def run():
    client = ITcrediblClient()
    tasks = [
        {"name":"Summary", "provider":os.getenv("ITCREDIBL_PROVIDER","openai"), "model":os.getenv("ITCREDIBL_MODEL","gpt-4o"), "q":"Summarize Q3 revenue performance in 3 bullets."},
        {"name":"Translate", "provider":"openai", "model":"gpt-4o", "q":"Translate to French: AI is changing the world."},
        {"name":"Brainstorm", "provider":"anthropic", "model":"claude-3-5-sonnet", "q":"Five ideas to reduce cloud costs for LLM workloads."},
    ]
    for t in tasks:
        print(f"\n[b]{t['name']}[/b]")
        resp = client.chat(
            messages=[{"role":"user", "content": t["q"]}],
            provider=t["provider"],
            model=t["model"],
            max_tokens=200,
        )
        content = resp.get("choices", [{}])[0].get("message", {}).get("content") or ""
        print(content)

if __name__ == "__main__":
    run()