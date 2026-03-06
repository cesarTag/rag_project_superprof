from __future__ import annotations

import json
from typing import Any, Dict, Optional

from langchain_core.documents import Document
from langchain_text_splitters import (
    CharacterTextSplitter,
    HTMLHeaderTextSplitter,
    LatexTextSplitter,
    MarkdownHeaderTextSplitter,
    NLTKTextSplitter,
    RecursiveCharacterTextSplitter,
    SpacyTextSplitter,
    TokenTextSplitter,
)

from .options import CHUNKERS
from .utils import safe_import


def parse_chunk_kwargs(raw: str | None) -> Dict[str, Any]:
    if not raw:
        return {}
    if isinstance(raw, dict):
        return raw
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError("chunk-kwargs must be valid JSON") from exc
    if not isinstance(data, dict):
        raise ValueError("chunk-kwargs must be a JSON object")
    return data


def get_splitter(
    chunker: str,
    chunk_size: int,
    chunk_overlap: int,
    chunk_kwargs: Optional[Dict[str, Any]] = None,
    embeddings=None,
):
    chunk_kwargs = chunk_kwargs or {}
    if chunker == "recursive":
        return RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            **chunk_kwargs,
        )
    if chunker == "character":
        return CharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            **chunk_kwargs,
        )
    if chunker == "token":
        return TokenTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            **chunk_kwargs,
        )
    if chunker == "nltk":
        return NLTKTextSplitter(**chunk_kwargs)
    if chunker == "spacy":
        return SpacyTextSplitter(**chunk_kwargs)
    if chunker == "markdown":
        return MarkdownHeaderTextSplitter(**chunk_kwargs)
    if chunker == "html":
        return HTMLHeaderTextSplitter(**chunk_kwargs)
    if chunker == "latex":
        return LatexTextSplitter(**chunk_kwargs)
    if chunker == "semantic":
        if embeddings is None:
            raise ValueError("semantic chunker requires embeddings")
        experimental = safe_import("langchain_experimental.text_splitter", "langchain-experimental")
        SemanticChunker = experimental.SemanticChunker
        return SemanticChunker(embeddings=embeddings, **chunk_kwargs)

    raise ValueError(f"Unknown chunker: {chunker}")


def chunk_documents(documents: list[Document], splitter) -> list[Document]:
    if hasattr(splitter, "split_documents"):
        return splitter.split_documents(documents)

    chunks: list[Document] = []
    for doc in documents:
        parts = splitter.split_text(doc.page_content)
        for part in parts:
            if isinstance(part, Document):
                chunks.append(part)
            else:
                chunks.append(Document(page_content=part, metadata=doc.metadata))
    return chunks
