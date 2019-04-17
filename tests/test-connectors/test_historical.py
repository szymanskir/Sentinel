
from datetime import datetime
from os.path import join, dirname, realpath

import pytest

from sentinel.connectors.historical import TwitterHistoricalConnector, ITweetSearcher
from sentinel.models.mentions import TwitterMentionMetadata
from sentinel.utils import read_pickle


def get_tweets_pkl():
    tweets_pkl_path = join(dirname(realpath(__file__)), 'tweets.pkl')
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


@pytest.mark.parametrize(
    "keywords , since, expected", 
    [(['nike', 'reebok'], datetime(2019, 3, 21), 'nike&OR&reebok&since=2019-03-21'),
     (['nike'], datetime(2019, 3, 21), 'nike&since=2019-03-21'),
    ])
def test_TwitterHistoricalConnector_build_query(keywords, since, expected):
    thc = TwitterHistoricalConnector()
    actual = thc._build_query(keywords, since)

    assert actual == expected


def test_TwitterHistoricalConnector_download_mentions(tweet_cursor_mock, tweets_test_case):
    connector = TwitterHistoricalConnector(tweet_cursor_mock)
    mention_generator = connector.download_mentions(['nike', 'reebok'], datetime(2019, 3, 21), None)
    mention_list = [mention for mention in mention_generator]
    assert len(mention_list) == len(tweets_test_case)
    for mention, tweet_test_case in zip(mention_list, tweets_test_case):
        urls = tweet_test_case.entities["urls"]
        expected_url = urls[0]["url"] if len(urls) > 0 else None
        metadata = TwitterMentionMetadata.from_status_json(tweet_test_case)
        assert mention.url == expected_url
        assert mention.text == tweet_test_case.text
        assert mention.creation_date == tweet_test_case.created_at
        assert mention.source == 'twitter'
        assert mention.metadata == metadata
