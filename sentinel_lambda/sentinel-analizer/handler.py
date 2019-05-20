import json
import base64
import boto3
from sentinel_common.mentions import Mention
from sentinel_common.db_writer import save_to_db

client = boto3.client('comprehend')


def analize_and_save(event, context):
    data = []

    for record in event["Records"]:
        payload = base64.b64decode(record["kinesis"]["data"]).decode("utf-8")
        mention = Mention.from_json(payload)
        sentiment_data = client.detect_sentiment(Text=mention.text,
                                                 LanguageCode="en"
                                                 )
        sentiment_score = map_sentiment_value(sentiment_data)
        data.append((mention, sentiment_score))

    result = save_to_db(data)

    for mention_db in result:
        print(f"{mention_db} .")

    body = {
        "message": f"{result}",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response


def map_sentiment_value(sentiment_data):
    sentiment_code = sentiment_data["Sentiment"]
    result = 0

    if sentiment_code == "POSITIVE":
        result = sentiment_data["SentimentScore"]["Positive"]
    elif sentiment_code == "NEGATIVE":
        result = -sentiment_data["SentimentScore"]["Negative"]
    elif sentiment_code == "NEUTRAL":
        result = (1 - sentiment_data["SentimentScore"]["Neutral"])
        result = result * (sentiment_data["SentimentScore"]["Positive"]
                           - sentiment_data["SentimentScore"]["Negative"])
    else:
        result = sentiment_data["SentimentScore"]["Mixed"]
        result = result * (sentiment_data["SentimentScore"]["Positive"]
                           - sentiment_data["SentimentScore"]["Negative"])

    return result
