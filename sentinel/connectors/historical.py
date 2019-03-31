from abc import ABCMeta, abstractmethod
from ..models.mentions import TwitterMention
from datetime import datetime
from typing import List
import tweepy

class IHistoricalConnector(metaclass=ABCMeta):
    pass

class TwitterHistoricalConnector(IHistoricalConnector):
    def __init__(self):
        auth = tweepy.OAuthHandler("7OQ3QuZHq9VLLHhEfiNLgkXRr", 
                                "1Y3KdcvUkrwjs8R6XVafRfN4ztMC1h6TShfbdLux6fsHEXpEQj")
        self.api = tweepy.API(auth)
        pass

    def _build_query(self, keywords: List[str] , since: datetime) -> str:
        or_statement = '&OR&'.join(keywords)

        query = f'{or_statement}&since={since.date()}'
        return query

    def download_mentions(self, keywords: List[str] , since: datetime, until: datetime) -> List[TwitterMention]:
        query=self._build_query(keywords, since)

        for tweets in tweepy.Cursor(self.api.search, q=query, count=15,
                                   result_type="recent",include_entities=True, 
                                    until=str(until.date())).pages():
            for tweet in tweets:
                yield TwitterMention.from_status_json(tweet)


if __name__ == "__main__":
    thc = TwitterHistoricalConnector()
    print([x for x in thc.download_mentions(['Russia'], datetime(2019, 3, 27), datetime(2019, 3, 30))])