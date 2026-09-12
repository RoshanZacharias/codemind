from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="Question about the repository",
    )


class Source(BaseModel):
    file: str
    language: str | None
    start_line: int
    end_line: int
    distance: float


class AskResponse(BaseModel):
    answer: str
    sources: list[Source]