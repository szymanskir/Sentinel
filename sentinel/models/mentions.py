from datetime import datetime
from typing import NamedTuple


class TweetMetadata(NamedTuple):
    created_at: datetime
    retweet_count: int

    @classmethod
    def from_status_json(cls, status_json):
        return cls(status_json.created_at, status_json.retweet_count)


class TwitterUserMetadata(NamedTuple):
    followers_count: int
    statuses_count: int
    friends_count: int
    verified: bool
    listed_count: int

    @classmethod
    def from_user_json(cls, user_json):
        return cls(user_json.followers_count, user_json.statuses_count,
                   user_json.friends_count, user_json.verified,
                   user_json.listed_count)


class TwitterMentionMetadata(NamedTuple):
    tweet_metadata: TweetMetadata
    twitter_user_metadata: TwitterUserMetadata

    @classmethod
    def from_status_json(cls, status_json):
        return cls(
            TweetMetadata.from_status_json(status_json),
            TwitterUserMetadata.from_user_json(status_json.user))


class TwitterMention():
    def __init__(self, text, url, metadata):
        self.text = text
        self.url = url
        self.metadata = metadata

    @classmethod
    def from_status_json(cls, status_json):
        urls = status_json.entities['urls']
        url = urls[0]['url'] if len(urls) > 0 else None
        metadata = TwitterMentionMetadata.from_status_json(status_json)
        return cls(status_json.text, url, metadata)
