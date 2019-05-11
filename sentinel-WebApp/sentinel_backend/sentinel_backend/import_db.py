from models import Keyword, Mention

Mention.create_table(read_capacity_units=1, write_capacity_units=1)
Keyword.create_table(read_capacity_units=1, write_capacity_units=1)

Keyword.dump("mentions.json")

# Mention.load('../../mock-data/mentions-dynamo.json')
# Keyword.load('../../mock-data/keywords-dynamo.json')
