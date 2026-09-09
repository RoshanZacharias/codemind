from datetime import datetime

from pydantic import BaseModel, HttpUrl


class RepositoryCreate(BaseModel):
    name: str
    url: HttpUrl
    branch: str = "main"


class RepositoryResponse(BaseModel):
    id: int
    project_id: int
    name: str
    url: str
    branch: str
    status: str
    created_at: datetime


class RepositoryFileResponse(BaseModel):
    id: int
    repository_id: int
    path: str
    language: str | None
    size: int
    content: str
    created_at: datetime