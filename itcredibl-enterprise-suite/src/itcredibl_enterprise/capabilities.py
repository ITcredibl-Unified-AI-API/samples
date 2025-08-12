import os


def base_url() -> str:
    return (os.getenv("ITCREDIBL_API_URL") or "https://api.itcredibl.com").rstrip("/")


def is_function_base() -> bool:
    url = base_url()
    return "/functions/" in url or url.endswith("/itcredibl-api")


# Hard rule: we never mock. We only run demos that the base most likely supports.
# You can override with explicit env switches if your function DOES implement these.
def supports_embeddings() -> bool:
    if os.getenv("ITCREDIBL_ENABLE_EMBEDDINGS") == "1":
        return True
    return not is_function_base()


def supports_moderation() -> bool:
    if os.getenv("ITCREDIBL_ENABLE_MODERATION") == "1":
        return True
    return not is_function_base()


def supports_usage() -> bool:
    # Usage is often gateway-specific; allow an override if your gateway exposes /v1/usage
    if os.getenv("ITCREDIBL_ENABLE_USAGE") == "1":
        return True
    return not is_function_base()
