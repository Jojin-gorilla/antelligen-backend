from datetime import datetime


class SavedArticle:
    """저장된 관심 기사 도메인 엔티티"""

    def __init__(
        self,
        title: str,
        link: str,
        source: str | None = None,
        published_at: str | None = None,
        snippet: str | None = None,
        content: str | None = None,
        article_id: int | None = None,
        saved_at: datetime | None = None,
    ):
        self.article_id = article_id
        self.title = title
        self.link = link
        self.source = source
        self.published_at = published_at
        self.snippet = snippet
        self.content = content
        self.saved_at = saved_at
