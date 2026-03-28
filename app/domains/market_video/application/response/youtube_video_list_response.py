from typing import Optional

from pydantic import BaseModel


class VideoItemResponse(BaseModel):
    title: str
    thumbnail_url: str
    channel_name: str
    published_at: str
    video_url: str


class YoutubeVideoListResponse(BaseModel):
    items: list[VideoItemResponse]
    next_page_token: Optional[str]
    prev_page_token: Optional[str]
    total_results: int
