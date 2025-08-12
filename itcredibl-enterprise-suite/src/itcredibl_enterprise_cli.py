import asyncio
import importlib
import os

import typer
from itcredibl_enterprise.console import box

app = typer.Typer(help="ITcredibl Enterprise Demo CLI")


# --- capability gates ---------------------------------------------------------
def _is_function_base() -> bool:
    base = (os.getenv("ITCREDIBL_API_URL") or "").lower()
    return "/functions/" in base or base.endswith("/itcredibl-api")


def supports_embeddings() -> bool:
    # If your function implements embeddings, explicitly enable with env.
    if os.getenv("ITCREDIBL_ENABLE_EMBEDDINGS") == "1":
        return True
    # Otherwise assume only /v1 bases expose /v1/embeddings.
    return not _is_function_base()


def supports_moderation() -> bool:
    if os.getenv("ITCREDIBL_ENABLE_MODERATION") == "1":
        return True
    return not _is_function_base()


def supports_usage() -> bool:
    if os.getenv("ITCREDIBL_ENABLE_USAGE") == "1":
        return True
    return not _is_function_base()


# --- runner -------------------------------------------------------------------
def run(module: str) -> None:
    try:
        m = importlib.import_module(module)
        if not hasattr(m, "main"):
            raise RuntimeError(f"Module {module} has no main()")
        asyncio.run(m.main())
    except Exception as e:
        # Pretty error instead of a long stack trace
        box(f"{type(e).__name__}: {e}", title="Error")
        raise typer.Exit(code=1) from e


# --- commands -----------------------------------------------------------------
@app.command()
def basic() -> None:
    run("demos.01_basic_chat")


@app.command()
def streaming() -> None:
    run("demos.02_streaming")


@app.command()
def routing() -> None:
    run("demos.03_routing_compare")


@app.command()
def fallbacks() -> None:
    run("demos.04_fallbacks")


@app.command()
def tools() -> None:
    run("demos.05_tools")


@app.command()
def embeddings() -> None:
    if not supports_embeddings():
        box(
            (
                "Embeddings not supported by this base URL. "
                "Set ITCREDIBL_API_URL to a /v1-compatible gateway, or set "
                "ITCREDIBL_ENABLE_EMBEDDINGS=1 if your function implements it."
            ),
            title="Unsupported",
        )
        raise typer.Exit(code=0)
    run("demos.06_embeddings")


@app.command()
def moderation() -> None:
    if not supports_moderation():
        box(
            (
                "Moderation not supported by this base URL. "
                "Set a /v1-compatible gateway, or set "
                "ITCREDIBL_ENABLE_MODERATION=1 if your function implements it."
            ),
            title="Unsupported",
        )
        raise typer.Exit(code=0)
    run("demos.07_moderation")


@app.command()
def usage() -> None:
    if not supports_usage():
        box(
            (
                "Gateway /v1/usage not detected for this base URL. "
                "Enable it (or set ITCREDIBL_ENABLE_USAGE=1) or use the "
                "client-side aggregation demo in demos/08_usage.py."
            ),
            title="Unsupported",
        )
        raise typer.Exit(code=0)
    run("demos.08_usage")


@app.command()
def batch() -> None:
    run("demos.09_batch_parallel")


@app.command()
def stress() -> None:
    run("demos.10_stress")


@app.command()
def policy() -> None:
    run("demos.11_policy_enforcement")


@app.command()
def residency() -> None:
    run("demos.12_data_residency")


@app.command()
def chaos() -> None:
    run("demos.13_chaos_failover")


@app.command()
def judge() -> None:
    run("demos.14_judge_quality")


if __name__ == "__main__":
    app()
