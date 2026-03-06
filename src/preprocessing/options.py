"""Lightweight option lists used by the CLI without heavy imports."""

EXTRACTORS = ["pypdf", "pdfplumber", "pymupdf", "pdfminer", "unstructured"]
OCR_MODES = ["auto", "tesseract", "easyocr", "llm", "off"]
CHUNKERS = [
    "recursive",
    "character",
    "token",
    "nltk",
    "spacy",
    "markdown",
    "html",
    "latex",
    "semantic",
]


def list_extractors() -> list[str]:
    return EXTRACTORS


def list_ocr_modes() -> list[str]:
    return OCR_MODES


def list_chunkers() -> list[str]:
    return CHUNKERS
