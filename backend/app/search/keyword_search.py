from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AsyncSessionLocal
from app.models.code_chunk import CodeChunk
from app.models.repository_file import RepositoryFile


async def keyword_search(
    repository_id: int,
    query: str,
    limit: int = 10,
):
    async with AsyncSessionLocal() as db:
        ts_query = func.plainto_tsquery(
            "english",
            query,
        )

        rank = func.ts_rank_cd(
            func.to_tsvector(
                "english",
                CodeChunk.content,
            ),
            ts_query,
        )

        result = await db.execute(
            select(
                CodeChunk,
                RepositoryFile.path,
                RepositoryFile.language,
                rank.label("rank"),
            )
            .join(
                RepositoryFile,
                RepositoryFile.id
                == CodeChunk.repository_file_id,
            )
            .where(
                RepositoryFile.repository_id
                == repository_id,
                func.to_tsvector(
                    "english",
                    CodeChunk.content,
                ).op("@@")(ts_query),
            )
            .order_by(rank.desc())
            .limit(limit)
        )

        rows = result.all()

        return [
            {
                "file_path": path,
                "language": language,
                "start_line": chunk.start_line,
                "end_line": chunk.end_line,
                "content": chunk.content,
                "score": float(score),
            }
            for chunk, path, language, score in rows
        ]