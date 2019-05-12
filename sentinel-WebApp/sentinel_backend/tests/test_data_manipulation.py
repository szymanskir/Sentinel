import pytest 
import pandas as pd

from datetime import datetime
from sentinel_backend.data_manipulation import get_keywords_mention_count
from os.path import join, dirname, realpath


@pytest.fixture
def test_mentions():
    data_filepath = join(dirname(realpath(__file__)), "test_mentions_data.json")
    return pd.read_json(data_filepath)


def test_get_keywords_mention_count(test_mentions):
    result = get_keywords_mention_count(test_mentions)
    expected = pd.DataFrame({
        'keyword': ['javascript', 'javascript', 'nike'],
        'date': [datetime(2017, 8, 31, 11, 9, 0), datetime(2017, 8, 31, 11, 10, 0), datetime(2017, 8, 31, 11, 10, 0)],
        'counts':  [2, 1, 1]
    })
    assert result.equals(expected)
