import pytest
from sentinel.connectors.historical import TwitterHistoricalConnector
from datetime import datetime



@pytest.mark.parametrize(
    "keywords , since, expected", 
    [(['nike', 'reebok'], datetime(2019, 3, 21), 'nike&OR&reebok&since=2019-03-21'),
     (['nike'], datetime(2019, 3, 21), 'nike&since=2019-03-21'),
    ])
def test_TwitterHistoricalConnector_build_query(keywords, since, expected):
    thc = TwitterHistoricalConnector()
    actual = thc._build_query(keywords, since)

    assert actual == expected