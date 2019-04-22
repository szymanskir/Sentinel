import json
import praw
import requests
import time

from abc import ABCMeta
from datetime import datetime
from typing import Any, Dict, Iterator
from newsapi import NewsApiClient

from .gn_common import create_gn_mention
from .reddit_common import map_reddit_comment

from ..models.mentions import Mention, HackerNewsMetadata


class IStreamConnector(metaclass=ABCMeta):
    def stream_comments(self) -> Iterator[Mention]:
        pass


class StreamConnectorFactory:
    def create_stream_connector(
        self, source: str, config: Dict[Any, Any]
    ) -> IStreamConnector:
        creation_strategy = {
            "reddit": RedditStreamConnector,
            "hacker-news": HackerNewsStreamConnector,
            "google-news": GoogleNewsStreamConnector,
        }
        factory_method = creation_strategy[source]

        return factory_method(config)


class RedditStreamConnector(IStreamConnector):
    def __init__(self, config: Dict[Any, Any]):
        self.reddit = praw.Reddit(
            user_agent="Comment Extraction (by /u/balindwalinstalin)",
            client_id=config["Default"]["REDDIT_CLIENT_ID"],
            client_secret=config["Default"]["REDDIT_CLIENT_SECRET"],
        )

    def stream_comments(self, subreddits=None):
        if not subreddits:
            subreddits = ["askreddit"]
        subreddits = "+".join(subreddits)

        for comment in self.reddit.subreddit(subreddits).stream.comments():
            yield map_reddit_comment(comment)


class HackerNewsStreamConnector(IStreamConnector):
    def __init__(self, config: Dict[Any, Any]):
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
        metadata = HackerNewsMetadata(author=comment["author"])
        return Mention(
            text=comment["body"],
            url=f'https://news.ycombinator.com/item?id={comment["id"]}',
            creation_date=datetime.utcnow(),
            download_date=datetime.utcnow(),
            source="hacker-news",
            metadata=metadata,
        )


class GoogleNewsStreamConnector(IStreamConnector):
    def __init__(self, config: Dict[Any, Any]):
        self._api_client = NewsApiClient(
            api_key=config["Default"]["GOOGLE_NEWS_API_KEY"]
        )
        self._REQUEST_INTERVAL = 60 * 15
        self._all_news_sources = None

    def _retrieve_news_sources(self) -> str:
        response = self._api_client.get_sources()
        assert response["status"] == "ok"
        all_news_sources = ",".join([s["id"] for s in response["sources"]])
        return all_news_sources

    def _search_top_stories(self):
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

    def stream_comments(self) -> Iterator[Mention]:
        for article in self._search_top_stories():
            yield create_gn_mention(article)
