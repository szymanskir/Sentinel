import pytest
from unittest.mock import patch

from os.path import join, dirname, realpath
from sentinel_connectors.stream import HackerNewsStreamConnector
from sentinel_connectors.utils import read_jsonpickle
from sentinel_connectors.hn_common import clean_html




def get_hn_comments_jsonpkl():
    hn_comments_jsonpkl_path= join(dirname(realpath(__file__)), "hn-stream_comments.json")
    return read_jsonpickle(hn_comments_jsonpkl_path)


def mock_stream_comments():
    for comment in get_hn_comments_jsonpkl():
        yield comment


@pytest.fixture
def hn_comments():
    return get_hn_comments_jsonpkl()


def test_HackerNewsStreamConnector_create_mention(hn_comments):
    test_comment = hn_comments[0]
    result = HackerNewsStreamConnector._create_hn_mention(test_comment)
    expected_text = "I always saw these tons of little packages are as a bad idea as they make package management (from the user's perspective) harder, they do not really provide any space benefit (code is small), if anything they make loading slower (i wrote a benchmark some time ago and a binary linked against a single dynamic library with tons of exports was faster to load than a binary linked against several dynamic libraries with fewer exports - but overall the same number of imports) and AFAIK the OS wont keep the entire library in memory anyway if it isn't needed (if anything the extra housework needed to all the libraries are probably a net negative). And of course these intimidating lists.And in practice applications do not use one or two of them, they use several of them and those libraries bring in several others, etc like spaghetti (so you have Konsole relying on Phonon as mentioned in another reply)."
    assert result.metadata.author == "Crinus"
    assert result.metadata.points is None
    assert result.metadata.relevancy_score is None
    assert result.text == expected_text
    assert result.url == "https://news.ycombinator.com/item?id=19691521"


def test_HackerNewsStreamConnector_stream_comments(hn_comments):
    with patch.object(
        HackerNewsStreamConnector,
        "_stream_comments",
        return_value=mock_stream_comments(),
    ):
        connector = HackerNewsStreamConnector(None)
        result = [mention for mention in connector.stream_comments()]

    expected = [
        HackerNewsStreamConnector._create_hn_mention(comment) for comment in hn_comments
    ]

    assert len(result) == len(expected)
    for r, e in zip(result, expected):
        assert r.text == clean_html(e.text)
        assert r.url == e.url
        assert r.metadata == e.metadata
        assert r.source == "hacker-news"
        assert r.creation_date is not None
