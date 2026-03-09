from __future__ import annotations

from typing import List, Iterable

from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_core.documents import Document

from .utils import safe_import
from .preflight import check_torch_health


def get_embeddings(model_name: str):
    if model_name == "GPT4AllEmbeddings":
        return GPT4AllEmbeddings()
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


def build_vectorstore_hybrid(
    documents: List[Document],
    persist_dir: str,
    collection: str,
    embedding_model: str,
    k: int = 5,
    weights: tuple[float, float] = (0.3, 0.7),
):
    store = build_vectorstore(
        documents=documents,
        persist_dir=persist_dir,
        collection=collection,
        embedding_model=embedding_model,
    )
    retriever = create_ensemble_retriever(
        documents=documents,
        vectorstore=store,
        k=k,
        weights=weights,
    )
    return store, retriever


def create_ensemble_retriever(
    documents: List[Document],
    vectorstore,
    k: int = 5,
    weights: tuple[float, float] = (0.3, 0.7),
):
    BM25Retriever = None
    EnsembleRetriever = None
    try:
        retrievers_mod = safe_import("langchain.retrievers", "langchain")
        BM25Retriever = getattr(retrievers_mod, "BM25Retriever", None)
        EnsembleRetriever = getattr(retrievers_mod, "EnsembleRetriever", None)
    except ImportError:
        BM25Retriever = None
        EnsembleRetriever = None

    if BM25Retriever is None:
        community_mod = safe_import("langchain_community.retrievers", "langchain-community")
        BM25Retriever = getattr(community_mod, "BM25Retriever", None)

    if BM25Retriever is None:
        raise ImportError("BM25Retriever is not available. Install langchain-community.")

    if not documents:
        raise ValueError("documents must be provided to build BM25 retriever")

    bm25_retriever = BM25Retriever.from_documents(documents)
    bm25_retriever.k = int(k)
    chroma_retriever = vectorstore.as_retriever(search_kwargs={"k": int(k)})
    if EnsembleRetriever is not None:
        ensemble_retriever = EnsembleRetriever(
            retrievers=[bm25_retriever, chroma_retriever],
            weights=list(weights),
        )
        return ensemble_retriever

    # Fallback: simple rank-fusion ensemble to avoid hard dependency on EnsembleRetriever
    return _SimpleEnsembleRetriever(
        retrievers=[bm25_retriever, chroma_retriever],
        weights=list(weights),
        k=int(k),
    )


def _doc_key(doc: Document) -> tuple:
    meta = doc.metadata or {}
    return (meta.get("source"), meta.get("page"), (doc.page_content or "")[:200])


class _SimpleEnsembleRetriever:
    def __init__(self, retrievers: Iterable, weights: List[float], k: int):
        self.retrievers = list(retrievers)
        self.weights = list(weights)
        self.k = int(k)

    def _retrieve(self, retriever, query: str) -> list[Document]:
        if hasattr(retriever, "invoke"):
            return retriever.invoke(query)
        return retriever.get_relevant_documents(query)

    def _rank(self, query: str) -> list[Document]:
        scores: dict[tuple, float] = {}
        docs_by_key: dict[tuple, Document] = {}
        for idx, retriever in enumerate(self.retrievers):
            weight = self.weights[idx] if idx < len(self.weights) else 1.0
            docs = self._retrieve(retriever, query)
            for rank, doc in enumerate(docs):
                key = _doc_key(doc)
                docs_by_key[key] = doc
                scores[key] = scores.get(key, 0.0) + weight * (1.0 / (rank + 1))
        ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)
        if self.k > 0:
            ranked = ranked[: self.k]
        return [docs_by_key[key] for key, _ in ranked]

    def get_relevant_documents(self, query: str) -> list[Document]:
        return self._rank(query)

    def invoke(self, query: str) -> list[Document]:
        return self._rank(query)


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


def get_existing_sources(store) -> set[str]:
    existing_sources: set[str] = set()
    if hasattr(store, "get"):
        try:
            data = store.get(include=["metadatas"])
            for meta in data.get("metadatas", []) or []:
                if meta and meta.get("source"):
                    existing_sources.add(meta.get("source"))
        except Exception:
            existing_sources = set()
    return existing_sources


def add_documents_dedup_by_source(store, documents: List[Document]) -> tuple[int, list[str]]:
    if not documents:
        return 0, []

    existing_sources = get_existing_sources(store)

    new_docs = []
    skipped_sources = []
    for doc in documents:
        source = (doc.metadata or {}).get("source")
        if source and source in existing_sources:
            if source not in skipped_sources:
                skipped_sources.append(source)
            continue
        new_docs.append(doc)

    if new_docs:
        store.add_documents(new_docs)
        _persist_if_supported(store)
    return len(new_docs), skipped_sources
