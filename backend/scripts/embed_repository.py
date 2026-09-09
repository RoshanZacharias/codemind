import asyncio
import sys

from app.ingestion.embedding_service import embed_chunks_for_repository


async def main():
    if len(sys.argv) != 2:
        print(
            "Usage: python scripts/embed_repository.py <repository_id>"
        )
        return

    repository_id = int(sys.argv[1])

    count = await embed_chunks_for_repository(
        repository_id
    )

    print(
        f"Successfully embedded {count} chunks "
        f"for repository {repository_id}"
    )


if __name__ == "__main__":
    asyncio.run(main())