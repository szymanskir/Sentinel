import pytest
from unittest.mock import patch

from datetime import datetime
from os.path import join, dirname, realpath
from sentinel_connectors.utils import read_jsonpickle
from sentinel_connectors.historical import HackerNewsHistoricalConnector
from sentinel_connectors.hn_common import clean_html


def get_hn_comments_jsonpkl():
    hn_comments_jsonpkl_path = join(
        dirname(realpath(__file__)), "hn-historical_comments.json"
    )
    return read_jsonpickle(hn_comments_jsonpkl_path)


def mock_search():
    return get_hn_comments_jsonpkl()


@pytest.fixture
def hn_comments():
    return get_hn_comments_jsonpkl()


@pytest.fixture
def hacker_news_comment_json():
    hn_comments_russia_json_pkl_path = join(
        dirname(realpath(__file__)), "hn-historical-russia.json"
    )
    return read_jsonpickle(hn_comments_russia_json_pkl_path)


def test_HackerNewsMetadata_create_metadata_empty_points_json(hacker_news_comment_json):
    hacker_news_metadata = HackerNewsHistoricalConnector.create_hn_mention_metadata(
        hacker_news_comment_json["hits"][0]
    )

    assert hacker_news_metadata.author == "arcticbull"
    assert hacker_news_metadata.points == 0
    assert hacker_news_metadata.relevancy_score == 8680


def test_HackerNewsHistoricalConnector_create_metadata(hacker_news_comment_json):
    hacker_news_metadata = HackerNewsHistoricalConnector.create_hn_mention_metadata(
        hacker_news_comment_json["hits"][1]
    )

    assert hacker_news_metadata.author == "vl"
    assert hacker_news_metadata.points == 33
    assert hacker_news_metadata.relevancy_score == 8680


def test_HackerNewsHistoricalConnector_download_mentions(hn_comments):
    with patch.object(
        HackerNewsHistoricalConnector, "_search", return_value=mock_search()
    ):
        connector = HackerNewsHistoricalConnector(None)
        mention_generator = connector.download_mentions(
            ["microsoft"], datetime(2019, 4, 10), datetime(2019, 4, 13)
        )
        mention_list = [mention for mention in mention_generator]

    for mention, hn_comment in zip(mention_list, hn_comments):
        metadata = connector.create_hn_mention_metadata(hn_comment)
        assert mention.text == clean_html(hn_comment["comment_text"])
        assert mention.url == hn_comment["story_url"]
        assert mention.creation_date == datetime.strptime(
            hn_comment["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        assert mention.source == "hacker-news"
        assert mention.metadata == metadata
