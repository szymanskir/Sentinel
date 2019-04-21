import time
from datetime import datetime
from newsapi import NewsApiClient
from typing import Any, Dict, List

from ..models.mentions import GoogleNewsMetadata, Mention


class GoogleNewsCommonConnector:
    def __init__(self, config: Dict[Any, Any]):
        self._api_client = NewsApiClient(
            api_key=config["Default"]["GOOGLE_NEWS_API_KEY"]
        )
        self._REQUEST_INTERVAL = 60 * 15
        self._all_news_sources = None

    def _create_query(self, keywords: List[str]) -> str:
        query = "&OR&".join(keywords)
        return query

    def search_news(self, keywords: List[str], since: datetime, until: datetime):
        response = self._api_client.get_everything(
            q=self._create_query(keywords),
            from_param=str(since.date()),
            to=str(until.date()),
        )

        assert response["status"] == "ok"
        for article in response["articles"]:
            yield article

    def _retrieve_news_sources(self) -> str:
        response = self._api_client.get_sources()
        assert response["status"] == "ok"
        all_news_sources = ",".join([s["id"] for s in response["sources"]])
        return all_news_sources

    def search_top_stories(self):
        if self._all_news_sources is None:
            self._all_news_sources = self._retrieve_news_sources()

        while True:
            response = self._api_client.get_top_headlines(
                sources=self._all_news_sources
            )
            assert response["status"] == "ok"
            for article in response["articles"]:
                yield article
            time.sleep(self._REQUEST_INTERVAL)

    @staticmethod
    def create_gn_mention(article) -> Mention:
        article_metadata = GoogleNewsCommonConnector.create_gn_mention_metadata(article)
        text = " ".join(
            filter(None, [article["title"], article["description"], article["content"]])
        )
        return Mention(
            text=text,
            url=article["url"],
            creation_date=article["publishedAt"],
            download_date=datetime.utcnow(),
            source="google-news",
            metadata=article_metadata,
        )

    @staticmethod
    def create_gn_mention_metadata(article) -> GoogleNewsMetadata:
        return GoogleNewsMetadata(
            author=article["author"], news_source=article["source"]["name"]
        )
