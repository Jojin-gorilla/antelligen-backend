import logging

import redis.asyncio as aioredis
from fastapi import APIRouter, Cookie, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.exception.app_exception import AppException
from app.common.response.base_response import BaseResponse
from app.domains.account.adapter.outbound.persistence.account_repository_impl import AccountRepositoryImpl
from app.domains.board.adapter.outbound.persistence.board_repository_impl import BoardRepositoryImpl
from app.domains.board.application.request.create_board_request import CreateBoardRequest
from app.domains.board.application.usecase.create_board_usecase import CreateBoardUseCase
from app.domains.board.application.usecase.get_board_detail_usecase import GetBoardDetailUseCase
from app.domains.board.application.usecase.get_board_list_usecase import GetBoardListUseCase
from app.infrastructure.cache.redis_client import get_redis
from app.infrastructure.database.database import get_db

logger = logging.getLogger(__name__)
SESSION_KEY_PREFIX = "session:"

router = APIRouter(prefix="/board", tags=["board"])


@router.get("/list")
async def get_board_list(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1),
    user_token: str = Cookie(None),
    db: AsyncSession = Depends(get_db),
    redis: aioredis.Redis = Depends(get_redis),
):
    if not user_token:
        raise AppException(status_code=401, message="인증이 필요합니다.")

    account_id_str = await redis.get(f"{SESSION_KEY_PREFIX}{user_token}")
    if not account_id_str:
        raise AppException(status_code=401, message="세션이 만료되었거나 유효하지 않습니다.")

    account_id = int(account_id_str)

    account_repo = AccountRepositoryImpl(db)
    account = await account_repo.find_by_id(account_id)
    if not account:
        raise AppException(status_code=401, message="유효하지 않은 계정입니다.")

    board_repo = BoardRepositoryImpl(db)
    usecase = GetBoardListUseCase(board_repo, account_repo)
    response = await usecase.execute(page=page, size=size)

    return BaseResponse.ok(data=response, message="게시물 리스트 조회 성공")


@router.get("/read/{board_id}")
async def get_board_detail(
    board_id: int,
    user_token: str = Cookie(None),
    db: AsyncSession = Depends(get_db),
    redis: aioredis.Redis = Depends(get_redis),
):
    if not user_token:
        raise AppException(status_code=401, message="인증이 필요합니다.")

    account_id_str = await redis.get(f"{SESSION_KEY_PREFIX}{user_token}")
    if not account_id_str:
        raise AppException(status_code=401, message="세션이 만료되었거나 유효하지 않습니다.")

    account_id = int(account_id_str)

    account_repo = AccountRepositoryImpl(db)
    account = await account_repo.find_by_id(account_id)
    if not account:
        raise AppException(status_code=401, message="유효하지 않은 계정입니다.")

    board_repo = BoardRepositoryImpl(db)
    usecase = GetBoardDetailUseCase(board_repo, account_repo)
    response = await usecase.execute(board_id=board_id)

    return BaseResponse.ok(data=response, message="게시물 상세 조회 성공")


@router.post("/register")
async def create_board(
    request: CreateBoardRequest,
    user_token: str = Cookie(None),
    db: AsyncSession = Depends(get_db),
    redis: aioredis.Redis = Depends(get_redis),
):
    if not user_token:
        raise AppException(status_code=401, message="인증이 필요합니다.")

    account_id_str = await redis.get(f"{SESSION_KEY_PREFIX}{user_token}")
    logger.info("[board/register] redis raw value: %r", account_id_str)
    if not account_id_str:
        raise AppException(status_code=401, message="세션이 만료되었거나 유효하지 않습니다.")

    account_id = int(account_id_str)
    logger.info("[board/register] account_id: %s", account_id)

    account_repo = AccountRepositoryImpl(db)
    account = await account_repo.find_by_id(account_id)
    logger.info("[board/register] account found: %s, nickname: %s", account is not None, account.nickname if account else None)
    if not account:
        raise AppException(status_code=401, message="유효하지 않은 계정입니다.")

    board_repo = BoardRepositoryImpl(db)
    usecase = CreateBoardUseCase(board_repo, account_repo)
    response = await usecase.execute(request=request, account_id=account_id)
    logger.info("[board/register] response nickname: %s", response.nickname)

    return BaseResponse.ok(data=response, message="게시물 작성 성공")
