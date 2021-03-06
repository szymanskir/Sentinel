import json
import praw
import requests
import time

from abc import ABCMeta
from datetime import datetime
from typing import Any, Dict, Iterator, Set
from newsapi import NewsApiClient
from pydantic import ValidationError

from .gn_common import create_gn_mention
from .hn_common import clean_html
from .reddit_common import map_reddit_comment
from .secrets_manager import (
    RedditSecretsManager,
    GoogleNewsSecretsManager,
    TwitterSecretsManager,
)

from sentinel_common.mentions import Mention, HackerNewsMetadata, TwitterMetadata
import twitter


class IStreamConnector(metaclass=ABCMeta):
    def stream_comments(self) -> Iterator[Mention]:
        pass


class StreamConnectorFactory:
    def create_stream_connector(self, source: str) -> IStreamConnector:
        creation_strategy = {
            "reddit": (RedditStreamConnector, RedditSecretsManager()),
            "hacker-news": (HackerNewsStreamConnector, None),
            "google-news": (GoogleNewsStreamConnector, GoogleNewsSecretsManager()),
            "twitter": (TwitterStreamConnector, TwitterSecretsManager()),
        }

        factory_method, secret_manager = creation_strategy[source]

        return factory_method(secret_manager)


class RedditStreamConnector(IStreamConnector):
    def __init__(self, secrets_manager: RedditSecretsManager):
        secrets = secrets_manager.get_secrets()
        self.reddit = praw.Reddit(
            user_agent="Comment Extraction (by /u/balindwalinstalin)",
            client_id=secrets["REDDIT_CLIENT_ID"],
            client_secret=secrets["REDDIT_CLIENT_SECRET"],
        )

    def stream_comments(self, subreddits=None):
        if not subreddits:
            subreddits = ["askreddit"]
        subreddits = "+".join(subreddits)

        for comment in self.reddit.subreddit(subreddits).stream.comments():
            yield map_reddit_comment(comment)


class HackerNewsStreamConnector(IStreamConnector):
    def __init__(self, secrets_manager: Any):
        self._comments_stream_url = "http://api.hnstream.com/comments/stream/"

    def stream_comments(self) -> Iterator[Mention]:
        for comment in self._stream_comments():
            yield self._create_hn_mention(comment)

    def _stream_comments(self) -> Iterator[str]:
        with requests.get(self._comments_stream_url, stream=True) as r:
            lines = r.iter_lines()  # each comment json correspons to a single line
            next(lines)  # first line is always about opening the stream
            for line in lines:
                yield line

    @staticmethod
    def _create_hn_mention(comment_json) -> Mention:
        comment = json.loads(str(comment_json, "utf-8"))
        try:
            metadata = HackerNewsMetadata(author=comment["author"])
            return Mention(
                text=clean_html(comment["body"]),
                url=f'https://news.ycombinator.com/item?id={comment["id"]}',
                origin_date=datetime.utcnow(),
                download_date=datetime.utcnow(),
                source="hacker-news",
                metadata=metadata,
            )
        except ValidationError as e:
            raise ValueError("Data parsing error", str(e), str(comment)) from e


class GoogleNewsStreamConnector(IStreamConnector):
    def __init__(self, secrets_manager: GoogleNewsSecretsManager):
        secrets = secrets_manager.get_secrets()
        self._api_client = NewsApiClient(api_key=secrets["GOOGLE_NEWS_API_KEY"])
        self._REQUEST_INTERVAL = 60 * 5
        self._PAGE_SIZE = 100
        self._all_news_sources = None
        self._last_download_time = None
        self._last_urls: Set[str] = set()

    def _retrieve_news_sources(self) -> str:
        response = self._api_client.get_sources(language="en")
        assert response["status"] == "ok"
        all_news_sources = ",".join([s["id"] for s in response["sources"]])
        return all_news_sources

    def _get_article_time(self, article: Dict) -> datetime:
        return datetime.strptime(article["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")

    def _search_top_stories(self):
        if self._all_news_sources is None:
            self._all_news_sources = self._retrieve_news_sources()

        response = self._api_client.get_top_headlines(
            sources=self._all_news_sources, page_size=self._PAGE_SIZE
        )

        assert response["status"] == "ok"

        self._last_download_time = datetime.utcnow()
        new_articles = [
            x for x in response["articles"] if x["url"] not in self._last_urls
        ]
        self._last_urls = set([x["url"] for x in response["articles"]])

        return new_articles

    def _listen_top_stories(self):
        # Free users can only retrieve a max of 100 results
        # in that case we can download just the first page
        # and increase the max size to 100. We do not have
        # to iterate through pages.
        while True:
            if (
                self._last_download_time is not None
                and (datetime.utcnow() - self._last_download_time).total_seconds()
                < self._REQUEST_INTERVAL
            ):
                time.sleep(self._REQUEST_INTERVAL)

            for article in self._search_top_stories():
                yield article

    def stream_comments(self) -> Iterator[Mention]:
        for article in self._listen_top_stories():
            yield create_gn_mention(article)


class TwitterStreamConnector(IStreamConnector):
    def __init__(self, secrets_manager: TwitterSecretsManager):
        secrets = secrets_manager.get_secrets()
        self.api = self._get_api_connection(secrets)

    def _get_api_connection(self, secrets: Dict[Any, Any]):
        return twitter.Api(
            consumer_key=secrets["TWITTER_CONSUMER_KEY"],
            consumer_secret=secrets["TWITTER_CONSUMER_SECRET"],
            access_token_key=secrets["TWITTER_ACCESS_TOKEN"],
            access_token_secret=secrets["TWITTER_ACCESS_TOKEN_SECRET"],
            sleep_on_rate_limit=True,
        )

    def stream_comments(self) -> Iterator[Mention]:
        for tweet in self._get_stream():
            twitter_mention_metadata = self.create_twitter_mention_metadata(tweet)
            username = tweet["user"]["screen_name"]
            url = f"https://twitter.com/{username}/status/{tweet['id_str']}"
            yield Mention(
                text=tweet["text"],
                url=url,
                origin_date=datetime.strptime(
                    tweet["created_at"], "%a %b %d %H:%M:%S  +0000 %Y"
                ),
                download_date=datetime.utcnow(),
                source="twitter",
                metadata=twitter_mention_metadata,
            )

    def _get_stream(self):
        # python-twitter enforces to specify at least one filter: list of tracked users,
        # list of keywords or list of locations.
        # Getting all tweets without filtering is achieved by specifying locations as
        # a range including all longitudes and latitudes
        return self.api.GetStreamFilter(
            languages=["en"], locations=["-180.0,-90.0,180.0,90.0"]
        )

    @staticmethod
    def create_twitter_mention_metadata(status_dict: Dict[Any, Any]) -> TwitterMetadata:
        user_dict = status_dict["user"]
        return TwitterMetadata(
            user_id=user_dict["id"],
            followers_count=user_dict["followers_count"],
            statuses_count=user_dict["statuses_count"],
            friends_count=user_dict["friends_count"],
            verified=user_dict["verified"],
            listed_count=user_dict["listed_count"],
            retweet_count=status_dict["retweet_count"],
        )
