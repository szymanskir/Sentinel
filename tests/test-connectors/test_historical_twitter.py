import pytest
from unittest.mock import patch

from datetime import datetime
from os.path import join, dirname, realpath
from sentinel.connectors.historical import TwitterHistoricalConnector
from sentinel.models.mentions import TwitterMentionMetadata
from sentinel.utils import read_pickle, read_jsonpickle

MOCK_CONFIG = {
    "Default": {
        "TWITTER_CONSUMER_KEY": "MOCK_KEY",
        "TWITTER_CONSUMER_SECRET": "MOCK_SECRET",
    }
}


def get_tweets_pkl():
    tweets_pkl_path = join(dirname(realpath(__file__)), "twitter-historical_comments.pkl")
    return read_pickle(tweets_pkl_path)


def mock_search():
    return get_tweets_pkl()


@pytest.fixture
def tweets_test_case():
    return get_tweets_pkl()


@pytest.fixture
def status_json():
    test_cases_dir = join(dirname(realpath(__file__)), "twitter-single_comment.json")
    return read_jsonpickle(test_cases_dir)


@pytest.mark.parametrize(
    "keywords , since, expected",
    [
        (["nike", "reebok"], datetime(2019, 3, 21), "nike&OR&reebok&since=2019-03-21"),
        (["nike"], datetime(2019, 3, 21), "nike&since=2019-03-21"),
    ],
)
def test_TwitterHistoricalConnector_build_query(keywords, since, expected):
    thc = TwitterHistoricalConnector(config=MOCK_CONFIG)
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


def test_TwitterHistoricalConnector_download_mentions(tweets_test_case):
    with patch.object(
        TwitterHistoricalConnector, "_search", return_value=mock_search()
    ):
        connector = TwitterHistoricalConnector(config=MOCK_CONFIG)
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
