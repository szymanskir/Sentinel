import pytest
from sentinel_common.all_keywords_matcher import AllKeywordsMatcher


@pytest.mark.parametrize(
    "keywords , text, expected",
    [
        (["Paris", "life"], "There is no life in Paris", ["life", "Paris"]),
        (["Paris", "life"], "There is no -life- in ,Paris.",
         ["life", "Paris"]),
        (["Paris", "life"], "There is no night in ,Pyris.", []),
        ([" "], "There is no night in ,Pyris.", []),
        ([""], "There is no night in ,Pyris.", []),
        (["Big Data"], "This is the era of Big Data.", ["Big Data"]),
        (["Big Data"], "This is the era of Bigger Data.", []),
    ],
)
def test_find_all_keywords(keywords, text, expected):
    matcher = AllKeywordsMatcher(set(keywords))
    assert matcher.all_occurring_keywords(text) == expected
