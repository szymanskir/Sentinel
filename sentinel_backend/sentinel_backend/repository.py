import os
import pandas as pd
from typing import List
from datetime import datetime
from sentinel_common.db_models import MentionDb, KeywordDb, MentionDateIndex


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
            else self._mentions_data.keyword == self._mentions_data.keyword
        )
        requested_data = self._mentions_data[
            is_mention_from_time_period & is_mention_from_keywords
        ]
        return requested_data
