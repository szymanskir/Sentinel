from abc import ABCMeta
from ..models.mentions import TwitterMention, Mention, HackerNewsMention
from datetime import datetime
from typing import Generator, List
from hn import search_by_date
import tweepy


class IHistoricalConnector(metaclass=ABCMeta):
    def download_mentions(
        self, keywords: List[str], since: datetime, until: datetime
    ) -> Generator[Mention, None, None]:
        pass


class TwitterHistoricalConnector(IHistoricalConnector):
    def __init__(self):
        auth = tweepy.OAuthHandler(
            "7OQ3QuZHq9VLLHhEfiNLgkXRr",
            "1Y3KdcvUkrwjs8R6XVafRfN4ztMC1h6TShfbdLux6fsHEXpEQj",
        )
        self.api = tweepy.API(auth)
        pass

    def _build_query(self, keywords: List[str], since: datetime) -> str:
        or_statement = "&OR&".join(keywords)

        query = f"{or_statement}&since={since.date()}"
        return query

    def download_mentions(
        self, keywords: List[str], since: datetime, until: datetime
    ) -> Generator[TwitterMention, None, None]:
        query = self._build_query(keywords, since)

        for tweets in tweepy.Cursor(
            self.api.search,
            q=query,
            count=15,
            result_type="recent",
            include_entities=True,
            until=str(until.date()),
        ).pages():
            for tweet in tweets:
                yield TwitterMention.from_status_json(tweet)


class HackerNewsHistoricalConnector(IHistoricalConnector):
    def download_mentions(
        self, keywords: List[str], since: datetime, until: datetime
    ) -> Generator[Mention, None, None]:
        for keyword in keywords:
            response = search_by_date(
                q=keyword,
                comments=True,
                created_at__gt=str(since.date()),
                created_at__lt=str(until.date()),
            )
            for hit in response:
                yield HackerNewsMention.from_algolia_json(hit)


class HistoricalConnectorFactory:
    def create_historical_connector(self, source: str):
        creation_strategy = {
            "twitter": TwitterHistoricalConnector,
            "hacker-news": HackerNewsHistoricalConnector,
        }
        factory_method = creation_strategy[source]

        return factory_method()
