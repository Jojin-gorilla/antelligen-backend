from app.domains.board.domain.entity.board import Board
from app.domains.board.infrastructure.orm.board_orm import BoardOrm


class BoardMapper:

    @staticmethod
    def to_entity(orm: BoardOrm) -> Board:
        return Board(
            board_id=orm.id,
            title=orm.title,
            content=orm.content,
            account_id=orm.account_id,
            created_at=orm.created_at,
            updated_at=orm.updated_at,
        )

    @staticmethod
    def to_orm(board: Board) -> BoardOrm:
        return BoardOrm(
            title=board.title,
            content=board.content,
            account_id=board.account_id,
            created_at=board.created_at,
            updated_at=board.updated_at,
        )
