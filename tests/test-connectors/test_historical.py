from os.path import join, dirname, realpath

import pytest

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
