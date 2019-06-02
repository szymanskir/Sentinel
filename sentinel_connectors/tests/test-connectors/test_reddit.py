import pytest
from unittest.mock import patch

from os.path import join, dirname, realpath
from sentinel_connectors.reddit_common import (
    filter_removed_comments,
    map_reddit_comment,
)
from sentinel_connectors.historical import RedditHistoricalConnector
from sentinel_connectors.utils import read_pickle
from datetime import datetime
from sentinel_connectors.secrets_manager import RedditSecretsManager

MOCK_CONFIG = MOCK_CONFIG = {
    "REDDIT_CLIENT_ID": "*******",
    "REDDIT_CLIENT_SECRET": "*******",
}


# pickle contains 5 good comments and 1 deleted, without body and author
@pytest.fixture
def reddit_comments():
    path = join(dirname(realpath(__file__)), "reddit.pkl")
    return read_pickle(path)


def test_map_reddit_comment(reddit_comments):
    comment = reddit_comments[0]
    result = map_reddit_comment(comment)

    expected_text = (
        "It's a hard thing to photo, it looks better in real life. "
        + "Such a cool deck with a truly inspiring story."
    )
    expected_url = (
        "https://reddit.com/r/playingcards/comments/"
        + "bdlrsv/bike_ww2_map_awesome_deck/ekz2bdl/"
    )

    assert result.text == expected_text
    assert result.url == expected_url
    assert result.origin_date.timestamp() == 1555365599
    assert result.download_date is not None
    assert result.source == "reddit"

    assert result.metadata.redditor == "1zgw3jt5"
    assert result.metadata.score == 8
    assert result.metadata.redditor_link_karma == 473
    assert result.metadata.redditor_comment_karma == 417


def test_deleted_comments_filtering(reddit_comments):
    result = list(filter_removed_comments(reddit_comments))
    assert len(result) == len(reddit_comments) - 1


def test_RedditHistoricalConnector_merging_comments(reddit_comments):
    with patch.object(
        RedditHistoricalConnector,
        "_fetch_comments",
        return_value=[reddit_comments[:3], reddit_comments[3:]],
    ), patch.object(RedditSecretsManager, "get_secrets", return_value=MOCK_CONFIG):
        connector = RedditHistoricalConnector(RedditSecretsManager())
        results = connector.download_mentions(
            ["life"], datetime(2019, 4, 15), datetime(2019, 4, 20)
        )
        results = list(results)

        assert len(results) == len(reddit_comments) - 1
        for exp, act in zip(reddit_comments, results):
            assert act.text == exp.body
            assert act.url == "https://reddit.com" + exp.permalink
            assert act.origin_date.timestamp() == int(exp.created_utc)
            assert act.download_date is not None
            assert act.source == "reddit"

            assert act.metadata.redditor == exp.author.id
            assert act.metadata.score == exp.score
            assert act.metadata.redditor_link_karma == exp.author.link_karma
            assert act.metadata.redditor_comment_karma == exp.author.comment_karma


def test_RedditHistoricalConnector_deduplicates_comments(reddit_comments):
    reddit_comments = reddit_comments[:3]
    reddit_comments[0].id = "foo"
    reddit_comments[1].id = "foo"

    with patch.object(
        RedditHistoricalConnector, "_fetch_comments", return_value=[reddit_comments]
    ), patch.object(RedditSecretsManager, "get_secrets", return_value=MOCK_CONFIG):
        connector = RedditHistoricalConnector(RedditSecretsManager())

        results = connector.download_mentions(
            ["life"], datetime(2019, 4, 15), datetime(2019, 4, 20)
        )
        results = list(results)

        assert len(results) == 2
        assert results[0].url != results[1].url
