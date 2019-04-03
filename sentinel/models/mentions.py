from datetime import datetime
from typing import NamedTuple


class Mention:

    def __init__(self, text, url, metadata):
        self.text = text
        self.url = url
        self.metadata = metadata


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


class TwitterMention(Mention):
    def __init__(self, text, url, metadata):
        super().__init__(text, url, metadata)

    @classmethod
    def from_status_json(cls, status_json):
        urls = status_json.entities['urls']
        url = urls[0]['url'] if len(urls) > 0 else None
        metadata = TwitterMentionMetadata.from_status_json(status_json)
        return cls(status_json.text, url, metadata)


class HackerNewsMetadata(NamedTuple):
    author: str
    points: int
    relevancy_score: int

    @classmethod
    def from_algolia_json(cls, hit_json):
        author = hit_json['author']
        points = hit_json['points']
        relevancy_score = hit_json['relevancy_score']
        return HackerNewsMetadata(author, points if points is not None else 0, relevancy_score)


class HackerNewsMention(Mention):

    def __init__(self, text, url, metadata):
        super().__init__(text, url, metadata)

    @classmethod
    def from_algolia_json(cls, hit_json):

        text = hit_json['comment_text']
        url = hit_json['story_url']
        metadata = HackerNewsMetadata.from_algolia_json(hit_json)
        return HackerNewsMention(text, url, metadata)



