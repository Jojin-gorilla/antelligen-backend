from dataclasses import dataclass


@dataclass
class VideoItem:
    video_id: str
    title: str
    thumbnail_url: str
    channel_name: str
    published_at: str
    video_url: str
