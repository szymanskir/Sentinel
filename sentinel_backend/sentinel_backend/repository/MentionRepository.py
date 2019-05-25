import pandas as pd
from datetime import datetime
from sentinel_common.db_models import MentionDb, MentionDateIndex
from typing import List


class MentionRepository:
    def get_mentions(
        self, user: str, since: datetime, until: datetime, keywords: List[str]
    ):
        queries = [
            MentionDateIndex.query(keyword, MentionDb.origin_date.between(since, until))
            for keyword in keywords
        ]

        mentions = []
        for keyword in queries:
            for m in keyword:
                mentions.append(map_mention_to_dto(m))

        return pd.DataFrame.from_records(mentions)


def map_mention_to_dto(m: MentionDb) -> dict:
    return {
        "author": m.author,
        "origin_date": m.origin_date,
        "keyword": m.keyword,
        "id": m.id,
        "download_date": m.download_date,
        "text": m.text,
        "url": m.url,
        "source": m.source,
        "sentiment_score": m.sentiment_score,
        "metadata": m.metadata,
    }
