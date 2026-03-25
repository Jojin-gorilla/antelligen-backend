from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.board.application.port.out.board_repository_port import BoardRepositoryPort
from app.domains.board.domain.entity.board import Board
from app.domains.board.infrastructure.mapper.board_mapper import BoardMapper
from app.domains.board.infrastructure.orm.board_orm import BoardOrm


class BoardRepositoryImpl(BoardRepositoryPort):
    def __init__(self, db: AsyncSession):
        self._db = db

    async def find_paginated(self, page: int, size: int) -> tuple[list[Board], int]:
        offset = (page - 1) * size

        count_stmt = select(func.count()).select_from(BoardOrm)
        count_result = await self._db.execute(count_stmt)
        total_count = count_result.scalar_one()

        stmt = (
            select(BoardOrm)
            .order_by(BoardOrm.created_at.desc())
            .offset(offset)
            .limit(size)
        )
        result = await self._db.execute(stmt)
        orm_list = result.scalars().all()

        return [BoardMapper.to_entity(orm) for orm in orm_list], total_count

    async def find_by_id(self, board_id: int) -> Board | None:
        stmt = select(BoardOrm).where(BoardOrm.id == board_id)
        result = await self._db.execute(stmt)
        orm = result.scalar_one_or_none()
        if orm is None:
            return None
        return BoardMapper.to_entity(orm)

    async def save(self, board: Board) -> Board:
        orm = BoardMapper.to_orm(board)
        self._db.add(orm)
        await self._db.commit()
        await self._db.refresh(orm)
        return BoardMapper.to_entity(orm)
