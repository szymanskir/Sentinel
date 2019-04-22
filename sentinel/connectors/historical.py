import hn
import tweepy.models
import tweepy
import praw
import psaw

from abc import ABCMeta
from datetime import datetime
from newsapi import NewsApiClient
from typing import Iterator, List, Dict, Any, Set
from itertools import chain

from ..models.mentions import (
    Mention,
    HackerNewsMetadata,
    TwitterMentionMetadata,
)
from .reddit_common import map_reddit_comment, filter_removed_comments
from .gn_common import create_gn_mention


class IHistoricalConnector(metaclass=ABCMeta):
    def download_mentions(
        self, keywords: List[str], since: datetime, until: datetime
    ) -> Iterator[Mention]:
        pass


class HistoricalConnectorFactory:
    def create_historical_connector(
        self, source: str, config: Dict[Any, Any]
    ) -> IHistoricalConnector:
        creation_strategy = {
            "twitter": TwitterHistoricalConnector,
            "hacker-news": HackerNewsHistoricalConnector,
            "google-news": GoogleNewsHistoricalConnector,
            "reddit": RedditHistoricalConnector,
        }
        factory_method = creation_strategy[source]

        return factory_method(config)


class TwitterHistoricalConnector(IHistoricalConnector):
    def __init__(self, config: Dict[Any, Any]):
        auth = tweepy.OAuthHandler(
            config["Default"]["TWITTER_CONSUMER_KEY"],
            config["Default"]["TWITTER_CONSUMER_SECRET"],
        )
        self.api = tweepy.API(auth)

    def download_mentions(
        self, keywords: List[str], since: datetime, until: datetime
    ) -> Iterator[Mention]:
        query = self._build_query(keywords, since)
        tweet_generator = self._search(query, until)

        for tweet in tweet_generator:
            twitter_mention_metadata = self.create_twitter_mention_metadata(tweet)
            urls = tweet.entities["urls"]
            url = urls[0]["url"] if len(urls) > 0 else None
            yield Mention(
                text=tweet.text,
                url=url,
                creation_date=tweet.created_at,
                download_date=datetime.utcnow(),
                source="twitter",
                metadata=twitter_mention_metadata,
            )

    def _build_query(self, keywords: List[str], since: datetime) -> str:
        or_statement = "&OR&".join(keywords)

        query = f"{or_statement}&since={since.date()}"
        return query

    def _search(self, q: str, until: datetime):
        for page in tweepy.Cursor(
            self.api.search,
            q=q,
            count=15,
            result_type="recent",
            include_entities=True,
            until=str(until.date()),
        ).pages():
            for tweet in page:
                yield tweet

    @staticmethod
    def create_twitter_mention_metadata(
        status_json: tweepy.models.Status
    ) -> TwitterMentionMetadata:
        user_json = status_json.user
        return TwitterMentionMetadata(
            followers_count=user_json.followers_count,
            statuses_count=user_json.statuses_count,
            friends_count=user_json.friends_count,
            verified=user_json.verified,
            listed_count=user_json.listed_count,
            retweet_count=status_json.retweet_count,
        )


class HackerNewsHistoricalConnector(IHistoricalConnector):
    def __init__(self, config: Dict[Any, Any]):
        pass

    def download_mentions(
        self, keywords: List[str], since: datetime, until: datetime
    ) -> Iterator[Mention]:
        for keyword in keywords:
            response = self._search(keyword, since, until)
            for hit in response:
                hn_metadata = self.create_hn_mention_metadata(hit)
                yield Mention(
                    text=hit["comment_text"],
                    url=hit["story_url"],
                    creation_date=datetime.strptime(
                        hit["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ"
                    ),
                    download_date=datetime.utcnow(),
                    source="hacker-news",
                    metadata=hn_metadata,
                )

    def _search(self, keyword: str, since: datetime, until: datetime) -> Dict[Any, Any]:
        response = hn.search_by_date(
            q=keyword,
            comments=True,
            created_at__gt=str(since.date()),
            created_at__lt=str(until.date()),
        )
        return response

    @staticmethod
    def create_hn_mention_metadata(hit_json: Dict[Any, Any]) -> HackerNewsMetadata:
        author = hit_json["author"]
        points = hit_json["points"]
        relevancy_score = hit_json["relevancy_score"]
        return HackerNewsMetadata(
            author=author,
            points=points if points is not None else 0,
            relevancy_score=relevancy_score,
        )


class GoogleNewsHistoricalConnector(IHistoricalConnector):
    def __init__(self, config: Dict[Any, Any]):
        self._api_client = NewsApiClient(
            api_key=config["Default"]["GOOGLE_NEWS_API_KEY"]
        )

    def _create_query(self, keywords: List[str]) -> str:
        query = "&OR&".join(keywords)
        return query

    def _search_news(self, keywords: List[str], since: datetime, until: datetime):
        response = self._api_client.get_everything(
            q=self._create_query(keywords),
            from_param=str(since.date()),
            to=str(until.date()),
        )

        assert response["status"] == "ok"
        for article in response["articles"]:
            yield article

    def download_mentions(
        self, keywords: List[str], since: datetime, until: datetime
    ) -> Iterator[Mention]:
        for article in self._search_news(keywords, since, until):
            yield create_gn_mention(article)


class RedditHistoricalConnector(IHistoricalConnector):
    def __init__(self, config: Dict[Any, Any]):
        reddit = praw.Reddit(
            user_agent="Comment Extraction (by /u/balindwalinstalin)",
            client_id=config["Default"]["REDDIT_CLIENT_ID"],
            client_secret=config["Default"]["REDDIT_CLIENT_SECRET"],
        )
        self.reddit = psaw.PushshiftAPI(reddit)

    def download_mentions(
        self, keywords: List[str], since: datetime, until: datetime
    ) -> Iterator[Mention]:

        queries = self._fetch_comments(
            keywords, int(since.timestamp()), int(until.timestamp())
        )
        comments = chain(*queries)
        duplicates = set()  # type: Set[str]

        for comment in filter_removed_comments(comments):
            if comment.id not in duplicates:
                duplicates.add(comment.id)
                yield map_reddit_comment(comment)

    def _fetch_comments(
        self, keywords: List[str], since: int, until: int
    ) -> List[Iterator[praw.models.Comment]]:
        # Pushshift does not allow specifying multiple keywords while searching,
        # thus this has to be an N query
        return [
            self.reddit.search_comments(q=keyword, after=since, before=until)
            for keyword in keywords
        ]
