# demos/15_rag_embeddings.py
import asyncio
import math
import os

from itcredibl_enterprise.client import ITCError, ITcrediblClient
from itcredibl_enterprise.console import box, header, kv_table

DOCS = [
    (
        "doc1",
        "Zero trust eliminates implicit trust and enforces continuous verification.",
    ),
    ("doc2", "Microsegmentation limits lateral movement within enterprise networks."),
    (
        "doc3",
        "Least privilege ensures users and services have only required permissions.",
    ),
]

MODEL = os.getenv("ITCREDIBL_MODEL", "gpt-4o")
EMBED_MODEL = os.getenv("ITCREDIBL_EMBED_MODEL", "text-embedding-3-small")


def cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b, strict=False))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb + 1e-12)


async def embed(client: ITcrediblClient, texts: list[str]) -> list[list[float]]:
    r = await client.embeddings(texts, model=EMBED_MODEL)
    out: list[list[float]] = []
    for item in r.get("data", []):
        vec = item.get("embedding")
        if isinstance(vec, list):
            out.append([float(v) for v in vec])
    return out


async def main():
    header("RAG via Embeddings — real endpoint")
    q = "How does zero trust improve enterprise security?"
    client = ITcrediblClient()

    try:
        q_vecs = await embed(client, [q])
        if not q_vecs:
            box(
                "Embeddings endpoint returned no vectors for query.",
                title="Embeddings Error",
            )
            await client.aclose()
            return
        qv = q_vecs[0]

        doc_texts = [text for _, text in DOCS]
        d_vecs = await embed(client, doc_texts)
        if len(d_vecs) != len(DOCS):
            box(
                "Embeddings endpoint returned unexpected vector count.",
                title="Embeddings Error",
            )
            await client.aclose()
            return
    except ITCError as e:
        box(
            f"Embeddings not available at the current base URL: {e}\n"
            "Fix: point ITCREDIBL_API_URL to a /v1 gateway that supports /v1/embeddings.",
            title="Unsupported",
        )
        await client.aclose()
        return

    scored: list[tuple[str, float]] = []
    for (doc_id, _), dv in zip(DOCS, d_vecs, strict=False):
        scored.append((doc_id, cosine(qv, dv)))

    top = sorted(scored, key=lambda x: x[1], reverse=True)[:2]
    top_ids = {doc_id for doc_id, _ in top}
    ctx = "\n\n".join(text for (doc_id, text) in DOCS if doc_id in top_ids)

    resp = await client.chat(
        [
            {
                "role": "system",
                "content": "Use the provided CONTEXT to answer. If unsure, say so.",
            },
            {"role": "user", "content": f"CONTEXT:\n{ctx}\n\nQUESTION: {q}"},
        ],
        model=MODEL,
        temperature=0.2,
    )
    answer = (resp.get("choices", [{}])[0].get("message", {}) or {}).get("content", "")
    kv_table(
        {
            "top_docs": ", ".join(doc_id for doc_id, _ in top),
            "similarity": ", ".join(f"{s:.3f}" for _, s in top),
        },
        title="RAG Selection",
    )
    box(answer.strip(), title="Answer")
    await client.aclose()


if __name__ == "__main__":
    asyncio.run(main())
