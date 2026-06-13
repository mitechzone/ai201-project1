"""
Document Ingestion
==================
Loads the cleaned CS 6515 review documents from disk.

The documents in `documents/` were already cleaned manually in Milestone 2
(HTML, nav, boilerplate stripped), so this stage does NOT clean — it only
reads each file into memory and tags it with its source filename.
"""

import re
from pathlib import Path

# Directory holding the cleaned .txt review documents, relative to project root.
DOCUMENTS_DIR = "documents"


def _numeric_key(path: Path):
    """Sort key so 2.txt comes before 10.txt (numeric, not lexicographic)."""
    match = re.match(r"(\d+)", path.stem)
    # Files named with a leading number sort by that number; anything else
    # falls back to its name so the ordering stays deterministic.
    return (0, int(match.group(1))) if match else (1, path.stem)


def load_documents(documents_dir: str | Path = DOCUMENTS_DIR) -> list[dict]:
    """
    Load every .txt document from `documents_dir`.

    Returns
    -------
    list[dict]
        One dict per document: {"source": "1.txt", "text": <file contents>}.
        Sorted numerically by filename (1.txt, 2.txt, ..., 10.txt).
    """
    folder = Path(documents_dir)
    if not folder.is_dir():
        raise FileNotFoundError(f"Documents directory not found: {folder.resolve()}")

    files = sorted(folder.glob("*.txt"), key=_numeric_key)
    if not files:
        raise FileNotFoundError(f"No .txt documents found in {folder.resolve()}")

    documents = []
    for path in files:
        text = path.read_text(encoding="utf-8")
        documents.append({"source": path.name, "text": text})

    return documents
