from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.post.adapter.outbound.persistence.post_repository_impl import PostRepositoryImpl
from app.domains.post.application.request.create_post_request import CreatePostRequest
from app.domains.post.application.response.create_post_response import CreatePostResponse
from app.domains.post.application.response.post_detail_response import PostDetailResponse
from app.domains.post.application.response.post_list_response import PostListResponse
from app.domains.post.application.usecase.create_post_usecase import CreatePostUseCase
from app.domains.post.application.usecase.get_post_list_usecase import GetPostListUseCase
from app.domains.post.application.usecase.get_post_usecase import GetPostUseCase
from app.infrastructure.database.database import get_db

router = APIRouter(prefix="/post", tags=["Post"])


@router.get("/list", response_model=PostListResponse)
async def get_post_list(
    page: int = Query(default=1, ge=1),
    size: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    repository = PostRepositoryImpl(db)
    usecase = GetPostListUseCase(repository)
    return await usecase.execute(page, size)


@router.get("/{post_id}", response_model=PostDetailResponse)
async def get_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
):
    repository = PostRepositoryImpl(db)
    usecase = GetPostUseCase(repository)
    result = await usecase.execute(post_id)
    if result is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=f"게시글을 찾을 수 없습니다: {post_id}")
    return result


@router.post("", response_model=CreatePostResponse, status_code=201)
async def create_post(
    request: CreatePostRequest,
    db: AsyncSession = Depends(get_db),
):
    repository = PostRepositoryImpl(db)
    usecase = CreatePostUseCase(repository)
    return await usecase.execute(request)
