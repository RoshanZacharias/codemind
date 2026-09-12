from .vector_search import search_code
from .keyword_search import keyword_search


async def hybrid_search(
    repository_id: int,
    query: str,
    limit: int = 10,
):
    vector_results = await search_code(
        repository_id,
        query,
        limit,
    )

    keyword_results = await keyword_search(
        repository_id,
        query,
        limit,
    )

    merged = {}

    for result in vector_results:
        merged[result["file_path"]] = {
            **result,
            "hybrid_score": 1.0 - result["distance"],
        }

    for result in keyword_results:
        if result["file_path"] in merged:
            merged[result["file_path"]][
                "hybrid_score"
            ] += result["score"]
        else:
            merged[result["file_path"]] = {
                **result,
                "hybrid_score": result["score"],
            }

    results = sorted(
        merged.values(),
        key=lambda item: item["hybrid_score"],
        reverse=True,
    )

    return results[:limit]