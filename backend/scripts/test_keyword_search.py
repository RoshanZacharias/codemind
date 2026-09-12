import asyncio
import sys

from app.search.keyword_search import keyword_search


async def main():
    repository_id = int(sys.argv[1])
    query = " ".join(sys.argv[2:])

    results = await keyword_search(
        repository_id,
        query,
    )

    for i, result in enumerate(results, 1):
        print("=" * 70)
        print(f"Result {i}")
        print(result["file_path"])
        print(
            f'Lines {result["start_line"]}-{result["end_line"]}'
        )
        print(f'Score: {result["score"]:.4f}')
        print("-" * 70)
        print(result["content"][:400])


asyncio.run(main())