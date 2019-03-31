from abc import ABCMeta, abstractmethod
from ..models.mentions import TwitterMention
import tweepy
#historical.py 'twitter' date_start date_end 
#skrypt 
# instance.get_historical_data()
# metoda przyjmująca zakres czasu i słowa kluczowe
# text, 
# url, (entities, urls, url)
# metadane {
#  created_at,
#  user {  
#       name
#       followers_count
#       statuses_count
#       friends_count
#       verified
#       listed_count
#   }
#   retweet_count
#   
class IHistoricalConnector(metaclass=ABCMeta):
    pass

class TwitterHistoricalConnector(IHistoricalConnector):
    def __init__(self):
        pass
    def print_tweets(self):
        auth = tweepy.OAuthHandler("7OQ3QuZHq9VLLHhEfiNLgkXRr", 
                                "1Y3KdcvUkrwjs8R6XVafRfN4ztMC1h6TShfbdLux6fsHEXpEQj")
        api = tweepy.API(auth)
        query='Russia&since=2019-03-27'
        i = 0
        for tweets in tweepy.Cursor(api.search, q=query, count=15,
                                    result_type="recent",include_entities=True, 
                                    until='2019-03-30').pages():
            for tweet in tweets:
                tweet_mention = TwitterMention.from_status_json(tweet)
                print(tweet_mention)




if __name__ == "__main__":
    thc = TwitterHistoricalConnector()
    thc.print_tweets()