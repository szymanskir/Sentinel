import pytest
from sentinel.models.mentions import HackerNewsMetadata, HackerNewsMention
from sentinel.utils import read_pickle
from os.path import dirname, join, realpath


@pytest.fixture
def hacker_news_comment_json():
    test_cases_dir = join(dirname(realpath(__file__)), "hacker_news_russia_json.pkl")
    return read_pickle(test_cases_dir)


def test_HackerNewsMetadata_from_algolia_empty_points_json(hacker_news_comment_json):
    hacker_news_metadata = HackerNewsMetadata.from_algolia_json(
        hacker_news_comment_json["hits"][0]
    )

    assert hacker_news_metadata.author == "arcticbull"
    assert hacker_news_metadata.points == 0
    assert hacker_news_metadata.relevancy_score == 8680


def test_HackerNewsMetadata_from_algolia_non_empty_points_json(
    hacker_news_comment_json
):
    hacker_news_metadata = HackerNewsMetadata.from_algolia_json(
        hacker_news_comment_json["hits"][1]
    )

    assert hacker_news_metadata.author == "vl"
    assert hacker_news_metadata.points == 33
    assert hacker_news_metadata.relevancy_score == 8680


def test_HackerNewsMention_from_algolia_empty_points_json(hacker_news_comment_json):
    hacker_news_mention: HackerNewsMention = HackerNewsMention.from_algolia_json(
        hacker_news_comment_json["hits"][0]
    )

    expected_comment_text = 'Thing is, I totally randomly met a British criminologist while visiting Svalbard a few \
years ago and I spent a while talking to him. He generally agrees that homogeneity reduces problems in a society. \
If everyone&#x27;s the same, everyone kind of gets along. There is merit to that argument for better or worse, \
although I believe we can also move past that in time.<p>Regarding incarceration rates specifically, the next 3 \
leading jailers behind the US (Russia, the Ukraine and Poland) are unbelievably homogeneous. I believe Poland is \
almost 97% white [1]. They&#x27;re my people, so I think I can safely say, they consider a mild tan to represent \
diversity. There are homogenous countries that lock people up, and there are homogenous countries that don&#x27;t. \
There are also diverse countries that lock people up, and diverse countries that don&#x27;t.<p>I was trying to be \
very careful in not comparing Norway&#x27;s incarceration rate (which is, itself, 1&#x2F;10th of the US) but \
rather their substantially lower recidivism rate which I think one can more easily treat as an apples-to-apples \
comparison, meaning that there is room to improve on the process.<p>[1] <a href="https:&#x2F;&#x2F;\
www.chicagotribune.com&#x2F;news&#x2F;ct-xpm-2005-10-16-0510150186-story.html" rel="nofollow">https:&#x2F;&#x2F;\
www.chicagotribune.com&#x2F;news&#x2F;ct-xpm-2005-10-16-051015...</a>'

    assert hacker_news_mention.text == expected_comment_text
    assert (
        hacker_news_mention.url
        == "https://www.theverge.com/2019/2/20/18233317/florida-department-of-corrections\
-class-action-lawsuit-william-demler-jpay-mp3-song-access"
    )
    expected_metadata = HackerNewsMetadata.from_algolia_json(
        hacker_news_comment_json["hits"][0]
    )
    assert hacker_news_mention.metadata == expected_metadata
