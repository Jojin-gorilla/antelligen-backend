from app.domains.post.application.port.post_repository import PostRepository
from app.domains.post.application.response.post_list_response import PostListResponse, PostSummaryResponse


class GetPostListUseCase:
    def __init__(self, post_repository: PostRepository):
        self._post_repository = post_repository

    async def execute(self, page: int, size: int) -> PostListResponse:
        posts, total = await self._post_repository.find_all(page, size)

        return PostListResponse(
            posts=[
                PostSummaryResponse(
                    post_id=post.post_id,
                    title=post.title,
                    created_at=post.created_at,
                )
                for post in posts
            ],
            total=total,
            page=page,
            size=size,
        )
