from __future__ import annotations

from typing import List

from langchain_core.documents import Document

from .utils import safe_import
from .preflight import check_torch_health


def get_embeddings(model_name: str):
    check_torch_health()
    embeddings_mod = safe_import("langchain_community.embeddings", "langchain-community")
    HuggingFaceEmbeddings = embeddings_mod.HuggingFaceEmbeddings
    return HuggingFaceEmbeddings(model_name=model_name)


def build_vectorstore(
    documents: List[Document],
    persist_dir: str,
    collection: str,
    embedding_model: str,
):
    embeddings = get_embeddings(embedding_model)
    chroma_mod = safe_import("langchain_chroma", "langchain-chroma")
    Chroma = chroma_mod.Chroma

    store = Chroma(
        collection_name=collection,
        embedding_function=embeddings,
        persist_directory=persist_dir,
    )
    if documents:
        store.add_documents(documents)
    _persist_if_supported(store)
    return store


def load_vectorstore(
    persist_dir: str,
    collection: str,
    embedding_model: str,
):
    embeddings = get_embeddings(embedding_model)
    chroma_mod = safe_import("langchain_chroma", "langchain-chroma")
    Chroma = chroma_mod.Chroma
    return Chroma(
        collection_name=collection,
        embedding_function=embeddings,
        persist_directory=persist_dir,
    )


def _persist_if_supported(store) -> None:
    if hasattr(store, "persist"):
        store.persist()
