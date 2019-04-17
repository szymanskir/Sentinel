from datetime import datetime
from os.path import join, dirname, realpath

import pytest

from sentinel.connectors.historical import TwitterHistoricalConnector, ITweetSearcher
from sentinel.models.mentions import TwitterMentionMetadata
from sentinel.utils import read_pickle


def get_tweets_pkl():
    tweets_pkl_path = join(dirname(realpath(__file__)), "tweets.pkl")
    return read_pickle(tweets_pkl_path)


class TweetCursorFactoryMock(ITweetSearcher):
    def search(self, q: str, until: datetime):
        return get_tweets_pkl()


@pytest.fixture
def tweet_cursor_mock():
    return TweetCursorFactoryMock()


@pytest.fixture
def tweets_test_case():
    return get_tweets_pkl()


@pytest.fixture
def status_json():
    test_cases_dir = join(dirname(realpath(__file__)), "tweet_status_json.pkl")
    return read_pickle(test_cases_dir)


@pytest.mark.parametrize(
    "keywords , since, expected",
    [
        (["nike", "reebok"], datetime(2019, 3, 21), "nike&OR&reebok&since=2019-03-21"),
        (["nike"], datetime(2019, 3, 21), "nike&since=2019-03-21"),
    ],
)
def test_TwitterHistoricalConnector_build_query(keywords, since, expected):
    thc = TwitterHistoricalConnector()
    actual = thc._build_query(keywords, since)

    assert actual == expected


def test_TwitterHistoricalConnector_create_mention_metadata(status_json):
    twitter_mention_metadata = TwitterHistoricalConnector.create_twitter_mention_metadata(
        status_json
    )
    assert twitter_mention_metadata.followers_count == 2503
    assert twitter_mention_metadata.statuses_count == 338796
    assert twitter_mention_metadata.friends_count == 3742
    assert twitter_mention_metadata.verified is False
    assert twitter_mention_metadata.listed_count == 1258
    assert twitter_mention_metadata.retweet_count == 4


def test_TwitterHistoricalConnector_download_mentions(
    tweet_cursor_mock, tweets_test_case
):
    connector = TwitterHistoricalConnector(tweet_cursor_mock)
    mention_generator = connector.download_mentions(
        ["nike", "reebok"], datetime(2019, 3, 21), None
    )
    mention_list = [mention for mention in mention_generator]
    assert len(mention_list) == len(tweets_test_case)
    for mention, tweet_test_case in zip(mention_list, tweets_test_case):
        urls = tweet_test_case.entities["urls"]
        expected_url = urls[0]["url"] if len(urls) > 0 else None
        metadata = connector.create_twitter_mention_metadata(tweet_test_case)
        assert mention.url == expected_url
        assert mention.text == tweet_test_case.text
        assert mention.creation_date == tweet_test_case.created_at
        assert mention.source == "twitter"
        assert mention.metadata == metadata
