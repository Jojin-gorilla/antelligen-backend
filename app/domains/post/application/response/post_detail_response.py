from datetime import datetime

from pydantic import BaseModel


class PostDetailResponse(BaseModel):
    post_id: int
    title: str
    content: str
    created_at: datetime
