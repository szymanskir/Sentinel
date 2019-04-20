import pytest

from datetime import datetime
from unittest.mock import patch
from os.path import join, dirname, realpath
from sentinel.connectors.historical import GoogleNewsHistoricalConnector 
from sentinel.utils import read_jsonpickle


MOCK_CONFIG = {
    'Default': {
        'GOOGLE_NEWS_API_KEY': 'XXX'
    }
}


def get_gn_articles():
    gn_articles_path = join(dirname(realpath(__file__)), "gn-historical_comments.json")
    return read_jsonpickle(gn_articles_path)


def mock_stream_comments():
    for comment in get_gn_articles():
        yield comment


def test_GoogleNewsHistoricalConnector_create_gn_metadata():
    test_comment = get_gn_articles()[0]
    result = GoogleNewsHistoricalConnector._create_gn_mention_metadata(test_comment)
    assert result.author == "Larry Hryb, Xbox Live's Major Nelson"
    assert result.description == "Spring Sale officially starts today with savings up to 65% on more than 500 digital games and add-on packs for Xbox One and Xbox 360. There are also 95 Xbox One games priced at $10 or less. Check out the full list of savings on Xbox digital games below. Addit…"
    assert result.news_source == "Majornelson.com"


def test_GoogleNewsHistoricalConnector_download_mentions():
    with patch.object(
        GoogleNewsHistoricalConnector,
        "_search_news",
        return_value=mock_stream_comments(),
    ):
        connector = GoogleNewsHistoricalConnector(config=MOCK_CONFIG)
        result = [mention for mention in connector.download_mentions(keywords='microsoft', since=datetime(2019, 4, 4), until=datetime(2019, 4, 5))]

    expected = get_gn_articles()

    assert len(result) == len(expected)
    for r, e in zip(result, expected):
        assert r.text == e["title"]
        assert r.url == e["url"]
        assert r.metadata == GoogleNewsHistoricalConnector._create_gn_mention_metadata(e)
        assert r.source == "google-news"
        assert r.creation_date is not None
