import pytest
from sentinel_connectors.keyword_finder import KeywordFinder


@pytest.mark.parametrize(
    "keywords , text, expected",
    [
        (["Paris", "life"], "There is no life in Paris", True),
        (["Paris", "life"], "There is no -life- in ,Paris.", True),
        (["Paris", "life"], "There is no night in ,Pyris.", False),
        (["Big Data"], "This is the era of Big Data.", True),
        (["Big  Data"], "This is the era of Big  Data.", True),
        (["Big Data"], "This is the era of Bigger Data.", False),
        (["Big Data"], "This is the era of Bigger Data.", False),
        ([""], "This is the era of Bigger Data.", False),
        ([], "This is the era of Bigger Data.", False),
        (None, "This is the era of Bigger Data.", False),
    ],
)
def test_KeywordFinder(keywords, text, expected):
    kf = KeywordFinder(keywords)
    actual = kf.match(text)

    assert actual == expected
