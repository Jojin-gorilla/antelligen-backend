from datetime import datetime

from pydantic import BaseModel


class BoardItemResponse(BaseModel):
    board_id: int
    title: str
    content: str
    nickname: str
    created_at: datetime
    updated_at: datetime


class BoardListResponse(BaseModel):
    boards: list[BoardItemResponse]
    page: int
    total_pages: int
    total_count: int
