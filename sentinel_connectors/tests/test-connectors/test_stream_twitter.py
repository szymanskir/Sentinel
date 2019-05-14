import pytest
from sentinel_connectors.stream import TwitterStreamConnector
from unittest.mock import patch
from datetime import datetime
from os.path import join, dirname, realpath
from sentinel_connectors.utils import read_jsonpickle

MOCK_CONFIG = {
    "Default": {
        "TWITTER_CONSUMER_KEY": "MOCK_KEY",
        "TWITTER_CONSUMER_SECRET": "MOCK_SECRET",
    }
}


def get_tweets_pkl():
    tweets_pkl_path = join(dirname(realpath(__file__)), "twitter-stream_comments.json")
    return read_jsonpickle(tweets_pkl_path)


def mock_get_stream(self):
    return get_tweets_pkl()


def mock_get_api_connection(self, config):
    return None


@pytest.fixture
def tweets_test_case():
    return get_tweets_pkl()


@pytest.fixture
def status_json():
    test_cases_dir = join(
        dirname(realpath(__file__)), "twitter-stream_single_comment.json"
    )
    return read_jsonpickle(test_cases_dir)


def test_TwitterStreamConnector_create_mention_metadata(status_json):
    twitter_mention_metadata = TwitterStreamConnector.create_twitter_mention_metadata(
        status_json
    )
    assert twitter_mention_metadata.followers_count == 358
    assert twitter_mention_metadata.statuses_count == 14584
    assert twitter_mention_metadata.friends_count == 287
    assert twitter_mention_metadata.verified is False
    assert twitter_mention_metadata.listed_count == 4
    assert twitter_mention_metadata.retweet_count == 0


def test_TwitterStreamConnector_download_mentions(tweets_test_case):
    with patch.multiple(
        TwitterStreamConnector,
        _get_stream=mock_get_stream,
        _get_api_connection=mock_get_api_connection,
    ):
        connector = TwitterStreamConnector(config=MOCK_CONFIG)
        mention_generator = connector.stream_comments()
        mention_list = [mention for mention in mention_generator]

        assert len(mention_list) == len(tweets_test_case)
        for mention, tweet_test_case in zip(mention_list, tweets_test_case):
            expected_url = f"https://twitter.com/statuses/{tweet_test_case['id_str']}"
            metadata = connector.create_twitter_mention_metadata(tweet_test_case)
            assert mention.url == expected_url
            assert mention.text == tweet_test_case["text"]
            assert mention.creation_date == datetime.strptime(
                tweet_test_case["created_at"], "%a %b %d %H:%M:%S +0000 %Y"
            )
            assert mention.source == "twitter"
            assert mention.metadata == metadata
