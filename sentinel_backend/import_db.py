import json
from sentinel_common.db_models import KeywordDb, MentionDb
from datetime import datetime


MentionDb.create_table(read_capacity_units=25, write_capacity_units=25)
KeywordDb.create_table(read_capacity_units=25, write_capacity_units=25)


def import_mentions(filename):
    with open(filename, "r") as file:
        mentions = json.load(file)
        for m in mentions:
            model = MentionDb(
                m["keyword"],
                m["id"],
                author=m["author"],
                text=m["text"],
                date=datetime.strptime(m["date"], "%Y-%m-%dT%H:%M"),
                sentiment_score=m["sentiment_score"],
            )
            model.save()


def import_keywords(filename):
    with open(filename, "r") as file:
        keywords = json.load(file)
        for k in keywords:
            model = KeywordDb(k["user"], k["keyword"])
            model.save()


import_mentions("../dynamo-dev/mock-data/mentions.json")
import_keywords("../dynamo-dev/mock-data/keywords.json")
