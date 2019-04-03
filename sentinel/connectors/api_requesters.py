import requests
from datetime import datetime
from typing import List


class IHackerNewsAlgoliaRequester():
    def search(self, query: str, tags: List[str], since: datetime, until: datetime):
        pass


class HackerNewsAlgoliaRequester(IHackerNewsAlgoliaRequester):
    def __init__(self):
        self.search_endpoint = 'http://hn.algolia.com/api/v1/search'

    def _or_tags(self, tags: List[str]) -> str:
        tags_collapsed = ','.join(tags)
        return f'({tags_collapsed})'

    def search(self, keyword: str, tags: List[str], since: datetime, until: datetime):
        since = since.timestamp()
        until = until.timestamp()
        request_argument = f'query={keyword}&tags={self._or_tags(tags)}&numericFilters=created_at_i>{since},created_at_i<{until}'

        return requests.get(f'{self.search_endpoint}?{request_argument}').json()
