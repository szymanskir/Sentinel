from os.path import join, dirname, realpath

import pytest

from sentinel.connectors.api_requesters import IHackerNewsAlgoliaRequester
from sentinel.connectors.historical import TwitterHistoricalConnector, HackerNewsHistoricalConnector
from typing import List, Generator
from datetime import datetime

from sentinel.models.mentions import Mention, HackerNewsMention, HackerNewsMetadata
from sentinel.utils import read_pickle


@pytest.mark.parametrize(
    "keywords , since, expected", 
    [(['nike', 'reebok'], datetime(2019, 3, 21), 'nike&OR&reebok&since=2019-03-21'),
     (['nike'], datetime(2019, 3, 21), 'nike&since=2019-03-21'),
    ])
def test_TwitterHistoricalConnector_build_query(keywords, since, expected):
    thc = TwitterHistoricalConnector()
    actual = thc._build_query(keywords, since)

    assert actual == expected

class HackerNewsAlgoliaRequesterMock(IHackerNewsAlgoliaRequester):
    def search(self, keyword: str, tags: List[str], since: datetime,
                          until: datetime):

        if keyword.lower == 'russia':
            return read_pickle(join(dirname(realpath(__file__)), '../test-models/hacker_news_russia_json.pkl'))

        elif keyword.lower == 'foo':
            return read_pickle(join(dirname(realpath(__file__)), 'hacker_news_foo_json.pkl'))



@pytest.mark.parametrize(
    "keywords, expected",
    [(['russia'], 20), (['foo'], 20), (['foo','russia'], 40)])
def test_HackerNewsHistoricalConnector_download_mentions(keywords: List[str], expected: int):
    requester_mock = HackerNewsAlgoliaRequesterMock()
    connector = HackerNewsHistoricalConnector(requester_mock)

    mentions = [mention for mention in connector.download_mentions(['russia'], datetime(2019, 3, 1),
                                                                   datetime(2019, 3, 4))]
    assert len(mentions) == expected
