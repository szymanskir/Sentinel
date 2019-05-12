import json
from models import Keyword, Mention
from datetime import datetime


Mention.create_table(read_capacity_units=1, write_capacity_units=1)
Keyword.create_table(read_capacity_units=1, write_capacity_units=1)


def import_mentions(filename):
    with open(filename, 'r') as file:
        mentions = json.load(file)
        for m in mentions:
            model = Mention(
                m['user'],
                m['id'],

                author=m['author'],
                text=m['text'],
                date=datetime.strptime(m['date'], '%Y-%m-%dT%H:%M'),
                sentimentScore=m['sentimentScore'],
                keyword=m['keyword']
            )
            model.save()


Mention.dump('../../mock-data/mentions-dynamo.json')
Keyword.dump('../../mock-data/keywords-dynamo.json')

# Mention.load('../../mock-data/mentions-dynamo.json')
# Keyword.load('../../mock-data/keywords-dynamo.json')
