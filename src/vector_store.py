"""
Vector Store
============
A thin wrapper around ChromaDB, bound to a single chunking strategy.

Each VectorStore instance owns its own persist directory
(chroma_db/<strategy>/) and its own PersistentClient, so chunks from
different chunking strategies live in completely separate databases and can
never be mixed or cross-retrieved.

Embeddings use sentence-transformers (all-MiniLM-L6-v2) — local, free, no API
key. Collections use cosine distance so the raw distances we report fall in
the 0–2 range the project's relevance thresholds assume.
"""

import chromadb
from chromadb.utils import embedding_functions

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
PERSIST_ROOT = "chroma_db"
COLLECTION_NAME = "chunks"


class VectorStore:
    """
    Manages a single ChromaDB collection for one chunking strategy.

    Parameters
    ----------
    strategy : str
        The chunking strategy this store holds (e.g. "fixed_size",
        "recursive"). Determines the persist directory: chroma_db/<strategy>/.
    persist_root : str
        Root directory under which each strategy gets its own subdirectory.
        Default: "chroma_db".
    """

    def __init__(self, strategy: str, persist_root: str = PERSIST_ROOT):
        self.strategy = strategy
        self.persist_dir = f"{persist_root}/{strategy}"
        self.client = chromadb.PersistentClient(path=self.persist_dir)
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=EMBEDDING_MODEL
        )

    def get_or_create_collection(self) -> chromadb.Collection:
        """Get or create this strategy's collection (cosine distance)."""
        return self.client.get_or_create_collection(
            name=COLLECTION_NAME,
            embedding_function=self.embedding_fn,
            metadata={"hnsw:space": "cosine"},
        )

    def reset_collection(self) -> chromadb.Collection:
        """Delete and recreate the collection — used for a clean re-index."""
        try:
            self.client.delete_collection(COLLECTION_NAME)
        except Exception:
            pass  # Collection didn't exist yet
        return self.client.create_collection(
            name=COLLECTION_NAME,
            embedding_function=self.embedding_fn,
            metadata={"hnsw:space": "cosine"},
        )

    def add_chunks(self, chunks: list[dict]) -> None:
        """
        Embed and store a flat list of chunk dicts.

        Each chunk must carry "text", "index", and "source" (the source
        document filename). IDs combine source + index so the per-document
        index stays unique across documents.
        """
        collection = self.get_or_create_collection()

        documents = [c["text"] for c in chunks]
        ids = [f"{c['source']}_{c['index']}" for c in chunks]
        metadatas = [
            {
                "source": c["source"],
                "strategy": self.strategy,
                "index": c["index"],
                "char_count": len(c["text"]),
            }
            for c in chunks
        ]

        collection.add(documents=documents, ids=ids, metadatas=metadatas)

    def query(self, query_text: str, n_results: int = 5) -> list[dict]:
        """
        Return the top-k chunks for a query, with their raw ChromaDB distance.

        Lower distance = closer match. With cosine space, distances fall in
        roughly 0–2; the project treats top results below ~0.5 as strong.
        """
        collection = self.get_or_create_collection()
        results = collection.query(
            query_texts=[query_text],
            n_results=n_results,
            include=["documents", "metadatas", "distances"],
        )

        output = []
        for doc, meta, dist in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        ):
            output.append({
                "text": doc,
                "distance": round(dist, 4),
                "source": meta.get("source", "unknown"),
                "strategy": meta.get("strategy", self.strategy),
                "index": meta.get("index", -1),
                "char_count": meta.get("char_count", len(doc)),
            })

        return output

    def stats(self) -> dict:
        """Return chunk count + average char_count for this strategy's store."""
        collection = self.get_or_create_collection()
        count = collection.count()
        if count == 0:
            return {"strategy": self.strategy, "chunk_count": 0, "avg_char_count": 0}

        all_items = collection.get(include=["metadatas"])
        char_counts = [m.get("char_count", 0) for m in all_items["metadatas"]]
        avg = sum(char_counts) / len(char_counts) if char_counts else 0

        return {
            "strategy": self.strategy,
            "chunk_count": count,
            "avg_char_count": round(avg),
        }

    def __repr__(self):
        return f"VectorStore(strategy={self.strategy!r}, persist_dir={self.persist_dir!r})"
