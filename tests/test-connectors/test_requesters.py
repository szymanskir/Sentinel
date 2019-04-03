import pytest
from sentinel.connectors.api_requesters import HackerNewsAlgoliaRequester
from datetime import datetime


def test_HackerNewAlgoliaRequester_search():
    keyword = "Russia"
    tags = ["comment"]
    since = datetime(2019, 3, 1)
    until = datetime(2019, 3, 4)

    requester = HackerNewsAlgoliaRequester()
    response = requester.search(keyword=keyword,
                                tags=tags,
                                since=since,
                                until=until)

    assert response.status_code == 200
    assert len(response.content) != 0
    for hit in response.json()['hits']:
        assert keyword.lower() in hit['comment_text'].lower()
        assert hit['created_at_i'] < until.timestamp()
        assert hit['created_at_i'] > since.timestamp()

