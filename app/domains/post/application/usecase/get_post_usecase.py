from app.domains.post.application.port.post_repository import PostRepository
from app.domains.post.application.response.post_detail_response import PostDetailResponse


class GetPostUseCase:
    def __init__(self, post_repository: PostRepository):
        self._post_repository = post_repository

    async def execute(self, post_id: int) -> PostDetailResponse | None:
        post = await self._post_repository.find_by_id(post_id)
        if post is None:
            return None

        return PostDetailResponse(
            post_id=post.post_id,
            title=post.title,
            content=post.content,
            created_at=post.created_at,
        )
