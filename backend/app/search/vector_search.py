from sqlalchemy import select

from ..ai.embedding_service import generate_embedding
from ..database import AsyncSessionLocal
from ..models.code_chunk import CodeChunk
from ..models.repository_file import RepositoryFile


async def search_code(
    repository_id: int,
    query: str,
    limit: int = 5,
):
    query_embedding = generate_embedding(query)

    async with AsyncSessionLocal() as db:
        similarity = CodeChunk.embedding.cosine_distance(
            query_embedding
        )

        result = await db.execute(
            select(
                CodeChunk,
                RepositoryFile.path,
                RepositoryFile.language,
                similarity.label("distance"),
            )
            .join(
                RepositoryFile,
                RepositoryFile.id == CodeChunk.repository_file_id,
            )
            .where(
                RepositoryFile.repository_id == repository_id,
                CodeChunk.embedding.is_not(None),
            )
            .order_by(similarity)
            .limit(limit)
        )

        rows = result.all()

        return [
            {
                "chunk_id": chunk.id,
                "file_path": path,
                "language": language,
                "start_line": chunk.start_line,
                "end_line": chunk.end_line,
                "content": chunk.content,
                "distance": float(distance),
            }
            for chunk, path, language, distance in rows
        ]