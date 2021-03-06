import pytest

from sentinel_common.mentions import TwitterMetadata, HackerNewsMetadata, Mention
from datetime import datetime


@pytest.mark.parametrize(
    "obj",
    [
        TwitterMetadata(
            user_id=2782689,
            followers_count=1,
            statuses_count=2,
            friends_count=3,
            verified=True,
            listed_count=4,
            retweet_count=5,
        )
    ],
)
def test_TwitterMentionMetadata(obj):
    json_rep = obj.json()
    recreated_obj = TwitterMetadata.parse_raw(json_rep)
    assert recreated_obj == obj


@pytest.mark.parametrize(
    "obj", [HackerNewsMetadata(author="John Doe", points=2, relevancy_score=3)]
)
def test_HackerNewsMetadata(obj):
    json_rep = obj.json()
    recreated_obj = HackerNewsMetadata.parse_raw(json_rep)
    assert recreated_obj == obj


@pytest.mark.parametrize(
    "obj",
    [
        Mention(
            text="Lorem ipsum",
            url="https://example.com",
            origin_date=datetime(2019, 4, 13),
            download_date=datetime(2019, 4, 13),
            source="twitter",
            metadata=HackerNewsMetadata(author="John Doe", points=2, relevancy_score=3),
        ),
        Mention(
            text="Lorem ipsum",
            url="https://example.com",
            origin_date=datetime(2019, 4, 13),
            download_date=datetime(2019, 4, 13),
            source="twitter",
            metadata=TwitterMetadata(
                user_id=2899563827,
                followers_count=1,
                statuses_count=2,
                friends_count=3,
                verified=True,
                listed_count=4,
                retweet_count=5,
            ),
        ),
    ],
)
def test_Mention(obj):
    json_rep = obj.to_json()
    recreated_obj = Mention.from_json(json_rep)
    assert recreated_obj == obj
