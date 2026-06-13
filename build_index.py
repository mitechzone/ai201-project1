"""
Build the vector-store indexes.

Run from the project root (after build_chunks.py):

    python build_index.py

Reads each strategy's chunk artifact and embeds it into that strategy's own
isolated ChromaDB under chroma_db/<strategy>/. The two strategies are built
independently and never share a database.
"""

import json
from pathlib import Path

from src.retrieval import STRATEGIES
from src.vector_store import VectorStore

# Each strategy's chunk artifact, produced by build_chunks.py.
CHUNK_FILES = {
    "fixed_size": "chunks-fixed.jsonl",
    "recursive": "chunks-recursive.jsonl",
}


def load_chunks(path: str) -> list[dict]:
    """Read a JSONL chunk artifact into a list of chunk dicts."""
    file = Path(path)
    if not file.is_file():
        raise FileNotFoundError(
            f"Chunk artifact not found: {file.resolve()} — run build_chunks.py first."
        )
    with file.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def main() -> None:
    for strategy in STRATEGIES:
        chunk_file = CHUNK_FILES[strategy]
        print(f"\n[{strategy}] loading {chunk_file} ...", flush=True)
        chunks = load_chunks(chunk_file)

        store = VectorStore(strategy)
        print(f"[{strategy}] resetting {store.persist_dir} and embedding "
              f"{len(chunks)} chunks (this can take a moment) ...", flush=True)
        store.reset_collection()
        store.add_chunks(chunks)

        s = store.stats()
        print(f"[{strategy}] done: {s['chunk_count']} chunks, "
              f"avg {s['avg_char_count']} chars  →  {store.persist_dir}")

    print("\nAll indexes built. Each strategy is stored separately under chroma_db/.")


if __name__ == "__main__":
    main()
