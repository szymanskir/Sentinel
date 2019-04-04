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
    ) -> Generator[Mention, None, None]:
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
                twitter_mention = TwitterMention.from_status_json(tweet)
                yield Mention(
                    text=twitter_mention.text,
                    url=twitter_mention.url,
                    creation_date=twitter_mention.creation_date,
                    download_date=datetime.utcnow(),
                    source="twitter",
                    metadata=twitter_mention.metadata
                )


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
                hn_mention = HackerNewsMention.from_algolia_json(hit)
                yield Mention(
                    text=hn_mention.text,
                    url=hn_mention.url,
                    creation_date=hn_mention.creation_date,
                    download_date=datetime.utcnow(),
                    source="hacker-news",
                    metadata=hn_mention.metadata
                )


class HistoricalConnectorFactory:
    def create_historical_connector(self, source: str):
        creation_strategy = {
            "twitter": TwitterHistoricalConnector,
            "hacker-news": HackerNewsHistoricalConnector,
        }
        factory_method = creation_strategy[source]

        return factory_method()
