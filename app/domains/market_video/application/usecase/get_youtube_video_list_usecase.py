from typing import Optional

from app.domains.market_video.application.port.out.youtube_video_provider import YoutubeVideoProvider
from app.domains.market_video.application.response.youtube_video_list_response import (
    VideoItemResponse,
    YoutubeVideoListResponse,
)


class GetYoutubeVideoListUseCase:
    def __init__(self, youtube_video_provider: YoutubeVideoProvider):
        self._provider = youtube_video_provider

    async def execute(self, page_token: Optional[str] = None) -> YoutubeVideoListResponse:
        result = await self._provider.search(page_token=page_token)

        items = [
            VideoItemResponse(
                title=item.title,
                thumbnail_url=item.thumbnail_url,
                channel_name=item.channel_name,
                published_at=item.published_at,
                video_url=item.video_url,
            )
            for item in result.items
        ]

        return YoutubeVideoListResponse(
            items=items,
            next_page_token=result.next_page_token,
            prev_page_token=result.prev_page_token,
            total_results=result.total_results,
        )
