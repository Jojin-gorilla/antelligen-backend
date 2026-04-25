from typing import Optional

from pydantic import BaseModel


class WatchlistNewsItem(BaseModel):
    title: str
    description: Optional[str] = None
    url: str
    published_at: Optional[str] = None
    stock_code: str
    stock_name: str


class WatchlistNewsFeedResponse(BaseModel):
    has_watchlist: bool
    items: list[WatchlistNewsItem]
    total: int
