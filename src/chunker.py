"""
Fixed-Size Chunker
==================
Splits text into chunks of a fixed character length with overlap. Makes no
attempt to respect word, sentence, or review boundaries — it splits wherever
the character count lands. This is the strategy specified in planning.md.

Sizing: planning.md specifies "300 tokens (~1,200 characters) / 50-token
(~200-character) overlap." We implement that at the character level, so
CHUNK_SIZE / OVERLAP are the ~1,200 / ~200 character operationalization.
"""

# Single source of truth for chunk sizing — reused by the embedding stage (M4).
CHUNK_SIZE = 1200   # characters per chunk (~300 tokens)
OVERLAP = 200       # characters repeated at the start of the next chunk (~50 tokens)


class FixedSizeChunker:
    """
    Splits text by character count with configurable size and overlap.

    Parameters
    ----------
    chunk_size : int
        Number of characters per chunk. Default: CHUNK_SIZE.
    overlap : int
        Number of characters repeated at the start of the next chunk. Overlap
        helps avoid cutting off context at chunk boundaries. Default: OVERLAP.
    """

    def __init__(self, chunk_size: int = CHUNK_SIZE, overlap: int = OVERLAP):
        if overlap >= chunk_size:
            raise ValueError("overlap must be smaller than chunk_size")
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, text: str) -> list[dict]:
        """
        Split text into fixed-size chunks.

        Returns a list of dicts with keys:
            - text: the chunk content
            - index: position of this chunk in the document
            - start_char: character offset where this chunk begins
            - strategy: always "fixed_size"
        """
        chunks = []
        start = 0
        index = 0

        while start < len(text):
            end = start + self.chunk_size
            chunks.append({
                "text": text[start:end],
                "index": index,
                "start_char": start,
                "strategy": "fixed_size",
            })
            # Advance by chunk_size minus overlap so the next chunk starts
            # slightly before the end of this one.
            start += self.chunk_size - self.overlap
            index += 1

        return chunks

    def __repr__(self):
        return f"FixedSizeChunker(chunk_size={self.chunk_size}, overlap={self.overlap})"
