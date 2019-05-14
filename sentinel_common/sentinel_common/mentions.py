from typing import Union, Optional
from uuid import uuid4, UUID
from pydantic import BaseModel, UrlStr
from datetime import datetime


class TwitterMentionMetadata(BaseModel):
    followers_count: int
    statuses_count: int
    friends_count: int
    verified: bool
    listed_count: int
    retweet_count: int

    class Config:
        allow_mutation = False


class HackerNewsMetadata(BaseModel):
    author: str
    points: Optional[int]
    relevancy_score: Optional[int]

    class Config:
        allow_mutation = False


class GoogleNewsMetadata(BaseModel):
    news_source: str
    author: Optional[str]

    class Config:
        allow_mutation = False


class RedditMetadata(BaseModel):
    redditor: str
    redditor_comment_karma: int
    redditor_link_karma: int
    score: int
    submission: str

    class Config:
        allow_mutation = False


class Mention(BaseModel):
    id: Optional[UUID] = uuid4()
    text: str
    url: Optional[UrlStr]
    creation_date: datetime
    download_date: datetime
    source: str
    metadata: Union[
        TwitterMentionMetadata, GoogleNewsMetadata, HackerNewsMetadata, RedditMetadata
    ]

    class Config:
        allow_mutation = False

    def to_json(self):
        return self.json()

    @classmethod
    def from_json(cls, data: str):
        return cls.parse_raw(data)