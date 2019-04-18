from typing import NamedTuple
from uuid import uuid4


class Mention:
    def __init__(self, text, url, creation_date, download_date, source, metadata):
        self.id = uuid4()
        self.text = text
        self.url = url
        self.creation_date = creation_date
        self.download_date = download_date
        self.source = source
        self.metadata = metadata


class TwitterMentionMetadata(NamedTuple):
    followers_count: int
    statuses_count: int
    friends_count: int
    verified: bool
    listed_count: int
    retweet_count: int


class HackerNewsMetadata(NamedTuple):
    author: str
    points: int
    relevancy_score: int
