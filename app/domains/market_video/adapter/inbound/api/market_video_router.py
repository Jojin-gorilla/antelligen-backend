import redis.asyncio as aioredis
from fastapi import APIRouter, Cookie, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.common.exception.app_exception import AppException
from app.common.response.base_response import BaseResponse
from app.domains.account.adapter.outbound.persistence.account_repository_impl import AccountRepositoryImpl
from app.domains.market_video.adapter.outbound.external.youtube_video_client import YoutubeVideoClient
from app.domains.market_video.application.usecase.get_youtube_video_list_usecase import GetYoutubeVideoListUseCase
from app.infrastructure.cache.redis_client import get_redis
from app.infrastructure.config.settings import get_settings
from app.infrastructure.database.database import get_db

SESSION_KEY_PREFIX = "session:"

router = APIRouter(prefix="/youtube", tags=["youtube"])


@router.get("/list")
async def get_youtube_video_list(
    page_token: Optional[str] = Query(default=None),
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

    settings = get_settings()
    provider = YoutubeVideoClient(api_key=settings.youtube_api_key)
    usecase = GetYoutubeVideoListUseCase(youtube_video_provider=provider)
    response = await usecase.execute(page_token=page_token)

    return BaseResponse.ok(data=response, message="YouTube 영상 목록 조회 성공")
