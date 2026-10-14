"""RAG — policy-grounded answers.

Task: answer a customer question using ONLY the retrieved help-center text. If the
answer isn't in the docs, the model must say it doesn't know (don't hallucinate).

Fill in YOUR_SYSTEM_PROMPT and YOUR_RETRIEVER.
Run:  python rag.py
"""
import os

from ollama import chat

MODEL = "llama3.1:8b"
DATA = os.path.join(os.path.dirname(__file__), "data", "help_center.txt")


def load_chunks() -> list[str]:
    with open(DATA, encoding="utf-8") as f:
        # one chunk per non-empty line
        return [line.strip() for line in f if line.strip()]


# TODO: return the subset of chunks relevant to `question` (simple keyword overlap is fine).
def YOUR_RETRIEVER(question: str, chunks: list[str]) -> list[str]:
    stopwords = {"the", "and", "you", "your", "how", "what", "what's", "can", "have", "for", "does", "long"}

    def words(text: str) -> list[str]:
        return [w.strip(".,?!:;'\"").lower() for w in text.split()]

    keywords = [w for w in words(question) if len(w) > 2 and w not in stopwords]
    found = []
    for chunk in chunks:
        chunk_words = [w for w in words(chunk) if len(w) > 3]
        if any(c.startswith(k) or k.startswith(c) for k in keywords for c in chunk_words):
            found.append(chunk)
    return found


# TODO: Fill this in! Force the model to answer only from the provided context.
YOUR_SYSTEM_PROMPT = """You answer customer questions for an online store's help desk.
Use only the information in the Context part of the message, not anything you know from outside.
If the context is empty or does not contain the answer, reply only: Sorry, I do not know that.
Keep the answer short and use the same words as the context, for example the exact number of days."""

CASES = [
    ("How long do I have to return an item?", ["30 days"]),
    ("Do you ship internationally?", ["international"]),
    ("What's your CEO's home address?", ["don't know", "do not know", "not sure", "cannot"]),
]


def answer(question: str) -> str:
    context = "\n".join(YOUR_RETRIEVER(question, load_chunks()))
    resp = chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": YOUR_SYSTEM_PROMPT},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
        ],
        options={"temperature": 0.0},
    )
    return resp.message.content.strip().lower()


def run() -> bool:
    passed = 0
    for question, needles in CASES:
        got = answer(question)
        ok = any(n.lower() in got for n in needles)
        passed += ok
        print(f"[{'PASS' if ok else 'FAIL'}] {question!r} -> {got[:80]!r}")
    print(f"{passed}/{len(CASES)} correct")
    return passed == len(CASES)


if __name__ == "__main__":
    run()
