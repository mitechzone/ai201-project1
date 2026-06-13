"""
Chunking Pipeline
=================
Ties ingestion and chunking together into a single importable entry point.

`build_chunks()` loads every cleaned document, chunks each one, tags every
chunk with its source filename, and returns a flat list. Milestone 4 imports
this directly to feed the embedding/vector-store stage — the `source` field
carries through as ChromaDB metadata for response attribution.
"""

from .chunker import FixedSizeChunker
from .ingest import DOCUMENTS_DIR, load_documents


def build_chunks(documents_dir: str = DOCUMENTS_DIR, chunker: FixedSizeChunker | None = None) -> list[dict]:
    """
    Load all documents and split them into a flat list of chunks.

    Each chunk dict carries:
        - text: the chunk content
        - index: position of the chunk within its source document
        - start_char: character offset within the source document
        - strategy: always "fixed_size"
        - source: source document filename (needed for attribution in M4/M5)

    Empty/whitespace-only chunks are filtered out.
    """
    chunker = chunker or FixedSizeChunker()
    documents = load_documents(documents_dir)

    all_chunks: list[dict] = []
    for doc in documents:
        for chunk in chunker.chunk(doc["text"]):
            if not chunk["text"].strip():
                continue  # drop empty / whitespace-only chunks
            chunk["source"] = doc["source"]
            all_chunks.append(chunk)

    return all_chunks
