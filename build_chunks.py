"""
Build & inspect document chunks.

Run from the project root:

    python build_chunks.py

Loads the cleaned CS 6515 review documents and splits them with TWO chunking
strategies — fixed-size and recursive — reporting each separately (count,
per-document stats, sample chunks, sanity scans). Writes one JSONL artifact
per strategy: chunks-fixed.jsonl and chunks-recursive.jsonl.
"""

import json
import random
import re
from collections import Counter
from pathlib import Path

from src.chunker import CHUNK_SIZE, OVERLAP, FixedSizeChunker
from src.ingest import load_documents
from src.pipeline import build_chunks
from src.recursive_chunker import RecursiveChunker

# Strategies to build: (label, chunker, output path). Both use the same
# target sizing (CHUNK_SIZE/OVERLAP) so the two are directly comparable.
STRATEGIES = [
    ("fixed", FixedSizeChunker(CHUNK_SIZE, OVERLAP), Path("chunks-fixed.jsonl")),
    ("recursive", RecursiveChunker(CHUNK_SIZE, OVERLAP), Path("chunks-recursive.jsonl")),
]

# Fewer than this many chunks => probably too large; more => probably too small.
MIN_CHUNKS = 50
MAX_CHUNKS = 2000

# Cleaning was done in Milestone 2 — these scans confirm nothing slipped through.
HTML_TAG = re.compile(r"<[^>]+>")
HTML_ENTITY = re.compile(r"&(amp|nbsp|lt|gt|#\d+);")


def _numeric_key(source: str):
    match = re.match(r"(\d+)", source)
    return (0, int(match.group(1))) if match else (1, source)


def _print_per_document_table(chunks: list[dict], doc_chars: dict[str, int]) -> None:
    by_source = Counter(c["source"] for c in chunks)
    print(f"{'Document':<12}{'Doc chars':>12}{'Chunks':>10}")
    print("-" * 34)
    for source in sorted(by_source, key=_numeric_key):
        print(f"{source:<12}{doc_chars.get(source, 0):>12,}{by_source[source]:>10}")
    print()


def _print_size_stats(chunks: list[dict]) -> None:
    sizes = [len(c["text"]) for c in chunks]
    avg = sum(sizes) // len(sizes)
    print(f"Chunk size (chars):  avg {avg:,}   min {min(sizes):,}   max {max(sizes):,}")
    print()


def _print_sample_chunks(chunks: list[dict], n: int = 5, max_per_source: int = 2) -> None:
    # Random sample, but cap per source so a high-volume file like 1.txt
    # doesn't dominate the inspection set.
    pool = list(chunks)
    random.shuffle(pool)

    picked: list[dict] = []
    per_source: Counter = Counter()
    for c in pool:
        if len(picked) >= n:
            break
        if per_source[c["source"]] >= max_per_source:
            continue
        picked.append(c)
        per_source[c["source"]] += 1

    print(f"=== {len(picked)} representative chunks (random, max {max_per_source}/file) ===\n")
    for c in picked:
        print(f"--- {c['source']}  (chunk index {c['index']}, {len(c['text'])} chars) ---")
        print(c["text"])
        print()


def _print_sanity_scans(chunks: list[dict]) -> None:
    empty = sum(1 for c in chunks if not c["text"].strip())
    html = [c for c in chunks if HTML_TAG.search(c["text"]) or HTML_ENTITY.search(c["text"])]

    print("=== Sanity scans ===")
    print(f"Empty chunks: {empty}")
    if html:
        print(f"⚠ Chunks with HTML tags/entities: {len(html)} (first: "
              f"{html[0]['source']} #{html[0]['index']}) — clean further before embedding")
    else:
        print("HTML tags/entities: none found")
    print()


def _report_strategy(label: str, chunker, output_path: Path, doc_chars: dict[str, int]) -> int:
    """Build, inspect, and persist chunks for a single strategy. Returns the count."""
    chunks = build_chunks(chunker=chunker)

    print("\n" + "=" * 60)
    print(f"STRATEGY: {label}   {chunker!r}")
    print("=" * 60 + "\n")

    total = len(chunks)
    print(f"=== Total chunks: {total} ===")
    if total < MIN_CHUNKS:
        print(f"⚠ Below {MIN_CHUNKS} — chunks may be too large (specific queries can't match precisely).")
    elif total > MAX_CHUNKS:
        print(f"⚠ Above {MAX_CHUNKS} — chunks may be too small (each carries too little semantic signal).")
    else:
        print(f"✓ Within the recommended {MIN_CHUNKS}–{MAX_CHUNKS} range.")
    print()

    _print_per_document_table(chunks, doc_chars)
    _print_size_stats(chunks)
    _print_sample_chunks(chunks)
    _print_sanity_scans(chunks)

    with output_path.open("w", encoding="utf-8") as f:
        for c in chunks:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    print(f"Wrote {total} chunks to {output_path}")

    return total


def main() -> None:
    # True per-document character counts (accurate for any strategy, including
    # the recursive chunker whose chunks carry no start_char offset).
    doc_chars = {d["source"]: len(d["text"]) for d in load_documents()}

    counts: dict[str, int] = {}
    for label, chunker, output_path in STRATEGIES:
        counts[label] = _report_strategy(label, chunker, output_path, doc_chars)

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for label, total in counts.items():
        print(f"  {label:<10} {total:>6} chunks")


if __name__ == "__main__":
    main()
