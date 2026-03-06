from __future__ import annotations

from typing import Any, Dict, Iterable, List

from langchain_core.documents import Document


def docs_to_records(docs: Iterable[Document]) -> List[Dict[str, Any]]:
    return [
        {
            "text": doc.page_content,
            "metadata": doc.metadata or {},
        }
        for doc in docs
    ]


def records_to_docs(records: Iterable[Dict[str, Any]]) -> List[Document]:
    docs = []
    for record in records:
        text = record.get("text", "")
        metadata = record.get("metadata") or {}
        docs.append(Document(page_content=text, metadata=metadata))
    return docs

