from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..messaging.rabbitmq import publish_message
from ..dependencies import get_current_user, get_db
from ..models.project import Project
from ..models.repository import Repository
from ..models.repository_file import RepositoryFile
from ..models.user import User
from ..schemas.repository import (
    RepositoryCreate,
    RepositoryResponse,
    RepositoryFileResponse,
)


router = APIRouter(
    prefix="/projects/{project_id}/repositories",
    tags=["Repositories"],
)


async def get_user_project(
    project_id: int,
    current_user: User,
    db: AsyncSession,
) -> Project:
    result = await db.execute(
        select(Project).where(
            Project.id == project_id,
            Project.user_id == current_user.id,
        )
    )

    project = result.scalar_one_or_none()

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    return project


@router.post(
    "",
    response_model=RepositoryResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_repository(
    project_id: int,
    repository_data: RepositoryCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await get_user_project(
        project_id,
        current_user,
        db,
    )

    repository = Repository(
        project_id=project_id,
        name=repository_data.name,
        url=str(repository_data.url),
        branch=repository_data.branch,
        status="pending",
    )

    db.add(repository)

    await db.commit()
    await db.refresh(repository)

    await publish_message(
        "repository_ingestion",
        {
            "repository_id": repository.id,
        },
    )

    return repository

@router.get(
    "",
    response_model=list[RepositoryResponse],
)
async def get_repositories(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await get_user_project(
        project_id,
        current_user,
        db,
    )

    result = await db.execute(
        select(Repository)
        .where(Repository.project_id == project_id)
        .order_by(Repository.created_at.desc())
    )

    repositories = result.scalars().all()

    return repositories



@router.get(
    "/{repository_id}/files",
    response_model=list[RepositoryFileResponse],
)
async def get_repository_files(
    project_id: int,
    repository_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await get_user_project(
        project_id,
        current_user,
        db,
    )

    result = await db.execute(
        select(RepositoryFile)
        .join(
            Repository,
            Repository.id == RepositoryFile.repository_id,
        )
        .where(
            RepositoryFile.repository_id == repository_id,
            Repository.project_id == project_id,
        )
        .order_by(RepositoryFile.path)
    )

    return result.scalars().all()