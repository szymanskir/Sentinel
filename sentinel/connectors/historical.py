from abc import ABCMeta
from ..models.mentions import Mention, HackerNewsMention, TwitterMentionMetadata
from datetime import datetime
from typing import Generator, List
from hn import search_by_date
from tweepy.models import Status
import tweepy


class IHistoricalConnector(metaclass=ABCMeta):
    def download_mentions(
        self, keywords: List[str], since: datetime, until: datetime
    ) -> Generator[Mention, None, None]:
        pass


class ITweetSearcher(metaclass=ABCMeta):
    def search(self, q: str, until: datetime) -> Generator[Status, None, None]:
        pass


class TweetSearcher(ITweetSearcher):
    def __init__(self):
        auth = tweepy.OAuthHandler(
            "7OQ3QuZHq9VLLHhEfiNLgkXRr",
            "1Y3KdcvUkrwjs8R6XVafRfN4ztMC1h6TShfbdLux6fsHEXpEQj",
        )
        self.api = tweepy.API(auth)

    def search(self, q: str, until: datetime):
        for page in tweepy.Cursor(
            self.api.search,
            q=q,
            count=15,
            result_type="recent",
            include_entities=True,
            until=str(until.date()),
        ).pages():
            for tweet in page:
                yield tweet


class TwitterHistoricalConnector(IHistoricalConnector):
    def __init__(self, tweet_searcher: TweetSearcher = TweetSearcher()):

        self._tweet_searcher = tweet_searcher
        pass

    def _build_query(self, keywords: List[str], since: datetime) -> str:
        or_statement = "&OR&".join(keywords)

        query = f"{or_statement}&since={since.date()}"
        return query

    def download_mentions(
        self, keywords: List[str], since: datetime, until: datetime
    ) -> Generator[Mention, None, None]:
        query = self._build_query(keywords, since)
        tweet_generator = self._tweet_searcher.search(query, until)

        for tweet in tweet_generator:
            twitter_mention_metadata = self.create_twitter_mention_metadata(tweet)
            urls = tweet.entities["urls"]
            url = urls[0]["url"] if len(urls) > 0 else None
            yield Mention(
                text=tweet.text,
                url=url,
                creation_date=tweet.created_at,
                download_date=datetime.utcnow(),
                source="twitter",
                metadata=twitter_mention_metadata,
            )

    @staticmethod
    def create_twitter_mention_metadata(status_json: Status):
        user_json = status_json.user
        return TwitterMentionMetadata(
            user_json.followers_count,
            user_json.statuses_count,
            user_json.friends_count,
            user_json.verified,
            user_json.listed_count,
            status_json.retweet_count,
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
                    metadata=hn_mention.metadata,
                )


class HistoricalConnectorFactory:
    def create_historical_connector(self, source: str):
        creation_strategy = {
            "twitter": TwitterHistoricalConnector,
            "hacker-news": HackerNewsHistoricalConnector,
        }
        factory_method = creation_strategy[source]

        return factory_method()
