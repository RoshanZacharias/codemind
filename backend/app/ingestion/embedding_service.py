from sqlalchemy import select

from ..ai.embedding_service import model
from ..database import AsyncSessionLocal
from ..models.code_chunk import CodeChunk
from ..models.repository_file import RepositoryFile


BATCH_SIZE = 32


async def embed_chunks_for_repository(repository_id: int) -> int:
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(CodeChunk)
            .join(
                RepositoryFile,
                RepositoryFile.id == CodeChunk.repository_file_id,
            )
            .where(
                RepositoryFile.repository_id == repository_id,
                CodeChunk.embedding.is_(None),
            )
            .order_by(CodeChunk.id)
        )

        chunks = result.scalars().all()

        if not chunks:
            return 0

        total_embedded = 0

        for start in range(0, len(chunks), BATCH_SIZE):
            batch = chunks[start:start + BATCH_SIZE]

            texts = [
                chunk.content
                for chunk in batch
            ]

            embeddings = model.encode(
                texts,
                normalize_embeddings=True,
            )

            for chunk, embedding in zip(batch, embeddings):
                chunk.embedding = embedding.tolist()

            await db.commit()

            total_embedded += len(batch)

            print(
                f"Embedded {total_embedded}/{len(chunks)} chunks"
            )

        return total_embedded