from datetime import datetime

from pydantic import BaseModel


class PostSummaryResponse(BaseModel):
    post_id: int
    title: str
    created_at: datetime


class PostListResponse(BaseModel):
    posts: list[PostSummaryResponse]
    total: int
    page: int
    size: int
