import hn
import tweepy.models
import tweepy
import praw
import psaw

from abc import ABCMeta
from datetime import datetime
from newsapi import NewsApiClient
from typing import Iterator, List, Dict, Any, Set
from itertools import chain
from pydantic import ValidationError

from sentinel_common.mentions import Mention, HackerNewsMetadata, TwitterMetadata
from .hn_common import clean_html
from .reddit_common import map_reddit_comment, filter_removed_comments
from .gn_common import create_gn_mention
from .secrets_manager import (
    RedditSecretsManager,
    GoogleNewsSecretsManager,
    TwitterSecretsManager,
)

MOCK_CONFIG = {
    "TWITTER_CONSUMER_KEY": "MOCK_KEY",
    "TWITTER_CONSUMER_SECRET": "MOCK_SECRET",
}


class IHistoricalConnector(metaclass=ABCMeta):
    def download_mentions(
        self, keywords: List[str], since: datetime, until: datetime
    ) -> Iterator[Mention]:
        pass


class HistoricalConnectorFactory:
    def create_historical_connector(self, source: str) -> IHistoricalConnector:
        creation_strategy = {
            "twitter": (TwitterHistoricalConnector, RedditSecretsManager()),
            "hacker-news": (HackerNewsHistoricalConnector, None),
            "google-news": (GoogleNewsHistoricalConnector, GoogleNewsSecretsManager()),
            "reddit": (RedditHistoricalConnector, TwitterSecretsManager()),
        }
        factory_method, secrets_manager = creation_strategy[source]

        return factory_method(secrets_manager)


class TwitterHistoricalConnector(IHistoricalConnector):
    def __init__(self, secrets_manager: TwitterSecretsManager):
        secrets = secrets_manager.get_secrets()
        auth = tweepy.OAuthHandler(
            secrets["TWITTER_CONSUMER_KEY"], secrets["TWITTER_CONSUMER_SECRET"]
        )
        self.api = tweepy.API(auth, wait_on_rate_limit=True)

    def download_mentions(
        self, keywords: List[str], since: datetime, until: datetime
    ) -> Iterator[Mention]:
        query = self._build_query(keywords)
        tweet_generator = self._search(query, since, until)
        for tweet in tweet_generator:
            try:
                twitter_mention_metadata = self.create_twitter_mention_metadata(tweet)
                url = f"https://twitter.com/statuses/{tweet.id_str}"
                yield Mention(
                    text=tweet.text,
                    url=url,
                    origin_date=tweet.created_at,
                    download_date=datetime.utcnow(),
                    source="twitter",
                    metadata=twitter_mention_metadata,
                )
            except ValidationError as e:
                raise ValueError("Data parsing error", str(e), str(tweet)) from e

    def _build_query(self, keywords: List[str]) -> str:
        return "&OR&".join(keywords)

    def _search(self, q: str, since: datetime, until: datetime):
        for page in tweepy.Cursor(
            self.api.search,
            q=q,
            count=100,
            result_type="recent",
            include_entities=True,
            since=str(since.date()),
            until=str(until.date()),
            lang="en",
        ).pages():
            for tweet in page:
                yield tweet

    @staticmethod
    def create_twitter_mention_metadata(
        status_json: tweepy.models.Status
    ) -> TwitterMetadata:
        user_json = status_json.user
        return TwitterMetadata(
            user_id=user_json.id,
            followers_count=user_json.followers_count,
            statuses_count=user_json.statuses_count,
            friends_count=user_json.friends_count,
            verified=user_json.verified,
            listed_count=user_json.listed_count,
            retweet_count=status_json.retweet_count,
        )


class HackerNewsHistoricalConnector(IHistoricalConnector):
    def __init__(self, secrets_manager: Any):
        pass

    def download_mentions(
        self, keywords: List[str], since: datetime, until: datetime
    ) -> Iterator[Mention]:
        for keyword in keywords:
            response = self._search(keyword, since, until)
            for hit in response:
                try:
                    hn_metadata = self.create_hn_mention_metadata(hit)
                    yield Mention(
                        text=clean_html(hit["comment_text"]),
                        url=hit["story_url"],
                        origin_date=datetime.strptime(
                            hit["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ"
                        ),
                        download_date=datetime.utcnow(),
                        source="hacker-news",
                        metadata=hn_metadata,
                    )
                except ValidationError as e:
                    raise ValueError("Data parsing error", str(e), str(hit)) from e

    def _search(self, keyword: str, since: datetime, until: datetime) -> Dict[Any, Any]:
        response = hn.search_by_date(
            q=keyword,
            comments=True,
            created_at__gt=str(since.date()),
            created_at__lt=str(until.date()),
        )
        return response

    @staticmethod
    def create_hn_mention_metadata(hit_json: Dict[Any, Any]) -> HackerNewsMetadata:
        author = hit_json["author"]
        points = hit_json["points"]
        relevancy_score = hit_json["relevancy_score"]
        return HackerNewsMetadata(
            author=author,
            points=points if points is not None else 0,
            relevancy_score=relevancy_score,
        )


class GoogleNewsHistoricalConnector(IHistoricalConnector):
    def __init__(self, secrets_manager: GoogleNewsSecretsManager):
        secrets = secrets_manager.get_secrets()
        self._api_client = NewsApiClient(api_key=secrets["GOOGLE_NEWS_API_KEY"])
        self._PAGE_SIZE = 100

    def _create_query(self, keywords: List[str]) -> str:
        query = "&OR&".join(keywords)
        return query

    def _search_news(self, keywords: List[str], since: datetime, until: datetime):
        # Free users can only retrieve a max of 100 results
        # in that case we can download just the first page
        # and increase the max size to 100. We do not have
        # to iterate through pages.
        response = self._api_client.get_everything(
            q=self._create_query(keywords),
            from_param=str(since.date()),
            to=str(until.date()),
            page_size=self._PAGE_SIZE,
        )

        assert response["status"] == "ok"
        yield from response["articles"]

    def download_mentions(
        self, keywords: List[str], since: datetime, until: datetime
    ) -> Iterator[Mention]:
        yield from [
            create_gn_mention(article)
            for article in self._search_news(keywords, since, until)
        ]


class RedditHistoricalConnector(IHistoricalConnector):
    def __init__(self, secrets_manager: RedditSecretsManager):
        secrets = secrets_manager.get_secrets()
        reddit = praw.Reddit(
            user_agent="Comment Extraction (by /u/balindwalinstalin)",
            client_id=secrets["REDDIT_CLIENT_ID"],
            client_secret=secrets["REDDIT_CLIENT_SECRET"],
        )
        self.reddit = psaw.PushshiftAPI(reddit)

    def download_mentions(
        self, keywords: List[str], since: datetime, until: datetime
    ) -> Iterator[Mention]:

        queries = self._fetch_comments(
            keywords, int(since.timestamp()), int(until.timestamp())
        )
        comments = chain(*queries)
        duplicates = set()  # type: Set[str]

        for comment in filter_removed_comments(comments):
            if comment.id not in duplicates:
                duplicates.add(comment.id)
                yield map_reddit_comment(comment)

    def _fetch_comments(
        self, keywords: List[str], since: int, until: int
    ) -> List[Iterator[praw.models.Comment]]:
        # Pushshift does not allow specifying multiple keywords while searching,
        # thus this has to be an N query
        return [
            self.reddit.search_comments(q=keyword, after=since, before=until)
            for keyword in keywords
        ]
