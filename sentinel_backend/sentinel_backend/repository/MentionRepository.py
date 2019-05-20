import pandas as pd
from datetime import datetime
from sentinel_common.db_models import Mention, MentionDateIndex
from typing import List


class MentionRepository:
    def get_mentions(
        self, user: str, since: datetime, until: datetime, keywords: List[str]
    ):
        queries = [
            MentionDateIndex.query(keyword, Mention.date.between(since, until))
            for keyword in keywords
        ]

        mentions = []
        for keyword in queries:
            for m in keyword:
                mentions.append(map_mention_to_dto(m))

        return pd.DataFrame.from_records(mentions)


def map_mention_to_dto(m: Mention) -> dict:
    return {
        "author": m.author,
        "text": m.text,
        "date": m.date,
        "sentimentScore": m.sentimentScore,
        "keyword": m.keyword,
    }