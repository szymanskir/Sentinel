from datetime import datetime
from typing import Dict
from ..models.mentions import GoogleNewsMetadata, Mention


def create_gn_mention(article: Dict) -> Mention:
    article_metadata = create_gn_mention_metadata(article)
    text = " ".join(
        filter(None, [article["title"], article["description"], article["content"]])
    )
    return Mention(
        text=text,
        url=article["url"],
        creation_date=article["publishedAt"],
        download_date=datetime.utcnow(),
        source="google-news",
        metadata=article_metadata,
    )


def create_gn_mention_metadata(article: Dict) -> GoogleNewsMetadata:
    return GoogleNewsMetadata(
        author=article["author"], news_source=article["source"]["name"]
    )
