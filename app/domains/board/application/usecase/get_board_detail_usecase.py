from app.common.exception.app_exception import AppException
from app.domains.account.application.port.out.account_repository_port import AccountRepositoryPort
from app.domains.board.application.port.out.board_repository_port import BoardRepositoryPort
from app.domains.board.application.response.board_detail_response import BoardDetailResponse


class GetBoardDetailUseCase:
    def __init__(self, board_repository: BoardRepositoryPort, account_repository: AccountRepositoryPort):
        self._board_repository = board_repository
        self._account_repository = account_repository

    async def execute(self, board_id: int) -> BoardDetailResponse:
        board = await self._board_repository.find_by_id(board_id)
        if board is None:
            raise AppException(status_code=404, message="게시물을 찾을 수 없습니다.")

        account = await self._account_repository.find_by_id(board.account_id)
        nickname = account.nickname if account and account.nickname else "알 수 없음"

        return BoardDetailResponse(
            board_id=board.board_id,
            title=board.title,
            content=board.content,
            nickname=nickname,
            created_at=board.created_at,
            updated_at=board.updated_at,
        )
