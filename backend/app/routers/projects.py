from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies import get_current_user, get_db
from ..models.project import Project
from ..models.user import User
from ..schemas.project import ProjectCreate, ProjectResponse


router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)


@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_project(
    project_data: ProjectCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    project = Project(
        name=project_data.name,
        description=project_data.description,
        user_id=current_user.id,
    )

    db.add(project)

    await db.commit()
    await db.refresh(project)

    return project


@router.get(
    "",
    response_model=list[ProjectResponse],
)
async def get_projects(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Project)
        .where(Project.user_id == current_user.id)
        .order_by(Project.created_at.desc())
    )

    return result.scalars().all()


@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
)
async def get_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
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