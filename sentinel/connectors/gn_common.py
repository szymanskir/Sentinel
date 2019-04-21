from datetime import datetime
from ..models.mentions import GoogleNewsMetadata, Mention


class GoogleNewsCommonUtils:

    def create_gn_mention(self, article) -> Mention:
        article_metadata = self.create_gn_mention_metadata(article)
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

    def create_gn_mention_metadata(self, article) -> GoogleNewsMetadata:
        return GoogleNewsMetadata(
            author=article["author"], news_source=article["source"]["name"]
        )
