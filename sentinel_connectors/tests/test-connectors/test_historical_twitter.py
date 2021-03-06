import pytest
from unittest.mock import patch

from datetime import datetime
from os.path import join, dirname, realpath
from sentinel_connectors.historical import TwitterHistoricalConnector
from sentinel_connectors.utils import read_pickle, read_jsonpickle
from sentinel_connectors.secrets_manager import TwitterSecretsManager

MOCK_SECRETS = {
    "TWITTER_CONSUMER_KEY": "MOCK_KEY",
    "TWITTER_CONSUMER_SECRET": "MOCK_SECRET",
}


def get_tweets_pkl():
    tweets_pkl_path = join(
        dirname(realpath(__file__)), "twitter-historical_comments.pkl"
    )
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
    "keywords, expected", [(["nike", "reebok"], "nike&OR&reebok"), (["nike"], "nike")]
)
def test_TwitterHistoricalConnector_build_query(keywords, expected):
    with patch.object(TwitterSecretsManager, "get_secrets", return_value=MOCK_SECRETS):
        thc = TwitterHistoricalConnector(TwitterSecretsManager())
        actual = thc._build_query(keywords)

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
    ), patch.object(TwitterSecretsManager, "get_secrets", return_value=MOCK_SECRETS):
        connector = TwitterHistoricalConnector(TwitterSecretsManager())
        mention_generator = connector.download_mentions(
            ["nike", "reebok"], datetime(2019, 3, 21), None
        )
        mention_list = [mention for mention in mention_generator]

    assert len(mention_list) == len(tweets_test_case)
    for mention, tweet_test_case in zip(mention_list, tweets_test_case):
        expected_url = f"https://twitter.com/{tweet_test_case.user.screen_name}/status/{tweet_test_case.id_str}"
        metadata = connector.create_twitter_mention_metadata(tweet_test_case)
        assert mention.url == expected_url
        assert mention.text == tweet_test_case.text
        assert mention.origin_date == tweet_test_case.created_at
        assert mention.source == "twitter"
        assert mention.metadata == metadata
