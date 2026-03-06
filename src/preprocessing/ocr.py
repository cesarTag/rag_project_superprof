from __future__ import annotations

import base64
from io import BytesIO
from pathlib import Path
from typing import Optional

from .utils import safe_import


OCR_ENGINES = ["tesseract", "easyocr", "llm"]


def ocr_pdf_pages(
    pdf_path: Path,
    engine: str,
    ocr_lang: str,
    easyocr_langs: list[str],
    llm_model: Optional[str],
    llm_max_tokens: int,
) -> list[str]:
    if engine not in OCR_ENGINES:
        raise ValueError(f"Unsupported OCR engine: {engine}")

    images = _render_pdf(pdf_path)
    if engine == "tesseract":
        return [_ocr_tesseract(img, ocr_lang) for img in images]
    if engine == "easyocr":
        return _ocr_easyocr(images, easyocr_langs)
    if engine == "llm":
        return _ocr_llm(images, llm_model=llm_model, max_tokens=llm_max_tokens)
    raise ValueError(f"Unknown OCR engine: {engine}")


def _render_pdf(pdf_path: Path) -> list:
    pdf2image = safe_import("pdf2image", "pdf2image")
    return pdf2image.convert_from_path(str(pdf_path), dpi=300)


def _ocr_tesseract(image, lang: str) -> str:
    pytesseract = safe_import("pytesseract", "pytesseract")
    return pytesseract.image_to_string(image, lang=lang) or ""


def _ocr_easyocr(images, langs: list[str]) -> list[str]:
    easyocr = safe_import("easyocr", "easyocr")
    reader = easyocr.Reader(langs, gpu=False)
    results = []
    for image in images:
        text = reader.readtext(image, detail=0, paragraph=True)
        results.append("\n".join(text).strip())
    return results


def _ocr_llm(images, llm_model: Optional[str], max_tokens: int) -> list[str]:
    #llm_model = "claude-haiku-4-5"
    if not llm_model:
        raise ValueError("LLM OCR requires --ocr-llm-model")

    langchain_messages = safe_import("langchain_core.messages", "langchain-core")
    langchain_anthropic = safe_import("langchain_anthropic", "langchain-anthropic")

    HumanMessage = langchain_messages.HumanMessage
    ChatAnthropic = langchain_anthropic.ChatAnthropic

    llm = ChatAnthropic(model=llm_model, max_tokens=max_tokens)
    results = []
    for image in images:
        payload = _image_to_base64(image)
        message = HumanMessage(
            content=[
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": payload,
                    },
                },
                {
                    "type": "text",
                    "text": "Transcribe the page exactly. Return only the text.",
                },
            ]
        )
        response = llm.invoke([message])
        results.append(str(getattr(response, "content", "")) or "")
    return results


def _image_to_base64(image) -> str:
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")

