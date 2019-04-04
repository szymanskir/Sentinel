from datetime import datetime
from typing import NamedTuple


class RedditCommentMetadata(NamedTuple):
    id: str
    score: int
    submission_id: str
    subreddit_id: str

    @classmethod
    def from_praw(cls, comment):
        return cls(
            comment.id,
            comment.score,
            comment.submission.id,
            comment.subreddit.id
        )

class RedditorMetadata(NamedTuple):
    id: str
    comment_karma: int
    link_karma: int
    created_at: datetime

    @classmethod
    def from_praw(cls, redditor):
        return cls(
            redditor.id,
            redditor.comment_karma,
            redditor.link_karma,
            datetime.fromtimestamp(redditor.created_utc)
        )

class RedditMentionMetadata(NamedTuple):
    comment_metadata: RedditCommentMetadata
    redditor_metadata: RedditorMetadata

    @classmethod
    def from_praw(cls, comment):
        return cls(
            RedditCommentMetadata.from_praw(comment),
            RedditorMetadata.from_praw(comment.author)
        )




