"""
Recursive Chunker
=================
Splits text using a hierarchy of separators, trying each in order until chunks
are small enough: paragraph breaks first, then single newlines, then
sentence-ending punctuation, then spaces, then raw characters as a last
resort. This preserves natural document structure as much as possible — the
opposite tradeoff to the fixed-size chunker, which splits blindly at a
character count.

This mirrors the RecursiveChunker from the Week 1 lecture demo, which itself
follows LangChain's RecursiveCharacterTextSplitter. For our review corpus the
paragraph-first hierarchy tends to keep an individual student's review (or a
self-contained paragraph of it) intact rather than cutting mid-thought.
"""

# Default sizing mirrors the fixed-size strategy so the two are comparable;
# imported here as a single source of truth for the project's chunk sizing.
from .chunker import CHUNK_SIZE, OVERLAP


class RecursiveChunker:
    """
    Splits text recursively using a hierarchy of separators.

    Parameters
    ----------
    chunk_size : int
        Target maximum character length for each chunk. Default: CHUNK_SIZE.
    overlap : int
        Characters repeated at chunk boundaries for context continuity.
        Default: OVERLAP.
    separators : list[str] | None
        Ordered list of separators to try. Defaults to a standard hierarchy.
    """

    DEFAULT_SEPARATORS = ["\n\n", "\n", ". ", "! ", "? ", " ", ""]

    def __init__(
        self,
        chunk_size: int = CHUNK_SIZE,
        overlap: int = OVERLAP,
        separators: list[str] | None = None,
    ):
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.separators = separators or self.DEFAULT_SEPARATORS

    def _split_text(self, text: str, separators: list[str]) -> list[str]:
        """
        Recursively split text using the first separator that produces chunks
        within the target size. Falls back to the next separator if needed.
        """
        if not separators:
            # Base case: no separators left — return as-is.
            return [text]

        separator = separators[0]
        remaining_separators = separators[1:]

        if separator == "":
            # Character-level split as last resort.
            step = self.chunk_size - self.overlap
            return [text[i:i + self.chunk_size] for i in range(0, len(text), step)]

        splits = text.split(separator)

        good_splits: list[str] = []
        current: list[str] = []
        current_len = 0

        for split in splits:
            split_len = len(split)

            if current_len + split_len + len(separator) > self.chunk_size and current:
                # Current accumulation is full — finalize it.
                good_splits.append(separator.join(current))
                # Keep overlap: retain the tail of current for context continuity.
                overlap_text = separator.join(current)
                tail = overlap_text[-self.overlap:] if self.overlap > 0 else ""
                # If the slice landed mid-word, drop the leading partial word so
                # the next chunk starts on a word boundary.
                if len(overlap_text) > self.overlap and not tail[:1].isspace():
                    space = tail.find(" ")
                    if space != -1:
                        tail = tail[space + 1:]
                current = [tail] if tail else []
                current_len = len(current[0]) if current else 0

            if split_len > self.chunk_size:
                # This individual split is too large — recurse with next separator.
                if current:
                    good_splits.append(separator.join(current))
                    current = []
                    current_len = 0
                good_splits.extend(self._split_text(split, remaining_separators))
            else:
                current.append(split)
                current_len += split_len + len(separator)

        if current:
            good_splits.append(separator.join(current))

        return [s for s in good_splits if s.strip()]

    def chunk(self, text: str) -> list[dict]:
        """
        Split text into chunks using the recursive separator hierarchy.

        Returns a list of dicts with keys:
            - text: the chunk content
            - index: position of this chunk in the document
            - strategy: always "recursive"
        """
        raw_chunks = self._split_text(text, self.separators)
        return [
            {
                "text": chunk_text.strip(),
                "index": i,
                "strategy": "recursive",
            }
            for i, chunk_text in enumerate(raw_chunks)
            if chunk_text.strip()
        ]

    def __repr__(self):
        return f"RecursiveChunker(chunk_size={self.chunk_size}, overlap={self.overlap})"
