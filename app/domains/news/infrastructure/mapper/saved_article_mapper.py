import hashlib

from app.domains.news.domain.entity.saved_article import SavedArticle
from app.domains.news.infrastructure.orm.saved_article_orm import SavedArticleOrm


class SavedArticleMapper:

    @staticmethod
    def to_orm(article: SavedArticle) -> SavedArticleOrm:
        return SavedArticleOrm(
            title=article.title,
            link=article.link,
            link_hash=hashlib.sha256(article.link.encode()).hexdigest(),
            source=article.source,
            published_at=article.published_at,
            snippet=article.snippet,
            content=article.content,
            saved_at=article.saved_at,
        )

    @staticmethod
    def to_entity(orm: SavedArticleOrm) -> SavedArticle:
        return SavedArticle(
            article_id=orm.id,
            title=orm.title,
            link=orm.link,
            source=orm.source,
            published_at=orm.published_at,
            snippet=orm.snippet,
            content=orm.content,
            saved_at=orm.saved_at,
        )
