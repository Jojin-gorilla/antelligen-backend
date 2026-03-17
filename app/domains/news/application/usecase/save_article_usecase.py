from app.common.exception.app_exception import AppException
from app.domains.news.application.port.article_content_provider import (
    ArticleContentProvider,
)
from app.domains.news.application.port.saved_article_repository import (
    SavedArticleRepository,
)
from app.domains.news.application.request.save_article_request import (
    SaveArticleRequest,
)
from app.domains.news.application.response.save_article_response import (
    SaveArticleResponse,
)
from app.domains.news.domain.entity.saved_article import SavedArticle


class SaveArticleUseCase:
    def __init__(
        self,
        repository: SavedArticleRepository,
        content_provider: ArticleContentProvider,
    ):
        self._repository = repository
        self._content_provider = content_provider

    async def execute(self, request: SaveArticleRequest) -> SaveArticleResponse:
        # 중복 링크 검사
        existing = await self._repository.find_by_link(request.link)
        if existing is not None:
            raise AppException(
                status_code=409,
                message=f"이미 저장된 기사입니다. (ID: {existing.article_id})",
            )

        # 링크에서 기사 본문 스크래핑
        content = await self._content_provider.fetch_content(request.link)

        # 도메인 엔티티 생성
        article = SavedArticle(
            title=request.title,
            link=request.link,
            source=request.source,
            published_at=request.published_at,
            snippet=request.snippet,
            content=content,
        )

        # 저장
        saved = await self._repository.save(article)

        return SaveArticleResponse(
            article_id=saved.article_id,
            title=saved.title,
            link=saved.link,
            source=saved.source,
            published_at=saved.published_at,
            snippet=saved.snippet,
            content=saved.content,
            saved_at=saved.saved_at,
        )
