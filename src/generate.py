"""
Grounded Generation
===================
Connects retrieval to the Groq LLM to produce answers grounded in the
retrieved review chunks only — never the model's training knowledge.

Attribution uses citation markers: each chunk is numbered in the context,
the model is instructed to cite the marker(s) it used after each claim, and
we parse those markers back out of the answer. This tells us which chunks the
model itself pointed to (verifiable by reading the chunk), rather than blindly
claiming all retrieved chunks were used.
"""

import re

from dotenv import load_dotenv
from groq import Groq

from .retrieval import STRATEGIES, retrieve

load_dotenv()

GROQ_MODEL = "llama-3.3-70b-versatile"
TEMPERATURE = 0.2
MAX_TOKENS = 400

# Exact sentence the model must return when the context can't answer the question.
INSUFFICIENT = "The retrieved sources don't contain enough information to answer that."

SYSTEM_PROMPT = (
    "You are a helpful assistant answering questions about Georgia Tech's CS 6515 Graduate Algorithms (GA) course "
    "using ONLY the numbered context below, which is excerpts from student reviews. "
    "Follow these rules strictly:\n"
    "1. Use only information in the numbered context. Never use outside knowledge or fill in gaps from what you already know.\n"
    "2. After each claim, cite the marker(s) it came from, e.g. 'Exams are 30% each [1].'\n"
    f"3. If the context does not contain enough information to answer, reply with exactly this sentence and nothing else: {INSUFFICIENT}\n"
    "Keep the answer concise (2-5 sentences)."
)

_client: Groq | None = None


def _get_client() -> Groq:
    global _client
    if _client is None:
        _client = Groq()  # reads GROQ_API_KEY from the environment
    return _client


def _format_context(chunks: list[dict]) -> str:
    """Number each chunk and label it with its source for citation."""
    return "\n\n---\n\n".join(
        f"[{i}] (Source: {c['source']}, chunk {c['index']})\n{c['text']}"
        for i, c in enumerate(chunks, 1)
    )


def generate_answer(query: str, chunks: list[dict]) -> str:
    """Call the LLM with the numbered context and return its raw answer."""
    user_prompt = (
        f"Context:\n{_format_context(chunks)}\n\n"
        f"Question: {query}\n\nAnswer:"
    )
    response = _get_client().chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
    )
    return response.choices[0].message.content.strip()


def _parse_citations(answer: str, chunks: list[dict]) -> list[dict]:
    """
    Extract [n] markers from the answer and map them to chunks.

    Markers are 1-based (matching _format_context). Handles grouped markers
    like "[1, 2]", "[1,2]", and "[1][2]". Out-of-range or duplicate markers
    are ignored. Returns the cited chunks in first-cited order.
    """
    seen: set[int] = set()
    cited: list[dict] = []
    # Match any bracket group containing digits/commas/spaces, e.g. [1] or [1, 2].
    for group in re.findall(r"\[([\d,\s]+)\]", answer):
        for num in re.findall(r"\d+", group):
            n = int(num)
            if 1 <= n <= len(chunks) and n not in seen:
                seen.add(n)
                cited.append(chunks[n - 1])
    return cited


def ask(query: str, strategy: str = "recursive", k: int = 5) -> dict:
    """
    End-to-end: retrieve from one strategy, generate a grounded answer, and
    resolve which chunks the model cited.

    Returns a dict with:
        answer        : the model's answer (with inline [n] markers), or INSUFFICIENT
        strategy      : the chunking strategy used
        chunks        : all retrieved chunks (supplied to the model)
        cited         : the chunks the model cited via [n] markers
        cited_sources : deduped source filenames from `cited` (first-cited order)
    """
    chunks = retrieve(query, strategy, k=k)
    if not chunks:
        return {"answer": INSUFFICIENT, "strategy": strategy,
                "chunks": [], "cited": [], "cited_sources": []}

    answer = generate_answer(query, chunks)
    cited = _parse_citations(answer, chunks)

    cited_sources: list[str] = []
    for c in cited:
        if c["source"] not in cited_sources:
            cited_sources.append(c["source"])

    return {"answer": answer, "strategy": strategy, "chunks": chunks,
            "cited": cited, "cited_sources": cited_sources}


def ask_compare(query: str, k: int = 5) -> dict[str, dict]:
    """Run `ask` for every strategy, keyed by strategy name (compare mode)."""
    return {strategy: ask(query, strategy, k=k) for strategy in STRATEGIES}
