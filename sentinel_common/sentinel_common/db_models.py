import os
from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute,
    NumberAttribute,
    UTCDateTimeAttribute,
    JSONAttribute,
)
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection


DB_ADDR = os.environ.get("DYNAMO_DB_URL")
DB_REGION = os.environ.get("DYNAMO_DB_REGION")


class MentionDateIndex(GlobalSecondaryIndex):
    class Meta:
        projection = AllProjection()
        host = DB_ADDR
        region = DB_REGION
        read_capacity_units = 25
        write_capacity_units = 25

    keyword = UnicodeAttribute(hash_key=True)
    origin_date = UTCDateTimeAttribute(range_key=True)


class MentionDb(Model):
    class Meta:
        table_name = "mentions"
        host = DB_ADDR
        region = DB_REGION

    author = UnicodeAttribute(hash_key=True)
    origin_date = UTCDateTimeAttribute(range_key=True)

    keyword = UnicodeAttribute(null=False)
    id = UnicodeAttribute(null=False)
    download_date = UTCDateTimeAttribute(null=False)

    text = UnicodeAttribute(null=False)
    url = UnicodeAttribute(null=True)
    source = UnicodeAttribute(null=False)
    sentiment_score = NumberAttribute(null=False)
    metadata = JSONAttribute(null=True)

    date_index = MentionDateIndex()


class KeywordDb(Model):
    class Meta:
        table_name = "keywords"
        host = DB_ADDR
        region = DB_REGION

    user = UnicodeAttribute(hash_key=True)
    keyword = UnicodeAttribute(range_key=True)
    creation_date = UTCDateTimeAttribute(null=False)
