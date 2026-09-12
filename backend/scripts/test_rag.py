import asyncio
import sys

from app.ai.rag_service import answer_question


async def main():
    if len(sys.argv) < 3:
        print(
            "Usage: python -m scripts.test_rag "
            "<repository_id> <question>"
        )
        return

    repository_id = int(sys.argv[1])
    question = " ".join(sys.argv[2:])

    result = await answer_question(
        repository_id=repository_id,
        question=question,
    )

    print("\n" + "=" * 80)
    print("ANSWER")
    print("=" * 80)
    print(result["answer"])

    print("\n" + "=" * 80)
    print("SOURCES")
    print("=" * 80)

    for source in result["sources"]:
        print(
            f"{source['file_path']}:"
            f"{source['start_line']}-"
            f"{source['end_line']}"
            f"  distance={source['distance']:.4f}"
        )


if __name__ == "__main__":
    asyncio.run(main())