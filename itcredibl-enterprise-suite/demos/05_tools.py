import asyncio, os, json
from itcredibl_enterprise.client import ITcrediblClient
from itcredibl_enterprise.console import header, box

MODEL = os.getenv("ITCREDIBL_MODEL", "gpt-4o-mini")

TOOLS = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current weather by city",
        "parameters": {"type": "object", "properties": {"city": {"type": "string"}}, "required": ["city"]}
    }
}]

async def main():
    header("Tool Calling")
    c = ITcrediblClient()
    r = await c.tool_call([
        {"role":"user","content":"What is the weather in Boston?"}
    ], model=MODEL, tools=TOOLS)
    box(json.dumps(r.get("choices", [{}])[0], indent=2), title="Model Response")
    await c.aclose()

if __name__ == "__main__":
    asyncio.run(main())