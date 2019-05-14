import re
from bs4 import BeautifulSoup


def clean_urls(text):
    return re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*',
                  '', text)


def clean_emojis(text):
    return text.encode('ascii', errors='ignore').decode()


def clean_tweet_user_mentions(text):
    return re.sub(r'@([_a-zA-Z0-9]{1,15})', '', text)


def clean_hashtags(text):
    return re.sub("([^0-9A-Za-z \t])", " ", text)


def clean_comment_text(text):
    return clean_hashtags(clean_tweet_user_mentions(
        clean_urls(clean_emojis(text))))


def clean_html_tags(text):
    return BeautifulSoup(text).text


def clean_article_text(text):
    return clean_comment_text(clean_html_tags(text))
