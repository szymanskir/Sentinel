from typing import List
from datetime import datetime
from .models import Mention, Keyword, MentionDateIndex


class DynamoDbRepository:
    def get_mentions(
            self,
            user: str,
            since: datetime,
            until: datetime,
            keywords: List[str]):

        if keywords is None or len(keywords) <= 0:
            keywords = self.get_keywords(user)

        queries = [MentionDateIndex.query(
            keyword, Mention.date.between(since, until))
            for keyword in keywords]

        mentions = []
        for keyword in queries:
            for m in keyword:
                mentions.append(map_mention_to_dto(m))

        return mentions

    def get_keywords(self, user):
        keywords = Keyword.query(user)
        return [k.keyword for k in keywords]

    def get_all_keywords(self):
        keywords = Keyword.scan()
        return list(
            set(
                [k.keyword for k in keywords]
            )
        )


def map_mention_to_dto(m: Mention) -> dict:
    return {
            'author': m.author,
            'text': m.text,
            'date': m.date.isoformat(),
            'sentimentScore': m.sentimentScore,
            'keyword': m.keyword
        }
