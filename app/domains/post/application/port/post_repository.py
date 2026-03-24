from abc import ABC, abstractmethod

from app.domains.post.domain.entity.post import Post


class PostRepository(ABC):

    @abstractmethod
    async def save(self, post: Post) -> Post:
        pass

    @abstractmethod
    async def find_all(self, page: int, size: int) -> tuple[list[Post], int]:
        pass

    @abstractmethod
    async def find_by_id(self, post_id: int) -> Post | None:
        pass
