from app.domains.account.application.port.out.account_repository_port import AccountRepositoryPort
from app.domains.board.application.port.out.board_repository_port import BoardRepositoryPort
from app.domains.board.application.request.create_board_request import CreateBoardRequest
from app.domains.board.application.response.create_board_response import CreateBoardResponse
from app.domains.board.domain.entity.board import Board


class CreateBoardUseCase:
    def __init__(self, board_repository: BoardRepositoryPort, account_repository: AccountRepositoryPort):
        self._board_repository = board_repository
        self._account_repository = account_repository

    async def execute(self, request: CreateBoardRequest, account_id: int) -> CreateBoardResponse:
        board = Board(
            title=request.title,
            content=request.content,
            account_id=account_id,
        )
        saved = await self._board_repository.save(board)

        account = await self._account_repository.find_by_id(account_id)
        nickname = account.nickname if account and account.nickname else "알 수 없음"

        return CreateBoardResponse(
            board_id=saved.board_id,
            title=saved.title,
            content=saved.content,
            nickname=nickname,
            created_at=saved.created_at,
            updated_at=saved.updated_at,
        )
