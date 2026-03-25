import math

from app.domains.account.application.port.out.account_repository_port import AccountRepositoryPort
from app.domains.board.application.port.out.board_repository_port import BoardRepositoryPort
from app.domains.board.application.response.board_list_response import BoardItemResponse, BoardListResponse


class GetBoardListUseCase:
    def __init__(self, board_repository: BoardRepositoryPort, account_repository: AccountRepositoryPort):
        self._board_repository = board_repository
        self._account_repository = account_repository

    async def execute(self, page: int, size: int) -> BoardListResponse:
        boards, total_count = await self._board_repository.find_paginated(page, size)

        board_items = []
        for board in boards:
            account = await self._account_repository.find_by_id(board.account_id)
            nickname = account.nickname if account and account.nickname else "알 수 없음"
            board_items.append(BoardItemResponse(
                board_id=board.board_id,
                title=board.title,
                content=board.content,
                nickname=nickname,
                created_at=board.created_at,
                updated_at=board.updated_at,
            ))

        total_pages = math.ceil(total_count / size) if total_count > 0 else 0

        return BoardListResponse(
            boards=board_items,
            page=page,
            total_pages=total_pages,
            total_count=total_count,
        )
