from typing import List
from datetime import datetime
from .models import Mention, Keyword


class DynamoDbRepository:
    def get_mentions(
            self,
            user: str,
            since: datetime,
            until: datetime,
            keywords: List[str]):
        condition = (Mention.date.between(since, until))
        if keywords is not None:
            condition = condition & (Mention.keyword.is_in(*keywords))

        mentions = Mention.query(user, filter_condition=condition)
        return [map_mention_to_dto(m) for m in mentions]

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
