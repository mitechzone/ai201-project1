"""
Retrieval
=========
The reusable retrieval API over the per-strategy vector stores.

Each chunking strategy has its own isolated ChromaDB (see vector_store.py),
so retrieving from one strategy never touches the other's database.
"""

from .vector_store import VectorStore

STRATEGIES = ["fixed_size", "recursive"]

# Lazily-opened VectorStore per strategy — each opens its own DB on first use.
_stores: dict[str, VectorStore] = {}


def _get_store(strategy: str) -> VectorStore:
    if strategy not in STRATEGIES:
        raise ValueError(f"Unknown strategy {strategy!r}. Choose from: {STRATEGIES}")
    if strategy not in _stores:
        _stores[strategy] = VectorStore(strategy)
    return _stores[strategy]


def retrieve(query: str, strategy: str, k: int = 5) -> list[dict]:
    """Return the top-k chunks for a query from a single strategy's store."""
    return _get_store(strategy).query(query, n_results=k)


def retrieve_strategies(
    query: str, strategies: list[str] = STRATEGIES, k: int = 5
) -> dict[str, list[dict]]:
    """
    Retrieve from multiple strategies, keyed by strategy name.

    Each strategy is queried against its own separate database; results are
    kept in separate lists, never merged into one ranking.
    """
    return {s: retrieve(query, s, k) for s in strategies}
