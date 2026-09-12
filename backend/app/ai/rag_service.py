from .context_builder import build_context
from .groq_service import generate_response
from ..search.vector_search import search_code
from ..search.hybrid_search import hybrid_search


SYSTEM_PROMPT = """
You are CodeMind, an AI software engineering assistant.

Answer the user's question using ONLY the repository context provided.

Rules:
1. Do not invent files, functions, classes, or implementation details.
2. Do not assume information that is not present in the context.
3. If the context is insufficient, clearly say so.
4. Explain the implementation clearly and concisely.
5. Do not create or guess source citations.
6. The application will provide source citations separately.
"""


async def answer_question(repository_id: int, question: str) -> dict:
    results = await hybrid_search(
        repository_id=repository_id,
        query=question,
        limit=10,
    )

    if not results:
        return {
            "answer": "I couldn't find relevant code in this repository.",
            "sources": [],
        }

    context = build_context(results)

    answer = await generate_response(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=f"""
Repository context:

{context}

Question:

{question}
""",
    )

    sources = [
        {
            "file": result["file_path"],
            "language": result["language"],
            "start_line": result["start_line"],
            "end_line": result["end_line"],
            "distance": result["distance"],
        }
        for result in results
    ]

    return {
        "answer": answer,
        "sources": sources,
    }