from datetime import datetime
from typing import Dict
from sentinel_common.mentions import GoogleNewsMetadata, Mention
from pydantic import ValidationError


def create_gn_mention(article: Dict) -> Mention:
    text = " ".join(
        filter(None, [article["title"], article["description"], article["content"]])
    )

    try:
        article_metadata = create_gn_mention_metadata(article)

        return Mention(
            text=text,
            url=article["url"],
            origin_date=article["publishedAt"],
            download_date=datetime.utcnow(),
            source="google-news",
            metadata=article_metadata,
        )
    except ValidationError as e:
        raise ValueError("Data parsing error", str(e), str(article)) from e


def create_gn_mention_metadata(article: Dict) -> GoogleNewsMetadata:
    return GoogleNewsMetadata(
        author=article["author"], news_source=article["source"]["name"]
    )
