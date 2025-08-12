import asyncio, typer, importlib

app = typer.Typer(help="ITcredibl Enterprise Demo CLI")

def run(module: str):
    m = importlib.import_module(module)
    asyncio.run(m.main())

@app.command()
def basic(): run("demos.01_basic_chat")

@app.command()
def streaming(): run("demos.02_streaming")

@app.command()
def routing(): run("demos.03_routing_compare")

@app.command()
def fallbacks(): run("demos.04_fallbacks")

@app.command()
def tools(): run("demos.05_tools")

@app.command()
def embeddings(): run("demos.06_embeddings")

@app.command()
def moderation(): run("demos.07_moderation")

@app.command()
def usage(): run("demos.08_usage")

@app.command()
def batch(): run("demos.09_batch_parallel")

@app.command()
def stress(): run("demos.10_stress")

@app.command()
def policy(): run("demos.11_policy_enforcement")

@app.command()
def residency(): run("demos.12_data_residency")

if __name__ == "__main__":
    app()