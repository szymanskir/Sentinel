import os
import pandas as pd
from typing import List
from datetime import datetime
from sentinel_common.db_models import Mention, Keyword, MentionDateIndex


class DynamoDbRepository:
    def get_mentions(
        self, user: str, since: datetime, until: datetime, keywords: List[str]
    ):

        if keywords is None or len(keywords) <= 0:
            keywords = self.get_keywords(user)

        queries = [
            MentionDateIndex.query(keyword, Mention.date.between(since, until))
            for keyword in keywords
        ]

        mentions = []
        for keyword in queries:
            for m in keyword:
                mentions.append(map_mention_to_dto(m))

        return pd.DataFrame.from_records(mentions)

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
        "date": m.date,
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
        # import pdb; pdb.set_trace()
        is_mention_from_keywords = (
            self._mentions_data.keyword.isin(keywords)
            if keywords
            else self._mentions_data.keyword == self._mentions_data.keyword
        )
        requested_data = self._mentions_data[
            is_mention_from_time_period & is_mention_from_keywords
        ]
        return requested_data