import pytest

from datetime import datetime
from unittest.mock import patch
from os.path import join, dirname, realpath
from sentinel.connectors.historical import GoogleNewsHistoricalConnector
from sentinel.connectors.stream import GoogleNewsStreamConnector
from sentinel.connectors.gn_common import create_gn_mention, create_gn_mention_metadata 
from sentinel.utils import read_jsonpickle


MOCK_CONFIG = {
    'Default': {
        'GOOGLE_NEWS_API_KEY': 'XXX'
    }
}


def get_gn_articles():
    gn_articles_path = join(dirname(realpath(__file__)), "gn-historical_comments.json")
    return read_jsonpickle(gn_articles_path)


def mock_comments():
    for comment in get_gn_articles():
        yield comment


def test_GoogleNewsHistoricalConnector_create_gn_metadata():
    test_comment = get_gn_articles()[0]
    result = create_gn_mention_metadata(test_comment)
    assert result.author == "Larry Hryb, Xbox Live's Major Nelson"
    assert result.news_source == "Majornelson.com"


def test_GoogleNewsHistoricalConnector_download_mentions():
    with patch.object(
        GoogleNewsHistoricalConnector,
        "_search_news",
        return_value=mock_comments(),
    ):
        connector = GoogleNewsHistoricalConnector(config=MOCK_CONFIG)
        result = [mention for mention in connector.download_mentions(keywords='microsoft', since=datetime(2019, 4, 4), until=datetime(2019, 4, 5))]

    expected = get_gn_articles()

    assert len(result) == len(expected)
    for r, e in zip(result, expected):
        assert r.text == " ".join(filter(None, [e["title"], e["description"], e["content"]]))
        assert r.url == e["url"]
        assert r.metadata == create_gn_mention_metadata(e)
        assert r.source == "google-news"
        assert r.creation_date is not None


def test_GoogleNewsStreamConnector_download_mentions():
    with patch.object(
        GoogleNewsStreamConnector,
        "_search_top_stories",
        return_value=mock_comments(),
    ):
        connector = GoogleNewsStreamConnector(config=MOCK_CONFIG)
        result = [mention for mention in connector.stream_comments()]

    expected = get_gn_articles()

    assert len(result) == len(expected)
    for r, e in zip(result, expected):
        assert r.text == " ".join(filter(None, [e["title"], e["description"], e["content"]]))
        assert r.url == e["url"]
        assert r.metadata == create_gn_mention_metadata(e)
        assert r.source == "google-news"
        assert r.creation_date is not None