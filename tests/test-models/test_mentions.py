import pytest
from datetime import datetime
from sentinel.models.mentions import (TweetMetadata, TwitterMentionMetadata,
                                      TwitterUserMetadata, TwitterMention,
                                      HackerNewsMetadata, HackerNewsMention)
from sentinel.utils import read_pickle
from os.path import dirname, join, realpath


@pytest.fixture
def status_json():
    test_cases_dir = join(dirname(realpath(__file__)),
                          'tweet_status_json.pkl')
    return read_pickle(test_cases_dir)


@pytest.fixture
def hacker_news_comment_json():
    test_cases_dir = join(dirname(realpath(__file__)),
                          'hacker_news_russia_json.pkl')
    return read_pickle(test_cases_dir)


@pytest.fixture
def status_with_url_json():
    test_cases_dir = join(dirname(realpath(__file__)),
                          'tweet_status_with_url_json.pkl')
    return read_pickle(test_cases_dir)


@pytest.mark.parametrize("created_at, retweet_count", [('2019-08-30', 100)])
def test_TweetMetadata_init(created_at, retweet_count):
    tweet_metadata = TweetMetadata(created_at, retweet_count)
    assert tweet_metadata.created_at == created_at
    assert tweet_metadata.retweet_count == retweet_count


def test_TweetMetadata_from_status_json(status_json):
    tweet_metadata = TweetMetadata.from_status_json(status_json)
    assert tweet_metadata.created_at == datetime(2019, 3, 29, 12, 45, 54)
    assert tweet_metadata.retweet_count == 4


@pytest.mark.parametrize(
    "followers_count, statuses_count, friends_count, verified, listed_count",
    [(100, 30, 15, False, 30), (100, 30, 15, True, 15)])
def test_TwitterUserMetadata_init(followers_count, statuses_count,
                                  friends_count, verified, listed_count):
    twitter_user_metadata = TwitterUserMetadata(
        followers_count, statuses_count, friends_count, verified, listed_count)

    assert twitter_user_metadata.followers_count == followers_count
    assert twitter_user_metadata.statuses_count == statuses_count
    assert twitter_user_metadata.friends_count == friends_count
    assert twitter_user_metadata.verified == verified
    assert twitter_user_metadata.listed_count == listed_count


def test_TwitterUserMetadata_from_status_json(status_json):
    twitter_user_metadata = TwitterUserMetadata.from_user_json(
        status_json.user)
    assert twitter_user_metadata.followers_count == 2503
    assert twitter_user_metadata.statuses_count == 338796
    assert twitter_user_metadata.friends_count == 3742
    assert twitter_user_metadata.verified is False
    assert twitter_user_metadata.listed_count == 1258


@pytest.mark.parametrize("tweet_metadata, twitter_user_metadata",
                         [(TweetMetadata('2019-08-30', 100),
                           TwitterUserMetadata(100, 30, 15, False, 30))])
def test_TwitterMentionMetadata_init(tweet_metadata, twitter_user_metadata):
    twitter_mention_metadata = TwitterMentionMetadata(tweet_metadata,
                                                      twitter_user_metadata)
    assert twitter_mention_metadata.tweet_metadata == tweet_metadata
    assert twitter_mention_metadata.twitter_user_metadata == twitter_user_metadata


def test_TwitterMentionMetadata_from_status_json(status_json):
    twitter_mention_metadata = TwitterMentionMetadata.from_status_json(
        status_json)
    assert (
            twitter_mention_metadata.tweet_metadata ==
            TweetMetadata.from_status_json(status_json)
    )
    assert (
            twitter_mention_metadata.twitter_user_metadata ==
            TwitterUserMetadata.from_user_json(status_json.user)
    )


def test_TwitterMention_init(status_json):
    metadata = TwitterMentionMetadata.from_status_json(status_json)
    text = 'Sample text'
    url = 'www.url.com'
    twitter_mention = TwitterMention(text, url, metadata)
    assert twitter_mention.text == text
    assert twitter_mention.url == url
    assert twitter_mention.metadata == metadata


def test_TwitterMention_from_status_json(status_json):
    twitter_mention = TwitterMention.from_status_json(status_json)
    metadata = TwitterMentionMetadata.from_status_json(status_json)
    assert twitter_mention.text == 'RT @snopes: Maddow’s audience has dipped on her two days back ' \
                                   'on the air since Attorney General William Barr reported that special counsel…'
    assert twitter_mention.url is None
    assert twitter_mention.metadata == metadata


def test_TwitterMention_from_status_with_url_json(status_with_url_json):
    twitter_mention = TwitterMention.from_status_json(status_with_url_json)
    metadata = TwitterMentionMetadata.from_status_json(status_with_url_json)
    assert twitter_mention.text == 'Pence: Russia’s military move.. "an unwelcome provocation". ' \
                                   'Whereas American militarty moves have been welcome worl… https://t.co/LF0sofqEVD'
    assert twitter_mention.url == 'https://t.co/LF0sofqEVD'
    assert twitter_mention.metadata == metadata


def test_HackerNewsMetadata_from_algolia_empty_points_json(hacker_news_comment_json):
    hacker_news_metadata = HackerNewsMetadata.from_algolia_json(hacker_news_comment_json['hits'][0])

    assert hacker_news_metadata.author == 'arcticbull'
    assert hacker_news_metadata.points == 0
    assert hacker_news_metadata.relevancy_score == 8680


def test_HackerNewsMetadata_from_algolia_non_empty_points_json(hacker_news_comment_json):
    hacker_news_metadata = HackerNewsMetadata.from_algolia_json(hacker_news_comment_json['hits'][1])

    assert hacker_news_metadata.author == 'vl'
    assert hacker_news_metadata.points == 33
    assert hacker_news_metadata.relevancy_score == 8680


def test_HackerNewsMention_from_algolia_empty_points_json(hacker_news_comment_json):
    hacker_news_mention: HackerNewsMention = HackerNewsMention.from_algolia_json(hacker_news_comment_json['hits'][0])

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
    assert hacker_news_mention.url == 'https://www.theverge.com/2019/2/20/18233317/florida-department-of-corrections\
-class-action-lawsuit-william-demler-jpay-mp3-song-access'
    expected_metadata = HackerNewsMetadata.from_algolia_json(hacker_news_comment_json['hits'][0])
    assert hacker_news_mention.metadata == expected_metadata
