from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

from langchain_core.documents import Document

from .utils import safe_import


@dataclass
class RerankOptions:
    enabled: bool
    model: str
    top_n: int
    threshold: float | None = None


DEFAULT_RERANK_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"


def rerank_documents(question: str, docs: List[Document], options: RerankOptions) -> List[Tuple[Document, float]]:
    if not options.enabled:
        return [(doc, 0.0) for doc in docs]

    st_mod = safe_import("sentence_transformers", "sentence-transformers")
    CrossEncoder = st_mod.CrossEncoder
    model = CrossEncoder(options.model)

    pairs = [(question, doc.page_content) for doc in docs]
    scores = model.predict(pairs)

    scored = list(zip(docs, scores))
    scored.sort(key=lambda item: item[1], reverse=True)
    if options.threshold is not None:
        scored = [(doc, score) for doc, score in scored if score >= options.threshold]
    if options.top_n > 0:
        scored = scored[: options.top_n]
    return scored
