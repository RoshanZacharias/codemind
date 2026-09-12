from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..ai.rag_service import answer_question
from ..dependencies import get_current_user, get_db
from ..models.project import Project
from ..models.repository import Repository
from ..models.user import User
from ..schemas.ask import AskRequest, AskResponse


router = APIRouter(
    prefix="/repositories",
    tags=["Ask"],
)


@router.post(
    "/{repository_id}/ask",
    response_model=AskResponse,
)
async def ask_repository(
    repository_id: int,
    request: AskRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Repository)
        .join(Project, Repository.project_id == Project.id)
        .where(
            Repository.id == repository_id,
            Project.user_id == current_user.id,
        )
    )

    repository = result.scalar_one_or_none()

    if repository is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Repository not found",
        )

    return await answer_question(
        repository_id=repository_id,
        question=request.question,
    )