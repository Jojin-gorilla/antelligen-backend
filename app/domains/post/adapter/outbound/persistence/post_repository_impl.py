from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.post.application.port.post_repository import PostRepository
from app.domains.post.domain.entity.post import Post
from app.domains.post.infrastructure.mapper.post_mapper import PostMapper
from app.domains.post.infrastructure.orm.post_orm import PostOrm


class PostRepositoryImpl(PostRepository):
    def __init__(self, db: AsyncSession):
        self._db = db

    async def save(self, post: Post) -> Post:
        orm = PostMapper.to_orm(post)
        self._db.add(orm)
        await self._db.commit()
        await self._db.refresh(orm)
        return PostMapper.to_entity(orm)

    async def find_all(self, page: int, size: int) -> tuple[list[Post], int]:
        offset = (page - 1) * size

        total_result = await self._db.execute(select(func.count()).select_from(PostOrm))
        total = total_result.scalar_one()

        result = await self._db.execute(
            select(PostOrm).order_by(PostOrm.created_at.desc()).offset(offset).limit(size)
        )
        posts = [PostMapper.to_entity(orm) for orm in result.scalars().all()]

        return posts, total

    async def find_by_id(self, post_id: int) -> Post | None:
        result = await self._db.execute(select(PostOrm).where(PostOrm.id == post_id))
        orm = result.scalar_one_or_none()
        return PostMapper.to_entity(orm) if orm else None
