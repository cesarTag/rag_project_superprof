from __future__ import annotations

import os
import argparse
import json
from pathlib import Path
from typing import Any

# Avoid third-party Pydantic plugin import warnings (e.g., logfire) unless user opts in
os.environ.setdefault("PYDANTIC_DISABLE_PLUGINS", "1")

# Safe defaults to avoid known hangs on macOS with transformers/tokenizers/TF
_SAFE_ENV_DEFAULTS = {
    "TRANSFORMERS_NO_TF": "1",
    "TOKENIZERS_PARALLELISM": "false",
    "OMP_NUM_THREADS": "1",
    "MKL_NUM_THREADS": "1",
    "OPENBLAS_NUM_THREADS": "1",
    "VECLIB_MAXIMUM_THREADS": "1",
}

_DISABLE_SAFE_ENV = "--no-safe-env" in os.sys.argv
if _DISABLE_SAFE_ENV:
    for key, value in _SAFE_ENV_DEFAULTS.items():
        if os.environ.get(key) == value:
            os.environ.pop(key, None)
else:
    for key, value in _SAFE_ENV_DEFAULTS.items():
        os.environ.setdefault(key, value)

from .config import deep_get, load_config, resolve_config_path
from .options import CHUNKERS, EXTRACTORS, OCR_MODES, list_chunkers, list_extractors, list_ocr_modes


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="PDF preprocessing pipeline")
    parser.add_argument("--config", help="Path to YAML config file", default=None)
    parser.add_argument(
        "--env-file",
        help="Path to .env file with API keys (defaults to .env if present)",
        default=None,
    )
    parser.add_argument(
        "--no-safe-env",
        action="store_true",
        help="Disable safe environment defaults for transformers/tokenizers/threads",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    list_cmd = subparsers.add_parser("list-options", help="List available extractors/ocr/chunkers")
    list_cmd.add_argument("--type", choices=["extractors", "ocr", "chunkers", "all"], default="all")

    extract = subparsers.add_parser("extract", help="Extract text from PDFs")
    extract.add_argument("--input-dir", required=False)
    extract.add_argument("--output", required=False)
    extract.add_argument("--recursive", action=argparse.BooleanOptionalAction, default=None)
    extract.add_argument("--extractor", choices=EXTRACTORS, default=None)
    extract.add_argument("--ocr", choices=OCR_MODES, default=None)
    extract.add_argument("--force-ocr", action=argparse.BooleanOptionalAction, default=None)
    extract.add_argument("--ocr-lang", default=None)
    extract.add_argument("--easyocr-lang", default=None)
    extract.add_argument("--min-text-per-page", type=int, default=None)
    extract.add_argument("--ocr-llm-model", default=None)
    extract.add_argument("--ocr-llm-max-tokens", type=int, default=None)

    chunk = subparsers.add_parser("chunk", help="Chunk extracted text")
    chunk.add_argument("--input", required=False)
    chunk.add_argument("--output", required=False)
    chunk.add_argument("--chunker", choices=CHUNKERS, default=None)
    chunk.add_argument("--chunk-size", type=int, default=None)
    chunk.add_argument("--chunk-overlap", type=int, default=None)
    chunk.add_argument("--chunk-kwargs", default=None)
    chunk.add_argument("--embedding-model", default=None)

    index = subparsers.add_parser("index", help="Build a Chroma vectorstore")
    index.add_argument("--input", required=False)
    index.add_argument("--persist-dir", required=False)
    index.add_argument("--collection", default=None)
    index.add_argument("--embedding-model", default=None)

    query = subparsers.add_parser("query", help="Query a Chroma vectorstore with Anthropic")
    query.add_argument("--persist-dir", required=False)
    query.add_argument("--collection", default=None)
    query.add_argument("--embedding-model", default=None)
    query.add_argument("--question", required=True)
    query.add_argument("--model", default=None)
    query.add_argument("--temperature", type=float, default=None)
    query.add_argument("--k", type=int, default=None)
    query.add_argument("--max-tokens", type=int, default=None)
    query.add_argument("--relevance-threshold", type=float, default=None)
    query.add_argument("--distance-threshold", type=float, default=None)
    query.add_argument("--rerank", action=argparse.BooleanOptionalAction, default=None)
    query.add_argument("--rerank-model", default=None)
    query.add_argument("--rerank-top-n", type=int, default=None)
    query.add_argument("--rerank-threshold", type=float, default=None)
    query.add_argument(
        "--score-metric",
        choices=["auto", "relevance", "distance"],
        default=None,
        help="Score metric to use for retrieval: auto|relevance|distance",
    )
    query.add_argument("--show-sources", action=argparse.BooleanOptionalAction, default=None)

    pipeline = subparsers.add_parser("pipeline", help="Run extract + chunk + index in one step")
    pipeline.add_argument("--input-dir", required=False)
    pipeline.add_argument("--work-dir", required=False)
    pipeline.add_argument("--recursive", action=argparse.BooleanOptionalAction, default=None)
    pipeline.add_argument("--extractor", choices=EXTRACTORS, default=None)
    pipeline.add_argument("--ocr", choices=OCR_MODES, default=None)
    pipeline.add_argument("--force-ocr", action=argparse.BooleanOptionalAction, default=None)
    pipeline.add_argument("--ocr-lang", default=None)
    pipeline.add_argument("--easyocr-lang", default=None)
    pipeline.add_argument("--min-text-per-page", type=int, default=None)
    pipeline.add_argument("--chunker", choices=CHUNKERS, default=None)
    pipeline.add_argument("--chunk-size", type=int, default=None)
    pipeline.add_argument("--chunk-overlap", type=int, default=None)
    pipeline.add_argument("--chunk-kwargs", default=None)
    pipeline.add_argument("--persist-dir", default=None)
    pipeline.add_argument("--collection", default=None)
    pipeline.add_argument("--embedding-model", default=None)
    pipeline.add_argument("--ocr-llm-model", default=None)
    pipeline.add_argument("--ocr-llm-max-tokens", type=int, default=None)

    return parser


def _resolve(arg_value: Any, cfg_value: Any, default: Any) -> Any:
    if arg_value is not None:
        return arg_value
    if cfg_value is not None:
        return cfg_value
    return default


def _parse_easyocr_langs(value: str | None, default: list[str]) -> list[str]:
    if value is None:
        return default
    if isinstance(value, list):
        return value
    return [part.strip() for part in value.split(",") if part.strip()]


def cmd_list_options(args):
    if args.type in ("extractors", "all"):
        print("Extractors:")
        for item in list_extractors():
            print(f"- {item}")
    if args.type in ("ocr", "all"):
        print("OCR modes:")
        for item in list_ocr_modes():
            print(f"- {item}")
    if args.type in ("chunkers", "all"):
        print("Chunkers:")
        for item in list_chunkers():
            print(f"- {item}")


def cmd_extract(args, cfg):
    from tqdm import tqdm
    from .documents import docs_to_records
    from .extraction import ExtractionOptions, extract_pdf_to_documents
    from .utils import find_pdfs

    input_dir = _resolve(args.input_dir, deep_get(cfg, ["input_dir"]), None)
    output = _resolve(args.output, deep_get(cfg, ["output_dir"]), None)
    if not input_dir or not output:
        raise SystemExit("extract requires --input-dir and --output (or config input_dir/output_dir)")

    extractor = _resolve(args.extractor, deep_get(cfg, ["extraction", "extractor"]), "pypdf")
    ocr_mode = _resolve(args.ocr, deep_get(cfg, ["extraction", "ocr"]), "auto")
    force_ocr = _resolve(args.force_ocr, deep_get(cfg, ["extraction", "force_ocr"]), False)
    ocr_lang = _resolve(args.ocr_lang, deep_get(cfg, ["extraction", "ocr_lang"]), "eng")
    easyocr_langs = _parse_easyocr_langs(
        _resolve(args.easyocr_lang, deep_get(cfg, ["extraction", "easyocr_langs"]), ["en"]),
        ["en"],
    )
    min_text = _resolve(args.min_text_per_page, deep_get(cfg, ["extraction", "min_text_per_page"]), 25)
    recursive = _resolve(args.recursive, deep_get(cfg, ["recursive"]), False)
    ocr_llm_model = _resolve(args.ocr_llm_model, deep_get(cfg, ["extraction", "ocr_llm_model"]), None)
    ocr_llm_max_tokens = _resolve(
        args.ocr_llm_max_tokens,
        deep_get(cfg, ["extraction", "ocr_llm_max_tokens"]),
        1024,
    )

    options = ExtractionOptions(
        extractor=extractor,
        ocr_mode=ocr_mode,
        force_ocr=bool(force_ocr),
        ocr_lang=ocr_lang,
        easyocr_langs=easyocr_langs,
        min_text_per_page=int(min_text),
        ocr_llm_model=ocr_llm_model,
        ocr_llm_max_tokens=int(ocr_llm_max_tokens),
    )

    pdfs = find_pdfs(input_dir, recursive=bool(recursive))
    if not pdfs:
        print("No PDFs found")
        return

    output_path = Path(output)
    print(f"Writing {len(pdfs)} PDFs to {output_path}")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        for pdf_path in tqdm(pdfs, desc="Extracting"):
            docs = extract_pdf_to_documents(pdf_path, options)
            for record in docs_to_records(docs):
                f.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"Extracted {len(pdfs)} PDFs -> {output_path}")


def cmd_chunk(args, cfg):
    from .chunking import chunk_documents, get_splitter, parse_chunk_kwargs
    from .documents import docs_to_records, records_to_docs
    from .utils import iter_jsonl

    default_extracted = None
    default_chunks = None
    output_dir = deep_get(cfg, ["output_dir"])
    if output_dir:
        default_extracted = str(Path(output_dir) / "extracted.jsonl")
        default_chunks = str(Path(output_dir) / "chunks.jsonl")

    input_path = _resolve(args.input, default_extracted, None)
    output_path_value = _resolve(args.output, default_chunks, None)
    if not input_path or not output_path_value:
        raise SystemExit("chunk requires --input and --output (or config output_dir)")

    chunker = _resolve(args.chunker, deep_get(cfg, ["chunking", "chunker"]), "recursive")
    chunk_size = _resolve(args.chunk_size, deep_get(cfg, ["chunking", "chunk_size"]), 1000)
    chunk_overlap = _resolve(args.chunk_overlap, deep_get(cfg, ["chunking", "chunk_overlap"]), 150)
    chunk_kwargs = _resolve(args.chunk_kwargs, deep_get(cfg, ["chunking", "chunk_kwargs"]), None)
    embedding_model = _resolve(
        args.embedding_model,
        deep_get(cfg, ["indexing", "embedding_model"]),
        "sentence-transformers/all-MiniLM-L6-v2",
    )

    splitter_kwargs = parse_chunk_kwargs(chunk_kwargs)
    embeddings = None
    if chunker == "semantic":
        from .vectorstore import get_embeddings
        embeddings = get_embeddings(embedding_model)

    splitter = get_splitter(
        chunker=chunker,
        chunk_size=int(chunk_size),
        chunk_overlap=int(chunk_overlap),
        chunk_kwargs=splitter_kwargs,
        embeddings=embeddings,
    )

    records = list(iter_jsonl(Path(input_path)))
    docs = records_to_docs(records)
    chunks = chunk_documents(docs, splitter)

    output_path = Path(output_path_value)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        for record in docs_to_records(chunks):
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"Chunked {len(docs)} docs -> {len(chunks)} chunks -> {output_path}")


def cmd_index(args, cfg):
    from .documents import records_to_docs
    from .utils import iter_jsonl
    from .vectorstore import build_vectorstore

    default_chunks = None
    output_dir = deep_get(cfg, ["output_dir"])
    if output_dir:
        default_chunks = str(Path(output_dir) / "chunks.jsonl")

    input_path = _resolve(args.input, default_chunks, None)
    persist_dir = _resolve(args.persist_dir, deep_get(cfg, ["indexing", "persist_dir"]), None)
    if not input_path or not persist_dir:
        raise SystemExit("index requires --input and --persist-dir (or config output_dir/indexing.persist_dir)")

    embedding_model = _resolve(
        args.embedding_model,
        deep_get(cfg, ["indexing", "embedding_model"]),
        "sentence-transformers/all-MiniLM-L6-v2",
    )
    collection = _resolve(args.collection, deep_get(cfg, ["indexing", "collection"]), "pdfs")

    records = list(iter_jsonl(Path(input_path)))
    docs = records_to_docs(records)
    build_vectorstore(
        documents=docs,
        persist_dir=persist_dir,
        collection=collection,
        embedding_model=embedding_model,
    )

    print(f"Indexed {len(docs)} chunks into {args.persist_dir} ({collection})")


def cmd_query(args, cfg):
    from .utils import safe_import
    from .vectorstore import load_vectorstore

    persist_dir = _resolve(args.persist_dir, deep_get(cfg, ["indexing", "persist_dir"]), None)
    if not persist_dir:
        raise SystemExit("query requires --persist-dir (or config indexing.persist_dir)")

    embedding_model = _resolve(
        args.embedding_model,
        deep_get(cfg, ["indexing", "embedding_model"]),
        "sentence-transformers/all-MiniLM-L6-v2",
    )
    collection = _resolve(args.collection, deep_get(cfg, ["indexing", "collection"]), "pdfs")
    model = _resolve(args.model, deep_get(cfg, ["query", "model"]), "claude-3-5-sonnet-latest")
    temperature = _resolve(args.temperature, deep_get(cfg, ["query", "temperature"]), 0.2)
    k = _resolve(args.k, deep_get(cfg, ["query", "k"]), 4)
    max_tokens = _resolve(args.max_tokens, deep_get(cfg, ["query", "max_tokens"]), 1024)
    relevance_threshold = _resolve(
        args.relevance_threshold,
        deep_get(cfg, ["query", "relevance_threshold"]),
        None,
    )
    distance_threshold = _resolve(
        args.distance_threshold,
        deep_get(cfg, ["query", "distance_threshold"]),
        None,
    )
    rerank_enabled = _resolve(
        args.rerank,
        deep_get(cfg, ["query", "rerank", "enabled"]),
        False,
    )
    rerank_model = _resolve(
        args.rerank_model,
        deep_get(cfg, ["query", "rerank", "model"]),
        "cross-encoder/ms-marco-MiniLM-L-6-v2",
    )
    rerank_top_n = _resolve(
        args.rerank_top_n,
        deep_get(cfg, ["query", "rerank", "top_n"]),
        5,
    )
    rerank_threshold = _resolve(
        args.rerank_threshold,
        deep_get(cfg, ["query", "rerank", "threshold"]),
        0.0,
    )
    score_metric = _resolve(
        args.score_metric,
        deep_get(cfg, ["query", "score_metric"]),
        "auto",
    )
    show_sources = _resolve(args.show_sources, deep_get(cfg, ["query", "show_sources"]), True)

    store = load_vectorstore(
        persist_dir=persist_dir,
        collection=collection,
        embedding_model=embedding_model,
    )

    langchain_anthropic = safe_import("langchain_anthropic", "langchain-anthropic")
    messages_mod = safe_import("langchain_core.messages", "langchain-core")
    ChatAnthropic = langchain_anthropic.ChatAnthropic
    SystemMessage = messages_mod.SystemMessage
    HumanMessage = messages_mod.HumanMessage

    llm = ChatAnthropic(model=model, temperature=float(temperature), max_tokens=int(max_tokens))

    docs = []
    scored_results = None
    score_label = None
    metric = str(score_metric).lower()
    if metric not in ("auto", "relevance", "distance"):
        raise SystemExit("score_metric must be one of: auto, relevance, distance")

    if metric == "relevance":
        if not hasattr(store, "similarity_search_with_relevance_scores"):
            raise SystemExit(
                "Requested relevance scores but this vectorstore does not support them. "
                "Use score_metric=auto or distance."
            )
        scored_results = store.similarity_search_with_relevance_scores(args.question, k=int(k))
        score_label = "relevance"
    elif metric == "distance":
        if not hasattr(store, "similarity_search_with_score"):
            raise SystemExit(
                "Requested distance scores but this vectorstore does not support them. "
                "Use score_metric=auto or relevance."
            )
        scored_results = store.similarity_search_with_score(args.question, k=int(k))
        score_label = "distance"
    else:
        if hasattr(store, "similarity_search_with_relevance_scores"):
            scored_results = store.similarity_search_with_relevance_scores(args.question, k=int(k))
            score_label = "relevance"
        elif hasattr(store, "similarity_search_with_score"):
            scored_results = store.similarity_search_with_score(args.question, k=int(k))
            score_label = "distance"

    if scored_results is not None:
        if score_label == "relevance":
            if distance_threshold is not None:
                print("Warning: distance_threshold ignored because score_metric=relevance.")
            if relevance_threshold is not None:
                threshold = float(relevance_threshold)
                scored_results = [(doc, score) for doc, score in scored_results if score >= threshold]
        elif score_label == "distance":
            if relevance_threshold is not None:
                print("Warning: relevance_threshold ignored because score_metric=distance.")
            if distance_threshold is not None:
                threshold = float(distance_threshold)
                scored_results = [(doc, score) for doc, score in scored_results if score <= threshold]
        docs = [doc for doc, _ in scored_results]
    else:
        retriever = store.as_retriever(search_kwargs={"k": int(k)})
        if hasattr(retriever, "invoke"):
            docs = retriever.invoke(args.question)
        else:
            docs = retriever.get_relevant_documents(args.question)

    if scored_results is None and (relevance_threshold is not None or distance_threshold is not None):
        print("Warning: threshold was set but scores were unavailable; threshold ignored.")

    rerank_scores = None
    if rerank_enabled and docs:
        try:
            from .rerank import RerankOptions, rerank_documents
            rerank_scores = rerank_documents(
                args.question,
                docs,
                RerankOptions(
                    enabled=True,
                    model=rerank_model,
                    top_n=int(rerank_top_n),
                    threshold=rerank_threshold if rerank_threshold is not None else None,
                ),
            )
            docs = [doc for doc, _ in rerank_scores]
        except ImportError as exc:
            print(f"Warning: rerank enabled but dependencies missing: {exc}. Continuing without rerank.")

    if not docs:
        print("No chunks met the relevance threshold. Try a lower threshold or disable it.")
        return

    context = "\n\n".join(doc.page_content for doc in docs)
    prompt = (
        "You are a helpful assistant. Use the provided context to answer the question.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {args.question}\n"
        "Answer in Spanish."
    )
    response = llm.invoke([SystemMessage(content="You are a helpful assistant."), HumanMessage(content=prompt)])
    answer = getattr(response, "content", response)
    print("Answer:")
    print(answer)

    if show_sources and docs:
        print("\nSources:")
        if scored_results is not None:
            for doc, score in scored_results:
                meta = doc.metadata or {}
                score_text = f"{score:.4f}" if isinstance(score, (int, float)) else str(score)
                print(f"- {meta.get('source')} (page: {meta.get('page')}) | {score_label}: {score_text}")
        else:
            for doc in docs:
                meta = doc.metadata or {}
                print(f"- {meta.get('source')} (page: {meta.get('page')}) | score: N/A")

    if rerank_scores is not None:
        print("\nRerank:")
        for doc, score in rerank_scores:
            meta = doc.metadata or {}
            score_text = f"{score:.4f}" if isinstance(score, (int, float)) else str(score)
            print(f"- {meta.get('source')} (page: {meta.get('page')}) | rerank_score: {score_text}")


def cmd_pipeline(args, cfg):
    from tqdm import tqdm
    from .chunking import chunk_documents, get_splitter, parse_chunk_kwargs
    from .documents import docs_to_records, records_to_docs
    from .extraction import ExtractionOptions, extract_pdf_to_documents
    from .utils import find_pdfs, iter_jsonl
    from .vectorstore import build_vectorstore, get_embeddings

    input_dir = _resolve(args.input_dir, deep_get(cfg, ["input_dir"]), None)
    output_dir = _resolve(args.work_dir, deep_get(cfg, ["output_dir"]), None)
    if not input_dir or not output_dir:
        raise SystemExit("pipeline requires --input-dir and --work-dir (or config input_dir/output_dir)")

    work_dir = Path(output_dir)
    work_dir.mkdir(parents=True, exist_ok=True)
    extract_output = work_dir / "extracted.jsonl"
    chunk_output = work_dir / "chunks.jsonl"
    persist_dir = _resolve(args.persist_dir, deep_get(cfg, ["indexing", "persist_dir"]), str(work_dir / "chroma"))

    # Reuse extract configuration
    extractor = _resolve(args.extractor, deep_get(cfg, ["extraction", "extractor"]), "pypdf")
    ocr_mode = _resolve(args.ocr, deep_get(cfg, ["extraction", "ocr"]), "auto")
    force_ocr = _resolve(args.force_ocr, deep_get(cfg, ["extraction", "force_ocr"]), False)
    ocr_lang = _resolve(args.ocr_lang, deep_get(cfg, ["extraction", "ocr_lang"]), "eng")
    easyocr_langs = _parse_easyocr_langs(
        _resolve(args.easyocr_lang, deep_get(cfg, ["extraction", "easyocr_langs"]), ["en"]),
        ["en"],
    )
    min_text = _resolve(args.min_text_per_page, deep_get(cfg, ["extraction", "min_text_per_page"]), 25)
    recursive = _resolve(args.recursive, deep_get(cfg, ["recursive"]), False)
    ocr_llm_model = _resolve(args.ocr_llm_model, deep_get(cfg, ["extraction", "ocr_llm_model"]), None)
    ocr_llm_max_tokens = _resolve(
        args.ocr_llm_max_tokens,
        deep_get(cfg, ["extraction", "ocr_llm_max_tokens"]),
        1024,
    )

    options = ExtractionOptions(
        extractor=extractor,
        ocr_mode=ocr_mode,
        force_ocr=bool(force_ocr),
        ocr_lang=ocr_lang,
        easyocr_langs=easyocr_langs,
        min_text_per_page=int(min_text),
        ocr_llm_model=ocr_llm_model,
        ocr_llm_max_tokens=int(ocr_llm_max_tokens),
    )

    pdfs = find_pdfs(input_dir, recursive=bool(recursive))
    if not pdfs:
        print("No PDFs found")
        return

    with extract_output.open("w", encoding="utf-8") as f:
        for pdf_path in tqdm(pdfs, desc="Extracting"):
            docs = extract_pdf_to_documents(pdf_path, options)
            for record in docs_to_records(docs):
                f.write(json.dumps(record, ensure_ascii=False) + "\n")

    chunker = _resolve(args.chunker, deep_get(cfg, ["chunking", "chunker"]), "recursive")
    chunk_size = _resolve(args.chunk_size, deep_get(cfg, ["chunking", "chunk_size"]), 1000)
    chunk_overlap = _resolve(args.chunk_overlap, deep_get(cfg, ["chunking", "chunk_overlap"]), 150)
    chunk_kwargs = _resolve(args.chunk_kwargs, deep_get(cfg, ["chunking", "chunk_kwargs"]), None)
    embedding_model = _resolve(
        args.embedding_model,
        deep_get(cfg, ["indexing", "embedding_model"]),
        "sentence-transformers/all-MiniLM-L6-v2",
    )
    collection = _resolve(args.collection, deep_get(cfg, ["indexing", "collection"]), "pdfs")

    splitter_kwargs = parse_chunk_kwargs(chunk_kwargs)
    embeddings = None
    if chunker == "semantic":
        embeddings = get_embeddings(embedding_model)

    splitter = get_splitter(
        chunker=chunker,
        chunk_size=int(chunk_size),
        chunk_overlap=int(chunk_overlap),
        chunk_kwargs=splitter_kwargs,
        embeddings=embeddings,
    )

    records = list(iter_jsonl(extract_output))
    docs = records_to_docs(records)
    chunks = chunk_documents(docs, splitter)
    with chunk_output.open("w", encoding="utf-8") as f:
        for record in docs_to_records(chunks):
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    build_vectorstore(
        documents=chunks,
        persist_dir=persist_dir,
        collection=collection,
        embedding_model=embedding_model,
    )

    print("Pipeline complete")
    print(f"Extracted: {extract_output}")
    print(f"Chunks: {chunk_output}")
    print(f"Chroma: {persist_dir} (collection: {collection})")


def _load_env(env_file: str | None) -> None:
    try:
        from dotenv import load_dotenv
    except Exception:
        return
    if env_file:
        load_dotenv(env_file)
    else:
        load_dotenv()


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    _load_env(args.env_file)
    cfg_path = resolve_config_path(args.config)
    cfg = load_config(cfg_path)

    if args.command == "list-options":
        cmd_list_options(args)
    elif args.command == "extract":
        cmd_extract(args, cfg)
    elif args.command == "chunk":
        cmd_chunk(args, cfg)
    elif args.command == "index":
        cmd_index(args, cfg)
    elif args.command == "query":
        cmd_query(args, cfg)
    elif args.command == "pipeline":
        cmd_pipeline(args, cfg)
    else:
        parser.error("Unknown command")


if __name__ == "__main__":
    main()
