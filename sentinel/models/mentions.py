from datetime import datetime
from typing import NamedTuple
from uuid import uuid4


class Mention:
    def __init__(
            self,
            text,
            url,
            creation_date,
            download_date,
            source,
            metadata
    ):
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

    @classmethod
    def from_status_json(cls, status_json):
        user_json = status_json.user
        return cls(
            user_json.followers_count,
            user_json.statuses_count,
            user_json.friends_count,
            user_json.verified,
            user_json.listed_count,
            status_json.retweet_count
        )


class HackerNewsMetadata(NamedTuple):
    author: str
    points: int
    relevancy_score: int

    @classmethod
    def from_algolia_json(cls, hit_json):
        author = hit_json["author"]
        points = hit_json["points"]
        relevancy_score = hit_json["relevancy_score"]
        return HackerNewsMetadata(
            author,
            points if points is not None else 0,
            relevancy_score
        )


class HackerNewsMention(NamedTuple):
    text: str
    url: str
    metadata: HackerNewsMetadata

    @classmethod
    def from_algolia_json(cls, hit_json):
        text = hit_json["comment_text"]
        url = hit_json["story_url"]
        metadata = HackerNewsMetadata.from_algolia_json(hit_json)
        return cls(text, url, metadata)
