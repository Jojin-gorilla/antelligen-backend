from pydantic import BaseModel, Field


class SaveArticleRequest(BaseModel):
    title: str = Field(..., min_length=1, description="기사 제목")
    link: str = Field(..., min_length=1, description="기사 링크")
    source: str | None = Field(None, description="출처")
    published_at: str | None = Field(None, description="발행일")
    snippet: str | None = Field(None, description="기사 요약")
