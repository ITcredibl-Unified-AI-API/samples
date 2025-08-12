from __future__ import annotations

from typing import Any

PROMPT = (
    "You are a strict grader. Score the ASSISTANT answer on a 0..1 scale given the USER task. "
    "Return JSON with keys: score (0..1), rationale (short)."
)


def build_messages(task: str, answer: str) -> list[dict[str, Any]]:
    return [
        {"role": "system", "content": PROMPT},
        {"role": "user", "content": f"TASK: {task}\nASSISTANT: {answer}"},
    ]
