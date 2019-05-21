import pytest
from unittest.mock import patch

from sentinel_connectors.keyword_manager import (
    ConstKeywordManager,
    DynamicKeywordManager,
)


def test_DynamicKeywordManager():
    dkm = DynamicKeywordManager()
    dkm.SLEEP_TIME = 0.0

    def mock_generator():
        first_keywords = ["k1a", "k1b"]
        yield first_keywords
        assert set(dkm._current_keywords) == set(first_keywords)
        first_kf = dkm.keyword_finder

        yield first_keywords
        assert dkm.keyword_finder == first_kf
        second_keywords = ["k2a", "k2b", "k2c"]

        yield second_keywords
        assert dkm.keyword_finder != first_kf
        assert set(dkm._current_keywords) == set(second_keywords)

        dkm._exit_event.set()  # next keyword will be last one
        third_keywords = ["k3a"]
        yield third_keywords
        assert False

    g = mock_generator()

    def mock_keywords():
        return next(g)

    with patch.object(
        DynamicKeywordManager, "_get_keywords", side_effect=mock_keywords
    ):
        dkm._update_keywords()
