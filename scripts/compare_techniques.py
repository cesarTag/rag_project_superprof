#!/usr/bin/env python3
from __future__ import annotations

import argparse
import time
from pathlib import Path
from typing import Dict, List

from preprocessing.chunking import get_splitter, parse_chunk_kwargs, chunk_documents
from preprocessing.extraction import ExtractionOptions, extract_pdf_to_documents
from preprocessing.options import EXTRACTORS, CHUNKERS
from preprocessing.vectorstore import (
    build_vectorstore,
    load_vectorstore,
    get_embeddings,
    create_ensemble_retriever,
)
from preprocessing.utils import safe_import
from preprocessing.utils import find_pdfs
from preprocessing.config import load_config, resolve_config_path, deep_get
from preprocessing.cli import _load_env


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compare extraction + chunking techniques")
    parser.add_argument("--config", default=None)
    parser.add_argument("--env-file", default=None)
    parser.add_argument("--question", required=True)
    parser.add_argument("--output", default=None)
    parser.add_argument("--limit-pdfs", type=int, default=None)
    parser.add_argument("--skip-existing", action=argparse.BooleanOptionalAction, default=None)
    return parser


def _chunker_kwargs(base_kwargs: dict, chunker: str) -> dict:
    kwargs = dict(base_kwargs or {})
    if chunker == "markdown":
        kwargs.setdefault("headers_to_split_on", [("#", "h1"), ("##", "h2")])
    if chunker == "html":
        kwargs.setdefault("headers_to_split_on", [("h1", "h1"), ("h2", "h2")])
    return kwargs


def _write_report(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _render_report(results: List[Dict]) -> str:
    lines = ["# Comparison Report", ""]
    lines.append(f"Total runs: {len(results)}")
    lines.append("")

    def _fmt(value) -> str:
        if value is None:
            return "N/A"
        return str(value)

    lines.append("## Summary Metrics")
    lines.append("")
    lines.append("| Name | Extractor | Chunker | PDFs | Docs | Chunks | Avg Chunk Size | Extract s | Chunk s | Index s | Query s | k | post-rerank |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for result in results:
        metrics = result.get("metrics", {})
        lines.append(
            "| {name} | {extractor} | {chunker} | {pdfs} | {docs} | {chunks} | {avg_chunk} | {t_extract} | {t_chunk} | {t_index} | {t_query} |".format(
                name=result["name"],
                extractor=result["extractor"],
                chunker=result["chunker"],
                pdfs=_fmt(metrics.get("pdf_count")),
                docs=_fmt(metrics.get("doc_count")),
                chunks=_fmt(metrics.get("chunk_count")),
                avg_chunk=_fmt(metrics.get("avg_chunk_size")),
                t_extract=_fmt(metrics.get("time_extract")),
                t_chunk=_fmt(metrics.get("time_chunk")),
                t_index=_fmt(metrics.get("time_index")),
                t_query=_fmt(metrics.get("time_query")),
                k=_fmt(metrics.get("retrieved_k")),
                post=_fmt(metrics.get("post_rerank_n")),
            )
        )

    lines.append("")
    for result in results:
        lines.append(f"## {result['name']}")
        lines.append("")
        lines.append(f"- Extractor: `{result['extractor']}`")
        lines.append(f"- Chunker: `{result['chunker']}`")
        lines.append(f"- Collection: `{result['collection']}`")
        lines.append("")
        lines.append("**Metrics**")
        lines.append("")
        metrics = result.get("metrics", {})
        lines.append(f"- PDFs: {_fmt(metrics.get('pdf_count'))}")
        lines.append(f"- Docs: {_fmt(metrics.get('doc_count'))}")
        lines.append(f"- Chunks: {_fmt(metrics.get('chunk_count'))}")
        lines.append(f"- Avg chunk size: {_fmt(metrics.get('avg_chunk_size'))}")
        lines.append(f"- Extract time (s): {_fmt(metrics.get('time_extract'))}")
        lines.append(f"- Chunk time (s): {_fmt(metrics.get('time_chunk'))}")
        lines.append(f"- Index time (s): {_fmt(metrics.get('time_index'))}")
        lines.append(f"- Query time (s): {_fmt(metrics.get('time_query'))}")
        lines.append("")
        lines.append("**Answer**")
        lines.append("")
        lines.append(result.get("answer", ""))
        lines.append("")
        if result.get("sources_pre_rerank"):
            lines.append("**Sources (pre-rerank)**")
            lines.append("")
            for src in result["sources_pre_rerank"]:
                lines.append(f"- {src}")
            lines.append("")
        if result.get("sources_post_rerank"):
            lines.append("**Sources (post-rerank)**")
            lines.append("")
            for src in result["sources_post_rerank"]:
                lines.append(f"- {src}")
            lines.append("")
        if result.get("sources"):
            lines.append("**Sources**")
            lines.append("")
            for src in result["sources"]:
                lines.append(f"- {src}")
            lines.append("")
    return "\n".join(lines)


def _metrics_from_store(store) -> dict:
    metrics = {
        "doc_count": None,
        "chunk_count": None,
        "avg_chunk_size": None,
    }
    if not hasattr(store, "get"):
        return metrics
    try:
        data = store.get(include=["documents", "metadatas"])
        documents = data.get("documents", []) or []
        metadatas = data.get("metadatas", []) or []
        chunk_count = len(documents)
        metrics["chunk_count"] = chunk_count
        if chunk_count:
            metrics["avg_chunk_size"] = int(sum(len(doc or "") for doc in documents) / chunk_count)
        doc_keys = set()
        for meta in metadatas:
            if not meta:
                continue
            source = meta.get("source")
            page = meta.get("page")
            if source is None:
                continue
            doc_keys.add((source, page))
        if doc_keys:
            metrics["doc_count"] = len(doc_keys)
    except Exception:
        return metrics
    return metrics


def _filter_non_empty(docs: List) -> tuple[List, int]:
    filtered = []
    dropped = 0
    for doc in docs:
        text = (doc.page_content or "").strip()
        if not text:
            dropped += 1
            continue
        filtered.append(doc)
    return filtered, dropped


def _doc_key(doc) -> tuple:
    meta = doc.metadata or {}
    return (
        meta.get("source"),
        meta.get("page"),
        (doc.page_content or "")[:200],
    )


def _format_source(doc, label: str | None, score_label: str | None = None, score=None) -> str:
    meta = doc.metadata or {}
    base = f"{meta.get('source')} (page: {meta.get('page')})"
    if score_label is not None and score is not None:
        score_text = f"{score:.4f}" if isinstance(score, (int, float)) else str(score)
        base += f" | {score_label}: {score_text}"
    if label:
        base += f" | {label}"
    return base


def _retrieve_with_config(
    store,
    question: str,
    k: int,
    score_metric: str,
    relevance_threshold: float | None,
    distance_threshold: float | None,
    hybrid: bool,
    docs_for_bm25,
):
    docs = []
    scored_results = None
    score_label = None
    used_hybrid = False
    hybrid_labels: dict[tuple, str] = {}
    hybrid_scores: dict[tuple, float] = {}
    hybrid_score_label = "hybrid_score"
    metric = str(score_metric).lower()

    if hybrid:
        try:
            from langchain_core.documents import Document

            docs_bm25_source = docs_for_bm25 or []
            if not docs_bm25_source and hasattr(store, "get"):
                data = store.get(include=["documents", "metadatas"])
                docs_bm25_source = [
                    Document(page_content=doc, metadata=meta or {})
                    for doc, meta in zip(data.get("documents", []), data.get("metadatas", []))
                ]
            if not docs_bm25_source:
                raise ValueError("No documents available to build BM25 retriever.")

            weights = (0.3, 0.7)
            ensemble_retriever = create_ensemble_retriever(
                documents=docs_bm25_source,
                vectorstore=store,
                k=int(k),
                weights=weights,
            )
            bm25_retriever = ensemble_retriever.retrievers[0]
            vector_retriever = ensemble_retriever.retrievers[1]

            if hasattr(bm25_retriever, "invoke"):
                docs_bm25 = bm25_retriever.invoke(question)
            else:
                docs_bm25 = bm25_retriever.get_relevant_documents(question)

            if hasattr(vector_retriever, "invoke"):
                docs_vec = vector_retriever.invoke(question)
            else:
                docs_vec = vector_retriever.get_relevant_documents(question)

            for doc in docs_bm25:
                hybrid_labels[_doc_key(doc)] = "BM25"
            for doc in docs_vec:
                key = _doc_key(doc)
                if key in hybrid_labels:
                    hybrid_labels[key] = "BM25+Vectorstore"
                else:
                    hybrid_labels[key] = "Vectorstore"

            for rank, doc in enumerate(docs_bm25):
                key = _doc_key(doc)
                hybrid_scores[key] = hybrid_scores.get(key, 0.0) + weights[0] * (1.0 / (rank + 1))
            for rank, doc in enumerate(docs_vec):
                key = _doc_key(doc)
                hybrid_scores[key] = hybrid_scores.get(key, 0.0) + weights[1] * (1.0 / (rank + 1))

            if hasattr(ensemble_retriever, "invoke"):
                docs = ensemble_retriever.invoke(question)
            else:
                docs = ensemble_retriever.get_relevant_documents(question)
            used_hybrid = True
        except Exception as exc:
            print(f"Warning: hybrid search failed, falling back to vectorstore only: {exc}")
            used_hybrid = False
            hybrid_labels.clear()
            hybrid_scores.clear()

    if not used_hybrid:
        if metric not in ("auto", "relevance", "distance"):
            metric = "auto"
        if metric == "relevance":
            if not hasattr(store, "similarity_search_with_relevance_scores"):
                raise SystemExit("Requested relevance scores but this vectorstore does not support them.")
            scored_results = store.similarity_search_with_relevance_scores(question, k=int(k))
            score_label = "relevance"
        elif metric == "distance":
            if not hasattr(store, "similarity_search_with_score"):
                raise SystemExit("Requested distance scores but this vectorstore does not support them.")
            scored_results = store.similarity_search_with_score(question, k=int(k))
            score_label = "distance"
        else:
            if hasattr(store, "similarity_search_with_relevance_scores"):
                scored_results = store.similarity_search_with_relevance_scores(question, k=int(k))
                score_label = "relevance"
            elif hasattr(store, "similarity_search_with_score"):
                scored_results = store.similarity_search_with_score(question, k=int(k))
                score_label = "distance"

    if scored_results is not None and not used_hybrid:
        if score_label == "relevance" and relevance_threshold is not None:
            scored_results = [(doc, score) for doc, score in scored_results if score >= float(relevance_threshold)]
        elif score_label == "distance" and distance_threshold is not None:
            scored_results = [(doc, score) for doc, score in scored_results if score <= float(distance_threshold)]
        docs = [doc for doc, _ in scored_results]
    elif not used_hybrid:
        retriever = store.as_retriever(search_kwargs={"k": int(k)})
        if hasattr(retriever, "invoke"):
            docs = retriever.invoke(question)
        else:
            docs = retriever.get_relevant_documents(question)

    return {
        "docs": docs,
        "scored_results": scored_results,
        "score_label": score_label,
        "used_hybrid": used_hybrid,
        "hybrid_labels": hybrid_labels,
        "hybrid_scores": hybrid_scores,
        "hybrid_score_label": hybrid_score_label,
    }


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    _load_env(args.env_file)

    cfg_path = resolve_config_path(args.config)
    cfg = load_config(cfg_path)

    input_dir = deep_get(cfg, ["input_dir"])
    if not input_dir:
        raise SystemExit("input_dir must be set in config.yml")

    persist_dir = deep_get(cfg, ["indexing", "persist_dir"], "./data/chroma")
    collection_base = deep_get(cfg, ["indexing", "collection"], "pdfs")
    recursive = deep_get(cfg, ["recursive"], True)

    ocr_mode = deep_get(cfg, ["extraction", "ocr"], "auto")
    force_ocr = deep_get(cfg, ["extraction", "force_ocr"], False)
    ocr_lang = deep_get(cfg, ["extraction", "ocr_lang"], "eng")
    easyocr_langs = deep_get(cfg, ["extraction", "easyocr_langs"], ["en"])
    min_text = deep_get(cfg, ["extraction", "min_text_per_page"], 25)

    chunk_size = deep_get(cfg, ["chunking", "chunk_size"], 1000)
    chunk_overlap = deep_get(cfg, ["chunking", "chunk_overlap"], 150)
    chunk_kwargs = parse_chunk_kwargs(deep_get(cfg, ["chunking", "chunk_kwargs"], None))

    embedding_model = deep_get(cfg, ["indexing", "embedding_model"], "sentence-transformers/all-MiniLM-L6-v2")

    model = deep_get(cfg, ["query", "model"], "claude-haiku-4-5")
    temperature = deep_get(cfg, ["query", "temperature"], 0.2)
    k = deep_get(cfg, ["query", "k"], 4)
    max_tokens = deep_get(cfg, ["query", "max_tokens"], 1024)
    score_metric = deep_get(cfg, ["query", "score_metric"], "auto")
    relevance_threshold = deep_get(cfg, ["query", "relevance_threshold"], None)
    distance_threshold = deep_get(cfg, ["query", "distance_threshold"], None)
    hybrid = deep_get(cfg, ["query", "search", "hybrid"], False)
    rerank_enabled = deep_get(cfg, ["query", "rerank", "enabled"], False)
    rerank_model = deep_get(
        cfg, ["query", "rerank", "model"], "cross-encoder/ms-marco-MiniLM-L-6-v2"
    )
    rerank_top_n = deep_get(cfg, ["query", "rerank", "top_n"], None)
    rerank_threshold = deep_get(cfg, ["query", "rerank", "threshold"], None)

    output_path = args.output or deep_get(cfg, ["comparison", "output"], "./reports/comparison.md")
    skip_existing = args.skip_existing if args.skip_existing is not None else deep_get(cfg, ["comparison", "skip_existing"], True)
    limit_pdfs = args.limit_pdfs if args.limit_pdfs is not None else deep_get(cfg, ["comparison", "limit_pdfs"], None)
    extractors = deep_get(cfg, ["comparison", "extractors"], EXTRACTORS)
    chunkers = deep_get(cfg, ["comparison", "chunkers"], CHUNKERS)

    pdfs = find_pdfs(input_dir, recursive=bool(recursive))
    if limit_pdfs:
        pdfs = pdfs[: int(limit_pdfs)]
    if not pdfs:
        raise SystemExit("No PDFs found")

    results = []
    missing_extractors = set()

    for extractor in extractors:
        for chunker in chunkers:
            name = f"{extractor} + {chunker}"
            collection = f"{collection_base}-{extractor}-{chunker}".replace("/", "-")
            collection_path = Path(persist_dir) / collection

            docs = []
            chunks = []
            embeddings = None
            t_extract = None
            t_chunk = None
            t_index = None
            doc_count = None
            chunk_count = None
            avg_chunk_size = None

            if extractor in missing_extractors and (not (skip_existing and collection_path.exists())):
                continue

            if skip_existing and collection_path.exists():
                store = load_vectorstore(
                    persist_dir=str(collection_path),
                    collection=collection,
                    embedding_model=embedding_model,
                )
                store_metrics = _metrics_from_store(store)
                doc_count = store_metrics.get("doc_count")
                chunk_count = store_metrics.get("chunk_count")
                avg_chunk_size = store_metrics.get("avg_chunk_size")
            else:
                t0 = time.perf_counter()
                try:
                    for pdf_path in pdfs:
                        options = ExtractionOptions(
                            extractor=extractor,
                            ocr_mode=ocr_mode,
                            force_ocr=bool(force_ocr),
                            ocr_lang=ocr_lang,
                            easyocr_langs=easyocr_langs,
                            min_text_per_page=int(min_text),
                        )
                        docs.extend(extract_pdf_to_documents(pdf_path, options))
                except ImportError as exc:
                    print(f"Skipping extractor {extractor} due to missing dependency: {exc}")
                    missing_extractors.add(extractor)
                    continue
                docs, dropped_docs = _filter_non_empty(docs)
                if dropped_docs:
                    print(f"Dropped {dropped_docs} empty docs for {extractor}")
                t_extract = time.perf_counter() - t0
                doc_count = len(docs)

                try:
                    if chunker == "semantic":
                        embeddings = get_embeddings(embedding_model)

                    t1 = time.perf_counter()
                    splitter = get_splitter(
                        chunker=chunker,
                        chunk_size=int(chunk_size),
                        chunk_overlap=int(chunk_overlap),
                        chunk_kwargs=_chunker_kwargs(chunk_kwargs, chunker),
                        embeddings=embeddings,
                    )
                    chunks = chunk_documents(docs, splitter)
                    chunks, dropped = _filter_non_empty(chunks)
                    if dropped:
                        print(f"Dropped {dropped} empty chunks for {extractor}+{chunker}")
                    t_chunk = time.perf_counter() - t1
                    chunk_count = len(chunks)
                    if chunks:
                        avg_chunk_size = int(sum(len(c.page_content) for c in chunks) / len(chunks))
                except (ImportError, LookupError) as exc:
                    print(f"Skipping chunker {chunker} for extractor {extractor} due to missing dependency: {exc}")
                    continue

                t2 = time.perf_counter()
                build_vectorstore(
                    documents=chunks,
                    persist_dir=str(collection_path),
                    collection=collection,
                    embedding_model=embedding_model,
                )
                t_index = time.perf_counter() - t2

                store = load_vectorstore(
                    persist_dir=str(collection_path),
                    collection=collection,
                    embedding_model=embedding_model,
                )

            from langchain_anthropic import ChatAnthropic
            from langchain_core.messages import HumanMessage, SystemMessage

            t3 = time.perf_counter()
            llm = ChatAnthropic(model=model, temperature=float(temperature), max_tokens=int(max_tokens))
            retrieval = _retrieve_with_config(
                store=store,
                question=args.question,
                k=int(k),
                score_metric=score_metric,
                relevance_threshold=relevance_threshold,
                distance_threshold=distance_threshold,
                hybrid=bool(hybrid),
                docs_for_bm25=chunks,
            )
            docs_retrieved = retrieval["docs"]
            scored_results = retrieval["scored_results"]
            score_label = retrieval["score_label"]
            used_hybrid = retrieval["used_hybrid"]
            hybrid_labels = retrieval["hybrid_labels"]
            hybrid_scores = retrieval["hybrid_scores"]
            hybrid_score_label = retrieval["hybrid_score_label"]

            pre_rerank_docs = list(docs_retrieved)
            pre_rerank_sources = []
            if rerank_enabled:
                if used_hybrid:
                    for doc in pre_rerank_docs:
                        key = _doc_key(doc)
                        label = hybrid_labels.get(key)
                        score = hybrid_scores.get(key)
                        pre_rerank_sources.append(
                            _format_source(doc, label, score_label=hybrid_score_label, score=score)
                        )
                elif scored_results is not None:
                    for doc, score in scored_results:
                        pre_rerank_sources.append(
                            _format_source(doc, None, score_label=score_label, score=score)
                        )
                else:
                    for doc in pre_rerank_docs:
                        pre_rerank_sources.append(_format_source(doc, None))

            rerank_scores = None
            if rerank_enabled and docs_retrieved:
                try:
                    from preprocessing.rerank import RerankOptions, rerank_documents

                    if rerank_top_n is None:
                        top_n = int(k)
                    else:
                        top_n = int(rerank_top_n)
                    if top_n < int(k):
                        print(
                            f"Warning: rerank_top_n={top_n} limits results even though k={k}. "
                            "Set query.rerank.top_n=null (or to the same value as k) to keep all results."
                        )
                    rerank_scores = rerank_documents(
                        args.question,
                        docs_retrieved,
                        RerankOptions(
                            enabled=True,
                            model=rerank_model,
                            top_n=int(top_n),
                            threshold=rerank_threshold if rerank_threshold is not None else None,
                        ),
                    )
                    docs_retrieved = [doc for doc, _ in rerank_scores]
                except ImportError as exc:
                    print(f"Warning: rerank enabled but dependencies missing: {exc}. Continuing without rerank.")

            context = "\n\n".join(doc.page_content for doc in docs_retrieved)
            prompt = (
                "You are a helpful assistant. Use the provided context to answer the question.\n\n"
                f"Context:\n{context}\n\n"
                f"Question: {args.question}\n"
                "Answer in Spanish."
            )
            response = llm.invoke([SystemMessage(content="You are a helpful assistant."), HumanMessage(content=prompt)])
            answer = getattr(response, "content", response)
            t_query = time.perf_counter() - t3

            sources = []
            sources_post = []
            if rerank_enabled:
                if rerank_scores is not None:
                    for doc, score in rerank_scores:
                        sources_post.append(
                            _format_source(doc, None, score_label="rerank_score", score=score)
                        )
                else:
                    for doc in docs_retrieved:
                        sources_post.append(_format_source(doc, None))
            else:
                if used_hybrid:
                    for doc in docs_retrieved:
                        key = _doc_key(doc)
                        label = hybrid_labels.get(key)
                        score = hybrid_scores.get(key)
                        sources.append(
                            _format_source(doc, label, score_label=hybrid_score_label, score=score)
                        )
                elif scored_results is not None:
                    for doc, score in scored_results:
                        sources.append(_format_source(doc, None, score_label=score_label, score=score))
                else:
                    for doc in docs_retrieved:
                        sources.append(_format_source(doc, None))

            results.append(
                {
                    "name": name,
                    "extractor": extractor,
                    "chunker": chunker,
                    "collection": str(collection_path),
                    "answer": answer,
                    "sources": sources,
                    "sources_pre_rerank": pre_rerank_sources if rerank_enabled else None,
                    "sources_post_rerank": sources_post if rerank_enabled else None,
                    "metrics": {
                        "pdf_count": len(pdfs),
                        "doc_count": doc_count,
                        "chunk_count": chunk_count,
                        "avg_chunk_size": avg_chunk_size,
                        "time_extract": round(t_extract, 3) if t_extract is not None else None,
                        "time_chunk": round(t_chunk, 3) if t_chunk is not None else None,
                        "time_index": round(t_index, 3) if t_index is not None else None,
                        "time_query": round(t_query, 3),
                        "retrieved_k": len(pre_rerank_docs) if pre_rerank_docs else 0,
                        "post_rerank_n": len(docs_retrieved) if rerank_enabled else None,
                    },
                }
            )

    report = _render_report(results)
    _write_report(Path(output_path), report)
    print(f"Report written to {output_path}")


if __name__ == "__main__":
    main()
