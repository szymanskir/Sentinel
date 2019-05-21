import pytest
import numpy as np
import pandas as pd

from datetime import datetime
from sentinel_backend.visualization import create_mentions_count_plot
from os.path import join, dirname, realpath


@pytest.fixture
def test_mentions():
    data_filepath = join(dirname(realpath(__file__)), "test_mentions_data.json")
    return pd.read_json(data_filepath)


def test_create_mentions_count_plot(test_mentions):
    result = create_mentions_count_plot(test_mentions)
    expected = [
        {
            "x": np.array([datetime(2017, 8, 31, 11, 10, 0)]),
            "y": np.array([1]),
            type: "scatter",
            "mode": "lines+points",
        },
        {
            "x": np.array(
                [datetime(2017, 8, 31, 11, 9, 0), datetime(2017, 8, 31, 11, 10, 0)]
            ),
            "y": np.array([2, 1]),
            type: "scatter",
            "mode": "lines+points",
        },
    ]
    assert result == expected
