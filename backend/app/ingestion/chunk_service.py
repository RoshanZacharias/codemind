from sqlalchemy import select

from ..database import AsyncSessionLocal
from ..models.code_chunk import CodeChunk
from ..models.repository_file import RepositoryFile
from .chunker import chunk_code


async def create_chunks_for_file(
    repository_file_id: int,
) -> int:
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(RepositoryFile).where(
                RepositoryFile.id == repository_file_id
            )
        )

        repository_file = result.scalar_one_or_none()

        if repository_file is None:
            return 0

        chunks = chunk_code(
            repository_file.content
        )

        for chunk in chunks:
            code_chunk = CodeChunk(
                repository_file_id=repository_file.id,
                chunk_index=chunk.chunk_index,
                start_line=chunk.start_line,
                end_line=chunk.end_line,
                content=chunk.content,
            )

            db.add(code_chunk)

        await db.commit()

        return len(chunks)


async def create_chunks_for_repository(
    repository_id: int,
) -> int:
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(RepositoryFile).where(
                RepositoryFile.repository_id == repository_id
            )
        )

        files = result.scalars().all()

    total_chunks = 0

    for repository_file in files:
        total_chunks += await create_chunks_for_file(
            repository_file.id
        )

    return total_chunks