import json
import praw
import requests
from datetime import datetime
from ..models.mentions import Mention, HackerNewsMetadata
from ..models.reddit import RedditMentionMetadata
from abc import ABCMeta


class IStreamConnector(metaclass=ABCMeta):
    pass


class StreamConnectorFactory:
    def create_stream_connector(self, source: str):
        creation_strategy = {
            "reddit": RedditStreamConnector,
            "hacker-news": HackerNewsStreamConnector,
        }
        factory_method = creation_strategy[source]

        return factory_method()


# https://praw.readthedocs.io/en/latest/index.html
class RedditStreamConnector(IStreamConnector):
    def __init__(self):
        self.reddit = praw.Reddit(
            user_agent="Comment Extraction (by /u/balindwalinstalin)",
            client_id="OqrZ_DehznAk8Q",
            client_secret="4WUBg15-g6fwXhnbl0mu8QlD944",
        )

    def stream_comments(self, subreddits=None):
        if not subreddits:
            subreddits = ["askreddit"]
        subreddits = "+".join(subreddits)
        for comment in self.reddit.subreddit(subreddits).stream.comments():
            metadata = RedditMentionMetadata.from_praw(comment)
            mention = Mention(
                comment.body,
                comment.permalink,
                datetime.fromtimestamp(comment.created_utc),
                datetime.utcnow(),
                "reddit",
                metadata,
            )
            yield mention


class IHackerNewsStreamReader(metaclass=ABCMeta):
    def stream_comments(self):
        pass


class HackerNewsStreamReader(IHackerNewsStreamReader):
    def __init__(self):
        self._comments_stream_url = "http://api.hnstream.com/comments/stream/"

    def stream_comments(self):
        with requests.get(self._comments_stream_url, stream=True) as r:
            lines = r.iter_lines()
            next(lines)
            for line in lines:
                yield line


class HackerNewsStreamConnector(IStreamConnector):
    def __init__(self, hn_stream_reader=HackerNewsStreamReader()):
        self._hn_stream_reader = hn_stream_reader

    def stream_comments(self):
        for comment in self._hn_stream_reader.stream_comments():
            yield self._create_hn_mention(comment)

    @staticmethod
    def _create_hn_mention(comment_json):
        comment = json.loads(str(comment_json, "utf-8"))
        metadata = HackerNewsMetadata(comment["author"], None, None)
        return Mention(
            text=comment["body"],
            url=None,
            creation_date=datetime.utcnow(),
            download_date=datetime.utcnow(),
            source="hacker-news",
            metadata=metadata,
        )
