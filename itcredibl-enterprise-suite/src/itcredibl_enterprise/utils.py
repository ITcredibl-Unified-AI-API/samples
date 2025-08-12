import os


def env_str(name: str, default: str = "") -> str:
    return os.getenv(name, default)


def env_list(name: str, default: str = ""):
    raw = os.getenv(name, default)
    return [s.strip() for s in raw.split(",") if s.strip()]
