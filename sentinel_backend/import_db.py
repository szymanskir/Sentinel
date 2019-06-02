import json
from sentinel_common.db_models import KeywordDb, MentionDb
from datetime import datetime


MentionDb.create_table(wait=True, read_capacity_units=25, write_capacity_units=25)
KeywordDb.create_table(wait=True, read_capacity_units=25, write_capacity_units=25)


def import_mentions(filename):
    with open(filename, "r") as file:
        mentions = json.load(file)
        for m in mentions:
            model = MentionDb(
                m["author"],
                datetime.strptime(m["origin_date"], "%Y-%m-%dT%H:%M:%S"),
                keyword=m["keyword"],
                id=m["id"],
                text=m["text"],
                url=m["url"],
                source=m["source"],
                sentiment_score=m["sentiment_score"],
                metadata=m["metadata"],
                download_date=datetime.strptime(
                    m["download_date"], "%Y-%m-%dT%H:%M:%S"
                ),
            )
            model.save()


def import_keywords(filename):
    with open(filename, "r") as file:
        keywords = json.load(file)
        for k in keywords:
            model = KeywordDb(
                k["user"],
                k["keyword"],
                creation_date=datetime.strptime(
                    k["creation_date"], "%Y-%m-%dT%H:%M:%S"
                ),
            )
            model.save()


import_mentions("../dynamo-dev/mock-data/mentions.json")
import_keywords("../dynamo-dev/mock-data/keywords.json")
