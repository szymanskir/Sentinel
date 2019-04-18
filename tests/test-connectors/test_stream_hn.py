import pytest

from os.path import join, dirname, realpath
from sentinel.connectors.stream import (
    IHackerNewsStreamReader,
    HackerNewsStreamConnector,
)
from sentinel.utils import read_pickle


def get_hn_comments_pkl():
    hn_comments_pkl_path = join(dirname(realpath(__file__)), "hn_stream_comments.pkl")
    return read_pickle(hn_comments_pkl_path)


class HackerNewsStreamReaderMock(IHackerNewsStreamReader):
    def stream_comments(self):
        for comment in get_hn_comments_pkl():
            yield comment


@pytest.fixture
def hn_comments():
    return get_hn_comments_pkl()


@pytest.fixture
def hacker_news_searcher_mock():
    return HackerNewsStreamReaderMock()


def test_HackerNewsStreamConnector_create_mention(hn_comments):
    test_comment = hn_comments[0]
    result = HackerNewsStreamConnector._create_hn_mention(test_comment)
    expected_text = "<p>I always saw these tons of little packages are as a bad idea as they make package management (from the user&#x27;s perspective) harder, they do not really provide any space benefit (code is small), if anything they make loading slower (i wrote a benchmark some time ago and a binary linked against a single dynamic library with tons of exports was faster to load than a binary linked against several dynamic libraries with fewer exports - but overall the same number of imports) and AFAIK the OS wont keep the entire library in memory anyway if it isn&#x27;t needed (if anything the extra housework needed to all the libraries are probably a net negative). And of course these intimidating lists.</p><p>And in practice applications do not use one or two of them, they use several of them and those libraries bring in several others, etc like spaghetti (so you have Konsole relying on Phonon as mentioned in another reply).</p>"
    assert result.metadata.author == "Crinus"
    assert result.metadata.points is None
    assert result.metadata.relevancy_score is None
    assert result.text == expected_text


def test_HackerNewsStreamConnector_stream_comments(
    hn_comments, hacker_news_searcher_mock
):
    connector = HackerNewsStreamConnector(hacker_news_searcher_mock)
    result = [mention for mention in connector.stream_comments()]
    expected = [
        HackerNewsStreamConnector._create_hn_mention(comment) for comment in hn_comments
    ]

    assert len(result) == len(expected)
    for r, e in zip(result, expected):
        assert r.text == e.text
        assert r.url == e.url
        assert r.metadata == e.metadata
        assert r.source == "hacker-news"
        assert r.creation_date is not None
