from app.common.exception.app_exception import AppException
from app.domains.account.application.port.out.account_repository_port import AccountRepositoryPort
from app.domains.board.application.port.out.board_repository_port import BoardRepositoryPort
from app.domains.board.application.request.update_board_request import UpdateBoardRequest
from app.domains.board.application.response.board_detail_response import BoardDetailResponse


class UpdateBoardUseCase:
    def __init__(self, board_repository: BoardRepositoryPort, account_repository: AccountRepositoryPort):
        self._board_repository = board_repository
        self._account_repository = account_repository

    async def execute(self, board_id: int, account_id: int, request: UpdateBoardRequest) -> BoardDetailResponse:
        board = await self._board_repository.find_by_id(board_id)
        if board is None:
            raise AppException(status_code=404, message="게시물을 찾을 수 없습니다.")
        if board.account_id != account_id:
            raise AppException(status_code=403, message="본인이 작성한 게시물만 수정할 수 있습니다.")

        board.title = request.title
        board.content = request.content
        updated = await self._board_repository.update(board)

        account = await self._account_repository.find_by_id(account_id)
        nickname = account.nickname if account and account.nickname else "알 수 없음"

        return BoardDetailResponse(
            board_id=updated.board_id,
            title=updated.title,
            content=updated.content,
            nickname=nickname,
            created_at=updated.created_at,
            updated_at=updated.updated_at,
        )
