import os
from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute
)
from pynamodb.indexes import (
    LocalSecondaryIndex, AllProjection
)


DB_ADDR = os.environ.get('DYNAMO_DB_URL')
DB_REGION = os.environ.get('DYNAMO_DB_REGION')


class MentionDateIndex(LocalSecondaryIndex):
    class Meta:
        projection = AllProjection()
        host = DB_ADDR
        region = DB_REGION

    keyword = UnicodeAttribute(hash_key=True)
    id = UnicodeAttribute(range_key=True)


class Mention(Model):
    class Meta:
        table_name = "mentions"
        host = DB_ADDR
        region = DB_REGION

    keyword = UnicodeAttribute(hash_key=True)
    id = UnicodeAttribute(range_key=True)

    author = UnicodeAttribute(null=False)
    text = UnicodeAttribute(null=False)
    date = UTCDateTimeAttribute(null=False)
    sentimentScore = NumberAttribute(null=False)
    date_index = MentionDateIndex()


class Keyword(Model):
    class Meta:
        table_name = "keywords"
        host = DB_ADDR
        region = DB_REGION

    user = UnicodeAttribute(hash_key=True)
    keyword = UnicodeAttribute(range_key=True)
