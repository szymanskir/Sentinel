import json
import base64
import os
from datetime import datetime
from sentinel_common.mentions import TwitterMentionMetadata, Mention
from db_writer import save_to_db


def hello(event, context):
    data = []

    for record in event["Records"]:
        payload = base64.b64decode(record["kinesis"]["data"]).decode("utf-8")
        mention = Mention.from_json(payload)
        data.append((mention, 1))

    result = save_to_db(data)

    for mention_db in result:
        print(f"{mention_db}")

    body = {
        "message": f"{result}",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response