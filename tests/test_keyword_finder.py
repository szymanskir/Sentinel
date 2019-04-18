import pytest
from sentinel.keyword_finder import KeywordFinder

@pytest.mark.parametrize(
    "keywords , text, expected", 
    [(["Paris", "life"], "There is no life in Paris", ["Paris", "life"]),
    (["Paris", "life"], "There is no -life- in ,Paris.", ["Paris", "life"])
    ])
def test_KeywordFinder(keywords, text, expected):
    kf = KeywordFinder(keywords)
    actual = kf.match(text)

    assert actual == expected