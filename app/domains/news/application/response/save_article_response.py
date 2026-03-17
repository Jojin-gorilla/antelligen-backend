from datetime import datetime

from pydantic import BaseModel


class SaveArticleResponse(BaseModel):
    article_id: int
    title: str
    link: str
    source: str | None = None
    published_at: str | None = None
    snippet: str | None = None
    content: str | None = None
    saved_at: datetime
