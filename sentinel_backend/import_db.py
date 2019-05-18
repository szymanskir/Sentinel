import json
from sentinel_common.db_models import Keyword, Mention
from datetime import datetime


Mention.create_table(read_capacity_units=25, write_capacity_units=25)
Keyword.create_table(read_capacity_units=25, write_capacity_units=25)


def import_mentions(filename):
    with open(filename, "r") as file:
        mentions = json.load(file)
        for m in mentions:
            model = Mention(
                m["keyword"],
                m["id"],
                author=m["author"],
                text=m["text"],
                date=datetime.strptime(m["date"], "%Y-%m-%dT%H:%M"),
                sentimentScore=m["sentimentScore"],
            )
            model.save()

def import_keywords(filename):
    with open(filename, "r") as file:
        keywords = json.load(file)
        for k in keywords:
            model = Keyword(
                        k["user"],
                        k["keyword"]
                    )
            model.save()
    


import_mentions("../dynamo-dev/mock-data/mentions.json")
import_keywords("../dynamo-dev/mock-data/keywords.json")
