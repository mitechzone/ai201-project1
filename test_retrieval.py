"""
Test retrieval

Run from the project root (after build_index.py):

    python test_retrieval.py                    # all eval questions, both strategies
    python test_retrieval.py --strategy recursive
    python test_retrieval.py --query "How many exams does GA have?" -k 5

Prints the top-k retrieved chunks and their raw ChromaDB distance (lower =
closer). Each strategy is queried against its own separate database and shown
in its own block — results are never merged into one ranking.
"""

import argparse

from src.retrieval import STRATEGIES, retrieve

# Querying your vector store with 3 of your test questions returns chunks that visibly relate to each question.
EVAL_QUERIES = [
    "Is GA a core course for all OMSCS specializations?",
    "How many exams does GA typically have in recent semesters?",
    "What's the cut score to pass GA in recent semesters?",
]

# Top results below this raw cosine distance are treated as strong matches.
STRONG_MATCH = 0.5
PREVIEW_CHARS = 260


def _print_results(strategy: str, query: str, results: list[dict]) -> None:
    print(f"\n  [{strategy}]")
    if not results:
        print("    (no results — is the index built? run build_index.py)")
        return

    for rank, r in enumerate(results, 1):
        flag = "strong" if r["distance"] < STRONG_MATCH else "weak"
        text = " ".join(r["text"].split())  # collapse whitespace for preview
        preview = text[:PREVIEW_CHARS] + ("..." if len(text) > PREVIEW_CHARS else "")
        print(f"    {rank}. distance {r['distance']:.4f} [{flag}]  "
              f"source={r['source']} #{r['index']}")
        print(f"       {preview}")

    distances = [r["distance"] for r in results]
    best = min(distances)
    avg = sum(distances) / len(distances)
    verdict = "PASS (top < 0.5)" if best < STRONG_MATCH else "weak — review chunks"
    print(f"    summary: best {best:.4f} | avg {avg:.4f}  →  {verdict}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Test retrieval over the chunk indexes.")
    parser.add_argument(
        "--strategy", choices=[*STRATEGIES, "both"], default="both",
        help="Which chunking strategy's index to query (default: both).",
    )
    parser.add_argument("--query", help="Run a single custom query instead of the eval set.")
    parser.add_argument("-k", type=int, default=5, help="Number of chunks to retrieve (default: 5).")
    args = parser.parse_args()

    strategies = STRATEGIES if args.strategy == "both" else [args.strategy]
    queries = [args.query] if args.query else EVAL_QUERIES

    for query in queries:
        print("\n" + "=" * 72)
        print(f"QUERY: {query}")
        print("=" * 72)
        for strategy in strategies:
            _print_results(strategy, query, retrieve(query, strategy, k=args.k))


if __name__ == "__main__":
    main()
