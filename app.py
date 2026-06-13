"""
The Unofficial Guide — CS 6515 (Graduate Algorithms) Q&A.

A Gradio interface over the grounded RAG pipeline. Ask a question about GA and
get an answer drawn only from student reviews, with the sources the model
cited. Switch chunking strategy, or compare both side-by-side.

Run from the project root (after build_index.py):

    python app.py        # then open http://localhost:7860
"""

import gradio as gr
from dotenv import load_dotenv

from src.generate import INSUFFICIENT, ask, ask_compare

load_dotenv()

MODES = ["recursive", "fixed_size", "compare both"]


def _marker(chunks: list[dict], chunk: dict) -> int:
    """The 1-based position of a cited chunk in the supplied context."""
    for i, c in enumerate(chunks, 1):
        if c is chunk:
            return i
    return 0


def _format_sources(result: dict) -> str:
    """Render 'Sources cited' — the exact chunk(s) the model used, with their text."""
    if result["answer"] == INSUFFICIENT:
        return "_No sources — the model declined to answer._"
    if not result["cited"]:
        # The model answered but cited no markers — be honest about it.
        retrieved = sorted({c["source"] for c in result["chunks"]})
        return (
            "_Model did not cite specific chunks. Retrieved from:_ "
            + ", ".join(f"`{s}`" for s in retrieved)
        )

    blocks = []
    for c in result["cited"]:
        n = _marker(result["chunks"], c)
        text = " ".join(c["text"].split())
        blocks.append(
            f"**[{n}] `{c['source']}` — chunk {c['index']}** "
            f"(distance {c['distance']:.3f})\n\n> {text}"
        )
    return "\n\n".join(blocks)


def _format_retrieved(result: dict) -> str:
    """Render the expandable 'Retrieved context' block (supplied, not necessarily used)."""
    if not result["chunks"]:
        return "_Nothing retrieved._"
    lines = []
    for i, c in enumerate(result["chunks"], 1):
        preview = " ".join(c["text"].split())[:240]
        lines.append(
            f"**[{i}]** `{c['source']}` (chunk {c['index']}, distance {c['distance']:.3f})\n\n"
            f"> {preview}…\n"
        )
    return "\n".join(lines)


def handle_query(question: str, mode: str, k: int):
    """Return (answer_md, sources_md, retrieved_md) for the chosen mode."""
    question = (question or "").strip()
    if not question:
        return "_Enter a question above._", "", ""

    if mode == "compare both":
        results = ask_compare(question, k=int(k))
        answer_md, retrieved_md = [], []
        for strategy in ("recursive", "fixed_size"):
            r = results[strategy]
            label = "Recursive" if strategy == "recursive" else "Fixed-size"
            # Keep each strategy's answer and its sources together in one block.
            answer_md.append(
                f"### {label}\n{r['answer']}\n\n"
                f"**Sources cited:**\n\n{_format_sources(r)}"
            )
            retrieved_md.append(f"### {label}\n{_format_retrieved(r)}")
        # Sources are shown inline per strategy, so the separate box stays empty.
        return "\n\n---\n\n".join(answer_md), "", "\n\n".join(retrieved_md)

    r = ask(question, strategy=mode, k=int(k))
    return r["answer"], _format_sources(r), _format_retrieved(r)


with gr.Blocks(title="Unofficial Guide — CS 6515 GA") as demo:
    gr.Markdown(
        "# The Unofficial Guide — CS 6515 Graduate Algorithms\n"
        "Ask about GA difficulty, exams, grading, workload, or study strategy. "
        "Answers come **only** from student reviews; the model cites the chunks it used."
    )

    with gr.Row():
        question = gr.Textbox(
            label="Your question", scale=4,
            placeholder="e.g. Is GA a core course for all OMSCS specializations?",
        )
        mode = gr.Radio(MODES, value="recursive", label="Chunking strategy", scale=2)

    k = gr.Slider(1, 8, value=5, step=1, label="Chunks to retrieve (top-k)")
    ask_btn = gr.Button("Ask", variant="primary")

    answer_out = gr.Markdown(label="Answer")
    sources_out = gr.Markdown(label="Sources cited")
    with gr.Accordion("Retrieved context (supplied to the model — not necessarily all used)", open=False):
        retrieved_out = gr.Markdown()

    inputs = [question, mode, k]
    outputs = [answer_out, sources_out, retrieved_out]
    ask_btn.click(handle_query, inputs=inputs, outputs=outputs)
    question.submit(handle_query, inputs=inputs, outputs=outputs)


if __name__ == "__main__":
    demo.launch()
