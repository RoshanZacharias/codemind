import asyncio
import sys

from app.search.vector_search import search_code


async def main():
    if len(sys.argv) < 3:
        print(
            "Usage: python -m scripts.search_code "
            "<repository_id> <query>"
        )
        return

    repository_id = int(sys.argv[1])
    query = " ".join(sys.argv[2:])

    results = await search_code(
        repository_id=repository_id,
        query=query,
        limit=5,
    )

    print(f"\nQuery: {query}")
    print(f"Results: {len(results)}\n")

    for index, result in enumerate(results, start=1):
        print("=" * 70)
        print(f"Result #{index}")
        print(f"File: {result['file_path']}")
        print(
            f"Lines: "
            f"{result['start_line']}-{result['end_line']}"
        )
        print(f"Distance: {result['distance']:.4f}")
        print("-" * 70)
        print(result["content"][:1000])
        print()


if __name__ == "__main__":
    asyncio.run(main())