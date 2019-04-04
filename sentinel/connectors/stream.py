import praw
from datetime import datetime
from ..models.mention import Mention
from ..models.reddit import RedditMentionMetadata
from abc import ABCMeta


class IStreamConnector(metaclass=ABCMeta):
    pass

class StreamConnectorFactory():
    def create_stream_connector(self, source: str):
        creation_strategy = {'reddit': RedditStreamConnector}
        factory_method = creation_strategy[source]

        return factory_method()

# https://praw.readthedocs.io/en/latest/index.html
class RedditStreamConnector(IStreamConnector):
    def __init__(self):
        self.reddit = praw.Reddit(user_agent='Comment Extraction (by /u/balindwalinstalin)',
                     client_id='OqrZ_DehznAk8Q', client_secret='4WUBg15-g6fwXhnbl0mu8QlD944')

    def stream_comments(self, subreddits = None):
        if not subreddits:
            subreddits = ['askreddit']
        subreddits = '+'.join(subreddits)
        for comment in self.reddit.subreddit(subreddits).stream.comments():
            metadata = RedditMentionMetadata.from_praw(comment)
            mention = Mention(
                comment.body,
                comment.permalink,
                datetime.fromtimestamp(comment.created_utc),
                datetime.utcnow(),
                'reddit',
                metadata
            )
            yield mention
   