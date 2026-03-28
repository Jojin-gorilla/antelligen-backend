from app.common.exception.app_exception import AppException
from app.domains.board.application.port.out.board_repository_port import BoardRepositoryPort


class DeleteBoardUseCase:
    def __init__(self, board_repository: BoardRepositoryPort):
        self._board_repository = board_repository

    async def execute(self, board_id: int, account_id: int) -> None:
        board = await self._board_repository.find_by_id(board_id)
        if board is None:
            raise AppException(status_code=404, message="게시물을 찾을 수 없습니다.")
        if board.account_id != account_id:
            raise AppException(status_code=403, message="본인이 작성한 게시물만 삭제할 수 있습니다.")
        await self._board_repository.delete(board_id)
