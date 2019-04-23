import pytest

from datetime import datetime
from newsapi import NewsApiClient
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




def mock_response():
    gn_response_path = join(dirname(realpath(__file__)), "gn-example_response.json")
    return read_jsonpickle(gn_response_path)

def mock_response_with_latest_article_removed():
    response = mock_response()
    response["articles"] = response["articles"][1:]
    return response

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
        "_listen_top_stories",
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

def test_GoogleNewsStreamConnector_duplicates_filtering():
    @patch.object(
        GoogleNewsStreamConnector,
        "_retrieve_news_sources",
        return_value="bbc.com"
    )
    def execute_test(mock_stream_connector):
        connector = GoogleNewsStreamConnector(config=MOCK_CONFIG)
        with patch.object(
            NewsApiClient,
            "get_top_headlines",
            return_value=mock_response_with_latest_article_removed()
        ):
            # run first request to set time of latest retrieved article
            first = connector._search_top_stories()
            first = [x for x in first]
        
        with patch.object(
            NewsApiClient,
            "get_top_headlines",
            return_value=mock_response(),
        ):
            second = connector._search_top_stories()
            assert next(second) == mock_response()["articles"][0]
        
    
    execute_test()