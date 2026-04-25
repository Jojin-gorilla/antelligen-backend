from app.domains.account.application.port.out.watchlist_repository_port import WatchlistRepositoryPort
from app.domains.news.application.port.collected_news_repository_port import CollectedNewsRepositoryPort
from app.domains.news.application.response.watchlist_news_feed_response import (
    WatchlistNewsFeedResponse,
    WatchlistNewsItem,
)


class GetWatchlistNewsFeedUseCase:
    def __init__(
        self,
        watchlist_port: WatchlistRepositoryPort,
        news_repository: CollectedNewsRepositoryPort,
    ):
        self._watchlist_port = watchlist_port
        self._news_repository = news_repository

    async def execute(self, account_id: int) -> WatchlistNewsFeedResponse:
        watchlist = await self._watchlist_port.find_all_by_account(account_id)

        if not watchlist:
            return WatchlistNewsFeedResponse(has_watchlist=False, items=[], total=0)

        items: list[WatchlistNewsItem] = []
        for stock in watchlist:
            articles = await self._news_repository.find_by_keyword(stock.stock_name, limit=10)
            for article in articles:
                items.append(
                    WatchlistNewsItem(
                        title=article.title,
                        description=article.description,
                        url=article.url,
                        published_at=article.published_at,
                        stock_code=stock.stock_code,
                        stock_name=stock.stock_name,
                    )
                )

        items.sort(key=lambda x: x.published_at or "", reverse=True)

        return WatchlistNewsFeedResponse(has_watchlist=True, items=items, total=len(items))
