from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional

from langchain_core.documents import Document

from .ocr import ocr_pdf_pages
from .options import EXTRACTORS, OCR_MODES
from .utils import safe_import


@dataclass
class ExtractionOptions:
    extractor: str
    ocr_mode: str
    force_ocr: bool
    ocr_lang: str
    easyocr_langs: list[str]
    min_text_per_page: int
    ocr_llm_model: Optional[str] = None
    ocr_llm_max_tokens: int = 1024


def _count_pages_pypdf(pdf_path: Path) -> int:
    pypdf = safe_import("pypdf", "pypdf")
    reader = pypdf.PdfReader(str(pdf_path))
    return len(reader.pages)


def _extract_pages_pypdf(pdf_path: Path) -> list[str]:
    pypdf = safe_import("pypdf", "pypdf")
    reader = pypdf.PdfReader(str(pdf_path))
    pages = []
    for page in reader.pages:
        text = page.extract_text() or ""
        pages.append(text)
    return pages


def _extract_pages_pdfplumber(pdf_path: Path) -> list[str]:
    pdfplumber = safe_import("pdfplumber", "pdfplumber")
    pages = []
    with pdfplumber.open(str(pdf_path)) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            pages.append(text)
    return pages


def _extract_pages_pymupdf(pdf_path: Path) -> list[str]:
    fitz = safe_import("fitz", "pymupdf")
    pages = []
    doc = fitz.open(str(pdf_path))
    for page in doc:
        text = page.get_text() or ""
        pages.append(text)
    doc.close()
    return pages


def _extract_pages_pdfminer(pdf_path: Path) -> list[str]:
    pdfminer = safe_import("pdfminer", "pdfminer.six")
    from pdfminer.high_level import extract_text

    text = extract_text(str(pdf_path)) or ""
    # pdfminer uses form feed for page breaks
    pages = [page for page in text.split("\f") if page is not None]
    # trim trailing empty page if needed
    if pages and not pages[-1].strip():
        pages = pages[:-1]
    return pages if pages else [""]


def _extract_pages_unstructured(pdf_path: Path) -> list[str]:
    loader_mod = safe_import(
        "langchain_community.document_loaders",
        "langchain-community (for UnstructuredPDFLoader)",
    )
    try:
        loader_cls = loader_mod.UnstructuredPDFLoader
    except AttributeError as exc:
        raise ImportError("UnstructuredPDFLoader not available in langchain-community") from exc

    loader = loader_cls(str(pdf_path))
    docs = loader.load()
    page_texts: dict[int, list[str]] = {}
    has_page = False
    for doc in docs:
        meta = doc.metadata or {}
        page = meta.get("page")
        if page is None:
            page = meta.get("page_number")
        if page is not None:
            has_page = True
            page_texts.setdefault(int(page), []).append(doc.page_content)
    if has_page:
        pages = []
        for idx in sorted(page_texts.keys()):
            pages.append("\n".join(page_texts[idx]).strip())
        return pages

    # fallback to a single combined document
    combined = "\n".join(d.page_content for d in docs).strip()
    return [combined]


def extract_pages_native(pdf_path: Path, extractor: str) -> list[str]:
    if extractor == "pypdf":
        return _extract_pages_pypdf(pdf_path)
    if extractor == "pdfplumber":
        return _extract_pages_pdfplumber(pdf_path)
    if extractor == "pymupdf":
        return _extract_pages_pymupdf(pdf_path)
    if extractor == "pdfminer":
        return _extract_pages_pdfminer(pdf_path)
    if extractor == "unstructured":
        return _extract_pages_unstructured(pdf_path)
    raise ValueError(f"Unknown extractor: {extractor}")


def extract_pdf_to_documents(
    pdf_path: Path,
    options: ExtractionOptions,
) -> list[Document]:
    num_pages = _count_pages_pypdf(pdf_path)
    ocr_engine = options.ocr_mode if options.ocr_mode in ("tesseract", "easyocr", "llm") else "tesseract"

    if options.force_ocr:
        ocr_texts = ocr_pdf_pages(
            pdf_path,
            engine=ocr_engine,
            ocr_lang=options.ocr_lang,
            easyocr_langs=options.easyocr_langs,
            llm_model=options.ocr_llm_model,
            llm_max_tokens=options.ocr_llm_max_tokens,
        )
        return _docs_from_page_texts(
            ocr_texts,
            pdf_path,
            extractor=options.extractor,
            ocr_engine=options.ocr_mode,
            page_count=num_pages,
            ocr_used=True,
        )

    native_pages = extract_pages_native(pdf_path, options.extractor)

    if options.ocr_mode == "off":
        return _docs_from_page_texts(
            native_pages,
            pdf_path,
            extractor=options.extractor,
            ocr_engine=None,
            page_count=num_pages,
            ocr_used=False,
        )

    # Decide OCR usage
    needs_ocr = []
    if len(native_pages) == num_pages:
        for text in native_pages:
            needs_ocr.append(len((text or "").strip()) < options.min_text_per_page)
    else:
        # No per-page alignment; use OCR for the whole document if native text is sparse
        sparse = all(len((text or "").strip()) < options.min_text_per_page for text in native_pages)
        needs_ocr = [sparse] * num_pages

    if not any(needs_ocr):
        return _docs_from_page_texts(
            native_pages,
            pdf_path,
            extractor=options.extractor,
            ocr_engine=None,
            page_count=num_pages,
            ocr_used=False,
        )

    ocr_texts = ocr_pdf_pages(
        pdf_path,
        engine=ocr_engine,
        ocr_lang=options.ocr_lang,
        easyocr_langs=options.easyocr_langs,
        llm_model=options.ocr_llm_model,
        llm_max_tokens=options.ocr_llm_max_tokens,
    )

    if len(native_pages) != num_pages:
        # In case of non-aligned native pages, return OCR results for all pages
        return _docs_from_page_texts(
            ocr_texts,
            pdf_path,
            extractor=options.extractor,
            ocr_engine=options.ocr_mode,
            page_count=num_pages,
            ocr_used=True,
        )

    merged_pages = []
    for idx, text in enumerate(native_pages):
        if idx < len(ocr_texts) and needs_ocr[idx]:
            merged_pages.append(ocr_texts[idx])
        else:
            merged_pages.append(text)

    return _docs_from_page_texts(
        merged_pages,
        pdf_path,
        extractor=options.extractor,
        ocr_engine=ocr_engine,
        page_count=num_pages,
        ocr_used=any(needs_ocr),
    )


def _docs_from_page_texts(
    pages: list[str],
    pdf_path: Path,
    extractor: str,
    ocr_engine: Optional[str],
    page_count: int,
    ocr_used: bool,
) -> list[Document]:
    docs: list[Document] = []
    if not pages:
        pages = [""]

    if len(pages) == page_count:
        for idx, text in enumerate(pages):
            docs.append(
                Document(
                    page_content=text or "",
                    metadata={
                        "source": str(pdf_path),
                        "page": idx,
                        "page_count": page_count,
                        "extractor": extractor,
                        "ocr_engine": ocr_engine if ocr_used else None,
                        "ocr_used": bool(ocr_used and (text or "").strip()),
                    },
                )
            )
        return docs

    # Non-aligned extractors return a single document
    combined = "\n".join(pages).strip()
    docs.append(
        Document(
            page_content=combined,
            metadata={
                "source": str(pdf_path),
                "page": None,
                "page_count": page_count,
                "extractor": extractor,
                "ocr_engine": ocr_engine if ocr_used else None,
                "ocr_used": bool(ocr_used),
            },
        )
    )
    return docs
