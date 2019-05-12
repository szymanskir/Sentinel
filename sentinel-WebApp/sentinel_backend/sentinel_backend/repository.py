import os
import pandas as pd
from typing import List
from datetime import datetime
from .models import Mention, Keyword


class DynamoDbRepository:
    def get_mentions(
        self, user: str, since: datetime, until: datetime, keywords: List[str]
    ):
        condition = Mention.date.between(since, until)
        if keywords is not None:
            condition = condition & (Mention.keyword.is_in(*keywords))

        mentions = Mention.query(user, filter_condition=condition)
        return [map_mention_to_dto(m) for m in mentions]

    def get_keywords(self, user):
        keywords = Keyword.query(user)
        return [k.keyword for k in keywords]

    def get_all_keywords(self):
        keywords = Keyword.scan()
        return list(set([k.keyword for k in keywords]))


def map_mention_to_dto(m: Mention) -> dict:
    return {
        "author": m.author,
        "text": m.text,
        "date": m.date.isoformat(),
        "sentimentScore": m.sentimentScore,
        "keyword": m.keyword,
    }


class MockRepository:
    def __init__(self, directory: str):
        self._validate_mock_data_directory(directory)
        self._source_directory = directory
        self._mentions_data = pd.read_json(f"{directory}/mentions.json")
        self._keywords = pd.read_json(f"{directory}/keywords.json")

    def _validate_mock_data_directory(self, directory: str):
        if not os.path.exists(directory):
            raise Exception(f"{directory} does not exist.")

        required_files = {"mentions.json", "keywords.json"}
        if not required_files < set(os.listdir(directory)):
            raise Exception(
                f"Not all required files are present in the mock data directory"
            )

    def get_keywords(self, user=None):
        keywords = (
            self._keywords[self._keywords.user == user].keyword
            if user
            else self._keywords.keyword
        )
        return list(set(keywords))

    def get_mentions(
        self, user: str, since: datetime, until: datetime, keywords: List[str]
    ) -> pd.DataFrame:
        mentions_data_dates = self._mentions_data.date
        is_mention_from_time_period = (mentions_data_dates >= since) & (
            mentions_data_dates <= until
        )
        is_mention_from_keywords = (
            self._mentions_data.keyword.isin(keywords)
            if keywords
            else self.mentions == self.mentions
        )
        requested_data = self._mentions_data[
            is_mention_from_time_period & is_mention_from_keywords
        ]
        return requested_data
