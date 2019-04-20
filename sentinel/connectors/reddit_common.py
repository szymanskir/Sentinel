import praw
from datetime import datetime
from ..models.mentions import Mention, RedditMetadata


def map_reddit_comment(comment: praw.models.Comment) -> Mention:
    metadata = RedditMetadata(
        redditor=comment.author.id,
        redditor_link_karma=comment.author.link_karma,
        redditor_comment_karma=comment.author.comment_karma,
        score=comment.score,
        submission=comment.submission.id,
    )

    return Mention(
        text=comment.body,
        url="https://reddit.com" + comment.permalink,
        creation_date=datetime.fromtimestamp(comment.created_utc),
        download_date=datetime.utcnow(),
        source="reddit",
        metadata=metadata,
    )


def filter_removed_comments(comments):
    # PRAW returns comments even if they are banned/deleted, we have to filter them manually
    # such comments have author removed
    # https://www.reddit.com/r/redditdev/comments/4xnk7c/do_removed_comments_show_in_praw/
    for c in comments:
        if c.author is not None:
            yield c
